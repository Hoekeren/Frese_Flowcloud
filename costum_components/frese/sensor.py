import logging
from datetime import timedelta
import requests
from homeassistant.helpers.entity import Entity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=5)

def setup_platform(hass, config, add_entities, discovery_info=None):
    api_key = config.get("api_key")
    add_entities([FreseSensor(api_key)])

class FreseSensor(Entity):
    def __init__(self, api_key):
        self._api_key = api_key
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return "Frese API Sensor"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    def update(self):
        url = "https://frese-api.systradigital.com/prod/devices/all"
        headers = {
            "Authorization": f"Bearer {self._api_key}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            self._state = "Online"
            self._attributes = data
        else:
            self._state = "Offline"
            _LOGGER.error("Failed to update Frese API sensor")