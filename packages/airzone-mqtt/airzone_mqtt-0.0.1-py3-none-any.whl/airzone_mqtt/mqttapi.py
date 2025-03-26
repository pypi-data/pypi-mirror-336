"""Airzone MQTT API."""

import asyncio
from collections.abc import Callable, Coroutine
from datetime import datetime
import json
import logging
from typing import Any

from .common import get_current_dt
from .const import (
    AMT_EVENTS,
    AMT_INVOKE,
    AMT_ONLINE,
    AMT_REQUEST,
    AMT_RESPONSE,
    AMT_STATUS,
    AMT_V1,
    API_AZ_GET_STATUS,
    API_AZ_SYSTEM,
    API_AZ_ZONE,
    API_BODY,
    API_CMD,
    API_DESTINATION,
    API_DEVICE_ID,
    API_DEVICE_TYPE,
    API_DEVICES,
    API_HEADERS,
    API_ONLINE,
    API_REQ_ID,
    API_SYSTEM_ID,
    API_TS,
    AZD_ONLINE,
    AZD_SYSTEMS,
    AZD_ZONES,
    EVENTS_TIMEOUT,
    POLL_TIMEOUT,
    TZ_UTC,
)
from .exceptions import AirzoneOffline, AirzonePollError, AirzoneTimeout
from .system import System
from .update import UpdateType
from .zone import Zone

ReceivePayloadType = str | bytes | bytearray
PayloadType = str | int | float | None

_LOGGER = logging.getLogger(__name__)


