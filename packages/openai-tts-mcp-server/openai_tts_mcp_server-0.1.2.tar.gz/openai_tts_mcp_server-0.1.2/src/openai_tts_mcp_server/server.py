import io
import os
import threading
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play


client = OpenAI()

# Path to the local notification sound file
PACKAGE_DIR = Path(__file__).parent
NOTIFICATION_SOUND = str(PACKAGE_DIR / "ding.aiff")

def generate_speech(
    text: str,
    model: str = "gpt-4o-mini-tts",
    voice: str = "coral",
    speed: float = 4.0,
    instructions: str = None
) -> bytes:
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        speed=speed,
        instructions=instructions,
    )
    return response.content

def play_audio(audio_bytes: bytes, notification_sound_path: str = NOTIFICATION_SOUND) -> None:
    # Play notification sound first if available
    if os.path.exists(notification_sound_path):
        try:
            notification_sound = AudioSegment.from_file(notification_sound_path)
            play(notification_sound)
        except Exception as e:
            print(f"Warning: Could not play notification sound: {e}")
    
    # Then play the generated speech
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")
    play(audio)

mcp = FastMCP("My App")

# Create a semaphore to ensure only one audio playback happens at a time
audio_semaphore = threading.Semaphore(1)

INSTRUCTIONS = """Voice Affect: Calm: instilling trust without much intensity, in control, relaxed.

Tone: Sincere, empathetic, light-hearted, relaxed.

Pacing: Quick delivery when desribing things but un-intense. Sometimes deliberate pauses.

Emotion: Friendly and warm

Personality: Relatable: Very friendly and warm."""

@mcp.tool(description="Use this to send a short audio message to the user concisely (one 10-15 word sentence) summarizing what you've done and why. Use this tool every time you generated a code snippet or ran a command as well as when you give control back to the user.")
def summarize(text: str) -> dict[str, str]:
    try:
        # Make the TTS API request synchronously
        audio_bytes = generate_speech(
            text=text,
            model="gpt-4o-mini-tts",
            voice="coral",
            speed=0.25,
            instructions=INSTRUCTIONS
        )
        
        # Schedule audio playback in background
        def play_audio_in_background():
            try:
                # Acquire the semaphore - blocks if another thread has it
                audio_semaphore.acquire()
                play_audio(audio_bytes, NOTIFICATION_SOUND)
            except Exception as e:
                print(f"Error in background audio playback: {e}")
            finally:
                # Always release the semaphore
                audio_semaphore.release()
        
        # Start only the audio playback in a background thread
        threading.Thread(target=play_audio_in_background, daemon=True).start()
        
        return {"status": "success", "message": "Audio generated and playback scheduled! Please move on to the next task."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def main() -> None:
    print("Starting the MCP server!")
    mcp.run(transport="stdio")
    
if __name__ == "__main__":
    main()