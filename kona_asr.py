import sys
import os
import argparse
try:
    import whisper
except ImportError:
    print("Error: Whisper is not installed. Run from whisper-env.")
    sys.exit(1)

from kona import ACTIONS, MODIFIERS, TARGETS

def get_lexicon_prompt():
    # Gather all Kona primitives to inject into Whisper's context
    actions = list(ACTIONS.keys())
    targets = list(TARGETS.keys())
    modifiers = list(MODIFIERS.keys())
    # Additional structural words
    structural = ["si", "te", "ali", "nomi", "fino", "ke", "kito", "pato", "oli", "uni", "notori", "no"]
    
    all_words = actions + targets + modifiers + structural
    return " ".join(all_words)

def transcribe_audio(audio_path, model_size="base"):
    if not os.path.exists(audio_path):
        print(f"File not found: {audio_path}")
        sys.exit(1)
        
    print(f"Loading Whisper '{model_size}' model...")
    model = whisper.load_model(model_size)
    
    prompt = get_lexicon_prompt()
    
    # Whisper's context window is 224 tokens. 
    # Our current lexicon fits easily. If it grows >200 words, Whisper will truncate the prompt.
    print(f"Transcribing '{audio_path}' with Kona zero-shot prompt tuning...")
    result = model.transcribe(audio_path, language="en", initial_prompt=prompt)
    
    text = result["text"].strip().lower()
    
    # Clean up standard punctuation injected by ASR
    for punc in [".", ",", "?", "!"]:
        text = text.replace(punc, "")
        
    return text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kona ASR (Speech-to-Text)")
    parser.add_argument("audio_file", help="Path to the audio file (.wav, .mp3, etc.)")
    parser.add_argument("--model", default="base", help="Whisper model size (base, small, medium)")
    
    args = parser.parse_args()
    
    transcript = transcribe_audio(args.audio_file, args.model)
    print("\n[Transcription]:")
    print(transcript)
