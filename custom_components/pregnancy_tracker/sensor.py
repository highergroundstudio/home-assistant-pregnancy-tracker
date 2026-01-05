"""Sensor platform for Pregnancy Tracker integration.

This integration has been developed with assistance from GitHub Copilot,
which has helped in code generation, improvements, and maintenance.
"""
from __future__ import annotations

import logging
from datetime import date, datetime, timedelta
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo

from .const import (
    DOMAIN,
    CONF_DUE_DATE,
    CONF_PREGNANCY_LENGTH,
    CONF_COMPARISON_MODE,
    CONF_CUSTOM_BIBLE_VERSES,
    DEFAULT_PREGNANCY_LENGTH,
    DEFAULT_COMPARISON_MODE,
    SENSOR_WEEKS,
    SENSOR_DAYS_ELAPSED,
    SENSOR_DAYS_REMAINING,
    SENSOR_PERCENT,
    SENSOR_TRIMESTER,
    SENSOR_STATUS,
    SENSOR_SIZE_COMPARISON,
    SENSOR_DAD_SIZE_COMPARISON,
    SENSOR_SIZE_COMPARISON_IMAGE,
    SENSOR_COUNTDOWN,
    SENSOR_DUE_DATE_RANGE,
    SENSOR_WEEKLY_SUMMARY,
    SENSOR_MILESTONE,
    SENSOR_BIBLE_VERSE,
    SENSOR_BIBLE_VERSE_REFERENCE,
)
from .comparisons import get_comparison, get_all_comparisons, get_weekly_summary, get_bible_verse, parse_bible_reference

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Pregnancy Tracker sensors from a config entry."""
    due_date_str = config_entry.data[CONF_DUE_DATE]
    pregnancy_length = config_entry.data.get(CONF_PREGNANCY_LENGTH, DEFAULT_PREGNANCY_LENGTH)
    custom_bible_verses = config_entry.data.get(CONF_CUSTOM_BIBLE_VERSES, "")

    due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
    start_date = due_date - timedelta(days=pregnancy_length)

    # Create device info for grouping sensors
    # Note: sw_version must match the version in manifest.json
    # After updating the version, users should restart Home Assistant or reload the integration
    device_info = DeviceInfo(
        identifiers={(DOMAIN, config_entry.entry_id)},
        name=f"Pregnancy Tracker {due_date_str}",
        manufacturer="Higher Ground Studio",
        model="Pregnancy Tracker",
        sw_version="1.0.2",
    )

    sensors = [
        PregnancyWeeksSensor(config_entry, due_date, start_date, pregnancy_length, device_info),
        PregnancyDaysElapsedSensor(config_entry, due_date, start_date, pregnancy_length, device_info),
        PregnancyDaysRemainingSensor(config_entry, due_date, start_date, pregnancy_length, device_info),
        PregnancyPercentSensor(config_entry, due_date, start_date, pregnancy_length, device_info),
        PregnancyTrimesterSensor(config_entry, due_date, start_date, pregnancy_length, device_info),
        PregnancyStatusSensor(config_entry, due_date, start_date, pregnancy_length, device_info),
        PregnancySizeComparisonSensor(config_entry, due_date, start_date, pregnancy_length, device_info),
        PregnancyDadSizeComparisonSensor(config_entry, due_date, start_date, pregnancy_length, device_info),
        PregnancySizeComparisonImageSensor(config_entry, due_date, start_date, pregnancy_length, device_info),
        PregnancyCountdownSensor(config_entry, due_date, start_date, pregnancy_length, device_info),
        PregnancyDueDateRangeSensor(config_entry, due_date, start_date, pregnancy_length, device_info),
        PregnancyWeeklySummarySensor(config_entry, due_date, start_date, pregnancy_length, device_info),
        PregnancyMilestoneSensor(config_entry, due_date, start_date, pregnancy_length, device_info),
        PregnancyBibleVerseSensor(config_entry, due_date, start_date, pregnancy_length, device_info, custom_bible_verses),
        PregnancyBibleVerseReferenceSensor(config_entry, due_date, start_date, pregnancy_length, device_info),
    ]

    async_add_entities(sensors)


class PregnancyTrackerSensorBase(SensorEntity):
    """Base class for Pregnancy Tracker sensors."""

    _attr_has_entity_name = True

    def __init__(
        self,
        config_entry: ConfigEntry,
        due_date: date,
        start_date: date,
        pregnancy_length: int,
        device_info: DeviceInfo,
    ) -> None:
        """Initialize the sensor."""
        self._config_entry = config_entry
        self._due_date = due_date
        self._start_date = start_date
        self._pregnancy_length = pregnancy_length
        self._attr_device_info = device_info

    def _calculate_values(self) -> dict[str, Any]:
        """Calculate all pregnancy values."""
        today = date.today()
        
        # Days elapsed since start
        days_elapsed = (today - self._start_date).days
        
        # Days remaining until due date
        days_remaining = (self._due_date - today).days
        
        # Weeks elapsed (rounded down)
        weeks_elapsed = days_elapsed // 7
        
        # Percentage complete
        percent = min(100, max(0, (days_elapsed / self._pregnancy_length) * 100))
        
        # Trimester (1, 2, or 3)
        if weeks_elapsed < 13:
            trimester = 1
        elif weeks_elapsed < 27:
            trimester = 2
        else:
            trimester = 3
        
        # Status
        if days_remaining < 0:
            status = "overdue"
        elif days_remaining == 0:
            status = "due_today"
        elif weeks_elapsed < 1:
            status = "just_started"
        else:
            status = "in_progress"
        
        return {
            "days_elapsed": days_elapsed,
            "days_remaining": days_remaining,
            "weeks_elapsed": weeks_elapsed,
            "percent": round(percent, 1),
            "trimester": trimester,
            "status": status,
        }


class PregnancyWeeksSensor(PregnancyTrackerSensorBase):
    """Sensor for weeks elapsed."""

    _attr_icon = "mdi:calendar-week"
    _attr_native_unit_of_measurement = "weeks"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        config_entry: ConfigEntry,
        due_date: date,
        start_date: date,
        pregnancy_length: int,
        device_info: DeviceInfo,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(config_entry, due_date, start_date, pregnancy_length, device_info)
        self._attr_unique_id = f"{config_entry.entry_id}_{SENSOR_WEEKS}"
        self._attr_name = "Weeks"

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        values = self._calculate_values()
        return values["weeks_elapsed"]

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        values = self._calculate_values()
        days_into_week = values["days_elapsed"] % 7
        return {
            "days_into_week": days_into_week,
            "week_description": f"{values['weeks_elapsed']}+{days_into_week}",
        }


class PregnancyDaysElapsedSensor(PregnancyTrackerSensorBase):
    """Sensor for days elapsed."""

    _attr_icon = "mdi:calendar-check"
    _attr_native_unit_of_measurement = "days"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        config_entry: ConfigEntry,
        due_date: date,
        start_date: date,
        pregnancy_length: int,
        device_info: DeviceInfo,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(config_entry, due_date, start_date, pregnancy_length, device_info)
        self._attr_unique_id = f"{config_entry.entry_id}_{SENSOR_DAYS_ELAPSED}"
        self._attr_name = "Days Elapsed"

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        values = self._calculate_values()
        return values["days_elapsed"]


class PregnancyDaysRemainingSensor(PregnancyTrackerSensorBase):
    """Sensor for days remaining."""

    _attr_icon = "mdi:calendar-clock"
    _attr_native_unit_of_measurement = "days"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        config_entry: ConfigEntry,
        due_date: date,
        start_date: date,
        pregnancy_length: int,
        device_info: DeviceInfo,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(config_entry, due_date, start_date, pregnancy_length, device_info)
        self._attr_unique_id = f"{config_entry.entry_id}_{SENSOR_DAYS_REMAINING}"
        self._attr_name = "Days Remaining"

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        values = self._calculate_values()
        return values["days_remaining"]

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        return {
            "due_date": self._due_date.isoformat(),
        }


class PregnancyPercentSensor(PregnancyTrackerSensorBase):
    """Sensor for percentage complete."""

    _attr_icon = "mdi:percent"
    _attr_native_unit_of_measurement = "%"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        config_entry: ConfigEntry,
        due_date: date,
        start_date: date,
        pregnancy_length: int,
        device_info: DeviceInfo,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(config_entry, due_date, start_date, pregnancy_length, device_info)
        self._attr_unique_id = f"{config_entry.entry_id}_{SENSOR_PERCENT}"
        self._attr_name = "Percent Complete"

    @property
    def native_value(self) -> float:
        """Return the state of the sensor."""
        values = self._calculate_values()
        return values["percent"]


class PregnancyTrimesterSensor(PregnancyTrackerSensorBase):
    """Sensor for trimester."""

    _attr_icon = "mdi:numeric"

    def __init__(
        self,
        config_entry: ConfigEntry,
        due_date: date,
        start_date: date,
        pregnancy_length: int,
        device_info: DeviceInfo,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(config_entry, due_date, start_date, pregnancy_length, device_info)
        self._attr_unique_id = f"{config_entry.entry_id}_{SENSOR_TRIMESTER}"
        self._attr_name = "Trimester"

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        values = self._calculate_values()
        return values["trimester"]

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        values = self._calculate_values()
        trimester_names = {
            1: "First Trimester",
            2: "Second Trimester",
            3: "Third Trimester",
        }
        return {
            "trimester_name": trimester_names.get(values["trimester"], "Unknown"),
        }


class PregnancyStatusSensor(PregnancyTrackerSensorBase):
    """Sensor for pregnancy status."""

    _attr_icon = "mdi:information"

    def __init__(
        self,
        config_entry: ConfigEntry,
        due_date: date,
        start_date: date,
        pregnancy_length: int,
        device_info: DeviceInfo,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(config_entry, due_date, start_date, pregnancy_length, device_info)
        self._attr_unique_id = f"{config_entry.entry_id}_{SENSOR_STATUS}"
        self._attr_name = "Status"

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        values = self._calculate_values()
        status_map = {
            "overdue": "Overdue",
            "due_today": "Due Today",
            "just_started": "Just Started",
            "in_progress": "In Progress",
        }
        return status_map.get(values["status"], "Unknown")


class PregnancySizeComparisonSensor(PregnancyTrackerSensorBase):
    """Sensor for size comparison."""

    _attr_icon = "mdi:ruler"

    def __init__(
        self,
        config_entry: ConfigEntry,
        due_date: date,
        start_date: date,
        pregnancy_length: int,
        device_info: DeviceInfo,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(config_entry, due_date, start_date, pregnancy_length, device_info)
        self._attr_unique_id = f"{config_entry.entry_id}_{SENSOR_SIZE_COMPARISON}"
        self._attr_name = "Size Comparison"

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        values = self._calculate_values()
        week = values["weeks_elapsed"]
        veggie_data = get_comparison(week, "veggie")
        return veggie_data["label"]

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes with all comparison modes and emojis."""
        values = self._calculate_values()
        week = values["weeks_elapsed"]
        
        comparisons = get_all_comparisons(week)
        
        return {
            "week": week,
            "veggie": comparisons["veggie"]["label"],
            "dad": comparisons["dad"]["label"],
            "veggie_image": comparisons["veggie"].get("image"),
            "dad_image": comparisons["dad"].get("image"),
        }


