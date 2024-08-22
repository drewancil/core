"""Platform for Floura Plant button integration."""

import logging

from fluoraled.fluora_client import FluoraClient

from homeassistant.components.button import ButtonEntity
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
    """Set up the Fluora Plant Button platform."""
    plant_client = hass.data["fluora"]["plant_client"]
    add_entities([FluoraButton(plant_client)])


class FluoraButton(ButtonEntity):
    """."""

    def __init__(
        self,
        plant_client: FluoraClient,
    ) -> None:
        """Initialize the button."""
        self._client = plant_client
        self._name = "Fluora Reboot"
        self._icon = "mdi:restart"
        self._attr_unique_id = f"fluora_{MAC_ADDRESS}_button_reboot"

    @property
    def name(self) -> str:
        """Return the display name of this button."""
        return self._name

    @property
    def icon(self) -> str:
        """Return the icon for this light."""
        return self._icon

    def press(self) -> None:
        """Handle the button press."""
        self._client.reboot()
