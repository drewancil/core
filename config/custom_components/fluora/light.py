"""Platform for Floura Plant Light integration."""

from dataclasses import dataclass
import logging
from typing import Any

from fluoraled.fluora_client import FluoraClient

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_EFFECT,
    ColorMode,
    LightEntity,
    LightEntityDescription,
    LightEntityFeature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import MAC_ADDRESS

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class FluoraLightEntityDescription(LightEntityDescription):
    """Fluora Light description."""


LIGHTS: tuple[FluoraLightEntityDescription, ...] = (
    FluoraLightEntityDescription(
        key="mainLight",
        name="Fluora Light",
        icon="mdi:sprout-outline",
    ),
)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    DiscoveryInfo: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Fluora Plant Light platform."""
    plant_client = hass.data["fluora"]["plant_client"]
    add_entities(FluoraLightEntity(plant_client, entity) for entity in LIGHTS)


class FluoraLightEntity(LightEntity):
    """Fluora Plant Light Entity."""

    def __init__(
        self,
        plant_client: FluoraClient,
        description: FluoraLightEntityDescription,
    ) -> None:
        """Initialize the light."""
        self._client = plant_client
        self.entity_description = description
        self._name = description.name
        self._icon = description.icon
        self._attr_color_mode = ColorMode.BRIGHTNESS
        self._attr_supported_color_modes = {
            ColorMode.BRIGHTNESS,
        }
        self._attr_supported_features = LightEntityFeature.EFFECT

        self._attr_unique_id = f"fluora_{MAC_ADDRESS}_light"
        self._attr_is_on = None
        self._state = None
        self._brightness = None
        # self._attr_brightness = None
        self._attr_effect: str | None = None
        self._effect_list = self._client.effect_list

        super().__init__()

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        if self._attr_device_info is None:
            return None
        return self._attr_device_info

    @property
    def name(self) -> str | None:
        """Return the display name of this light."""
        if self._name is None:
            return None
        return str(self._name)

    @property
    def icon(self) -> str | None:
        """Return the icon for this light."""
        return self._icon

    @property
    def brightness(self) -> int | None:
        """Return the brightness of this light between 0..255."""
        if self._brightness is None:
            return 255
        return self._brightness

    @property
    def is_on(self) -> bool | None:
        """Return true if light is on."""
        return self._state

    @property
    def effect(self) -> str | None:
        """Return the current effect of the light."""
        return self._attr_effect

    @property
    def effect_list(self) -> list[str] | None:
        """Return the list of supported effects."""
        # return [effect.name for effect in AnimationModeManual]
        return self._effect_list

    def turn_on(self, **kwargs: Any) -> None:
        """Instruct the light to turn on."""
        self._client.power(1)
        self._attr_is_on = True
        self._state = True
        if ATTR_BRIGHTNESS in kwargs:
            self._brightness = kwargs.get(ATTR_BRIGHTNESS, 255)
            # convert the brightness to a float between 0 and 1
            convert_brightness = kwargs.get(ATTR_BRIGHTNESS, 255) / 255
            self._client.brightness_set(convert_brightness)
            self._attr_brightness = kwargs.get(ATTR_BRIGHTNESS, 255)

        if ATTR_EFFECT in kwargs:
            self._attr_effect = kwargs.get(ATTR_EFFECT)
            self._client.animation_set(str(self._attr_effect))

        self.schedule_update_ha_state()

    def turn_off(self, **kwargs: Any) -> None:
        """Instruct the light to turn off."""
        self._client.power(0)
        self._attr_is_on = False
        self._state = False
        self.schedule_update_ha_state()
