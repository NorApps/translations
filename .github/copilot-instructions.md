# FotMob Community Translations Repository

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Repository Overview
FotMob Community Translations is a JSON-based translation repository containing translations for FotMob app in 30+ languages. The repository contains 2,255+ translation keys across 32 JSON files with no build system required.

### Essential Setup Commands
Run these commands in order for a fresh repository setup:

```bash
# Verify you're in the correct directory
pwd  # Should be /path/to/translations

# Check repository structure
ls -la  # Should show: .git, .gitignore, README.md, base_languages/

# Verify translation files exist
ls base_languages/*.json | wc -l  # Should show 32 files

# Test JSON validity (takes ~2 seconds)
for file in base_languages/*.json; do echo -n "Testing $file: "; jq empty "$file" && echo "✅ valid" || echo "❌ invalid"; done
```

### Validation and Testing
**NEVER CANCEL these validation commands. They complete quickly but are thorough.**

```bash
# Comprehensive JSON validation (1-2 seconds to complete)
python3 -c "
import json
from pathlib import Path

def validate_all():
    base_dir = Path('base_languages')
    json_files = list(base_dir.glob('*.json'))
    valid = 0
    
    for file in json_files:
        try:
            with open(file, 'r') as f:
                json.load(f)
            print(f'✅ {file.name}')
            valid += 1
        except Exception as e:
            print(f'❌ {file.name}: {e}')
    
    print(f'Validation complete: {valid}/{len(json_files)} files valid')
    return valid == len(json_files)

validate_all()
"
```

```bash
# Check translation completeness (1-2 seconds to complete)
python3 -c "
import json
from pathlib import Path

en_file = Path('base_languages/en.json')
with open(en_file) as f:
    en_data = json.load(f)
en_keys = set(en_data['translations'].keys())

print(f'English reference: {len(en_keys)} keys')
print('Language coverage:')

for file in sorted(Path('base_languages').glob('*.json')):
    if file.name in ['en.json', 'summary.json', 'metadata.json']:
        continue
    
    with open(file) as f:
        data = json.load(f)
    
    lang_keys = set(data.get('translations', {}).keys())
    coverage = len(lang_keys & en_keys) / len(en_keys) * 100
    print(f'{file.stem:10s}: {len(lang_keys):4d} keys ({coverage:5.1f}%)')
"
```

```bash
# Quick lint check using jq (1 second to complete)
find base_languages -name "*.json" -exec jq empty {} \; && echo "✅ All JSON files are well-formed"
```

## File Structure Navigation

```
.
├── README.md                    # Main documentation
├── .gitignore                  # Git ignore rules
└── base_languages/             # Translation files directory
    ├── en.json                 # English reference (2,255 keys)
    ├── es.json                 # Spanish translations
    ├── fr.json                 # French translations
    ├── de.json                 # German translations
    ├── [language].json         # Other language files
    ├── summary.json            # Translation coverage statistics
    └── metadata.json           # Translation metadata and tags
```

## Working with Translations

### Key File Formats
All translation files follow this structure:
```json
{
  "language": "en",
  "translations": {
    "translation_key": {
      "comment": "Context explanation",
      "english": "English reference text",
      "value": "Translated text"
    }
  }
}
```

### Common Translation Tasks

**View translation statistics:**
```bash
# View coverage summary (already generated)
cat base_languages/summary.json | jq '.coverage'
```

**Check specific translation key:**
```bash
# Example: Check a specific key across languages
key="common_goal"
for file in base_languages/{en,es,fr}.json; do
  echo "=== $file ==="
  jq -r ".translations.\"$key\".value" "$file" 2>/dev/null || echo "Key not found"
done
```

**Validate translation structure:**
```bash
# Check if a translation file has required structure
file="base_languages/en.json"
jq 'has("language") and has("translations")' "$file"
```

## Validation Requirements

### Before Making Changes
Always run these validation checks before committing changes:

```bash
# 1. JSON syntax validation (NEVER CANCEL - takes 1-2 seconds)
echo "Validating JSON syntax..."
find base_languages -name "*.json" -exec jq empty {} \; && echo "✅ JSON syntax valid"

# 2. Translation structure check (NEVER CANCEL - takes 1-2 seconds)
echo "Checking translation structure..."
python3 -c "
import json
from pathlib import Path

for file in Path('base_languages').glob('*.json'):
    if file.name in ['summary.json', 'metadata.json']:
        continue
    
    with open(file) as f:
        data = json.load(f)
    
    if 'language' not in data or 'translations' not in data:
        print(f'❌ {file.name}: Missing required structure')
        exit(1)

print('✅ All files have correct structure')
"

# 3. Placeholder consistency check (NEVER CANCEL - takes 1-2 seconds)
echo "Checking placeholder consistency..."
python3 -c "
import json, re
from pathlib import Path

en_file = Path('base_languages/en.json')
with open(en_file) as f:
    en_data = json.load(f)

issues = []
for key, entry in list(en_data['translations'].items())[:50]:  # Check sample
    if 'value' not in entry:
        continue
    
    en_placeholders = len(re.findall(r'%[sd]', entry['value']))
    if en_placeholders == 0:
        continue
    
    # Check in other languages
    for lang_file in ['es.json', 'fr.json', 'de.json']:
        try:
            with open(f'base_languages/{lang_file}') as f:
                lang_data = json.load(f)
            
            if key in lang_data['translations'] and 'value' in lang_data['translations'][key]:
                lang_value = lang_data['translations'][key]['value']
                lang_placeholders = len(re.findall(r'%[sd]', lang_value))
                
                if en_placeholders != lang_placeholders:
                    issues.append(f'{lang_file}: {key} placeholder mismatch')
        except:
            pass

if issues:
    print('⚠️ Found placeholder issues:')
    for issue in issues[:5]:
        print(f'  {issue}')
else:
    print('✅ Placeholder consistency check passed')
"
```