class AirzoneMqttApi:
    """Airzone MQTT API."""

    callback_function: Callable[[dict[str, Any]], None] | None
    callback_lock: asyncio.Lock
    mqtt_publish: Callable[[str, PayloadType, int, bool], Coroutine[Any, Any, None]]

    def __init__(self, mqtt_topic: str) -> None:
        """Airzone MQTT API init."""
        self.api_init: bool = False
        self.api_lock: asyncio.Lock = asyncio.Lock()
        self.api_raw_data: dict[str, Any] = {
            API_AZ_GET_STATUS: None,
        }
        self.api_resp: asyncio.Event = asyncio.Event()
        self.api_req_id: str = ""
        self.callback_function = None
        self.callback_lock = asyncio.Lock()
        self.loop = asyncio.get_running_loop()
        self.mqtt_prefix: str = f"{mqtt_topic}/{AMT_V1}"
        self.mqtt_topic: str = mqtt_topic
        self.online: bool = False
        self.update_dt: datetime | None = None
        self.systems: dict[str, System] = {}
        self.zones: dict[str, Zone] = {}

        cur_dt = get_current_dt()
        cur_date = f"{cur_dt.year}/{cur_dt.month}/{cur_dt.day}"
        cur_time = f"{cur_dt.hour}:{cur_dt.minute}:{cur_dt.second}"
        cur_us = cur_dt.microsecond
        self.mqtt_req_id = f"{cur_date}-{cur_time}.{cur_us}"

    def api_safe_str(self, topic: str) -> str:
        """Airzone MQTT API safe string."""
        return topic.replace(".", "_")

    def api_az_get_status(self, data: dict[str, Any]) -> None:
        """Airzone MQTT API az->get_status."""
        cur_dt = get_current_dt()

        self.api_raw_data[API_AZ_GET_STATUS] = data

        body: dict[str, Any] = data.get(API_BODY, {})
        devices: list[dict[str, Any]] = body.get(API_DEVICES, [])

        for device in devices:
            dev_type = device.get(API_DEVICE_TYPE)

            if dev_type == API_AZ_SYSTEM:
                system = System(device)
                system_id = system.get_id()
                if system_id not in self.systems:
                    self.systems[system_id] = system
            elif dev_type == API_AZ_ZONE:
                zone = Zone(device)
                zone_id = zone.get_id()
                if zone_id not in self.zones:
                    self.zones[zone_id] = zone
            else:
                _LOGGER.warning("api_az_get_status: unknown device=%s", device)

        _LOGGER.debug("api_az_get_status: API init done.")

        self.api_init = True
        self.update_dt = cur_dt

    def cmd_destination(self, topic: str) -> str:
        """Airzone MQTT cmd destination."""
        topic = self.api_safe_str(topic)
        return f"{self.mqtt_prefix}/{AMT_RESPONSE}/{topic}"

    def cmd_req_id(self, req_id: str) -> str:
        """Airzone MQTT cmd req_id."""
        req_id = self.api_safe_str(req_id)
        return f"{AMT_REQUEST}-{self.mqtt_req_id}-{req_id}"

    def cmd_payload(self, data: dict[str, Any]) -> str:
        """Airzone MQTT cmd payload."""
        return json.dumps(data)

    async def cmd_invoke(self, data: dict[str, Any]) -> None:
        """Airzone MQTT cmd invoke."""
        topic = f"{self.mqtt_prefix}/{AMT_INVOKE}"
        payload = self.cmd_payload(data)

        headers = data.get(API_HEADERS, {})
        req_id = headers.get(API_REQ_ID, "")

        async with self.api_lock:
            self.api_resp.clear()
            self.api_req_id = req_id
            await self.mqtt_publish(topic, payload, 0, False)
            await self.api_resp.wait()

    async def cmd_az_get_status(self) -> None:
        """Airzone MQTT cmd az->get_status."""
        data: dict[str, Any] = {
            API_HEADERS: {
                API_CMD: API_AZ_GET_STATUS,
                API_DESTINATION: self.cmd_destination(API_AZ_GET_STATUS),
                API_REQ_ID: self.cmd_req_id(API_AZ_GET_STATUS),
            },
            API_BODY: None,
        }

        await self.cmd_invoke(data)

    def msg_events_status(
        self, topic: list[str], payload: ReceivePayloadType, dt: datetime | None
    ) -> None:
        """Airzone MQTT events status message."""
        if topic[0] == AMT_STATUS:
            topic.pop(0)

        data = json.loads(payload)

        body = data.get(API_BODY, {})
        device_id = body.get(API_DEVICE_ID)
        device_type = body.get(API_DEVICE_TYPE)
        system_id = body.get(API_SYSTEM_ID)

        if device_type == API_AZ_SYSTEM:
            system = self.get_system(system_id, device_id)
            if system is not None:
                system.update(data, UpdateType.PARTIAL)
                self.update_callback(data)
        elif device_type == API_AZ_ZONE:
            zone = self.get_zone(system_id, device_id)
            if zone is not None:
                zone.update(data, UpdateType.PARTIAL)
                self.update_callback(data)
        else:
            _LOGGER.warning(
                "msg_events: topic=%s payload=%s datetime=%s", topic, payload, dt
            )

    def msg_events(
        self, topic: list[str], payload: ReceivePayloadType, dt: datetime | None
    ) -> None:
        """Airzone MQTT events message."""
        if topic[0] == AMT_EVENTS:
            topic.pop(0)

        if topic[0] == AMT_STATUS:
            self.msg_events_status(topic, payload, dt)
        else:
            _LOGGER.warning(
                "msg_events: topic=%s payload=%s datetime=%s", topic, payload, dt
            )

    def msg_invoke(
        self, topic: list[str], payload: ReceivePayloadType, dt: datetime | None
    ) -> None:
        """Airzone MQTT invoke message."""
        _LOGGER.debug("msg_invoke: topic=%s payload=%s datetime=%s", topic, payload, dt)

    def msg_online(self, payload: ReceivePayloadType) -> None:
        """Airzone MQTT online message."""
        data = json.loads(payload)

        self.online = data.get(API_ONLINE, False)

        _LOGGER.debug("Airzone MQTT online=%s.", self.online)

    def msg_response(
        self, topic: list[str], payload: ReceivePayloadType, dt: datetime | None
    ) -> None:
        """Airzone MQTT response message."""
        data = json.loads(payload)

        headers = data.get(API_HEADERS, {})
        req_id = headers.get(API_REQ_ID)

        if req_id == self.api_req_id:
            self.loop.call_soon_threadsafe(self.api_resp.set)
        else:
            _LOGGER.error("Unexpected API response: req_id=%s", req_id)

        if topic[0] == AMT_RESPONSE:
            topic.pop(0)

        if topic[0] == self.api_safe_str(API_AZ_GET_STATUS):
            self.api_az_get_status(data)
        else:
            _LOGGER.warning(
                "msg_response: topic=%s payload=%s datetime=%s", topic, payload, dt
            )

    def msg_unknown(
        self, topic: list[str], payload: ReceivePayloadType, dt: datetime | None
    ) -> None:
        """Airzone MQTT unknown message."""
        _LOGGER.warning(
            "msg_unknown: topic=%s payload=%s datetime=%s", topic, payload, dt
        )

    def msg_callback(
        self, topic_str: str, payload: ReceivePayloadType, dt: datetime | None
    ) -> None:
        """Airzone MQTT message callback."""
        topic_str = topic_str.removeprefix(f"{self.mqtt_prefix}/")

        topic = topic_str.split("/")
        if topic[0] == AMT_EVENTS:
            self.msg_events(topic, payload, dt)
        elif topic[0] == AMT_INVOKE:
            self.msg_invoke(topic, payload, dt)
        elif topic[0] == AMT_ONLINE:
            self.msg_online(payload)
        elif topic[0] == AMT_RESPONSE:
            self.msg_response(topic, payload, dt)
        else:
            self.msg_unknown(topic, payload, dt)

    def get_api_raw_data(self) -> dict[str, Any]:
        """Airzone MQTT API raw data."""
        return self.api_raw_data

    def get_system(self, system_id: str, device_id: str) -> System | None:
        """Airzone MQTT get system by IDs."""
        return self.systems.get(f"{system_id}:{device_id}")

    def get_zone(self, system_id: str, device_id: str) -> Zone | None:
        """Airzone MQTT get zone by IDs."""
        return self.zones.get(f"{system_id}:{device_id}")

    def data(self) -> dict[str, Any]:
        """Airzone MQTT data."""
        data: dict[str, Any] = {
            AZD_ONLINE: self.online,
            AZD_SYSTEMS: {},
            AZD_ZONES: {},
        }

        for system_id, system in self.systems.items():
            data[AZD_SYSTEMS][system_id] = system.data()

        for zone_id, zone in self.zones.items():
            data[AZD_ZONES][zone_id] = zone.data()

        return data

    async def _update_events(self) -> bool:
        """Perform an events update of Airzone MQTT data."""
        if not self.api_init:
            return False

        if not self.online:
            return False

        if self.update_dt is None:
            return False

        return (get_current_dt() - self.update_dt) <= EVENTS_TIMEOUT

    async def _update_polling(self) -> None:
        """Perform a polling update of Airzone MQTT data."""
        try:
            async with asyncio.timeout(POLL_TIMEOUT):
                await self.cmd_az_get_status()
        except TimeoutError as err:
            self.api_lock.release()
            raise AirzoneTimeout(err) from err

        if not self.online:
            raise AirzoneOffline("Airzone MQTT device offline")
        if not self.api_init:
            raise AirzonePollError("Airzone MQTT polling failed")

    async def update(self) -> None:
        """Airzone MQTT update."""
        if not await self._update_events():
            await self._update_polling()

    async def _update_callback(self) -> None:
        """Perform update callback."""
        if self.callback_function:
            async with self.callback_lock:
                self.callback_function(self.data())

    def update_callback(self, data: dict[str, Any]) -> None:
        """Create update callback task."""
        data_ts = data.get(API_HEADERS, {}).get(API_TS)
        if data_ts is not None:
            self.update_dt = datetime.fromtimestamp(float(data_ts), tz=TZ_UTC)
        else:
            self.update_dt = get_current_dt()

        if self.callback_function:
            asyncio.ensure_future(self._update_callback())

    def set_update_callback(
        self, callback_function: Callable[[dict[str, Any]], None]
    ) -> None:
        """Set update callback."""
        self.callback_function = callback_function
