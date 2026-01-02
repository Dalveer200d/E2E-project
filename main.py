import whisper
from pathlib import Path

AUDIO_PATH = "sample_voice_telugu.wav"   
WHISPER_MODEL = "turbo"           
# use base - model for faster but less accurate results
# use small - model for a balance between speed and accuracy
# use medium - model for better accuracy but slower speed
# use these models if running on local CPU as they are less resource draining
# two other models are large/large-v2 and turbo
# but these two are hevery resource draining and may crash pc.

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

TELUGU_FILE = OUTPUT_DIR / "telugu.txt"
ENGLISH_FILE = OUTPUT_DIR / "english.txt"

model = whisper.load_model(WHISPER_MODEL, device="gpu")
print(f"Using device: {model.device}")

#Telugu audio → Telugu text
telugu_result = model.transcribe(
    AUDIO_PATH,
    language="te",
    task="transcribe"
)

telugu_text = telugu_result["text"].strip()
TELUGU_FILE.write_text(telugu_text, encoding="utf-8")

# English audio → English text
# Telugu audio → English text
english_result = model.transcribe(
    AUDIO_PATH,
    task="translate",   # always outputs English
    language="en"
)

english_text = english_result["text"].strip()
ENGLISH_FILE.write_text(english_text, encoding="utf-8")

print("Completed successfully.")
print("Saved files:")
print(TELUGU_FILE)
print(ENGLISH_FILE)
