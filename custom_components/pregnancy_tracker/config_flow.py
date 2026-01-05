"""Config flow for Pregnancy Tracker integration."""
from __future__ import annotations

import logging
from datetime import date, datetime
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_DUE_DATE,
    CONF_PREGNANCY_LENGTH,
    CONF_COMPARISON_MODE,
    CONF_CUSTOM_BIBLE_VERSES,
    DEFAULT_PREGNANCY_LENGTH,
    DEFAULT_COMPARISON_MODE,
    COMPARISON_MODE_VEGGIE,
    COMPARISON_MODE_DAD,
)

_LOGGER = logging.getLogger(__name__)


class PregnancyTrackerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Pregnancy Tracker."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> PregnancyTrackerOptionsFlow:
        """Get the options flow for this handler."""
        return PregnancyTrackerOptionsFlow(config_entry)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Validate due date is in the future
            due_date_str = user_input[CONF_DUE_DATE]
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                if due_date < date.today():
                    errors["due_date"] = "due_date_past"
                else:
                    # Create unique ID based on due date
                    await self.async_set_unique_id(f"pregnancy_{due_date_str}")
                    self._abort_if_unique_id_configured()

                    return self.async_create_entry(
                        title=f"Pregnancy Tracker ({due_date_str})",
                        data={
                            CONF_DUE_DATE: due_date_str,
                            CONF_PREGNANCY_LENGTH: user_input.get(
                                CONF_PREGNANCY_LENGTH, DEFAULT_PREGNANCY_LENGTH
                            ),
                            CONF_CUSTOM_BIBLE_VERSES: user_input.get(
                                CONF_CUSTOM_BIBLE_VERSES, ""
                            ),
                        },
                    )
            except ValueError:
                errors["due_date"] = "invalid_date"

        data_schema = vol.Schema(
            {
                vol.Required(CONF_DUE_DATE): selector.DateSelector(),
                vol.Optional(
                    CONF_PREGNANCY_LENGTH, default=DEFAULT_PREGNANCY_LENGTH
                ): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=1, max=365, mode=selector.NumberSelectorMode.BOX
                    )
                ),
                vol.Optional(CONF_CUSTOM_BIBLE_VERSES, default=""): selector.TextSelector(
                    selector.TextSelectorConfig(
                        multiline=False,
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )


class PregnancyTrackerOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Pregnancy Tracker."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self._config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Validate due date
            due_date_str = user_input[CONF_DUE_DATE]
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                # Allow past dates in case user wants to track a completed pregnancy
                # or correct a mistake
                
                # Update the config entry data
                self.hass.config_entries.async_update_entry(
                    self.config_entry,
                    data={
                        CONF_DUE_DATE: due_date_str,
                        CONF_PREGNANCY_LENGTH: user_input.get(
                            CONF_PREGNANCY_LENGTH, DEFAULT_PREGNANCY_LENGTH
                        ),
                        CONF_CUSTOM_BIBLE_VERSES: user_input.get(
                            CONF_CUSTOM_BIBLE_VERSES, ""
                        ),
                    },
                    title=f"Pregnancy Tracker ({due_date_str})",
                )
                
                # Reload the integration to apply changes
                await self.hass.config_entries.async_reload(self.config_entry.entry_id)
                
                return self.async_create_entry(title="", data={})
                
            except ValueError:
                errors["due_date"] = "invalid_date"

        # Get current values
        current_due_date = self.config_entry.data.get(CONF_DUE_DATE, date.today().isoformat())
        current_pregnancy_length = self.config_entry.data.get(
            CONF_PREGNANCY_LENGTH, DEFAULT_PREGNANCY_LENGTH
        )
        current_custom_bible_verses = self.config_entry.data.get(
            CONF_CUSTOM_BIBLE_VERSES, ""
        )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_DUE_DATE, default=current_due_date): selector.DateSelector(),
                vol.Optional(
                    CONF_PREGNANCY_LENGTH, default=current_pregnancy_length
                ): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=1, max=365, mode=selector.NumberSelectorMode.BOX
                    )
                ),
                vol.Optional(
                    CONF_CUSTOM_BIBLE_VERSES, default=current_custom_bible_verses
                ): selector.TextSelector(
                    selector.TextSelectorConfig(
                        multiline=False,
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "current_due_date": current_due_date,
            },
        )