class PregnancyDadSizeComparisonSensor(PregnancyTrackerSensorBase):
    """Sensor for dad-mode size comparison."""

    _attr_icon = "mdi:ruler"

    def __init__(
        self,
        config_entry: ConfigEntry,
        due_date: date,
        start_date: date,
        pregnancy_length: int,
        device_info: DeviceInfo,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(config_entry, due_date, start_date, pregnancy_length, device_info)
        self._attr_unique_id = f"{config_entry.entry_id}_{SENSOR_DAD_SIZE_COMPARISON}"
        self._attr_name = "Dad Size Comparison"

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        values = self._calculate_values()
        week = values["weeks_elapsed"]
        dad_data = get_comparison(week, "dad")
        return dad_data["label"]

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        values = self._calculate_values()
        week = values["weeks_elapsed"]
        comparisons = get_all_comparisons(week)
        return {
            "week": week,
            "veggie": comparisons["veggie"]["label"],
            "dad": comparisons["dad"]["label"],
            "veggie_image": comparisons["veggie"].get("image"),
            "dad_image": comparisons["dad"].get("image"),
        }


class PregnancySizeComparisonImageSensor(PregnancyTrackerSensorBase):
    """Sensor exposing image URLs for size comparisons."""

    _attr_icon = "mdi:image-outline"

    def __init__(
        self,
        config_entry: ConfigEntry,
        due_date: date,
        start_date: date,
        pregnancy_length: int,
        device_info: DeviceInfo,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(config_entry, due_date, start_date, pregnancy_length, device_info)
        self._attr_unique_id = f"{config_entry.entry_id}_{SENSOR_SIZE_COMPARISON_IMAGE}"
        self._attr_name = "Size Comparison Image"

    @property
    def native_value(self) -> str | None:
        """Return the primary image URL (veggie) for convenience."""
        values = self._calculate_values()
        week = values["weeks_elapsed"]
        comparisons = get_all_comparisons(week)
        return comparisons["veggie"].get("image")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return both veggie and dad image URLs plus labels."""
        values = self._calculate_values()
        week = values["weeks_elapsed"]
        comparisons = get_all_comparisons(week)
        return {
            "week": week,
            "veggie": comparisons["veggie"]["label"],
            "veggie_image": comparisons["veggie"].get("image"),
            "dad": comparisons["dad"]["label"],
            "dad_image": comparisons["dad"].get("image"),
        }


class PregnancyCountdownSensor(PregnancyTrackerSensorBase):
    """Sensor for countdown to due date."""

    _attr_icon = "mdi:timer-outline"

    def __init__(
        self,
        config_entry: ConfigEntry,
        due_date: date,
        start_date: date,
        pregnancy_length: int,
        device_info: DeviceInfo,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(config_entry, due_date, start_date, pregnancy_length, device_info)
        self._attr_unique_id = f"{config_entry.entry_id}_{SENSOR_COUNTDOWN}"
        self._attr_name = "Countdown"

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        values = self._calculate_values()
        days_remaining = values["days_remaining"]
        weeks_remaining = days_remaining // 7
        days_in_week = days_remaining % 7
        
        if days_remaining < 0:
            return f"Overdue by {abs(days_remaining)} days"
        elif days_remaining == 0:
            return "Due today!"
        elif weeks_remaining == 0:
            return f"{days_remaining} days"
        else:
            return f"{weeks_remaining}w {days_in_week}d"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        values = self._calculate_values()
        days_remaining = values["days_remaining"]
        
        return {
            "days_remaining": days_remaining,
            "weeks_remaining": days_remaining // 7,
            "days_in_week": days_remaining % 7,
            "due_date": self._due_date.isoformat(),
        }


class PregnancyDueDateRangeSensor(PregnancyTrackerSensorBase):
    """Sensor for due date range."""

    _attr_icon = "mdi:calendar-range"

    def __init__(
        self,
        config_entry: ConfigEntry,
        due_date: date,
        start_date: date,
        pregnancy_length: int,
        device_info: DeviceInfo,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(config_entry, due_date, start_date, pregnancy_length, device_info)
        self._attr_unique_id = f"{config_entry.entry_id}_{SENSOR_DUE_DATE_RANGE}"
        self._attr_name = "Due Date Range"

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        early_date = (self._due_date - timedelta(days=14)).strftime("%b %d")
        late_date = (self._due_date + timedelta(days=14)).strftime("%b %d")
        return f"{early_date} - {late_date}"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        values = self._calculate_values()
        weeks = values["weeks_elapsed"]
        
        # Calculate term status
        if weeks < 37:
            term_status = "Preterm"
        elif weeks < 39:
            term_status = "Early term"
        elif weeks < 41:
            term_status = "Full term"
        elif weeks < 42:
            term_status = "Late term"
        else:
            term_status = "Post term"
        
        return {
            "early_date": (self._due_date - timedelta(days=14)).isoformat(),
            "due_date": self._due_date.isoformat(),
            "late_date": (self._due_date + timedelta(days=14)).isoformat(),
            "term_status": term_status,
        }


class PregnancyWeeklySummarySensor(PregnancyTrackerSensorBase):
    """Sensor for weekly development summary."""

    _attr_icon = "mdi:text-box-outline"

    def __init__(
        self,
        config_entry: ConfigEntry,
        due_date: date,
        start_date: date,
        pregnancy_length: int,
        device_info: DeviceInfo,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(config_entry, due_date, start_date, pregnancy_length, device_info)
        self._attr_unique_id = f"{config_entry.entry_id}_{SENSOR_WEEKLY_SUMMARY}"
        self._attr_name = "Weekly Summary"

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        values = self._calculate_values()
        week = values["weeks_elapsed"]
        return get_weekly_summary(week)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        values = self._calculate_values()
        return {
            "week": values["weeks_elapsed"],
        }


class PregnancyMilestoneSensor(PregnancyTrackerSensorBase):
    """Sensor for pregnancy milestones."""

    _attr_icon = "mdi:trophy-outline"

    def __init__(
        self,
        config_entry: ConfigEntry,
        due_date: date,
        start_date: date,
        pregnancy_length: int,
        device_info: DeviceInfo,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(config_entry, due_date, start_date, pregnancy_length, device_info)
        self._attr_unique_id = f"{config_entry.entry_id}_{SENSOR_MILESTONE}"
        self._attr_name = "Milestone"

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        values = self._calculate_values()
        week = values["weeks_elapsed"]
        
        # Define milestones
        if week >= 40:
            return "Due date reached!"
        elif week >= 37:
            return "Full term"
        elif week >= 27:
            return "Third trimester"
        elif week >= 24:
            return "Viability"
        elif week >= 13:
            return "Second trimester"
        elif week >= 5:
            return "Heartbeat detected"
        else:
            return "Early pregnancy"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        values = self._calculate_values()
        week = values["weeks_elapsed"]
        
        # Track which milestones have been reached
        milestones_reached = []
        if week >= 5:
            milestones_reached.append("Heartbeat detected (Week 5)")
        if week >= 13:
            milestones_reached.append("Second trimester (Week 13)")
        if week >= 24:
            milestones_reached.append("Viability (Week 24)")
        if week >= 27:
            milestones_reached.append("Third trimester (Week 27)")
        if week >= 37:
            milestones_reached.append("Full term (Week 37)")
        if week >= 40:
            milestones_reached.append("Due date (Week 40)")
        
        # Calculate next milestone
        next_milestone = None
        next_milestone_weeks = None
        if week < 5:
            next_milestone = "Heartbeat detected"
            next_milestone_weeks = 5 - week
        elif week < 13:
            next_milestone = "Second trimester"
            next_milestone_weeks = 13 - week
        elif week < 24:
            next_milestone = "Viability"
            next_milestone_weeks = 24 - week
        elif week < 27:
            next_milestone = "Third trimester"
            next_milestone_weeks = 27 - week
        elif week < 37:
            next_milestone = "Full term"
            next_milestone_weeks = 37 - week
        elif week < 40:
            next_milestone = "Due date"
            next_milestone_weeks = 40 - week
        
        return {
            "week": week,
            "milestones_reached": milestones_reached,
            "milestone_count": len(milestones_reached),
            "next_milestone": next_milestone,
            "weeks_to_next_milestone": next_milestone_weeks,
        }


class PregnancyBibleVerseSensor(PregnancyTrackerSensorBase):
    """Sensor for weekly Bible verse."""

    _attr_icon = "mdi:book-open-variant"

    def __init__(
        self,
        config_entry: ConfigEntry,
        due_date: date,
        start_date: date,
        pregnancy_length: int,
        device_info: DeviceInfo,
        custom_bible_verses: str = "",
    ) -> None:
        """Initialize the sensor."""
        super().__init__(config_entry, due_date, start_date, pregnancy_length, device_info)
        self._attr_unique_id = f"{config_entry.entry_id}_{SENSOR_BIBLE_VERSE}"
        self._attr_name = "Bible Verse"
        self._custom_bible_verses = custom_bible_verses

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        values = self._calculate_values()
        week = values["weeks_elapsed"]
        verse_data = get_bible_verse(week, self._custom_bible_verses if self._custom_bible_verses else None)
        return verse_data["text"]

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        values = self._calculate_values()
        week = values["weeks_elapsed"]
        verse_data = get_bible_verse(week, self._custom_bible_verses if self._custom_bible_verses else None)
        return {
            "week": week,
            "reference": verse_data["reference"],
            "text": verse_data["text"],
            "custom_verses_enabled": bool(self._custom_bible_verses),
        }


class PregnancyBibleVerseReferenceSensor(PregnancyTrackerSensorBase):
    """Sensor for Bible verse reference (book and chapter)."""

    _attr_icon = "mdi:bookmark-outline"

    def __init__(
        self,
        config_entry: ConfigEntry,
        due_date: date,
        start_date: date,
        pregnancy_length: int,
        device_info: DeviceInfo,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(config_entry, due_date, start_date, pregnancy_length, device_info)
        self._attr_unique_id = f"{config_entry.entry_id}_{SENSOR_BIBLE_VERSE_REFERENCE}"
        self._attr_name = "Bible Verse Reference"

    @property
    def native_value(self) -> str:
        """Return the state of the sensor (book and chapter)."""
        values = self._calculate_values()
        week = values["weeks_elapsed"]
        verse_data = get_bible_verse(week)
        reference_parts = parse_bible_reference(verse_data["reference"])
        return reference_parts["book_and_chapter"]

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        values = self._calculate_values()
        week = values["weeks_elapsed"]
        verse_data = get_bible_verse(week)
        reference_parts = parse_bible_reference(verse_data["reference"])
        return {
            "week": week,
            "book": reference_parts["book"],
            "chapter": reference_parts["chapter"],
            "verse": reference_parts["verse"],
            "full_reference": verse_data["reference"],
        }
