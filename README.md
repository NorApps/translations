# FotMob Community Translations 🌍

Welcome to the FotMob community translations repository! This is where our amazing community helps translate FotMob into 30+ languages.

## 🎯 How to Contribute

### For Translators

1. **Fork this repository** on GitHub

2. **Find your language file** in the `base_languages/` folder:
   - 🇬🇧 English: `en.json` (reference language)
   - 🇪🇸 Spanish: `es.json`
   - 🇫🇷 French: `fr.json`
   - 🇩🇪 German: `de.json`
   - ... and many more!

3. **Edit your language's JSON file** to add or improve translations

4. **Submit a Pull Request** with your changes

### Translation Guidelines

✅ **DO:**
- Keep translations natural and conversational
- Maintain the same meaning as the English version
- Check `metadata.json` for context about each string
- Preserve placeholders like `%s`, `%d`, `{0}`, etc.
- Test your translations in context when possible

❌ **DON'T:**
- Don't translate brand names (FotMob, Twitter, etc.)
- Don't use machine translation without review
- Don't change the JSON structure or keys
- Don't translate placeholder markers

## 📁 File Structure

```
base_languages/
├── en.json           # English (reference)
├── es.json           # Spanish
├── fr.json           # French
├── de.json           # German
├── ...               # Other languages
├── metadata.json     # Context and comments for strings
└── summary.json      # Translation coverage statistics
```

## 📊 Translation Format

Each language file contains translations in this format:

```json
{
  "language": "es",
  "translations": {
    "notifications_add_widget": "Añadir widget",
    "notifications_app_widget_description": "Consejo: Puedes cambiar el tamaño del widget"
  }
}
```

The `metadata.json` file provides context:

```json
{
  "notifications_add_widget": {
    "tags": ["android"],
    "comment": "Call to action button for user adding widget to home screen."
  }
}
```

## 🌐 Supported Languages

| Language | Code | File |
|----------|------|------|
| Arabic | ar | `ar.json` |
| Chinese (Simplified) | zh-Hans | `zh-Hans.json` |
| Danish | da | `da.json` |
| Dutch | nl | `nl.json` |
| English | en | `en.json` |
| English (UK) | en-GB | `en-GB.json` |
| Finnish | fi | `fi.json` |
| French | fr | `fr.json` |
| German | de | `de.json` |
| Greek | el | `el.json` |
| Hindi | hi | `hi.json` |
| Indonesian | id | `id.json` |
| Italian | it | `it.json` |
| Japanese | ja | `ja.json` |
| Korean | ko | `ko.json` |
| Norwegian | nb | `nb.json` |
| Persian | fa | `fa.json` |
| Polish | pl | `pl.json` |
| Portuguese | pt-PT | `pt-PT.json` |
| Portuguese (Brazil) | pt-BR | `pt-BR.json` |
| Romanian | ro | `ro.json` |
| Russian | ru | `ru.json` |
| Spanish | es | `es.json` |
| Swahili | sw | `sw.json` |
| Swedish | sv | `sv.json` |
| Thai | th | `th.json` |
| Turkish | tr | `tr.json` |
| Ukrainian | uk | `uk.json` |
| Vietnamese | vi | `vi.json` |

## 🚀 Quick Start Example

```bash
# 1. Fork this repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/translations.git
cd translations

# 3. Create a branch for your changes
git checkout -b improve-spanish-translations

# 4. Edit your language file
# Open base_languages/es.json in your favorite editor

# 5. Commit your changes
git add base_languages/es.json
git commit -m "Improve Spanish translations for notifications"

# 6. Push to your fork
git push origin improve-spanish-translations

# 7. Open a Pull Request on GitHub
```

## 🏆 Recognition

We greatly appreciate all contributions! Contributors will be recognized in:
- The app's credits section
- Our contributor wall (coming soon)
- Special contributor badges (for regular contributors)

## ❓ Questions?

- **Translation questions:** Open an issue in this repository
- **App questions:** Contact support@fotmob.com
- **Bug reports:** Use the in-app feedback feature

## 📝 License

By contributing translations, you agree that your contributions will be licensed under the same terms as the FotMob application.

---

**Thank you for helping make FotMob accessible to millions of football fans worldwide! ⚽️🌍**