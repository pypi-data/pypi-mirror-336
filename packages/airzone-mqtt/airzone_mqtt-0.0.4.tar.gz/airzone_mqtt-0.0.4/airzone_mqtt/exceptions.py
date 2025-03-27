"""Airzone MQTT Exceptions."""

from __future__ import annotations


class AirzoneMqttError(Exception):
    """Base class for Airzone MQTT errors."""


class AirzoneOffline(AirzoneMqttError):
    """Exception raised when Airzone device is offline."""


class AirzonePollError(AirzoneMqttError):
    """Exception raised when Airzone device polling fails."""


class AirzoneTimeout(AirzoneMqttError):
    """Exception raised when Airzone device times out."""
