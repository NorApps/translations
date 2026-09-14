#!/usr/bin/env python3
"""Validate community translation changes in base_languages/*.json.

Only values the pull request actually changed are checked, so pre-existing
issues elsewhere in the file never block a contribution.
"""

import argparse
import json
import os
import re
import subprocess
import sys

PLACEHOLDER = re.compile(r"%(?:\d+\$)?[@dsf]|%%")
HTML_TAG = re.compile(r"</?[a-zA-Z][^>]*>")
PLURAL_FORMS = ("zero", "one", "two", "few", "many", "other")

FORBIDDEN_CHARS = {
    "\u200b": "ZERO WIDTH SPACE",
    "\ufeff": "ZERO WIDTH NO-BREAK SPACE",
    "\u2060": "WORD JOINER",
}

SUSPECT_CHARS = {
    "\u00a0": "NO-BREAK SPACE",
}

LOAN_WORD_SHARE = 0.4

BRAND_TOKENS = ("FotMob", "Opta", "VAR", "xG", "PlayStation")

MAX_ROWS = 50

ARABIC_SCRIPT_FIXES = {
    "fa": {"ي": "ی", "ك": "ک", "ى": "ی", "ھ": "ه"},
    "ckb": {"ي": "ی", "ك": "ک", "ى": "ی", "ھ": "ه", "ة": "ە"},
}
CKB_FINAL_HEH = re.compile("ه(?=[‌]|\\s|$|[.,،:;!؟)»\\]])")


class Finding:
    def __init__(self, level, path, key, form, code, message, line=None):
        self.level = level
        self.path = path
        self.key = key
        self.form = form
        self.code = code
        self.message = message
        self.line = line