## Manual Validation Scenarios

After making translation changes, always test these scenarios:

### Scenario 1: JSON File Integrity
```bash
# Verify modified files are still valid JSON (1 second)
for file in base_languages/*.json; do
  if ! jq empty "$file" 2>/dev/null; then
    echo "❌ Invalid JSON in $file"
    exit 1
  fi
done
echo "✅ All JSON files valid"
```

### Scenario 2: Translation Key Completeness
```bash
# Check that modified translations maintain key structure (1-2 seconds)
python3 -c "
import json
from pathlib import Path

en_file = Path('base_languages/en.json')
with open(en_file) as f:
    en_data = json.load(f)

# Check a sample translation file structure
test_file = Path('base_languages/es.json')
with open(test_file) as f:
    test_data = json.load(f)

sample_keys = list(en_data['translations'].keys())[:10]
missing = []

for key in sample_keys:
    if key not in test_data.get('translations', {}):
        missing.append(key)

if missing:
    print(f'❌ Missing keys in {test_file.name}: {missing[:3]}...')
else:
    print(f'✅ Sample key structure validated')
"
```

### Scenario 3: Character Encoding Test
```bash
# Verify file encoding is preserved (1 second)
file base_languages/*.json | grep -q "UTF-8\|JSON text data" && echo "✅ All files are properly encoded" || echo "❌ Encoding issues found"
```

## Troubleshooting

### Common Issues and Solutions

**Invalid JSON Error:**
```bash
# Find the specific line with JSON error
jq . base_languages/problematic_file.json
# Use the error message to locate and fix the syntax issue
```

**Missing Translation Keys:**
```bash
# Compare against English reference
python3 -c "
import json
with open('base_languages/en.json') as f: en = json.load(f)
with open('base_languages/target_lang.json') as f: target = json.load(f)
missing = set(en['translations'].keys()) - set(target['translations'].keys())
print(f'Missing keys: {list(missing)[:10]}')
"
```

**Placeholder Validation Failure:**
```bash
# Check specific key for placeholder issues
key="your_translation_key"
echo "English:" && jq -r ".translations.\"$key\".value" base_languages/en.json
echo "Spanish:" && jq -r ".translations.\"$key\".value" base_languages/es.json
# Manually verify placeholder count matches
```

## Repository Workflow

### For Translation Updates:
1. **Validate current state** (run validation commands above)
2. **Edit translation files** using any text editor
3. **Re-validate after changes** (run all validation commands)
4. **Test specific translation scenarios** (run manual validation)
5. **Commit only if all validations pass**

### For Adding New Languages:
1. **Copy `en.json` as template** for new language
2. **Update `language` field** to new language code
3. **Translate `value` fields** (keep `english` and `comment` unchanged)
4. **Run full validation suite** before committing

## Important Notes

- **NEVER modify** the `english` or `comment` fields in translation files
- **ALWAYS preserve** placeholder markers like `%s`, `%d`, `{0}` in translations
- **DO NOT translate** brand names (FotMob, Twitter, etc.)
- **MAINTAIN** the same JSON structure across all language files
- **VALIDATE** every change with the provided scripts before committing

## Quick Reference Commands

```bash
# Quick validation (1-2 seconds total)
jq empty base_languages/*.json && echo "✅ JSON valid"

# Translation count
ls base_languages/*.json | wc -l

# Coverage check
jq '.coverage | to_entries | .[] | "\(.key): \(.value.percentage)%"' base_languages/summary.json

# Find translation by key
grep -r "specific_translation_key" base_languages/

# Validate specific file
jq . base_languages/target_file.json > /dev/null && echo "Valid"
```

## Performance Expectations

- **JSON validation**: 1-2 seconds for all files
- **Structure validation**: 1-2 seconds  
- **Completeness check**: 1-2 seconds
- **Placeholder validation**: 1-2 seconds
- **Full test suite**: 5-10 seconds total

**NEVER CANCEL** any validation commands - they complete very quickly and are essential for maintaining translation quality.