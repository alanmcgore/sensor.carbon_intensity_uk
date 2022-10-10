"""
Custom integration to integrate UK Carbon Intensity API with Home Assistant.

For more details about this integration, please refer to
https://github.com/alanmcgore/sensor.carbon_intensity_uk
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, TypedDict, cast
from collections.abc import Mapping

from homeassistant.const import Platform
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from carbonintensity.client import Client as CarbonIntensityApi

from .const import (
    CONF_POSTCODE,
    DOMAIN,
    PLATFORMS,
    STARTUP_MESSAGE,
)


class CO2SignalData(TypedDict):
    """Data field."""

    carbonIntensity: int
    fossilFuelPercentage: float
    forecast: list
    lowCarbonPercentage: float
    status: str
    optimalFrom: datetime
    optimalTo: datetime


class CO2SignalResponse(TypedDict):
    """API response."""

    status: str
    data: CO2SignalData


SCAN_INTERVAL = timedelta(seconds=600)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    postcode = entry.data.get(CONF_POSTCODE)
    _LOGGER.debug("Postcode setup: %s" % postcode)

    coordinator = CarbonIntensityDataUpdateCoordinator(hass, entry, postcode=postcode)
    _LOGGER.debug("Coordinator refresh triggered")
    await coordinator.async_config_entry_first_refresh()
    _LOGGER.debug("Coordinator refresh completed")
    if not coordinator.last_update_success:
        raise ConfigEntryNotReady
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Handle removal of an entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
                if platform in coordinator.platforms
            ]
        )
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


class CarbonIntensityDataUpdateCoordinator(DataUpdateCoordinator[CO2SignalResponse]):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, postcode):
        """Initialize."""
        self.api = CarbonIntensityApi(postcode)
        self.platforms = PLATFORMS

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )
        self._entry = entry

    @property
    def entry_id(self) -> str:
        """Return entry ID."""
        return self._entry.entry_id

    async def _async_update_data(self) -> CO2SignalResponse:
        """Update data via library."""
        try:
            _LOGGER.debug("Coordinator update data async")
            data = await self.api.async_get_data()
            _LOGGER.debug("Coordinator update done")
            responseData: CO2SignalData = {
                "carbonIntensity": data.get("data").get("current_period_forecast"),
                "fossilFuelPercentage": data.get("data").get(
                    "current_fossil_fuel_percentage"
                ),
                "forecast": data.get("data").get("forecast"),
                "lowCarbonPercentage": data.get("data").get(
                    "current_low_carbon_percentage"
                ),
                "status": data.get("data").get("current_period_index"),
                "optimalTo": data.get("data").get("optimal_window_to"),
                "optimalFrom": data.get("data").get("optimal_window_from"),
            }

            response: CO2SignalResponse = {
                "status": data.get("data").get("current_period_index"),
                "data": responseData,
            }

            _LOGGER.debug(
                f"update_data carbonIntensity response is: {response['data']}"
            )
            return response

        except Exception as exception:
            raise UpdateFailed(exception)

    async def get_data(
        hass: HomeAssistant, config: Mapping[str, Any]
    ) -> CO2SignalResponse:
        """Get data from the API."""
        if CONF_POSTCODE in config:
            postcode = None
        else:
            postcode = config.get(CONF_POSTCODE, hass.config.postcode)
        api = CarbonIntensityApi(postcode)
        data = await api.async_get_data()

        responseData: CO2SignalData = {
            "carbonIntensity": data.get("data").get("current_period_forecast"),
            "fossilFuelPercentage": data.get("data").get(
                "current_fossil_fuel_percentage"
            ),
            "forecast": data.get("data").get("forecast"),
            "lowCarbonPercentage": data.get("data").get(
                "current_low_carbon_percentage"
            ),
            "status": data.get("data").get("current_period_index"),
            "optimalTo": data.get("data").get("optimal_window_to"),
            "optimalFrom": data.get("data").get("optimal_window_from"),
        }

        response: CO2SignalResponse = {
            "status": data.get("data").get("current_period_index"),
            "data": responseData,
        }
        _LOGGER.debug(f"get_data response is: {response}")
        return response


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
