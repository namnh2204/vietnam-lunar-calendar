"""Config flow for Vietnamese Lunar Calendar integration."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

DOMAIN = "vietnamese_lunar_calendar"


class VietnameseLunarCalendarConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Vietnamese Lunar Calendar."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            # Check if already configured
            await self.async_set_unique_id("vietnamese_lunar_calendar")
            self._abort_if_unique_id_configured()
            
            return self.async_create_entry(
                title="Vietnamese Lunar Calendar",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
            description_placeholders={"name": "Vietnamese Lunar Calendar"},
        )
