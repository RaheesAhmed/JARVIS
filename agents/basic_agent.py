from langchain.agents import Tool, AgentExecutor
from langchain.agents import create_react_agent
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from typing import List
import os
import dotenv
from tools.system_tools import (
    open_application,
    close_application,
    open_file,
    create_folder,
    open_browser,
    search_on_browser,
    search_on_internet,
)

dotenv.load_dotenv()

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
    Tool(
        name="SearchOnInternet",
        func=search_on_internet,
        description="Useful for searching on the internet. Input should be the search query.",
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


async def process_command(command: str) -> str:
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=3,  # Limit the number of iterations
    )

    try:
        # Add a friendly acknowledgment
        print(f"Certainly! I'll help you with: {command}")

        result = agent_executor.invoke({"input": command})

        # Extract the final answer and the intermediate steps
        final_answer = result.get("output", "")
        intermediate_steps = result.get("intermediate_steps", [])

        # Process intermediate steps to create a friendly response
        friendly_response = "Here's what I did:\n"
        for step in intermediate_steps:
            action = step[0]
            friendly_response += f"- I'm going to {action.tool}: {action.tool_input}\n"
            friendly_response += f"  {step[1]}\n"

        # Combine the friendly response with the final answer
        complete_response = f"{friendly_response}\n{final_answer}"

        return complete_response
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return "I'm sorry, I encountered an error while processing your request. Could you please try rephrasing your command?"


async def chat_with_user(user_input: str, chat_history: List[dict]) -> str:
    chat_messages = [
        SystemMessage(
            content="You are Jarvis, a friendly and helpful AI assistant. Engage in casual conversation and provide information when asked. If the user requests a specific task, politely inform them you'll use your tools to help."
        ),
    ]

    # Add chat history
    for message in chat_history:
        if message["role"] == "user":
            chat_messages.append(HumanMessage(content=message["content"]))
        else:
            chat_messages.append(AIMessage(content=message["content"]))

    # Add the current user input
    chat_messages.append(HumanMessage(content=user_input))

    response = llm(chat_messages)
    return response.content


def is_task_request(user_input: str) -> bool:
    task_keywords = [
        "open",
        "close",
        "search",
        "find",
        "create",
        "run",
        "execute",
        "start",
        "stop",
    ]
    return any(keyword in user_input.lower() for keyword in task_keywords)


class BasicAgent:
    async def process_input(self, user_input: str, chat_history: List[dict]) -> str:
        if is_task_request(user_input):
            print("Jarvis: Certainly! I'll use my tools to help you with that task.")
            response = await process_command(user_input)
        else:
            response = await chat_with_user(user_input, chat_history)
        return response


if __name__ == "__main__":
    chat_history = []
    print(
        "Jarvis: Hello! I'm Jarvis, your personal assistant. How can I help you today?"
    )

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit", "goodbye"]:
            print("Jarvis: Goodbye! Have a great day!")
            break

        if is_task_request(user_input):
            print("Jarvis: Certainly! I'll use my tools to help you with that task.")
            response = process_command(user_input)
        else:
            response = chat_with_user(user_input, chat_history)

        print(f"Jarvis: {response}")

        # Update chat history
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": response})

        # Limit chat history to last 10 messages to prevent token limit issues
        chat_history = chat_history[-10:]
