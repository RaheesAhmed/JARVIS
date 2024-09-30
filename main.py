from voice.tts import TTSEngine
from voice.stt import STTEngine
from agents.basic_agent import chat_with_user, process_command, is_task_request


def main():
    tts = TTSEngine()
    stt = STTEngine()
    chat_history = []

    tts.sync_speak(
        "Hello, I am Jarvis, your personal assistant. How can I help you today?"
    )

    while True:
        user_input = stt.listen()
        if user_input:
            if user_input.lower() in ["exit", "quit", "goodbye"]:
                tts.sync_speak("Goodbye! Have a great day!")
                break

            if is_task_request(user_input):
                tts.sync_speak(
                    "Certainly! I'll use my tools to help you with that task."
                )
                response = process_command(user_input)
            else:
                response = chat_with_user(user_input, chat_history)

            tts.sync_speak(response)

            # Update chat history
            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": response})

            # Limit chat history to last 10 messages
            chat_history = chat_history[-10:]


if __name__ == "__main__":
    main()
