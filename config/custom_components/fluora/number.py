"""Support for Fluora numbers."""

import logging

from fluoraled.fluora_client import FluoraClient

from homeassistant.components.number import NumberEntity, NumberEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN, MAC_ADDRESS

_LOGGER = logging.getLogger(__name__)

ENTITY_TYPES: tuple[NumberEntityDescription, ...] = (
    NumberEntityDescription(
        key="audioGain",
        translation_key="audio_gain",
        name="Fluora Audio Gain",
        icon="mdi:volume-high",
        native_min_value=1,
        native_max_value=100,
        native_step=1,
        entity_category=EntityCategory.CONFIG,
    ),
    NumberEntityDescription(
        key="audioAttack",
        translation_key="audio_attack",
        name="Fluora Audio Attack",
        icon="mdi:forward",
        native_min_value=1,
        native_max_value=100,
        native_step=1,
        entity_category=EntityCategory.CONFIG,
    ),
    NumberEntityDescription(
        key="audioRelease",
        translation_key="audio_release",
        name="Fluora Audio Release",
        icon="mdi:text-short",
        native_min_value=1,
        native_max_value=100,
        native_step=1,
        entity_category=EntityCategory.CONFIG,
    ),
    NumberEntityDescription(
        key="audioFilter",
        translation_key="audio_filter",
        name="Fluora Audio Filter",
        icon="mdi:filter",
        native_min_value=1,
        native_max_value=100,
        native_step=1,
        entity_category=EntityCategory.CONFIG,
    ),
    NumberEntityDescription(
        key="paletteHue",
        translation_key="palette_hue",
        name="Fluora Palette Hue",
        icon="mdi:eyedropper-variant",
        native_min_value=1,
        native_max_value=100,
        native_step=1,
    ),
    NumberEntityDescription(
        key="paletteSaturation",
        translation_key="palette_saturation",
        name="Fluora Palette Saturation",
        icon="mdi:format-color-fill",
        native_min_value=1,
        native_max_value=100,
        native_step=1,
    ),
    NumberEntityDescription(
        key="animationBloom",
        translation_key="animation_bloom",
        name="Fluora Animation Bloom",
        icon="mdi:flower-outline",
        native_min_value=1,
        native_max_value=100,
        native_step=1,
    ),
    NumberEntityDescription(
        key="animationSpeed",
        translation_key="animation_speed",
        name="Fluora Animation Speed",
        icon="mdi:speedometer",
        native_min_value=1,
        native_max_value=100,
        native_step=1,
    ),
    NumberEntityDescription(
        key="animationSize",
        translation_key="animation_size",
        name="Fluora Animation Size",
        icon="mdi:image-size-select-small",
        native_min_value=1,
        native_max_value=100,
        native_step=1,
    ),
)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    DiscoveryInfo: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Fluora Plant Switch platform."""
    plant_client = hass.data["fluora"]["plant_client"]
    add_entities(FluoraNumberEntity(plant_client, entity) for entity in ENTITY_TYPES)


class FluoraNumberEntity(NumberEntity):
    """Fluora Plant Number Entity."""

    def __init__(
        self,
        plant_client: FluoraClient,
        description: NumberEntityDescription,
    ) -> None:
        """Initialize the number."""
        self._client = plant_client
        self._attr_unique_id = (
            f"fluora_{MAC_ADDRESS}_number_{description.translation_key}"
        )
        # name, icon, min/max values, etc defined here
        self._entity_description = description
        self._attr_device_info = DeviceInfo(
            name="Fluora LED Plant",
            manufacturer="Fluora",
            identifiers={
                # Serial numbers are unique identifiers within a specific domain
                (str(DOMAIN), str(MAC_ADDRESS))
            },
        )
        # remove when state is received
        self._attr_native_value: float = 0.5

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        if self._attr_device_info is None:
            return None
        return self._attr_device_info

    @property
    def name(self) -> str:
        """Return the display name of this entity."""
        return str(self._entity_description.name)

    @property
    def icon(self) -> str:
        """Return the icon for this entity."""
        return str(self._entity_description.icon)

    @property
    def native_value(self) -> float | None:
        """Return the state of the Fluora number entity."""
        return self._attr_native_value

    def set_native_value(self, value: float) -> None:
        """Set the Fluora number current value."""
        _LOGGER.info("Set value %s", str(float))
        if self._entity_description.key == "audioGain":
            self._client.audio_gain_set(float(value) / 100)
        if self._entity_description.key == "audioAttack":
            self._client.audio_attack_set(float(value) / 100)
        if self._entity_description.key == "audioRelease":
            self._client.audio_release_set(float(value) / 100)
        if self._entity_description.key == "audioFilter":
            self._client.audio_filter_set(float(value) / 100)
        if self._entity_description.key == "paletteHue":
            self._client.palette_hue_set(float(value) / 100)
        if self._entity_description.key == "paletteSaturation":
            self._client.palette_saturation_set(float(value) / 100)
        if self._entity_description.key == "animationBloom":
            self._client.animation_control_bloom(float(value) / 100)
        if self._entity_description.key == "animationSpeed":
            self._client.animation_control_speed(float(value) / 100)
        if self._entity_description.key == "animationSize":
            self._client.animation_control_size(float(value) / 100)

        self._attr_native_value = float(value)
        self.schedule_update_ha_state()
