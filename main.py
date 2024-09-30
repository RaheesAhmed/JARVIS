import asyncio
from agents.basic_agent import BasicAgent
from tools.system_tools import SystemTools
from tools.custom_tools import CustomTools
from voice.tts import text_to_speech
from voice.stt import speech_to_text


async def main():
    agent = BasicAgent()
    system_tools = SystemTools()
    custom_tools = CustomTools()
    chat_history = []

    print(
        "Jarvis: Hello! I'm Jarvis, your personal assistant. How can I help you today?"
    )
    await text_to_speech(
        "Hello! I'm Jarvis, your personal assistant. How can I help you today?"
    )

    while True:
        print("You: ", end="", flush=True)
        user_input = await speech_to_text()
        print(user_input)

        if user_input.lower() in ["exit", "quit", "goodbye"]:
            final_message = "Goodbye! Have a great day!"
            print(f"Jarvis: {final_message}")
            await text_to_speech(final_message)
            break

        # Asynchronous processing of tasks
        tasks = [
            agent.process_input(user_input, chat_history),
            system_tools.async_task(),
            custom_tools.async_task(),
        ]
        results = await asyncio.gather(*tasks)

        response = results[0]  # The response from process_input
        print(f"Jarvis: {response}")
        await text_to_speech(response)

        # Update chat history
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": response})

        # Limit chat history to last 10 messages to prevent token limit issues
        chat_history = chat_history[-10:]


if __name__ == "__main__":
    asyncio.run(main())
