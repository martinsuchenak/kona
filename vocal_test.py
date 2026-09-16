#!/usr/bin/env python3
"""
Kona Vocal Test Suite
Generates high-clarity speech synthesis samples across multiple voice engines.
"""

import subprocess
import os
import sys

AUDIO_DIR = "/Users/martin/Documents/Samples/kona/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

TEST_CASES = [
    {
        "id": "test1_code_guard",
        "title": "Code Refactor with Guard Invariant",
        "kona": "de-kwe poya security pa ve-tori kodo no-tori migrations pa fasa mesa",
        "meaning": "Deep search repo for security -> Propose code refactor (DO NOT touch migrations) -> Summarize as table"
    },
    {
        "id": "test2_web_json",
        "title": "Web Research to JSON",
        "kona": "kwe veba AWS Azure pa fasa jano",
        "meaning": "Query web for AWS Azure -> Summarize into JSON"
    },
    {
        "id": "test3_test_deploy",
        "title": "Test Pipeline & Execution",
        "kona": "teli poya pa yuki tafu",
        "meaning": "Verify repository -> Execute workflow"
    },
    {
        "id": "test4_brief_summary",
        "title": "Concise Bullet-Point Summary",
        "kona": "su-fasa fili readme pa poti",
        "meaning": "Briefly summarize file readme -> Output as bullet list"
    }
]

VOICES = [
    {"name": "Samantha", "lang": "en_US", "rate": 180, "note": "Clear standard English profile"},
    {"name": "Alice",    "lang": "it_IT", "rate": 175, "note": "Pure 5 cardinal vowels (Italian acoustic engine)"},
    {"name": "Monica",   "lang": "es_ES", "rate": 175, "note": "Crisp plosives & pure vowels (Spanish acoustic engine)"},
]

def generate_audio_samples():
    print("=" * 70)
    print("Generating Kona Vocal Samples (AI-Optimized Phonology)")
    print("=" * 70)

    generated_files = []

    for case in TEST_CASES:
        print(f"\n🎧 [Phrase]: {case['title']}")
        print(f"   Kona:    \"{case['kona']}\"")
        print(f"   Meaning: {case['meaning']}")

        for voice in VOICES:
            aiff_path = os.path.join(AUDIO_DIR, f"{case['id']}_{voice['name'].lower()}.aiff")
            wav_path = os.path.join(AUDIO_DIR, f"{case['id']}_{voice['name'].lower()}.wav")

            cmd_say = [
                "say",
                "-v", voice["name"],
                "-r", str(voice["rate"]),
                "-o", aiff_path,
                case["kona"]
            ]
            
            # Synthesize
            res = subprocess.run(cmd_say, capture_output=True, text=True)
            if res.returncode != 0:
                print(f"   ❌ Failed with voice {voice['name']}: {res.stderr.strip()}")
                continue

            # Convert to standard WAV
            cmd_conv = ["afconvert", "-f", "WAVE", "-d", "LEI16", aiff_path, wav_path]
            subprocess.run(cmd_conv, check=True)
            
            # Clean up temp aiff
            if os.path.exists(aiff_path):
                os.remove(aiff_path)

            file_size_kb = os.path.getsize(wav_path) / 1024
            print(f"   ✓ Voice [{voice['name']} ({voice['lang']})]: {os.path.basename(wav_path)} ({file_size_kb:.1f} KB)")
            generated_files.append((case, voice, wav_path))

    return generated_files

def play_live(sample_idx=0, voice_name="Alice"):
    case = TEST_CASES[sample_idx]
    print(f"\n🔊 Playing live over speakers:")
    print(f"   Voice: {voice_name}")
    print(f"   Kona:  \"{case['kona']}\"")
    subprocess.run(["say", "-v", voice_name, "-r", "175", case["kona"]])

if __name__ == "__main__":
    files = generate_audio_samples()
    print("\n" + "=" * 70)
    print(f"All {len(files)} audio test samples successfully generated in:")
    print(f"{AUDIO_DIR}")
    print("=" * 70)

    # Play Test 1 live through the user's speakers with Alice (pure 5 cardinal vowels)
    if "--play" in sys.argv:
        play_live(0, "Alice")
