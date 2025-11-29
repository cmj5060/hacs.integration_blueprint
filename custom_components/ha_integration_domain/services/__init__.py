"""Services package for ha_integration_domain."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.ha_integration_domain.const import LOGGER
from custom_components.ha_integration_domain.services.example_service import (
    async_handle_example_action,
    async_handle_reload_data,
)
from homeassistant.core import ServiceCall

if TYPE_CHECKING:
    from custom_components.ha_integration_domain.data import IntegrationBlueprintConfigEntry
    from homeassistant.core import HomeAssistant

# Service names - only used within services module
SERVICE_EXAMPLE_ACTION = "example_action"
SERVICE_RELOAD_DATA = "reload_data"


async def async_register_services(
    hass: HomeAssistant,
    entry: IntegrationBlueprintConfigEntry,
) -> None:
    """Register services for the integration."""

    async def handle_example_action(call: ServiceCall) -> None:
        """Handle the example_action service call."""
        await async_handle_example_action(hass, entry, call)

    async def handle_reload_data(call: ServiceCall) -> None:
        """Handle the reload_data service call."""
        await async_handle_reload_data(hass, entry, call)

    # Register services
    hass.services.async_register(
        entry.domain,
        SERVICE_EXAMPLE_ACTION,
        handle_example_action,
    )

    hass.services.async_register(
        entry.domain,
        SERVICE_RELOAD_DATA,
        handle_reload_data,
    )

    LOGGER.debug("Services registered for %s", entry.domain)


async def async_unregister_services(
    hass: HomeAssistant,
    entry: IntegrationBlueprintConfigEntry,
) -> None:
    """Unregister services for the integration."""
    hass.services.async_remove(entry.domain, SERVICE_EXAMPLE_ACTION)
    hass.services.async_remove(entry.domain, SERVICE_RELOAD_DATA)
    LOGGER.debug("Services unregistered for %s", entry.domain)
