"""Config flow for the Message Queue integration."""

import re

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_DEFAULT_SHOW_SECONDS,
    CONF_QUEUES,
    CONF_ROTATION_INTERVAL,
    DEFAULT_ROTATION_INTERVAL,
    DEFAULT_SHOW_SECONDS,
    DOMAIN,
)

QUEUE_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


class MessageQueueConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle the initial config flow for Message Queue."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Handle the initial setup step."""
        # Only allow one instance of the integration
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            return self.async_create_entry(
                title="Message Queue",
                data={
                    CONF_ROTATION_INTERVAL: user_input[CONF_ROTATION_INTERVAL],
                    CONF_DEFAULT_SHOW_SECONDS: user_input[CONF_DEFAULT_SHOW_SECONDS],
                },
                options={
                    CONF_QUEUES: [],
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(
                    CONF_ROTATION_INTERVAL, default=DEFAULT_ROTATION_INTERVAL
                ): vol.All(int, vol.Range(min=1)),
                vol.Required(
                    CONF_DEFAULT_SHOW_SECONDS, default=DEFAULT_SHOW_SECONDS
                ): vol.All(int, vol.Range(min=1)),
            }),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Get the options flow handler."""
        return MessageQueueOptionsFlow(config_entry)


class MessageQueueOptionsFlow(OptionsFlow):
    """Handle options flow for managing queues and settings."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        self._config_entry = config_entry

    async def async_step_init(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Show the options menu."""
        return self.async_show_menu(
            step_id="init",
            menu_options=["add_queue", "remove_queue", "settings"],
        )

    async def async_step_add_queue(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Add a new queue."""
        errors = {}

        if user_input is not None:
            queue_name = user_input["queue_name"].strip().lower()
            existing = self._config_entry.options.get(CONF_QUEUES, [])

            if not QUEUE_NAME_PATTERN.match(queue_name):
                errors["queue_name"] = "invalid_name"
            elif queue_name in existing:
                errors["queue_name"] = "duplicate_name"
            else:
                new_queues = [*existing, queue_name]
                return self.async_create_entry(
                    data={
                        **self._config_entry.options,
                        CONF_QUEUES: new_queues,
                    },
                )

        return self.async_show_form(
            step_id="add_queue",
            data_schema=vol.Schema({
                vol.Required("queue_name"): str,
            }),
            errors=errors,
        )

    async def async_step_remove_queue(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Remove an existing queue."""
        existing = self._config_entry.options.get(CONF_QUEUES, [])

        if not existing:
            return self.async_abort(reason="no_queues")

        if user_input is not None:
            queue_name = user_input["queue_name"]
            new_queues = [q for q in existing if q != queue_name]
            return self.async_create_entry(
                data={
                    **self._config_entry.options,
                    CONF_QUEUES: new_queues,
                },
            )

        return self.async_show_form(
            step_id="remove_queue",
            data_schema=vol.Schema({
                vol.Required("queue_name"): vol.In(
                    {q: q for q in existing}
                ),
            }),
        )

    async def async_step_settings(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Edit global settings."""
        if user_input is not None:
            # Update data on the config entry (not options)
            self.hass.config_entries.async_update_entry(
                self._config_entry,
                data={
                    **self._config_entry.data,
                    CONF_ROTATION_INTERVAL: user_input[CONF_ROTATION_INTERVAL],
                    CONF_DEFAULT_SHOW_SECONDS: user_input[CONF_DEFAULT_SHOW_SECONDS],
                },
            )
            return self.async_create_entry(data=self._config_entry.options)

        current_data = self._config_entry.data
        return self.async_show_form(
            step_id="settings",
            data_schema=vol.Schema({
                vol.Required(
                    CONF_ROTATION_INTERVAL,
                    default=current_data.get(
                        CONF_ROTATION_INTERVAL, DEFAULT_ROTATION_INTERVAL
                    ),
                ): vol.All(int, vol.Range(min=1)),
                vol.Required(
                    CONF_DEFAULT_SHOW_SECONDS,
                    default=current_data.get(
                        CONF_DEFAULT_SHOW_SECONDS, DEFAULT_SHOW_SECONDS
                    ),
                ): vol.All(int, vol.Range(min=1)),
            }),
        )
