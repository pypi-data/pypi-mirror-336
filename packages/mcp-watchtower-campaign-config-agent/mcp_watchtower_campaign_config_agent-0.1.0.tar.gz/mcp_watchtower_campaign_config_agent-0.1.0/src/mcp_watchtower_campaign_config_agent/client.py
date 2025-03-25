import aiohttp
from typing import Optional
from .config import ServerConfig, ApiResponse
from .utils import encrypt_with_public_key

class CampaignClient:
    def __init__(self, config: ServerConfig):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            
    def _get_headers(self) -> dict:
        api_key = encrypt_with_public_key(self.config.api_key, self.config.public_key)
        return {
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
        
    async def _handle_response(self, response: aiohttp.ClientResponse) -> ApiResponse:
        if response.status == 401:
            return ApiResponse(code=401, message="Unauthorized: Invalid API key", data=None, timestamp=0)
        elif response.status != 200:
            error_text = await response.text()
            return ApiResponse(
                code=response.status,
                message=error_text,
                data=None,
                timestamp=0
            )
        return ApiResponse(**await response.json())
    
    async def get_campaign_info(self, campaign_id: Optional[str] = None, campaign_name: Optional[str] = None) -> ApiResponse:
        params = {}
        if campaign_id:
            params['campaignId'] = campaign_id
        if campaign_name:
            params['campaignName'] = campaign_name
            
        async with self.session.get(
            f"{self.config.base_url}/campaign/info",
            params=params,
            headers=self._get_headers()
        ) as response:
            return await self._handle_response(response)
            
    async def bind_campaign_channel(self, channel_name: str, campaign_id: str, campaign_name: str) -> ApiResponse:
        data = {
            "channelName": channel_name,
            "campaignId": campaign_id,
            "campaignName": campaign_name
        }
        
        async with self.session.post(
            f"{self.config.base_url}/campaign/channel",
            json=data,
            headers=self._get_headers()
        ) as response:
            return await self._handle_response(response)
            
    async def list_c_type_campaigns(self) -> ApiResponse:
        async with self.session.get(
            f"{self.config.base_url}/campaign/c-type",
            headers=self._get_headers()
        ) as response:
            return await self._handle_response(response)