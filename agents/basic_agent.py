from langchain.agents import Tool, AgentExecutor
from langchain.agents import create_react_agent
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from typing import List
import os
import dotenv
import subprocess
import webbrowser

dotenv.load_dotenv()


# Define custom tools
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


# Create LangChain tools
tools = [
    Tool(
        name="OpenApplication",
        func=open_application,
        description="Useful for opening applications on the computer. Input should be the application name.",
    ),
    Tool(
        name="CloseApplication",
        func=close_application,
        description="Useful for closing applications on the computer. Input should be the application name.",
    ),
    Tool(
        name="OpenFile",
        func=open_file,
        description="Useful for opening files on the computer. Input should be the file path.",
    ),
    Tool(
        name="CreateFolder",
        func=create_folder,
        description="Useful for creating new folders on the computer. Input should be the folder path.",
    ),
    Tool(
        name="OpenBrowser",
        func=open_browser,
        description="Useful for opening a web browser with a specific URL. Input should be the URL.",
    ),
    Tool(
        name="SearchOnBrowser",
        func=search_on_browser,
        description="Useful for searching on the web browser. Input should be the search query.",
    ),
]

# Set up the prompt template
template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: To answer this question, I need to use one of the available tools.
{agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create the agent
agent = create_react_agent(llm, tools, prompt)

# Set up the agent executor
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True
)


def process_command(command: str) -> str:
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
    )

    try:
        result = agent_executor.invoke({"input": command})
        return result["output"]
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return "I'm sorry, I encountered an error while processing your request. Could you please try rephrasing your command?"


if __name__ == "__main__":
    result = process_command("Open the Chrome browser and search for 'OpenAI'")
    print(result)
