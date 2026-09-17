import sys
import os
import argparse
try:
    import whisper
except ImportError:
    print("Error: Whisper is not installed. Run from whisper-env.")
    sys.exit(1)

from kona import ACTIONS, MODIFIERS, TARGETS, PARTICLES, QUALITIES, FORMATS

# Whisper's conditioning prompt is capped at 224 tokens.
WHISPER_PROMPT_TOKEN_BUDGET = 224


def get_lexicon_prompt(budget=WHISPER_PROMPT_TOKEN_BUDGET):
    """Build Whisper's conditioning prompt from the live lexicon.

    Every word class comes from kona.py. The structural words used to be a
    hand-written list here, which had already drifted: it named `kito`, `pato`,
    `oli` and `uni`, none of which the compiler knew at the time.

    The lexicon now exceeds Whisper's prompt budget, so the prompt is
    prioritised rather than silently truncated mid-list by the decoder: the
    closed classes that carry sentence structure come first, then actions, then
    targets, which are the most recoverable from context.
    """
    ordered = (
        list(PARTICLES)          # structure: si, te, ali, ke, ina, uta, ...
        + list(MODIFIERS)        # bound prefixes
        + list(FORMATS)
        + list(QUALITIES)
        + list(ACTIONS)
        + list(TARGETS)
    )

    # Whisper counts tokens, not words; Kona roots are out-of-vocabulary and
    # average well above one token each. Budget conservatively at ~2 tokens per
    # word so the tail is dropped here, by priority, instead of arbitrarily.
    max_words = max(1, budget // 2)
    selected = ordered[:max_words]
    dropped = len(ordered) - len(selected)
    if dropped:
        print(f"[lexicon prompt] {len(selected)} of {len(ordered)} words sent; "
              f"{dropped} lowest-priority targets omitted to stay within "
              f"Whisper's {budget}-token prompt limit.")
    return " ".join(selected)

def transcribe_audio(audio_path, model_size="base"):
    if not os.path.exists(audio_path):
        print(f"File not found: {audio_path}")
        sys.exit(1)
        
    print(f"Loading Whisper '{model_size}' model...")
    model = whisper.load_model(model_size)
    
    prompt = get_lexicon_prompt()

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
