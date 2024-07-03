# File: custom_components/electric_usage/sensor.py
import json
import requests
from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import BASE_URL, DEVICE_INFO, DOMAIN


async def async_setup_platform(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities, discovery_info=None):
    # 配置API URL和可能的认证信息
    url = BASE_URL+DEVICE_INFO
    headers = {
        # 如果需要认证
        # "Authorization": "Bearer YOUR_API_TOKEN",
    }

    
    api_key = config_entry.data.get('api_key')
    data = {
        "device_type_id": 1,
        "time": 30,
        "login_key": api_key,
        "browser": 1
    }
    # 获取JSON数据
    response = requests.post(url, headers=headers)
    data = response.json()
    
    # 解析数据
    org_data = data.get('orgData', {})
    device_info = org_data.get('device', {})
    degree_all = device_info.get('degree_all')
    price = device_info.get('price')
    
    # 创建传感器实体
    sensor = ElectricUsageSensor('Electric Usage', degree_all, price)
    async_add_entities([sensor])

class ElectricUsageSensor(Entity):
    def __init__(self, name, degree_all, price):
        self._name = name
        self._degree_all = degree_all
        self._price = price
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        # 根据你的需求返回电量、费用或其他数据
        return self._state

    @property
    def extra_state_attributes(self):
        # 返回额外的状态属性，例如费用
        return {
            'total_degree': self._degree_all,
            'total_price': self._price
        }

    def update(self):
        # 这里将包含逻辑来定期更新传感器状态
        # 例如，你可以在这里重新调用API并更新self._state
        pass