"""Sensor platform for Pregnancy Tracker integration."""
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
    DEFAULT_PREGNANCY_LENGTH,
    DEFAULT_COMPARISON_MODE,
    SENSOR_WEEKS,
    SENSOR_DAYS_ELAPSED,
    SENSOR_DAYS_REMAINING,
    SENSOR_PERCENT,
    SENSOR_TRIMESTER,
    SENSOR_STATUS,
    SENSOR_SIZE_COMPARISON,
)
from .comparisons import get_comparison, get_all_comparisons

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Pregnancy Tracker sensors from a config entry."""
    due_date_str = config_entry.data[CONF_DUE_DATE]
    pregnancy_length = config_entry.data.get(CONF_PREGNANCY_LENGTH, DEFAULT_PREGNANCY_LENGTH)

    due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
    start_date = due_date - timedelta(days=pregnancy_length)

    # Create device info for grouping sensors
    device_info = DeviceInfo(
        identifiers={(DOMAIN, config_entry.entry_id)},
        name=f"Pregnancy Tracker {due_date_str}",
        manufacturer="Higher Ground Studio",
        model="Pregnancy Tracker",
        sw_version="0.2.0-beta",
    )

    sensors = [
        PregnancyWeeksSensor(config_entry, due_date, start_date, pregnancy_length, device_info),
        PregnancyDaysElapsedSensor(config_entry, due_date, start_date, pregnancy_length, device_info),
        PregnancyDaysRemainingSensor(config_entry, due_date, start_date, pregnancy_length, device_info),
        PregnancyPercentSensor(config_entry, due_date, start_date, pregnancy_length, device_info),
        PregnancyTrimesterSensor(config_entry, due_date, start_date, pregnancy_length, device_info),
        PregnancyStatusSensor(config_entry, due_date, start_date, pregnancy_length, device_info),
        PregnancySizeComparisonSensor(config_entry, due_date, start_date, pregnancy_length, device_info),
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
        
        # Show veggie comparison with emoji as the main value
        veggie_data = get_comparison(week, "veggie")
        return f"{veggie_data['emoji']} {veggie_data['label']}"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes with all comparison modes and emojis."""
        values = self._calculate_values()
        week = values["weeks_elapsed"]
        
        comparisons = get_all_comparisons(week)
        
        return {
            "week": week,
            "veggie": comparisons["veggie"]["label"],
            "veggie_emoji": comparisons["veggie"]["emoji"],
            "dad": comparisons["dad"]["label"],
            "dad_emoji": comparisons["dad"]["emoji"],
        }
