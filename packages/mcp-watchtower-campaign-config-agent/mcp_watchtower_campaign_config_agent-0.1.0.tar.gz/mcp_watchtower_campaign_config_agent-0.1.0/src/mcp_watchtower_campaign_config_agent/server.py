import asyncio
import json  # Add this import

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
from .config import ServerConfig
from .client import CampaignClient

server = Server("mcp-watchtower-campaign-config-agent")
config = ServerConfig()
client: CampaignClient = None

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get-campaign-info",
            description="Get campaign information by ID or name",
            inputSchema={
                "type": "object",
                "properties": {
                    "campaignId": {"type": "string"},
                    "campaignName": {"type": "string"},
                },
                "anyOf": [
                    {"required": ["campaignId"]},
                    {"required": ["campaignName"]}
                ]
            },
        ),
        types.Tool(
            name="bind-campaign-channel",
            description="Bind a campaign to a channel",
            inputSchema={
                "type": "object",
                "properties": {
                    "channelName": {"type": "string"},
                    "campaignId": {"type": "string"},
                    "campaignName": {"type": "string"},
                },
                "required": ["channelName", "campaignId", "campaignName"],
            },
        ),
        types.Tool(
            name="list-c-type-campaigns",
            description="List all C-type campaigns",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        match name:
            case "get-campaign-info":
                if not arguments:
                    raise ValueError("Please provide either campaignId or campaignName")
                    
                response = await client.get_campaign_info(
                    arguments.get("campaignId"),
                    arguments.get("campaignName")
                )
                
                if response.code != 200:
                    return [types.TextContent(
                        type="text",
                        text=f"Error: {response.message}"
                    )]
                    
                # For get-campaign-info response
                return [types.TextContent(
                    type="text",
                    text=f"Campaign information:\n{json.dumps(response.data, indent=2, ensure_ascii=False)}"
                )]
                
            case "bind-campaign-channel":
                if not arguments or not all(k in arguments for k in ["channelName", "campaignId", "campaignName"]):
                    raise ValueError("Please provide channelName, campaignId, and campaignName")
                    
                response = await client.bind_campaign_channel(
                    arguments["channelName"],
                    arguments["campaignId"],
                    arguments["campaignName"]
                )
                
                if response.code != 200:
                    return [types.TextContent(
                        type="text",
                        text=f"Error: {response.message}"
                    )]
                    
                return [types.TextContent(
                    type="text",
                    text="Successfully bound campaign to channel!"
                )]
                    
            case "list-c-type-campaigns":
                response = await client.list_c_type_campaigns()
                
                if response.code != 200:
                    return [types.TextContent(
                        type="text",
                        text=f"Error: {response.message}"
                    )]
                    
                # For list-c-type-campaigns response
                campaigns = response.data
                return [types.TextContent(
                    type="text",
                    text="C-type campaigns:\n" + "\n".join(
                        f"Campaign Details:\n"
                        f"  Name: {c['campaignName']}\n"
                        f"  ID: {c['campaignId']}\n"
                        f"  Channel: {c['channelName']}\n"
                        f"  Partner: {c['partnerName']}\n"
                        f"  Creator: {c['creator']}\n"
                        f"  Created: {c['gmtCreated']}\n"
                        f"  Modified: {c['gmtModified']}\n"
                        f"  Last Modified By: {c['modifier']}\n"
                        f"-------------------"
                        for c in campaigns
                    )
                )]
                
            case _:
                raise ValueError(f"Unknown tool: {name}")
                
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"Error: {str(e)}\nPlease check your input parameters and try again."
        )]

async def main():
    global client
    client = CampaignClient(config)
    
    async with client:
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="mcp-watchtower-campaign-config-agent",
                    server_version="0.1.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )