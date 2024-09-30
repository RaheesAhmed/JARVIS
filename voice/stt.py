import whisper
import numpy as np
import sounddevice as sd


class STTEngine:
    def __init__(self, model_name="base"):
        self.model = whisper.load_model(model_name)

    def listen(self, duration=5, sample_rate=16000):
        print("Listening...")
        audio_data = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="float32",
        )
        sd.wait()
        audio_data = audio_data.flatten()

        result = self.model.transcribe(audio_data)

        print(f"You said: {result['text']}")
        return result["text"]


async def speech_to_text():
    stt_engine = STTEngine()
    return stt_engine.listen()


if __name__ == "__main__":
    stt_engine = STTEngine()
    text = stt_engine.listen()
    print(f"Transcribed text: {text}")
