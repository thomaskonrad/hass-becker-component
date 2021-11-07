"""The becker component."""
from itertools import chain
import logging

from homeassistant.const import MATCH_ALL

from .rf_device import PyBecker

_LOGGER = logging.getLogger(__name__)


def initialise_templates(hass, templates, attribute_templates=None):
    """Initialise templates and attribute templates."""
    if attribute_templates is None:
        attribute_templates = dict()
    for template in chain(templates.values(), attribute_templates.values()):
        if template is None:
            continue
        template.hass = hass


async def async_setup(hass, config):
    """Initiate becker component for home assistant."""

    # Register this component's services
    await PyBecker.async_register_services(hass)

    return True
