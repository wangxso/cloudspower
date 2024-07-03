# File: custom_components/electric_usage/config_flow.py
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN  # 你的组件的域名

class ElectricUsageConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_UNKNOWN

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title=user_input["name"],
                data=user_input
            )
        
        return self.async_show_form(
            step_id="user", data_schema=vol.Schema({
                vol.Required("name"): str,
                vol.Required("api_key"): str,
            }), errors=errors
        )



    async def async_step_import(self, user_input):
        # 处理YAML文件导入的配置
        return await self.async_step_user(user_input)

    async def async_step_external(self, discovery_info):
        # 处理通过外部API发现的配置
        return await self.async_step_user(discovery_info)