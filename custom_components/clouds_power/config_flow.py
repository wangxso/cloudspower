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
            # 验证用户输入的数据
            valid = await self._validate_user_input(user_input)

            if valid:
                # 如果数据有效，创建配置条目
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

    @staticmethod
    async def _validate_user_input(user_input):
        # 这里实现API调用以验证API密钥是否有效
        session = async_get_clientsession(self.hass)
        try:
            response = await session.get(f"https://api.yourdomain.com/validate", params={
                "api_key": user_input["api_key"]
            })
            response.raise_for_status()
            return True
        except Exception:
            return False

    async def async_step_import(self, user_input):
        # 处理YAML文件导入的配置
        return await self.async_step_user(user_input)

    async def async_step_external(self, discovery_info):
        # 处理通过外部API发现的配置
        return await self.async_step_user(discovery_info)