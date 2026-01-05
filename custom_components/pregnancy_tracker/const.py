"""Constants for the Pregnancy Tracker integration."""

DOMAIN = "pregnancy_tracker"

# Config keys
CONF_DUE_DATE = "due_date"
CONF_PREGNANCY_LENGTH = "pregnancy_length"
CONF_COMPARISON_MODE = "comparison_mode"
CONF_CUSTOM_COMPARISONS = "custom_comparisons"  # For advanced users (manual config only)

# Default values
DEFAULT_PREGNANCY_LENGTH = 280
DEFAULT_COMPARISON_MODE = "veggie"

# Comparison modes
COMPARISON_MODE_VEGGIE = "veggie"
COMPARISON_MODE_DAD = "dad"
COMPARISON_MODE_CUSTOM = "custom"  # For advanced users (manual config only)

# Sensor types
SENSOR_WEEKS = "weeks"
SENSOR_DAYS_ELAPSED = "days_elapsed"
SENSOR_DAYS_REMAINING = "days_remaining"
SENSOR_PERCENT = "percent"
SENSOR_TRIMESTER = "trimester"
SENSOR_STATUS = "status"
SENSOR_SIZE_COMPARISON = "size_comparison"
SENSOR_DAD_SIZE_COMPARISON = "dad_size_comparison"
SENSOR_SIZE_COMPARISON_IMAGE = "size_comparison_image"
SENSOR_COUNTDOWN = "countdown"
SENSOR_DUE_DATE_RANGE = "due_date_range"
SENSOR_WEEKLY_SUMMARY = "weekly_summary"
SENSOR_MILESTONE = "milestone"
SENSOR_BIBLE_VERSE = "bible_verse"
SENSOR_BIBLE_VERSE_REFERENCE = "bible_verse_reference"
