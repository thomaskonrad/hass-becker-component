"""Handling of the Becker USB device."""

import logging
import os

import voluptuous as vol
from pybecker.becker import Becker

from .const import CONF_CHANNEL, CONF_UNIT, DEFAULT_CONF_USB_STICK_PATH, DOMAIN

_LOGGER = logging.getLogger(__name__)

PAIR_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_CHANNEL): vol.All(int, vol.Range(min=1, max=7)),
        vol.Optional(CONF_UNIT): vol.All(int, vol.Range(min=1, max=5)),
    }
)

DEFAULT_DATABASE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'centronic-stick.db')

class PyBecker:
    """Manages a (single, global) pybecker Becker instance."""

    becker = None

    @classmethod
    def setup(cls, stick_path=None):
        """Initiate becker instance."""

        if not stick_path:
            stick_path = DEFAULT_CONF_USB_STICK_PATH

        cls.becker = Becker(stick_path, True, DEFAULT_DATABASE_PATH)

    @classmethod
    async def async_register_services(cls, hass):
        """Register component services."""

        hass.services.async_register(DOMAIN, "pair", cls.handle_pair, PAIR_SCHEMA)
        hass.services.async_register(DOMAIN, "log_units", cls.handle_log_units)

    @classmethod
    async def handle_pair(cls, call):
        """Service to pair with a cover receiver."""

        channel = call.data.get(CONF_CHANNEL)
        unit = call.data.get(CONF_UNIT, 1)
        await cls.becker.pair(f"{unit}:{channel}")

    @classmethod
    async def handle_log_units(cls, call):
        """Service that logs all paired units."""
        units = await cls.becker.list_units()

        # Apparently the SQLite results are implicitly returned in unit id
        # order. This seems pretty dirty to rely on.
        unit_id = 1
        _LOGGER.info("Configured Becker centronic units:")
        for row in units:
            unit_code, increment = row[0:2]
            _LOGGER.info(
                "Unit id %d, unit code %s, increment %d", unit_id, unit_code, increment
            )
            unit_id += 1
