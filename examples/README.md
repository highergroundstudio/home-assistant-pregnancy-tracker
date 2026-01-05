# Examples

This directory contains example files to help you customize your Pregnancy Tracker integration.

## Custom Bible Verses Examples

We provide three example files demonstrating different approaches to customizing Bible verses:

### 1. `custom_bible_verses_example.json` - Basic Example
A straightforward example with 10 weeks of verses, perfect for getting started.

### 2. `custom_bible_verses_comfort.json` - Comfort & Encouragement
11 weeks of verses focused on comfort, strength, and God's presence during pregnancy. Ideal for those seeking reassurance and peace.

### 3. `custom_bible_verses_milestones.json` - Key Milestones
8 carefully selected verses for major pregnancy milestones (weeks 1, 5, 13, 20, 24, 27, 37, 40). A minimalist approach that highlights the most significant moments.

### How to Use

1. **Choose an example file** that matches your needs, or create your own

2. **Copy the file** to your Home Assistant config directory:
   ```bash
   cp custom_bible_verses_comfort.json /config/pregnancy_bible_verses.json
   ```

3. **Edit the file** (optional):
   - Open the file in a text editor
   - Modify verses to match your preferences
   - Add or remove weeks as needed

4. **Configure the integration**:
   - Go to Settings → Devices & Services → Pregnancy Tracker
   - Click Configure or Options
   - Enter `pregnancy_bible_verses.json` in the Custom Bible Verses File field
   - Click Submit

5. **Verify it works**:
   - Check the `sensor.pregnancy_bible_verse` entity
   - The `custom_verses_enabled` attribute should be `true`
   - Your custom verses should appear for the weeks you specified

### File Format

All files use JSON format with week numbers as keys:

```json
{
  "week_number": {
    "text": "The complete verse text",
    "reference": "Book Chapter:Verse"
  }
}
```

**Important Notes:**
- Week numbers must be strings (e.g., `"1"`, not `1`)
- You only need to include weeks you want to customize
- Weeks not in your file will use the default verses
- Both `text` and `reference` are recommended

### Mixing and Matching

You can create your own custom file by combining verses from different examples:
1. Start with one of the example files
2. Add verses from other examples that resonate with you
3. Add your own personal favorite verses
4. Save it with a unique name

### Tips

- Start with an example and modify it gradually
- Test with just a few weeks first
- Back up your custom file before making major changes
- Use a JSON validator to check your syntax (jsonlint.com)
- Check Home Assistant logs if verses don't appear
- You can switch between example files by changing the configuration

### More Information

For a complete guide on customizing Bible verses, including:
- Detailed format specifications
- Troubleshooting tips
- Use case examples
- Advanced configurations

See the main [CUSTOM_BIBLE_VERSES.md](../CUSTOM_BIBLE_VERSES.md) documentation.
