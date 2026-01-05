# Home Assistant Pregnancy Tracker (Beta)

> **⚠️ Beta Status**: This integration is currently in beta. Expect potential breaking changes and limited real-world testing. Please report issues on GitHub!

A **privacy-first Home Assistant custom integration** that tracks pregnancy progress locally and presents it in a clear, human-friendly way — including fun size comparisons like *Veggie Mode* and *Dad Mode*.

No cloud services. No external APIs. All data stays inside your Home Assistant instance.

---

## Features

* 📅 Track pregnancy progress from a **due date**
* 📊 Automatically calculated:

  * Weeks along
  * Days elapsed
  * Days remaining
  * Percent complete
  * Trimester
* 🥕 **Veggie Mode** – baby size compared to fruits & vegetables
* 🧰 **Dad Mode** – baby size compared to everyday / garage items
* 🧩 **Custom Mode** – bring your own comparisons
* 📖 **Bible Verses** – weekly spiritual encouragement with carefully selected verses
* 🏆 **Milestones** – track important pregnancy milestones
* 📝 **Weekly Summaries** – baby development information for each week
* 🖼 Optional image support (bring your own images)
* ⚙️ Fully configurable through the Home Assistant UI
* 🔒 Privacy-first: no cloud, no accounts, no data sharing

---

## Installation

### Option 1: HACS Store (Recommended)

This integration is now available directly in the HACS store!

1. Open **HACS**
2. Go to **Integrations**
3. Search for **Pregnancy Tracker**
4. Click **Download**
5. Restart Home Assistant

### Option 2: Custom Repository

Alternatively, you can add it as a custom repository:

1. Open **HACS**
2. Go to **Integrations**
3. Click the three-dot menu → **Custom repositories**
4. Add this repository URL
   * Category: **Integration**
5. Search for **Pregnancy Tracker** and install
6. Restart Home Assistant

---

## Configuration

### Initial Setup

After installation:

1. Go to **Settings → Devices & Services**
2. Click **Add Integration**
3. Search for **Pregnancy Tracker**
4. Enter:

   * **Due date** (required)
   * Optional pregnancy length (default: 280 days)

No YAML configuration required.

---

## Entities Created

The integration creates the following sensors:

| Entity                                  | Description                           |
| --------------------------------------- | ------------------------------------- |
| `sensor.pregnancy_weeks`                | Current pregnancy week                |
| `sensor.pregnancy_days`                 | Days elapsed                          |
| `sensor.pregnancy_days_remaining`       | Countdown to due date                 |
| `sensor.pregnancy_percent`              | Percent complete                      |
| `sensor.pregnancy_trimester`            | First / Second / Third                |
| `sensor.pregnancy_status`               | Human-readable summary                |
| `sensor.pregnancy_size_comparison`      | Veggie size comparison                |
| `sensor.pregnancy_dad_size_comparison`  | Dad mode size comparison              |
| `sensor.pregnancy_size_comparison_image`| Image URLs for comparisons            |
| `sensor.pregnancy_countdown`            | Countdown in weeks and days format    |
| `sensor.pregnancy_due_date_range`       | Due date range with term status       |
| `sensor.pregnancy_weekly_summary`       | Baby development summary              |
| `sensor.pregnancy_milestone`            | Pregnancy milestones tracker          |
| `sensor.pregnancy_bible_verse`          | Weekly Bible verse for encouragement  |

### Size Comparison Sensor Attributes

`sensor.pregnancy_size_comparison` includes:

* `week`
* `mode` (veggie / dad / custom)
* `label`
* `image` (path where images would be located if you provide your own)

This makes it easy to display text comparisons in Lovelace cards, and optionally add images if you provide them.

### Bible Verse Sensor

`sensor.pregnancy_bible_verse` provides spiritual encouragement throughout your pregnancy journey with carefully selected Bible verses:

* **Weekly verses**: A different verse for each week of pregnancy (weeks 1-42)
* **State**: The verse text is displayed as the sensor state
* **Attributes**: 
  * `week` - Current pregnancy week
  * `reference` - Bible verse reference (e.g., "Psalm 139:13")
  * `text` - Full verse text

