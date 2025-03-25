from pydantic import BaseModel, Field
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class ServerConfig(BaseModel):
    host: str = Field(default=os.getenv("MCP_HOST", "localhost"))
    port: int = Field(default=int(os.getenv("MCP_PORT", "8080")))
    api_key: str = Field(default=os.getenv("MCP_API_KEY", ""))
    public_key: str = Field(default=os.getenv("MCP_PUBLIC_KEY", "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmhvGBsvSCZoKvj+wSxynOo0azgI2lwt9bLEm2cH5Y0Z0YjOiK4Z4XnI2QskUhwm0RJ79hEbrGrmtaSiNwwq10GMIcpTVWP0NUmbeGQyu01XEDgSZ4dyjEmrDhC0FeMc7BgrhEiDqwS7uUOAczZWI5Q9i/ZUXhFy3V0A0//w+10TWKORV9U3WPICurKPhCfM5Wtu0RbbjyJX4UbkHS4Yw1JUFQcXfxdq30AR7NzATvwN61YS/5GCbQzlrYdvQSLtNwI5ErLfviETZYyfz4RghMTbIPQ5QhoAVwF8mxUPK6fYyEsIxzjlAnKDCPnCLlQPNBngETUtqcWFDdhY3L4zZTwIDAQAB"))
    api_path: str = Field(default="/api/v1/open/mcp/agent")

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}{self.api_path}"

class CampaignInfo(BaseModel):
    campaignId: int
    campaignName: str
    channelName: Optional[str]
    creator: str
    gmtCreated: str
    gmtModified: str
    modifier: str
    partnerName: str

class ApiResponse(BaseModel):
    code: int
    message: str
    data: Optional[dict | list | int]
    timestamp: int