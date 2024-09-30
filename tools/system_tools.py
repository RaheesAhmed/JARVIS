import os
import subprocess
import webbrowser
from tavily import TavilyClient
import shutil
import asyncio

# ... (keep all existing functions)


class SystemTools:
    def __init__(self):
        # Initialize any necessary attributes here
        pass

    async def async_task(self):
        # This is a placeholder async method
        await asyncio.sleep(0)
        return "SystemTools async task completed"


# ... (keep all existing functions)


def open_application(app_name: str) -> str:
    try:
        subprocess.Popen(app_name)
        return f"Opened {app_name}"
    except Exception as e:
        return f"Failed to open {app_name}: {str(e)}"


def close_application(app_name: str) -> str:
    try:
        os.system(f"taskkill /F /IM {app_name}.exe")
        return f"Closed {app_name}"
    except Exception as e:
        return f"Failed to close {app_name}: {str(e)}"


def open_file(file_path: str) -> str:
    try:
        os.startfile(file_path)
        return f"Opened file: {file_path}"
    except Exception as e:
        return f"Failed to open file {file_path}: {str(e)}"


def create_folder(folder_path: str) -> str:
    try:
        os.makedirs(folder_path, exist_ok=True)
        return f"Created folder: {folder_path}"
    except Exception as e:
        return f"Failed to create folder {folder_path}: {str(e)}"


def open_browser(url: str) -> str:
    try:
        webbrowser.open(url)
        return f"Opened browser with URL: {url}"
    except Exception as e:
        return f"Failed to open browser with URL {url}: {str(e)}"


def search_on_browser(query: str) -> str:
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    return open_browser(search_url)


def search_on_internet(query: str) -> str:
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    results = client.search(query)
    return results


def open_vscode(path: str = None) -> str:
    try:
        if path:
            subprocess.Popen(["code", path])
            return f"Opened VS Code with path: {path}"
        else:
            subprocess.Popen(["code"])
            return "Opened VS Code"
    except Exception as e:
        return f"Failed to open VS Code: {str(e)}"


def create_file(file_path: str, content: str = "") -> str:
    try:
        with open(file_path, "w") as f:
            f.write(content)
        return f"Created file: {file_path}"
    except Exception as e:
        return f"Failed to create file {file_path}: {str(e)}"


def run_python_script(script_path: str) -> str:
    try:
        result = subprocess.run(["python", script_path], capture_output=True, text=True)
        return f"Script output:\n{result.stdout}\nErrors (if any):\n{result.stderr}"
    except Exception as e:
        return f"Failed to run script {script_path}: {str(e)}"


def list_directory_contents(path: str = ".") -> str:
    try:
        contents = os.listdir(path)
        return f"Contents of {path}:\n" + "\n".join(contents)
    except Exception as e:
        return f"Failed to list contents of {path}: {str(e)}"


def move_file(source: str, destination: str) -> str:
    try:
        shutil.move(source, destination)
        return f"Moved {source} to {destination}"
    except Exception as e:
        return f"Failed to move {source} to {destination}: {str(e)}"


def copy_file(source: str, destination: str) -> str:
    try:
        shutil.copy2(source, destination)
        return f"Copied {source} to {destination}"
    except Exception as e:
        return f"Failed to copy {source} to {destination}: {str(e)}"


def delete_file_or_folder(path: str) -> str:
    try:
        if os.path.isfile(path):
            os.remove(path)
            return f"Deleted file: {path}"
        elif os.path.isdir(path):
            shutil.rmtree(path)
            return f"Deleted folder: {path}"
        else:
            return f"Path not found: {path}"
    except Exception as e:
        return f"Failed to delete {path}: {str(e)}"


def run_command(command: str) -> str:
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return f"Command output:\n{result.stdout}\nErrors (if any):\n{result.stderr}"
    except Exception as e:
        return f"Failed to run command '{command}': {str(e)}"
