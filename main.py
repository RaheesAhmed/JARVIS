import asyncio
import os
from agents.basic_agent import BasicAgent
from tools.system_tools import SystemTools
from tools.custom_tools import CustomTools
from voice.tts import text_to_speech
from voice.stt import speech_to_text


class JarvisAPI:
    def __init__(self):
        self.agent = BasicAgent()
        self.system_tools = SystemTools()
        self.custom_tools = CustomTools()
        self.chat_history = []

    async def process_input(self, user_input):
        if user_input.lower() in ["exit", "quit", "goodbye"]:
            response = "Goodbye! Have a great day!"
        else:
            tasks = [
                self.agent.process_input(user_input, self.chat_history),
                self.system_tools.async_task(),
                self.custom_tools.async_task(),
            ]
            results = await asyncio.gather(*tasks)
            response = results[0]  # The response from process_input

        # Update chat history
        self.chat_history.append({"role": "user", "content": user_input})
        self.chat_history.append({"role": "assistant", "content": response})
        self.chat_history = self.chat_history[-10:]  # Limit to last 10 messages

        await text_to_speech(response)
        return response

    async def listen(self):
        user_input = await speech_to_text()
        return user_input


async def main():
    api = JarvisAPI()

    print(
        "Jarvis: Hello! I'm Jarvis, your personal assistant. How can I help you today?"
    )
    await text_to_speech(
        "Hello! I'm Jarvis, your personal assistant. How can I help you today?"
    )

    while True:
        user_input = await api.listen()
        print(f"You: {user_input}")

        response = await api.process_input(user_input)
        print(f"Jarvis: {response}")

        if user_input.lower() in ["exit", "quit", "goodbye"]:
            break


if __name__ == "__main__":
    asyncio.run(main())
