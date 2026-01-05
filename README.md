# Home Assistant Pregnancy Tracker

Home Assistant Pregnancy Tracker is a privacy-focused custom integration that lets you track pregnancy progress entirely inside Home Assistant. Because if Home Assistant can track your pool temperature, it can track this too.

## Features

- **Privacy-First**: All calculations are done locally with date-based math. No cloud services or APIs.
- **Complete Tracking**: Monitor weeks, days elapsed, days remaining, percent complete, trimester, and status
- **Size Comparisons**: Fun size comparisons in "veggie" mode, "dad" mode, or custom JSON mapping
- **UI Configuration**: Easy setup through Home Assistant's UI with config flow
- **Customizable**: Set your own pregnancy length (default 280 days)

## Sensors

The integration creates the following sensors:

1. **Weeks** - Current week of pregnancy (with days into week as attribute)
2. **Days Elapsed** - Total days since pregnancy start
3. **Days Remaining** - Days until due date
4. **Percent Complete** - Percentage of pregnancy completed
5. **Trimester** - Current trimester (1, 2, or 3)
6. **Status** - Current status (Just Started, In Progress, Due Today, or Overdue)
7. **Size Comparison** - Fun size comparison based on current week

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/highergroundstudio/home-assistant-pregnancy-tracker`
6. Select category "Integration"
7. Click "Add"
8. Find "Pregnancy Tracker" in the integration list and click "Download"
9. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/pregnancy_tracker` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to Settings → Devices & Services
2. Click "+ Add Integration"
3. Search for "Pregnancy Tracker"
4. Enter the following information:
   - **Due Date**: The expected due date in YYYY-MM-DD format
   - **Pregnancy Length**: Optional, defaults to 280 days
   - **Comparison Mode**: Choose between "veggie" or "dad" mode

## Size Comparison Modes

### Veggie Mode
Compares baby size to fruits and vegetables (e.g., Week 8: Raspberry, Week 20: Banana)

### Dad Mode
Compares baby size to items dads can relate to (e.g., Week 8: Dad's golf tee, Week 20: Dad's laptop charger)

### Custom Mode (Advanced)
For advanced users who want to provide custom comparisons, you can manually edit the integration's configuration in `.storage/core.config_entries` and add a `custom_comparisons` field with week-to-text mappings. Custom mode will fall back to veggie mode for any weeks not defined.

## Examples

### Automation Example

```yaml
automation:
  - alias: "Pregnancy Milestone Alert"
    trigger:
      - platform: state
        entity_id: sensor.pregnancy_tracker_trimester
    action:
      - service: notify.mobile_app
        data:
          message: "Entered trimester {{ states('sensor.pregnancy_tracker_trimester') }}!"
```

### Lovelace Card Example

```yaml
type: entities
title: Pregnancy Tracker
entities:
  - entity: sensor.pregnancy_tracker_weeks
  - entity: sensor.pregnancy_tracker_days_remaining
  - entity: sensor.pregnancy_tracker_percent_complete
  - entity: sensor.pregnancy_tracker_trimester
  - entity: sensor.pregnancy_tracker_size_comparison
```

## Privacy

This integration is completely privacy-focused:
- No internet connection required
- No data sent to external services
- All calculations done locally using date math
- No tracking or analytics

## Support

For issues, questions, or feature requests, please use the [GitHub Issues](https://github.com/highergroundstudio/home-assistant-pregnancy-tracker/issues) page.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
