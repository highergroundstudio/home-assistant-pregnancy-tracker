"""The Pregnancy Tracker integration."""
from __future__ import annotations

import logging
import os
import shutil
from pathlib import Path
from datetime import date

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Pregnancy Tracker from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Copy bundled images to www directory for web access
    await hass.async_add_executor_job(_setup_images, hass)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


def _setup_images(hass: HomeAssistant) -> None:
    """Copy bundled images to www directory."""
    # Source: integration's images directory
    integration_path = Path(__file__).parent
    source_images = integration_path / "images"
    
    # Destination: /config/www/pregnancy_tracker/
    www_path = Path(hass.config.path("www"))
    dest_images = www_path / "pregnancy_tracker"
    
    # Only copy if source exists
    if not source_images.exists():
        _LOGGER.warning("Bundled images not found at %s", source_images)
        return
    
    _LOGGER.debug("Bundled images found at %s", source_images)
    
    try:
        # Create www directory if it doesn't exist
        www_path.mkdir(exist_ok=True)
        
        # Copy images if not already present
        if not dest_images.exists():
            _LOGGER.info("Copying pregnancy tracker images to %s", dest_images)
            shutil.copytree(source_images, dest_images)
            _LOGGER.info("Successfully copied pregnancy tracker images")
        else:
            _LOGGER.debug("Pregnancy tracker images already exist at %s", dest_images)
    except Exception as e:
        _LOGGER.error(
            "Failed to copy pregnancy tracker images from %s to %s: %s",
            source_images,
            dest_images,
            e,
        )


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
