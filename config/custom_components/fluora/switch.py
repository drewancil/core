"""Platform for Floura Plant light integration."""

import logging
from typing import Any

from fluoraled.fluora_client import FluoraClient

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import MAC_ADDRESS

_LOGGER = logging.getLogger(__name__)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    DiscoveryInfo: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Fluora Plant Switch platform."""
    plant_client = hass.data["fluora"]["plant_client"]
    add_entities([FluoraSwitch(plant_client)])


class FluoraSwitch(SwitchEntity):
    """Fluora Plant Switch Entity."""

    def __init__(
        self,
        plant_client: FluoraClient,
    ) -> None:
        """Initialize the switch."""
        self._client = plant_client
        self._name = "Fluora Light Sensor"
        self._icon = "mdi:lightbulb-night-outline"
        self._attr_unique_id = f"fluora_{MAC_ADDRESS}_switch_light_sensor"
        # self._state = None
        self._state = False

    @property
    def name(self) -> str:
        """Return the display name of this switch."""
        return self._name

    @property
    def icon(self) -> str:
        """Return the icon for this switch."""
        return self._icon

    @property
    def is_on(self) -> bool | None:
        """Return true if switch is on."""
        return self._state

    def turn_on(self, **kwargs: Any) -> None:
        """Instruct the light sensor switch to turn on."""
        self._client.light_sensor(1)
        self._state = True
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs: Any) -> None:
        """Instruct the light sensor switch to turn off."""
        self._client.light_sensor(0)
        self._state = False
        self.schedule_update_ha_state()
