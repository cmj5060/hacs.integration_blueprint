"""
DataUpdateCoordinator for ha_integration_domain.

This module implements the coordinator that manages data fetching and updates
for all entities in the integration. It handles refresh cycles, error handling,
and triggers reauthentication when needed.

For more information on coordinators:
https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import IntegrationBlueprintApiClientAuthenticationError, IntegrationBlueprintApiClientError
from .const import LOGGER

if TYPE_CHECKING:
    from .data import IntegrationBlueprintConfigEntry


class IntegrationBlueprintDataUpdateCoordinator(DataUpdateCoordinator):
    """
    Class to manage fetching data from the API.

    This coordinator handles all data fetching for the integration and distributes
    updates to all entities. It manages:
    - Periodic data updates based on update_interval
    - Error handling and recovery
    - Authentication failure detection and reauthentication triggers
    - Data distribution to all entities

    For more information:
    https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities

    Attributes:
        config_entry: The config entry for this integration instance.
    """

    config_entry: IntegrationBlueprintConfigEntry

    async def _async_update_data(self) -> Any:
        """
        Fetch data from API endpoint.

        This is the only method that should be implemented in a DataUpdateCoordinator.
        It is called automatically based on the update_interval.

        The API client uses the credentials from config_entry to authenticate:
        - username: from config_entry.data["username"]
        - password: from config_entry.data["password"]

        Expected API response structure (example):
        {
            "userId": 1,      # Used as device identifier
            "id": 1,          # Data record ID
            "title": "...",   # Additional metadata
            "body": "...",    # Additional content
            # In production, would include:
            # "air_quality": {"aqi": 45, "pm25": 12.3},
            # "filter": {"life_remaining": 75, "runtime_hours": 324},
            # "settings": {"fan_speed": "medium", "humidity": 55}
        }

        Returns:
            The data from the API as a dictionary.

        Raises:
            ConfigEntryAuthFailed: If authentication fails, triggers reauthentication.
            UpdateFailed: If data fetching fails for other reasons.
        """
        try:
            return await self.config_entry.runtime_data.client.async_get_data()
        except IntegrationBlueprintApiClientAuthenticationError as exception:
            LOGGER.warning("Authentication error - %s", exception)
            raise ConfigEntryAuthFailed(
                translation_domain="ha_integration_domain",
                translation_key="authentication_failed",
            ) from exception
        except IntegrationBlueprintApiClientError as exception:
            LOGGER.exception("Error communicating with API")
            raise UpdateFailed(
                translation_domain="ha_integration_domain",
                translation_key="update_failed",
            ) from exception