def git_show(sha, path):
    result = subprocess.run(
        ["git", "show", f"{sha}:{path}"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout


def changed_files(base_sha):
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base_sha}...HEAD", "--", "base_languages/"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [p for p in result.stdout.split("\n") if p.endswith(".json")]


def entry_values(entry):
    values = {}
    if isinstance(entry.get("value"), str):
        values["value"] = entry["value"]
    plurals = entry.get("plurals")
    if isinstance(plurals, dict):
        for form, text in plurals.items():
            if isinstance(text, str):
                values[form] = text
    return values


def english_for(entry, form):
    english = entry.get("english")
    if form == "value":
        return english if isinstance(english, str) else None
    plurals = entry.get("english_plurals")
    if isinstance(plurals, dict) and isinstance(plurals.get(form), str):
        return plurals[form]
    if isinstance(english, dict) and isinstance(english.get(form), str):
        return english[form]
    return english if isinstance(english, str) else None


def line_of(text, key):
    needle = f'"{key}"'
    index = text.find(needle)
    if index < 0:
        return None
    return text.count("\n", 0, index) + 1


def placeholders(value):
    """Placeholder multiset, ignoring positional indices.

    `%1$d` and `%d` are the same conversion; reordering arguments is a normal
    thing for a translation to need. A changed conversion (`%s` to `%@`) is not.
    """
    return sorted(re.sub(r"^%\d+\$", "%", p) for p in PLACEHOLDER.findall(value))


def check_value(lang, path, text, key, form, old, new, english, add, trusted=False, loan_word=False):
    if not new.strip():
        add("error", "empty", "Translation is empty.")
        return

    new_ph = placeholders(new)
    old_ph = placeholders(old) if old is not None else None
    en_ph = placeholders(english) if english else None

    if en_ph is not None and new_ph != en_ph:
        # Matching English is the goal, so a value that already matches is never
        # a finding however much it changed. Breaking a match is; drifting from
        # one wrong set to another is only worth a warning.
        level = "error" if (old_ph is not None and old_ph == en_ph) else "warning"
        if trusted:
            level = "warning"
        add(
            level,
            "placeholder-changed" if level == "error" else "placeholder-mismatch",
            f"Placeholders {new_ph or 'none'} do not match English {en_ph or 'none'}"
            + (f" (was {old_ph or 'none'})." if old_ph is not None and old_ph != new_ph else "."),
        )
    elif en_ph is None and old_ph is not None and new_ph != old_ph:
        add(
            "warning" if trusted else "error",
            "placeholder-changed",
            f"Placeholders changed: was {old_ph or 'none'}, now {new_ph or 'none'}.",
        )

    if old is not None:
        new_tags = sorted(HTML_TAG.findall(new))
        old_tags = sorted(HTML_TAG.findall(old))
        if new_tags != old_tags:
            add(
                "error",
                "html-changed",
                f"HTML tags changed: was {old_tags or 'none'}, now {new_tags or 'none'}.",
            )

    if (
        english
        and not loan_word
        and new.strip() == english.strip()
        and old is not None
        and old.strip() != english.strip()
    ):
        add(
            "warning" if trusted else "error",
            "untranslated",
            "Value was replaced with the English source text.",
        )

    for char, name in FORBIDDEN_CHARS.items():
        if char in new and (old is None or char not in old):
            add(
                "error",
                "invisible-character",
                f"Contains {name} (U+{ord(char):04X}). Remove it.",
            )

    for char, name in SUSPECT_CHARS.items():
        if char in new and (old is None or char not in old):
            add(
                "warning",
                "invisible-character",
                f"Contains {name} (U+{ord(char):04X}). Intentional in French "
                "typography; elsewhere usually a paste artefact.",
            )

    if any(ord(c) < 32 and c not in "\t" for c in new):
        add("error", "control-character", "Contains a control character.")

    if new != new.strip():
        add("warning", "whitespace", "Leading or trailing whitespace.")
    if "  " in new:
        add("warning", "whitespace", "Contains a double space.")
    if ".." in new and (old is None or ".." not in old):
        add("warning", "punctuation", "Contains a double period.")
    if re.search(r"[،,](?=\S)", new) and (old is None or not re.search(r"[،,](?=\S)", old)):
        add("warning", "punctuation", "Comma is not followed by a space.")

    fixes = ARABIC_SCRIPT_FIXES.get(lang, {})
    for char, correct in fixes.items():
        if char in new and (old is None or char not in old):
            add(
                "warning",
                "orthography",
                f"Uses U+{ord(char):04X} '{char}'; {lang} normally uses '{correct}'.",
            )
    if lang == "ckb" and CKB_FINAL_HEH.search(new) and (old is None or not CKB_FINAL_HEH.search(old)):
        add(
            "warning",
            "orthography",
            "Word-final ه; Sorani normally ends the word with ە.",
        )

    if english and old is not None:
        for token in BRAND_TOKENS:
            if token in english and token in old and token not in new:
                add(
                    "warning",
                    "brand-token",
                    f"'{token}' was dropped. Brand and stat names stay in Latin script.",
                )

    if old and new.startswith(old.rstrip()) and len(new) > len(old):
        tail = new[len(old.rstrip()):].strip()
        if len(tail) >= 4 and tail in old:
            add(
                "warning",
                "duplicated-text",
                f"Text appears to be duplicated at the end: '{tail}'.",
            )


def validate_file(path, base_sha, trusted=False, loan_keys=frozenset()):
    findings = []
    head_text = open(path, encoding="utf-8").read()
    lang = os.path.splitext(os.path.basename(path))[0]

    try:
        head = json.loads(head_text)
    except json.JSONDecodeError as error:
        return [
            Finding(
                "error",
                path,
                None,
                None,
                "invalid-json",
                f"File is not valid JSON: {error.msg} (line {error.lineno}, column {error.colno}). "
                "Check for a missing or extra comma.",
                error.lineno,
            )
        ]

    head_entries = head.get("translations")
    if not isinstance(head_entries, dict):
        return findings

    base_text = git_show(base_sha, path)
    base_entries = {}
    if base_text:
        try:
            base_entries = json.loads(base_text).get("translations") or {}
        except json.JSONDecodeError:
            base_entries = {}

    if base_entries:
        key_level = "warning" if trusted else "error"
        for key in sorted(set(base_entries) - set(head_entries)):
            findings.append(
                Finding(key_level, path, key, None, "key-removed", f"Key '{key}' was removed.")
            )
        added = sorted(set(head_entries) - set(base_entries))
        for key in added[:MAX_ROWS]:
            findings.append(
                Finding(
                    key_level,
                    path,
                    key,
                    None,
                    "key-added",
                    f"Key '{key}' is not in the source file. Keys come from strings.txt.",
                    line_of(head_text, key),
                )
            )
        if len(added) > MAX_ROWS:
            findings.append(
                Finding(
                    key_level, path, None, None, "key-added",
                    f"{len(added) - MAX_ROWS} further keys not in the source file.",
                )
            )

    for key, entry in head_entries.items():
        if not isinstance(entry, dict):
            continue
        base_entry = base_entries.get(key) if isinstance(base_entries.get(key), dict) else None
        old_values = entry_values(base_entry) if base_entry else {}
        reference = base_entry or entry
        line = None

        if base_entry is not None:
            for field in ("english", "english_plurals"):
                if entry.get(field) != base_entry.get(field):
                    findings.append(
                        Finding(
                            # An export regenerates this field whenever the English
                            # source changes, which is most of the time. Only a
                            # contributor editing it by hand is suspicious.
                            "warning" if trusted else "error",
                            path,
                            key,
                            None,
                            "english-modified",
                            f"The '{field}' field was changed. It is generated from the source file — "
                            "only the 'value' and 'plurals' fields may be edited.",
                            line_of(head_text, key),
                        )
                    )

        for form, new in entry_values(entry).items():
            old = old_values.get(form)
            if base_entry is not None and old == new:
                continue
            if line is None:
                line = line_of(head_text, key)

            def add(level, code, message, _key=key, _form=form, _line=line):
                findings.append(Finding(level, path, _key, _form, code, message, _line))

            check_value(
                lang,
                path,
                head_text,
                key,
                form,
                old,
                new,
                english_for(reference, form),
                add,
                trusted,
                key in loan_keys,
            )

    return findings


def find_loan_words(directory="base_languages"):
    """Keys most locales deliberately leave in English.

    "Momentum", "VAR", "xG" and the like are not missing translations, and
    `review_and_apply.py` already treats a wide majority keeping the English as
    intentional. Without this, a correct export trips the untranslated check.
    """
    english_count = {}
    total = 0
    for name in sorted(os.listdir(directory)):
        if not name.endswith(".json") or name in ("summary.json", "metadata.json"):
            continue
        try:
            entries = json.load(open(os.path.join(directory, name), encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        entries = entries.get("translations")
        if not isinstance(entries, dict):
            continue
        total += 1
        for key, entry in entries.items():
            if not isinstance(entry, dict):
                continue
            english = entry.get("english")
            value = entry.get("value")
            if isinstance(english, str) and isinstance(value, str) and value.strip() == english.strip():
                english_count[key] = english_count.get(key, 0) + 1
    if total < 8:
        return frozenset()
    return frozenset(k for k, n in english_count.items() if n / total >= LOAN_WORD_SHARE)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-sha", required=True)
    parser.add_argument(
        "--trusted",
        action="store_true",
        help="PR is from this repo, not a fork: an export legitimately adds keys, "
        "so key-set changes are reported as warnings rather than errors.",
    )
    parser.add_argument("files", nargs="*")
    args = parser.parse_args()

    files = args.files or changed_files(args.base_sha)
    loan_keys = find_loan_words()
    if not files:
        print("No translation files changed.")
        return 0

    findings = []
    for path in files:
        if not os.path.exists(path):
            continue
        findings.extend(validate_file(path, args.base_sha, args.trusted, loan_keys))

    errors = [f for f in findings if f.level == "error"]
    warnings = [f for f in findings if f.level == "warning"]

    for finding in findings:
        location = f"file={finding.path}"
        if finding.line:
            location += f",line={finding.line}"
        label = finding.key or os.path.basename(finding.path)
        if finding.form and finding.form != "value":
            label += f" [{finding.form}]"
        print(f"::{finding.level} {location},title={label}::{finding.message}")

    summary = [f"## Translation validation: {len(errors)} error(s), {len(warnings)} warning(s)", ""]
    if not findings:
        summary.append("All changed values passed.")
    for level, group in (("Errors", errors), ("Warnings", warnings)):
        if not group:
            continue
        summary.append(f"### {level}")
        summary.append("")
        summary.append("| File | Key | Check | Detail |")
        summary.append("| --- | --- | --- | --- |")
        for finding in group[:MAX_ROWS]:
            key = finding.key or "—"
            if finding.form and finding.form != "value":
                key += f" [{finding.form}]"
            detail = finding.message.replace("|", "\\|")
            summary.append(
                f"| `{os.path.basename(finding.path)}` | `{key}` | {finding.code} | {detail} |"
            )
        if len(group) > MAX_ROWS:
            summary.append(f"| … | | | {len(group) - MAX_ROWS} more not listed |")
        summary.append("")

    text = "\n".join(summary)
    step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary:
        with open(step_summary, "a", encoding="utf-8") as handle:
            handle.write(text + "\n")
    print(text)

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
