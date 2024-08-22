"""Fluora LED Plant integration."""

from __future__ import annotations

import logging

from fluoraled.fluora_client import FluoraClient

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, IP_ADDRESS, PORT_NUMBER

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [
    Platform.BUTTON,
    Platform.LIGHT,
    Platform.NUMBER,
    Platform.SWITCH,
]


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Your controller/hub specific code."""
    # Data that you want to share with your platforms

    plant = FluoraClient(IP_ADDRESS, PORT_NUMBER)
    hass.data[DOMAIN] = {"plant_client": plant}

    hass.helpers.discovery.load_platform(Platform.BUTTON.value, DOMAIN, {}, config)
    hass.helpers.discovery.load_platform(Platform.LIGHT.value, DOMAIN, {}, config)
    hass.helpers.discovery.load_platform(Platform.NUMBER.value, DOMAIN, {}, config)
    hass.helpers.discovery.load_platform(Platform.SWITCH.value, DOMAIN, {}, config)

    return True
