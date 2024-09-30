import os
from tavily import TavilyClient
import asyncio


def search_on_internet(query: str) -> str:
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    results = client.search(query)
    return results


class CustomTools:
    def __init__(self):
        # Initialize any necessary attributes here
        pass

    async def async_task(self):
        # This is a placeholder async method
        await asyncio.sleep(0)
        return "CustomTools async task completed"
