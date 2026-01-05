Below is a **clean, HACS-ready `README.md`** you can drop directly into the repo. It is written to Home Assistant community norms, clear for non-technical users, and credible for maintainers.

---

# Home Assistant Pregnancy Tracker

A **privacy-first Home Assistant custom integration** that tracks pregnancy progress locally and presents it in a clear, human-friendly way — including fun size comparisons like *Veggie Mode* and *Dad Mode*, with optional images for dashboards and notifications.

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
* 🧩 **Custom Mode** – bring your own comparisons and images
* 🖼 Optional image support for dashboards and notifications
* ⚙️ Fully configurable through the Home Assistant UI
* 🔒 Privacy-first: no cloud, no accounts, no data sharing

---

## Installation (HACS)

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

| Entity                             | Description            |
| ---------------------------------- | ---------------------- |
| `sensor.pregnancy_weeks`           | Current pregnancy week |
| `sensor.pregnancy_days`            | Days elapsed           |
| `sensor.pregnancy_days_remaining`  | Countdown to due date  |
| `sensor.pregnancy_percent`         | Percent complete       |
| `sensor.pregnancy_trimester`       | First / Second / Third |
| `sensor.pregnancy_status`          | Human-readable summary |
| `sensor.pregnancy_size_comparison` | Fun size comparison    |

### Size Comparison Sensor Attributes

`sensor.pregnancy_size_comparison` includes:

* `week`
* `mode` (veggie / dad / custom)
* `label`
* `image` (URL or `/local/` path, if provided)

This makes it easy to display text *and* images in Lovelace cards.

---

## Comparison Modes

### Veggie Mode

Baby size compared to fruits and vegetables by week.

### Dad Mode

Baby size compared to everyday and garage items (tools, sports gear, etc.).

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
* Picture:

  ```
  {{ state_attr('sensor.pregnancy_size_comparison', 'image') }}
  ```

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

---

## Disclaimer

This integration is for **informational and personal use only**.
It is not medical advice and should not be used for medical decision-making.
