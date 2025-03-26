"""Airzone MQTT System."""

import logging
from typing import Any

from .device import Device
from .update import UpdateType

_LOGGER = logging.getLogger(__name__)


class System(Device):
    """Airzone MQTT System."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Airzone MQTT System init."""
        super().__init__(data)

        _LOGGER.debug("System created with id=%s", self.device_id)

        self.update(data, UpdateType.FULL)

    def data(self) -> dict[str, Any]:
        """Airzone MQTT System data."""
        data = super().data()

        return data

    def update(self, data: dict[str, Any], update_type: UpdateType) -> None:
        """Airzone MQTT System update data."""
        super().update(data, update_type)

        if update_type == UpdateType.PARTIAL:
            _LOGGER.warning("System[%s] updated with data=%s", self.get_id(), data)
