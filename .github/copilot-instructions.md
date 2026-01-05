# Copilot Instructions for Pregnancy Tracker

This is a **Home Assistant custom integration** that calculates and tracks pregnancy progress with fun, privacy-first comparisons.

**⚠️ Beta Status**: This integration is currently in beta. Expect potential breaking changes and limited real-world testing.

## Architecture Overview

The integration follows Home Assistant's standard custom component structure:

- **`__init__.py`**: Integration lifecycle (setup/unload config entries)
- **`config_flow.py`**: YAML-free configuration UI validation
- **`sensor.py`**: Seven sensor entities with real-time calculations
- **`comparisons.py`**: Week-indexed lookup tables (veggie/dad modes)
- **`const.py`**: Domain constants and sensor identifiers

**Key Design Principle**: All calculations are done daily (date-based), not stored. Sensors derive state from today's date, due date, and pregnancy length.

## Configuration & Setup Flow

The config flow validates and stores three pieces of data:

1. **`due_date`** (required): Must be future-dated (`YYYY-MM-DD` format)
2. **`pregnancy_length`** (optional): Days (default: 280)
3. **`comparison_mode`** (optional): `"veggie"` or `"dad"` (default: `"veggie"`)

See [config_flow.py](custom_components/pregnancy_tracker/config_flow.py#L19-L32) for validation pattern. Unique IDs use `pregnancy_{due_date_str}` to prevent duplicates.

## Sensor Entities & Calculations

All seven sensors inherit from `PregnancyTrackerSensorBase` which computes:
- `days_elapsed = today - start_date`
- `days_remaining = due_date - today`
- `weeks_elapsed = days_elapsed // 7`
- `percent = (days_elapsed / pregnancy_length) * 100`
- `trimester`: 1 (weeks 0-12), 2 (weeks 13-26), 3 (weeks 27+)
- `status`: "overdue" | "due_today" | "just_started" | "in_progress"

See [sensor.py](custom_components/pregnancy_tracker/sensor.py#L89-L123) for `_calculate_values()` method.

Each sensor class overrides `native_value` and optionally `extra_state_attributes`. Example:
- `PregnancyWeeksSensor`: Returns `weeks_elapsed`; attributes include `days_into_week`
- `PregnancySizeComparisonSensor`: Calls `get_comparison(week, mode)` from comparisons module

## Comparison System

[comparisons.py](custom_components/pregnancy_tracker/comparisons.py) contains two dicts:
- `VEGGIE_COMPARISONS`: Week 1-42 mapped to fruit/vegetable names
- `DAD_COMPARISONS`: Week 1-42 mapped to "Dad's [item]" descriptions

`get_comparison(week, mode, custom_data=None)` returns the string label for a given week and mode. For custom mode, it falls back to manual config or a generic fallback.

## Patterns & Conventions

**Date Handling**: Use `datetime.strptime()` to parse config strings to `date` objects. Calculations use `date.today()` and `timedelta`.

**Entity Naming**: Sensor unique IDs follow `{entry_id}_{SENSOR_CONSTANT}`. The `_attr_has_entity_name = True` pattern means entity names are auto-generated from class `_attr_name` (e.g., "Weeks", "Days Elapsed").

**Device Grouping**: All sensors share a single `DeviceInfo` with identifiers `{(DOMAIN, config_entry.entry_id)}` to group them in the UI.

**No State Persistence**: All values recalculate from `date.today()` on each poll. No stored state means restarts have zero impact.

## Version Bumps

To release a new version:
1. Update the `version` field in [manifest.json](custom_components/pregnancy_tracker/manifest.json).
2. Keep `sw_version` in [sensor.py](custom_components/pregnancy_tracker/sensor.py) `DeviceInfo` in sync with the manifest version.
3. Restart/reload the integration in Home Assistant so the new version is reflected.
4. If using HACS releases, create a matching Git tag (e.g., `v0.x.y`) so HACS shows the semantic version instead of a commit hash.

## Common Tasks

**Adding a new sensor**: Create a class in [sensor.py](custom_components/pregnancy_tracker/sensor.py), inherit from `PregnancyTrackerSensorBase`, implement `native_value` property, add to `async_setup_entry()` sensor list.

**Updating comparison data**: Edit the week-indexed dicts in [comparisons.py](custom_components/pregnancy_tracker/comparisons.py).

**Changing defaults**: Update [const.py](custom_components/pregnancy_tracker/const.py) constants (e.g., `DEFAULT_PREGNANCY_LENGTH`, `DEFAULT_COMPARISON_MODE`).

**Validation errors**: Config flow uses Home Assistant's `voluptuous` schema with `vol.In()`, `vol.Range()`, and custom error keys like `"due_date_past"` (resolved by [strings.json](custom_components/pregnancy_tracker/strings.json)).

## Dependencies & Integration Points

- **Home Assistant Core**: `homeassistant.components.sensor`, `config_entries`, `helpers.entity`
- **External deps**: None (IoT class: `"calculated"`)
- **Manifest**: [manifest.json](custom_components/pregnancy_tracker/manifest.json) defines domain, version (1.0.0), and platform (sensor)

## Testing & Validation

No test suite currently exists. When adding features, manually verify in Home Assistant by:
1. Installing the component via HACS or dev copy
2. Adding/reloading the integration via UI
3. Checking sensors appear in Developer Tools > States
4. Validating entity attributes and state updates

For date edge cases (e.g., due date == today, pregnancy length = 1 day), verify `_calculate_values()` logic handles bounds correctly.
