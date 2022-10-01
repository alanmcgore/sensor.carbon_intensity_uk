"""Sensor platform for carbon intensity UK."""
from custom_components.carbon_intensity_uk.const import (
    DEFAULT_NAME,
    DOMAIN,
    ICON,
    HIGH_ICON,
    LOW_ICON,
    MODERATE_ICON,
    SENSOR,
    INTENSITY,
)
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
from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import cast

from . import CarbonIntensityDataUpdateCoordinator

@dataclass
class CO2SensorEntityDescription(SensorEntityDescription):
    """Provide a description of a CO2 sensor."""

    # For backwards compat, allow description to override unique ID key to use
    unique_id: str | None = None

SENSORS = (
    CO2SensorEntityDescription(
        key="carbonIntensityUKRegional",
        name="CO2 intensity UK Regional",
        unique_id="co2intensityUKRegional",
        native_unit_of_measurement="gCO2eq/KWh"
    ),
    CO2SensorEntityDescription(
        key="fossilFuelPercentageUKRegional",
        name="Grid fossil fuel percentage UK Regional",
        native_unit_of_measurement=PERCENTAGE,
    ),
    CO2SensorEntityDescription(
        key="lowCarbonPercentageUKRegional",
        name="Grid low carbon percentage UK Regional",
        native_unit_of_measurement=PERCENTAGE,
    ),
    CO2SensorEntityDescription(
        key="carbonIntensityForecastRegional",
        name="Grid carbon intensity forecast (48h, regional)"
    )
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Carbon Intensity sensor."""
    coordinator: CarbonIntensityDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(CarbonIntensitySensor(coordinator, description) for description in SENSORS)


class CarbonIntensitySensor(CoordinatorEntity[CarbonIntensityDataUpdateCoordinator], SensorEntity):
    """Carbon Intensity Sensor class."""
    entity_description: CO2SensorEntityDescription
    _attr_attribution = ""
    _attr_has_entity_name = True
    _attr_icon = "mdi:molecule-co2"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self, coordinator: CarbonIntensityDataUpdateCoordinator, description: CO2SensorEntityDescription
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description

        # self._attr_extra_state_attributes = {
        #     "country_code": coordinator.data["countryCode"],
        # }
        self._attr_device_info = DeviceInfo(
            configuration_url="https://github.com/alanmcgore/sensor.carbon_intensity_uk",
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, coordinator.entry_id)},
            manufacturer="https://github.com/alanmcgore/sensor.carbon_intensity_uk",
            name="Carbon Intensity Sensor",
        )
        self._attr_unique_id = (
            f"{coordinator.entry_id}_{description.unique_id or description.key}"
        )

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            super().available
            and self.entity_description.key in self.coordinator.data["data"]
        )

    @property
    def native_value(self) -> float | None:
        """Return sensor state."""
        if (value := self.coordinator.data["data"][self.entity_description.key]) is None:  # type: ignore[literal-required]
            return None
        return round(value, 2)

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the unit of measurement."""
        if self.entity_description.native_unit_of_measurement:
            return self.entity_description.native_unit_of_measurement
        return cast(
            str, self.coordinator.data["units"].get(self.entity_description.key)
        )

# class CarbonIntensitySensor(CarbonIntensityEntity):
#     """Carbon Intensity Sensor class."""

#     @property
#     def name(self):
#         """Return the name of the sensor."""
#         return f"{DEFAULT_NAME}"

#     @property
#     def state(self):
#         """Return the state of the sensor."""
#         return self.coordinator.data.get("current_period_index")

#     @property
#     def icon(self):
#         """Return the icon of the sensor."""
#         index = self.coordinator.data.get("current_period_index")
#         intensity = INTENSITY[index]
#         if intensity >= INTENSITY["high"]:
#             return HIGH_ICON
#         elif intensity == INTENSITY["moderate"]:
#             return MODERATE_ICON
#         elif intensity <= INTENSITY["low"]:
#             return LOW_ICON
#         else:
#             return ICON

# class CarbonIntensitySensor2(CarbonIntensityEntity2):
#     """Carbon Intensity Sensor class2."""

#     @property
#     def name(self):
#         """Return the name of the sensor."""
#         return f"CO2 Sensor 2"

#     @property
#     def state(self):
#         """Return the state of the sensor."""
#         return self.coordinator.data.get("current_period_forecast")