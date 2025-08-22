# FotMob Community Translations 🌍

Welcome to the FotMob community translations repository! This is where our amazing community helps translate FotMob into 30+ languages.

## 🎯 How to Contribute (Super Easy!)

### No Technical Knowledge Required! Edit Directly in Your Browser:

1. **Find your language file** in the `base_languages/` folder above
   - Click on your language (e.g., `es.json` for Spanish)

2. **Click the pencil icon** ✏️ in the top right corner of the file view
   - This opens the file editor

3. **Make your translations**
   - You'll see the English text in `"english":` field
   - Edit the text in `"value":` field with your translation
   - The `"comment":` field explains the context

4. **Save your changes**
   - Scroll down and click "Propose changes"
   - Add a short description like "Updated Spanish translations"
   - Click "Create pull request"

5. **That's it!** We'll review and merge your translations

### 📸 Visual Example

When you open a language file, you'll see entries like this:

```json
"common_goal": {
  "english": "Goal",
  "comment": "When a player scores",
  "value": "Gol"
}
```

Simply update the `"value"` field with your translation!

For plural forms:
```json
"common_days": {
  "english": {
    "one": "1 day",
    "other": "%d days"
  },
  "comment": "Number of days",
  "plurals": {
    "one": "1 día",
    "other": "%d días"
  }
}
```

## 📁 File Structure

```
base_languages/
├── en.json           # English (reference)
├── es.json           # Spanish
├── fr.json           # French
├── de.json           # German
├── ...               # Other languages
└── summary.json      # Translation coverage statistics
```

## ✅ Translation Guidelines

### DO:
- Keep translations natural and conversational
- Maintain the same meaning as the English version
- Preserve placeholders like `%s`, `%d`, `{0}`, etc.
- Read the `"comment"` field for context

### DON'T:
- Don't translate brand names (FotMob, Twitter, etc.)
- Don't translate placeholder markers (`%s`, `%d`, etc.)
- Don't change the JSON structure

## 🌐 Supported Languages

| Language | Code | File | Coverage |
|----------|------|------|----------|
| English | en | [`en.json`](base_languages/en.json) | 100% |
| Spanish | es | [`es.json`](base_languages/es.json) | Check file |
| French | fr | [`fr.json`](base_languages/fr.json) | Check file |
| German | de | [`de.json`](base_languages/de.json) | Check file |
| Italian | it | [`it.json`](base_languages/it.json) | Check file |
| Portuguese | pt-PT | [`pt-PT.json`](base_languages/pt-PT.json) | Check file |
| Portuguese (Brazil) | pt-BR | [`pt-BR.json`](base_languages/pt-BR.json) | Check file |
| Russian | ru | [`ru.json`](base_languages/ru.json) | Check file |
| Arabic | ar | [`ar.json`](base_languages/ar.json) | Check file |
| Chinese (Simplified) | zh-Hans | [`zh-Hans.json`](base_languages/zh-Hans.json) | Check file |
| Japanese | ja | [`ja.json`](base_languages/ja.json) | Check file |
| Korean | ko | [`ko.json`](base_languages/ko.json) | Check file |
| And 18 more languages... | | | |

## 💡 Tips for Translators

1. **Start small** - Even translating a few strings helps!
2. **Use the search function** - Press `Ctrl+F` (or `Cmd+F` on Mac) to find specific text
3. **Check the comment** - It explains where and how the text is used
4. **Keep placeholders** - If you see `%s` or `%d`, keep them in the same position
5. **Ask questions** - Open an issue if you're unsure about something

## 🆘 Need Help?

### Common Questions:

**Q: I made a mistake, how do I fix it?**
A: Just edit the file again and submit another pull request!

**Q: What does `%s` or `%d` mean?**
A: These are placeholders. `%s` is replaced with text, `%d` with numbers. Keep them in your translation!

**Q: I don't see my language?**
A: Open an issue and let us know - we can add it!

**Q: Can I use Google Translate?**
A: Please don't rely only on machine translation. Native speakers should review all translations.

## 🏆 Thank You!

We greatly appreciate all contributions from our community!

## 📝 Advanced Users Only

If you prefer using Git locally:

<details>
<summary>Click to expand Git instructions</summary>

```bash
# Fork the repository first on GitHub
git clone https://github.com/YOUR_USERNAME/translations.git
cd translations
git checkout -b improve-spanish-translations
# Edit files locally
git add base_languages/es.json
git commit -m "Improve Spanish translations"
git push origin improve-spanish-translations
# Open Pull Request on GitHub
```

</details>

## ❓ Questions?

- **Translation questions:** [Open an issue](https://github.com/NorApps/translations/issues/new)
- **App questions:** Contact support@fotmob.com

---

**Thank you for helping make FotMob accessible to millions of football fans worldwide! ⚽️🌍**