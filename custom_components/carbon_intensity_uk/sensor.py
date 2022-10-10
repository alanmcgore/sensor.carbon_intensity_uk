"""Sensor platform for carbon intensity UK."""
from __future__ import annotations
from typing import cast
from dataclasses import dataclass
from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DEFAULT_NAME,
    DOMAIN,
    ICON,
    HIGH_ICON,
    LOW_ICON,
    MODERATE_ICON,
    SENSOR,
    INTENSITY,
)

from . import CarbonIntensityDataUpdateCoordinator


@dataclass
class CO2SensorEntityDescription(SensorEntityDescription):
    """Provide a description of a CO2 sensor."""

    # For backwards compat, allow description to override unique ID key to use
    unique_id: str | None = None


SENSORS = (
    CO2SensorEntityDescription(
        key="carbonIntensity",
        name="Local Grid CO2 Intensity",
        unique_id="co2intensityUKRegional",
        native_unit_of_measurement="gCO2eq/kWh",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    CO2SensorEntityDescription(
        key="fossilFuelPercentage",
        name="Local Grid Fossil Fuel %",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    CO2SensorEntityDescription(
        key="lowCarbonPercentage",
        name="Local Grid Low Carbon %",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    CO2SensorEntityDescription(
        key="forecast",
        name="Local CO2 intensity forecast (48h)",
        state_class=None,
    ),
    CO2SensorEntityDescription(
        key="status", name="Local Grid CO2 Levels", state_class=None
    ),
    CO2SensorEntityDescription(
        key="optimalFrom", name="Local Optimal Window From", state_class=None
    ),
    CO2SensorEntityDescription(
        key="optimalTo", name="Local Optimal Window To", state_class=None
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Carbon Intensity sensor."""
    coordinator: CarbonIntensityDataUpdateCoordinator = hass.data[DOMAIN][
        entry.entry_id
    ]
    async_add_entities(
        CarbonIntensitySensor(coordinator, description) for description in SENSORS
    )


class CarbonIntensitySensor(
    CoordinatorEntity[CarbonIntensityDataUpdateCoordinator], SensorEntity
):
    """Carbon Intensity Sensor class."""

    entity_description: CO2SensorEntityDescription
    _attr_attribution = ""
    _attr_has_entity_name = True
    _attr_icon = "mdi:molecule-co2"

    def __init__(
        self,
        coordinator: CarbonIntensityDataUpdateCoordinator,
        description: CO2SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_state_class = description.state_class

        if description.key == "forecast":
            self._attr_extra_state_attributes = {
                "forecast": self.coordinator.data["data"][self.entity_description.key]
            }

        self._attr_device_info = DeviceInfo(
            configuration_url="https://github.com/alanmcgore/sensor.carbon_intensity_uk",
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, coordinator.entry_id)},
            manufacturer="Carbon Intensity UK",
            name="Grid CO2 UK",
        )
        self._attr_unique_id = f"{description.unique_id or description.key}"

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            super().available
            # and self.entity_description.key in self.coordinator.data["data"]
        )

    @property
    def state(self):
        """Return the state of the sensor."""
        if isinstance(self.coordinator.data["data"][self.entity_description.key], list):
            return None
        return self.coordinator.data["data"][self.entity_description.key]

    @property
    def native_value(self) -> float | None:
        """Return sensor state."""
        if isinstance(
            value := self.coordinator.data["data"][self.entity_description.key], list
        ):
            return None
        return round(value, 2)

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the unit of measurement."""
        if self.entity_description.native_unit_of_measurement:
            return self.entity_description.native_unit_of_measurement

    @property
    def icon(self):
        """Return the icon of the sensor."""
        index = self.coordinator.data.get("status")

        intensity = INTENSITY[index]
        if intensity >= INTENSITY["high"]:
            return HIGH_ICON
        elif intensity == INTENSITY["moderate"]:
            return MODERATE_ICON
        elif intensity <= INTENSITY["low"]:
            return LOW_ICON
        else:
            return ICON
