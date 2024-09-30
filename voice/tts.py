import asyncio
import edge_tts
import pygame
import io


class TTSEngine:
    def __init__(self):
        self.voice = "en-US-AriaNeural"
        self.rate = "+0%"
        self.volume = "+0%"
        pygame.mixer.init()

    async def speak(self, text):
        communicate = edge_tts.Communicate(text, self.voice)
        audio_stream = b""

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_stream += chunk["data"]
                if len(audio_stream) > 32000:  # Play audio in chunks
                    await self._play_audio(audio_stream)
                    audio_stream = b""

        if audio_stream:  # Play any remaining audio
            await self._play_audio(audio_stream)

    async def _play_audio(self, audio_data):
        sound = pygame.mixer.Sound(io.BytesIO(audio_data))
        sound.play()
        while pygame.mixer.get_busy():
            await asyncio.sleep(0.1)

    def sync_speak(self, text):
        asyncio.run(self.speak(text))


async def text_to_speech(text):
    # Your existing code here
    pass


if __name__ == "__main__":
    tts = TTSEngine()
    tts.sync_speak(
        "Hello, I am Jarvis, your Personal assistant. How can I help you today?"
    )
