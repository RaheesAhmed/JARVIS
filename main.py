from voice.tts import TTSEngine
from voice.stt import STTEngine
from agents.basic_agent import process_command


def main():
    tts = TTSEngine()
    stt = STTEngine()

    tts.sync_speak(
        "Hello, I am Jarvis your Personal assistant. How can I help you today?"
    )

    while True:
        user_input = stt.listen()
        if user_input:
            if user_input.lower() in ["exit", "quit", "goodbye"]:
                tts.sync_speak("Goodbye!")
                break

            response = process_command(user_input)
            tts.sync_speak(response)


if __name__ == "__main__":
    main()
