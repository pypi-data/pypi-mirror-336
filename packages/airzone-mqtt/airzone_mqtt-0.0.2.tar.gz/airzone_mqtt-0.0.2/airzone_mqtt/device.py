"""Airzone MQTT Device."""

import logging
from typing import Any

from .common import TemperatureUnit
from .const import (
    API_DEVICE_ID,
    API_IS_CONNECTED,
    API_META,
    API_PARAMETERS,
    API_SYSTEM_ID,
    API_UNITS,
    AZD_DEVICE_ID,
    AZD_ID,
    AZD_IS_CONNECTED,
    AZD_SYSTEM_ID,
    AZD_UNITS,
)
from .update import UpdateType

_LOGGER = logging.getLogger(__name__)


class Device:
    """Airzone MQTT Device."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Airzone MQTT Device init."""
        self.device_id = data.get(API_DEVICE_ID)
        self.is_connected = False
        self.system_id = data.get(API_SYSTEM_ID)
        self.units = TemperatureUnit.CELSIUS

        _LOGGER.debug("Device created with id=%s", self.device_id)

        self.update(data, UpdateType.FULL)

    def get_id(self) -> str:
        """Airzone MQTT Device ID."""
        return f"{self.system_id}:{self.device_id}"

    def data(self) -> dict[str, Any]:
        """Airzone MQTT Device data."""
        data: dict[str, Any] = {
            AZD_DEVICE_ID: self.device_id,
            AZD_ID: self.get_id(),
            AZD_IS_CONNECTED: self.is_connected,
            AZD_SYSTEM_ID: self.system_id,
            AZD_UNITS: self.units,
        }

        return data

    def update(self, data: dict[str, Any], update_type: UpdateType) -> None:
        """Airzone MQTT Device update."""
        meta: dict[str, Any] = data.get(API_META, {})
        parameters: dict[str, Any] = data.get(API_PARAMETERS, {})

        is_connected = parameters.get(API_IS_CONNECTED)
        if is_connected is not None:
            self.is_connected = bool(is_connected)

        units = meta.get(API_UNITS)
        if units is not None:
            self.units = TemperatureUnit(units)

        if update_type == UpdateType.PARTIAL:
            _LOGGER.debug("Device[%s] updated with data=%s", self.get_id(), data)
