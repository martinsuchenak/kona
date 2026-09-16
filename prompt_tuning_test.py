import os
import whisper

commands = [
    "dekwe poya security te",
    "vetori kodo notori migrations te",
    "fasa mesa"
]

for i, cmd in enumerate(commands):
    os.system(f"say -o cmd_{i}.wav --data-format=LEI16@16000 '{cmd}'")

model = whisper.load_model("base")

kona_lexicon = "dekwe poya security te vetori kodo notori migrations fasa mesa yuki maki tori koso"

print("\n[Baseline] vs [Prompt-Tuned Whisper]")
for i, cmd in enumerate(commands):
    print(f"\nGround Truth : {cmd}")
    
    res_base = model.transcribe(f"cmd_{i}.wav", language="en")
    print(f"Base Output  : {res_base['text'].strip().lower().replace('.', '').replace(',', '')}")
    
    res_tuned = model.transcribe(f"cmd_{i}.wav", language="en", initial_prompt=kona_lexicon)
    print(f"Tuned Output : {res_tuned['text'].strip().lower().replace('.', '').replace(',', '')}")
    
    os.remove(f"cmd_{i}.wav")

