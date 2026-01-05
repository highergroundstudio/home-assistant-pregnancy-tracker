"""Config flow for Pregnancy Tracker integration."""
from __future__ import annotations

import logging
from datetime import date, datetime
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_DUE_DATE,
    CONF_PREGNANCY_LENGTH,
    CONF_COMPARISON_MODE,
    DEFAULT_PREGNANCY_LENGTH,
    DEFAULT_COMPARISON_MODE,
    COMPARISON_MODE_VEGGIE,
    COMPARISON_MODE_DAD,
)

_LOGGER = logging.getLogger(__name__)


class PregnancyTrackerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Pregnancy Tracker."""

    VERSION = 1

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
                            CONF_COMPARISON_MODE: user_input.get(
                                CONF_COMPARISON_MODE, DEFAULT_COMPARISON_MODE
                            ),
                        },
                    )
            except ValueError:
                errors["due_date"] = "invalid_date"

        data_schema = vol.Schema(
            {
                vol.Required(CONF_DUE_DATE): str,
                vol.Optional(
                    CONF_PREGNANCY_LENGTH, default=DEFAULT_PREGNANCY_LENGTH
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=365)),
                vol.Optional(
                    CONF_COMPARISON_MODE, default=DEFAULT_COMPARISON_MODE
                ): vol.In([COMPARISON_MODE_VEGGIE, COMPARISON_MODE_DAD]),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )
