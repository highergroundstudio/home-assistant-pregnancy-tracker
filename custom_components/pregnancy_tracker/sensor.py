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
