"""Base entity for the Fluora integration."""

from __future__ import annotations

from homeassistant.const import ATTR_CONNECTIONS
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC, DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import FluoraDataUpdateCoordinator


def valid_global_mac_address(mac: str | None) -> bool:
    """Check if a MAC address is valid, non-locally administered address."""
    if not isinstance(mac, str):
        return False
    try:
        first_octet = int(mac.split(":")[0], 16)
        # If the second least-significant bit is set, it's a locally administered address, should not be used as an ID
        return not bool(first_octet & 0x2)
    except ValueError:
        return False


class FluoraEntity(CoordinatorEntity[FluoraDataUpdateCoordinator], Entity):
    """Defines a Fluora entity."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: FluoraDataUpdateCoordinator) -> None:
        """Initialize the Fluora entity."""
        super().__init__(coordinator=coordinator)

        device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.data["deviceID"])},
            name=coordinator.data["deviceName"],
            manufacturer=coordinator.data["deviceManufacturer"],
            model=coordinator.data["deviceModel"],
            sw_version=coordinator.data["appVersionName"],
        )
        if "Mac" in coordinator.data and valid_global_mac_address(
            coordinator.data["Mac"]
        ):
            device_info[ATTR_CONNECTIONS] = {
                (CONNECTION_NETWORK_MAC, coordinator.data["Mac"])
            }
        self._attr_device_info = device_info
