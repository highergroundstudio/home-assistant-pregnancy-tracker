# Custom Bible Verses Guide

This guide explains how to customize the Bible verses displayed by the Pregnancy Tracker integration.

## Overview

The Pregnancy Tracker includes 42 weeks of carefully selected Bible verses that provide spiritual encouragement throughout your pregnancy journey. However, you can customize these verses to match your preferences or specific spiritual needs.

## Features

- 📖 **Default Verses**: 42 weeks of pre-selected, encouraging Bible verses
- ✏️ **Customizable**: Override any or all weeks with your own verses
- 🔄 **Flexible**: Only customize the weeks you want; others use defaults
- 🎯 **Simple Format**: Easy-to-edit JSON file format
- 🔒 **Privacy**: All data stays local on your Home Assistant instance

## How to Customize

### Step 1: Create Your Custom Verses File

Create a JSON file with your custom verses. You can name it anything you like (e.g., `pregnancy_bible_verses.json`).

**File Location Options:**
- In your Home Assistant config directory: `/config/pregnancy_bible_verses.json`
- Any other location accessible to Home Assistant

**File Format:**

```json
{
  "1": {
    "text": "Your verse text for week 1",
    "reference": "Book Chapter:Verse"
  },
  "2": {
    "text": "Your verse text for week 2",
    "reference": "Book Chapter:Verse"
  },
  "20": {
    "text": "Every good gift and every perfect gift is from above.",
    "reference": "James 1:17"
  }
}
```

**Important Notes:**
- Week numbers must be strings in quotes (e.g., `"1"`, `"20"`, `"42"`)
- You only need to include weeks you want to customize
- Weeks not in your file will use the default verses
- Both `text` and `reference` fields are recommended but optional

### Step 2: Configure the Integration

1. Go to **Settings → Devices & Services** in Home Assistant
2. Find **Pregnancy Tracker** in your integrations
3. Click **Configure** (or **Options** if you see that instead)
4. In the **Custom Bible Verses File** field, enter the path to your file:
   - **Relative path**: `pregnancy_bible_verses.json` (looks in `/config/`)
   - **Absolute path**: `/config/my_verses.json`
5. Click **Submit**

The integration will automatically reload and start using your custom verses!

### Step 3: Verify

Check the `sensor.pregnancy_bible_verse` entity:
- The sensor will show your custom verses for the weeks you specified
- Check the `custom_verses_enabled` attribute - it should be `true`
- Weeks not in your custom file will show the default verses

## Example Custom Verses File

See [`examples/custom_bible_verses_example.json`](examples/custom_bible_verses_example.json) for a complete example with 10 weeks customized.

## JSON Format Details

### Complete Format

```json
{
  "week_number": {
    "text": "The verse text",
    "reference": "Book Chapter:Verse"
  }
}
```

### Minimal Format

You can also use a simplified format with just the text:

```json
{
  "1": "Your verse text here"
}
```

**Note**: When using the minimal format, the reference will be empty.

## Common Use Cases

### 1. Personal Favorite Verses

Select verses that have personal meaning to you and your family:

```json
{
  "1": {
    "text": "This is the day the Lord has made; let us rejoice and be glad in it.",
    "reference": "Psalm 118:24"
  },
  "40": {
    "text": "For I know the plans I have for you, declares the Lord, plans to prosper you.",
    "reference": "Jeremiah 29:11"
  }
}
```

### 2. Themed Verses

Create themed verses for different phases:

```json
{
  "1": {
    "text": "In the beginning...",
    "reference": "Genesis 1:1"
  },
  "13": {
    "text": "Rejoice in hope, be patient in tribulation.",
    "reference": "Romans 12:12"
  },
  "40": {
    "text": "A time to be born.",
    "reference": "Ecclesiastes 3:2"
  }
}
```

### 3. Multi-Language Verses

Include verses in your preferred language:

```json
{
  "1": {
    "text": "Antes que te formases en el vientre te conocí.",
    "reference": "Jeremías 1:5"
  }
}
```

## Troubleshooting

### Verses Not Showing

**Problem**: Your custom verses aren't appearing.

**Solutions**:
1. Check the file path is correct
2. Verify the JSON syntax is valid (use a JSON validator)
3. Make sure week numbers are strings (in quotes)
4. Check Home Assistant logs for error messages
5. Try using an absolute path instead of relative

### Finding the File Path

To verify your file exists:
1. Go to **Settings → Add-ons → File Editor** (if installed)
2. Browse to your file location
3. Or use **Settings → System → Logs** to see any error messages

### JSON Validation

If you're unsure if your JSON is valid:
1. Copy your JSON content
2. Use an online JSON validator (e.g., jsonlint.com)
3. Fix any syntax errors it reports

### Logs

Check Home Assistant logs for messages:
- Successfully loaded: You'll see `Successfully loaded N custom Bible verses`
- File not found: `Custom Bible verses file not found: [path]`
- Invalid format: `Custom Bible verses file has invalid format`
- JSON errors: `Failed to parse custom Bible verses JSON file`

## Default Verses

If you don't specify a custom file, the integration includes these default verses for all 42 weeks:

- **Week 1**: Jeremiah 1:5 - God knew you before formation
- **Week 2**: Psalm 139:13 - Knit together in the womb
- **Week 5**: Psalm 127:3 - Children are a heritage
- **Week 20**: Isaiah 55:12 - Joy and peace
- **Week 40**: Luke 1:37 - Nothing is impossible with God
- And 37 more weeks of encouraging verses!

See the [full list in the code](custom_components/pregnancy_tracker/comparisons.py).

## Privacy & Security

- All custom verses are stored locally on your Home Assistant instance
- No data is sent to external servers
- Your custom verse file is only read by the Pregnancy Tracker integration
- File paths must be accessible to the Home Assistant user

## Tips

1. **Start Small**: Customize just a few key weeks first, then add more
2. **Backup**: Keep a backup copy of your custom verses file
3. **Test**: After configuring, check the sensor to ensure verses appear correctly
4. **Share**: Create verse collections and share them with others (while respecting copyright)
5. **Update Anytime**: You can change the file path or update verses by reconfiguring the integration

## Support

If you encounter issues:
1. Check the Home Assistant logs
2. Verify your JSON syntax
3. Try the example file first
4. Open an issue on GitHub with your configuration (without personal data)

## Contributing

Have a great set of verses to share? Consider contributing:
1. Create a themed verse collection
2. Submit it as an example
3. Help others by sharing your customizations

---

**Note**: When selecting verses, ensure you respect copyright laws and translations. Most modern Bible translations are copyrighted, but many older translations (like KJV) are in the public domain.