The verses change weekly based on your pregnancy progress, offering relevant encouragement and inspiration. Each verse has been selected to provide comfort, hope, and spiritual support during this special time.

**Example verses:**
- Week 2: "For you created my inmost being; you knit me together in my mother's womb." - Psalm 139:13
- Week 20: "You will go out in joy and be led forth in peace; the mountains and hills will burst into song before you." - Isaiah 55:12
- Week 40: "For nothing is impossible with God." - Luke 1:37

---

## Comparison Modes

The integration includes **bundled comparison images** for both Veggie and Dad modes! Images are automatically copied to your `/config/www/pregnancy_tracker/` directory on setup.

### 🥬 Veggie Mode

Baby size compared to fruits and vegetables by week.
- Week 8: Raspberry
- Week 20: Banana  
- Week 40: Small pumpkin

**Includes 42 weeks of veggie images!**

### 👨 Dad Mode

Baby size compared to everyday and garage items (tools, sports gear, etc.).
- Week 8: Dad's golf tee
- Week 20: Dad's laptop charger
- Week 40: Dad's grill

**Includes 42 weeks of dad images!**

### Custom Mode

Use your own comparison labels and images.

Create a file like:

`/config/pregnancy_tracker_custom.json`

```json
{
  "4":  { "label": "Poppy Seed", "image": "/local/pregnancy/04.webp" },
  "12": { "label": "Plum", "image": "https://example.com/plum.webp" }
}
```

Then enable **Custom Mode** in the integration options.

**Note:** You can override the bundled images by placing your own images at `/config/www/pregnancy_tracker/{mode}/week_{week}.png`

---

## Updating the Integration

When a new version of the integration is released:

1. Update the integration via HACS
2. **Restart Home Assistant** to load the new version
3. Alternatively, you can reload the integration from **Settings → Devices & Services → Pregnancy Tracker → ⋮ → Reload**

**Note**: For major version updates, a full Home Assistant restart is recommended to ensure all changes are properly applied.

---

## Options

From **Devices & Services → Pregnancy Tracker → Options**:

* Change comparison mode
* Set custom comparison file path
* Clamp countdown to 0 after due date

Changes apply instantly — no restart required.

---

## Dashboard Example

Use any standard card. Example with a Mushroom Template Card:

* Primary: `sensor.pregnancy_status`
* Secondary: `sensor.pregnancy_size_comparison`

Or with the Entity card:

```yaml
type: entity
entity: sensor.pregnancy_size_comparison
```

### Bible Verse Card Example

Display weekly Bible verses for spiritual encouragement:

```yaml
type: markdown
content: >
  ## 📖 This Week's Verse

  {{ states('sensor.pregnancy_bible_verse') }}

  *{{ state_attr('sensor.pregnancy_bible_verse', 'reference') }}*
```

Or use a simple entity card:

```yaml
type: entity
entity: sensor.pregnancy_bible_verse
```

**Note**: The integration provides text-based size comparisons by default. Images are **not included** but can be optionally added by placing your own images at `/config/www/pregnancy_tracker/{mode}/week_{number}.png`. The `sensor.pregnancy_size_comparison` entity includes an `image` attribute with the path where images would be located if you add them.

No custom Lovelace cards required.

---

## Privacy

This integration:

* Uses only local date calculations
* Makes no network requests
* Stores no data outside Home Assistant

Perfect for sensitive, personal information.

---

## License

MIT License — free to use, modify, and share.

---

## Contributions

Contributions are welcome:

* New comparison modes
* Image sets
* Localization
* Bug fixes and enhancements

Please open an issue or pull request.

### Development and Testing

This repository includes automated testing and quality assurance via GitHub Actions:

* **Test Suite**: Runs on Python 3.9, 3.10, 3.11, and 3.12
* **Code Quality**: Automated linting with flake8, Black, and isort
* **Validation**: JSON structure validation for manifest and strings files

The workflow runs automatically on push and pull requests to `main` and `develop` branches. All checks must pass before merging.

**Note**: This integration has been developed with assistance from GitHub Copilot, which has helped in code generation, improvements, and maintenance throughout the development process.

---

## Disclaimer

This integration is for **informational and personal use only**.
It is not medical advice and should not be used for medical decision-making.
