import os
import subprocess
import webbrowser
from tavily import TavilyClient
import shutil


def search_on_internet(query: str) -> str:
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    results = client.search(query)
    return results
