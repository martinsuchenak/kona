import os
import time
import whisper

print("[1] Generating Synthetic Speech (macOS 'say')...")
commands = [
    "dekwe poya security te",
    "vetori kodo notori migrations te",
    "fasa mesa"
]

# Generate audio files silently
for i, cmd in enumerate(commands):
    # Use macOS say to generate a WAV file (16kHz 16-bit PCM for whisper)
    os.system(f"say -o cmd_{i}.wav --data-format=LEI16@16000 '{cmd}'")

print("[2] Loading Whisper Base Model (this may take a moment)...")
model = whisper.load_model("base")

print("\n==========================================================")
print(" KONA ACOUSTIC TRANSCRIPTION BENCHMARK (Whisper ASR)")
print("==========================================================")

for i, cmd in enumerate(commands):
    print(f"\n[Ground Truth] : {cmd}")
    result = model.transcribe(f"cmd_{i}.wav", language="en") 
    transcription = result["text"].strip().lower()
    
    # Simple formatting to remove punctuation Whisper might inject
    transcription = transcription.replace(".", "").replace(",", "")
    print(f"[Whisper Output]: {transcription}")
    
    # Clean up audio file
    os.remove(f"cmd_{i}.wav")

print("\n==========================================================")
