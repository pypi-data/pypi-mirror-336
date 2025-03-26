"""Airzone MQTT Zone."""

import logging
from typing import Any

from .common import AirzoneMode
from .const import (
    API_AIR_ACTIVE,
    API_HUMIDITY,
    API_MAX,
    API_MIN,
    API_MODE,
    API_MODE_AVAILABLE,
    API_NAME,
    API_PARAMETERS,
    API_POWER,
    API_RAD_ACTIVE,
    API_RANGE_SP,
    API_SETPOINT,
    API_STEP,
    API_ZONE_WORK_TEMP,
    AZD_ACTIVE,
    AZD_AIR_ACTIVE,
    AZD_HUMIDITY,
    AZD_MODE,
    AZD_MODE_AVAILABLE,
    AZD_NAME,
    AZD_POWER,
    AZD_RAD_ACTIVE,
    AZD_SETPOINT,
    AZD_SETPOINT_MAX,
    AZD_SETPOINT_MIN,
    AZD_STEP,
    AZD_ZONE_WORK_TEMP,
)
from .device import Device
from .update import UpdateType

_LOGGER = logging.getLogger(__name__)


class Zone(Device):
    """Airzone MQTT Zone."""

    name: str

    def __init__(self, data: dict[str, Any]) -> None:
        """Airzone MQTT Zone init."""
        super().__init__(data)

        self.air_active: bool | None = None
        self.humidity: int | None = None
        self.mode: AirzoneMode | None = None
        self.mode_available: list[AirzoneMode] = []
        self.power: bool | None = None
        self.rad_active: bool | None = None
        self.setpoint: float | None = None
        self.step: float | None = None
        self.zone_work_temp: float | None = None

        _LOGGER.debug("Zone created with id=%s", self.device_id)

        self.update(data, UpdateType.FULL)

    def get_active(self) -> bool:
        """Airzone MQTT Zone active."""
        return bool(self.air_active) or bool(self.rad_active)

    def get_air_active(self) -> bool | None:
        """Airzone MQTT Zone air active."""
        return self.air_active

    def get_humidity(self) -> int | None:
        """Airzone MQTT Zone humidity."""
        return self.humidity

    def get_mode(self) -> AirzoneMode | None:
        """Airzone MQTT Zone mode."""
        return self.mode

    def get_mode_available(self) -> list[AirzoneMode] | None:
        """Airzone MQTT Zone mode available."""
        if len(self.mode_available) > 0:
            return self.mode_available
        return None

    def get_name(self) -> str:
        """Airzone MQTT Zone name."""
        if self.name is not None:
            return self.name
        return f"Zone [{self.get_id()}]"

    def get_power(self) -> bool | None:
        """Airzone MQTT Zone power."""
        return self.power

    def get_rad_active(self) -> bool | None:
        """Airzone MQTT Zone rad active."""
        return self.rad_active

    def get_setpoint(self) -> float | None:
        """Airzone MQTT Zone setpoint."""
        if self.setpoint is not None:
            return round(self.setpoint, 1)
        return None

    def get_setpoint_max(self) -> float | None:
        """Airzone MQTT Zone max setpoint."""
        if self.setpoint_max is not None:
            return round(self.setpoint_max, 1)
        return None

    def get_setpoint_min(self) -> float | None:
        """Airzone MQTT Zone min setpoint."""
        if self.setpoint_min is not None:
            return round(self.setpoint_min, 1)
        return None

    def get_step(self) -> float | None:
        """Airzone MQTT Zone step."""
        if self.step is not None:
            return round(self.step, 1)
        return None

    def get_zone_work_temp(self) -> float | None:
        """Airzone MQTT Zone work temp."""
        if self.zone_work_temp is not None:
            return round(self.zone_work_temp, 1)
        return None

    def data(self) -> dict[str, Any]:
        """Airzone MQTT Zone data."""
        data = super().data()

        data[AZD_ACTIVE] = self.get_active()

        air_active = self.get_air_active()
        if air_active is not None:
            data[AZD_AIR_ACTIVE] = air_active

        humidity = self.get_humidity()
        if humidity is not None:
            data[AZD_HUMIDITY] = humidity

        mode = self.get_mode()
        if mode is not None:
            data[AZD_MODE] = mode

        mode_available = self.get_mode_available()
        if mode_available is not None:
            data[AZD_MODE_AVAILABLE] = mode_available

        name = self.get_name()
        if name is not None:
            data[AZD_NAME] = name

        power = self.get_power()
        if power is not None:
            data[AZD_POWER] = power

        rad_active = self.get_rad_active()
        if rad_active is not None:
            data[AZD_RAD_ACTIVE] = rad_active

        setpoint = self.get_setpoint()
        if setpoint is not None:
            data[AZD_SETPOINT] = setpoint

        setpoint_max = self.get_setpoint_max()
        if setpoint_max is not None:
            data[AZD_SETPOINT_MAX] = setpoint_max

        setpoint_min = self.get_setpoint_min()
        if setpoint_min is not None:
            data[AZD_SETPOINT_MIN] = setpoint_min

        step = self.get_step()
        if step is not None:
            data[AZD_STEP] = step

        zone_work_temp = self.get_zone_work_temp()
        if zone_work_temp is not None:
            data[AZD_ZONE_WORK_TEMP] = zone_work_temp

        return data

    def update(self, data: dict[str, Any], update_type: UpdateType) -> None:
        """Airzone MQTT Zone update data."""
        super().update(data, update_type)

        parameters: dict[str, Any] = data.get(API_PARAMETERS, {})

        air_active = parameters.get(API_AIR_ACTIVE)
        if air_active is not None:
            self.air_active = bool(air_active)

        humidity = parameters.get(API_HUMIDITY)
        if humidity is not None:
            self.humidity = int(humidity)

        mode = parameters.get(API_MODE)
        if mode is not None:
            self.mode = AirzoneMode(mode)

        mode_available = parameters.get(API_MODE_AVAILABLE)
        if mode_available is not None:
            self.mode_available = []
            for cur_mode in mode_available:
                self.mode_available.extend([AirzoneMode(cur_mode)])

        name = parameters.get(API_NAME)
        if name is not None:
            self.name = str(name)

        power = parameters.get(API_POWER)
        if power is not None:
            self.power = bool(power)

        rad_active = parameters.get(API_RAD_ACTIVE)
        if rad_active is not None:
            self.rad_active = bool(rad_active)

        range_sp = parameters.get(API_RANGE_SP, {})
        setpoint_max = range_sp.get(API_MAX)
        if setpoint_max is not None:
            self.setpoint_max = float(setpoint_max)
        setpoint_min = range_sp.get(API_MIN)
        if setpoint_min is not None:
            self.setpoint_min = float(setpoint_min)

        setpoint = parameters.get(API_SETPOINT)
        if setpoint is not None:
            self.setpoint = float(setpoint)

        step = parameters.get(API_STEP)
        if step is not None:
            self.step = float(step)

        zone_work_temp = parameters.get(API_ZONE_WORK_TEMP)
        if zone_work_temp is not None:
            self.zone_work_temp = float(zone_work_temp)

        if update_type == UpdateType.PARTIAL:
            _LOGGER.warning("Zone[%s] updated with data=%s", self.get_id(), data)
