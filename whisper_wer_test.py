#!/usr/bin/env python3
"""Acoustic A/B: does Kona actually transcribe better than terse English?

This is the experiment the project's central claim rests on, and it had never
been run. The previous version of this file synthesised three Kona utterances,
printed what Whisper heard, and stopped -- no English control, no noise, no
word-error-rate computation. You cannot conclude anything from that.

What this measures, over matched semantic pairs:

  1. terse English            -- the baseline Kona has to beat
  2. Kona, no lexicon prompt  -- off-the-shelf ASR, no knowledge of Kona
  3. Kona, lexicon prompt     -- ASR conditioned on the vocabulary

Condition 3 is the fair test of the phonology. Condition 2 matters too, because
it is what happens when Kona meets a recogniser that has never heard of it.

Run:
    ./whisper-env/bin/python whisper_wer_test.py
    ./whisper-env/bin/python whisper_wer_test.py --snr 10   # additive noise
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import wave

import numpy as np
import whisper

from kona_asr import get_lexicon_prompt

# Matched pairs: same instruction, expressed each way.
PAIRS = [
    ("dekwe poya sekuriti te fasa mesa",
     "deep search the security repo then report a table"),
    ("vetori kodo notori migrasoni te fasa difa",
     "dry run refactor the code never touch migrations then show a diff"),
    ("kwe veba te fasa jano",
     "search the web then output json"),
    ("si teli bono te yuki tafu ali fasa baki",
     "if the test passes run the task else report a bug"),
    ("oki pakokaba te yuki tesi te fasa poti",
     "start the sandbox then run the tests then report a list"),
    ("leke vasi te teli kodo",
     "fetch git then check the code"),
    ("si seli dura te nuki seli te reteli toko",
     "if the lock is held release the lock then retry the loop"),
    ("visi visikoso mapo visipeji te do meso",
     "check the camera and the display then send a message"),
    ("sufasa tokopasa baki",
     "brief summary of the error log"),
    ("tori seku te do memo pasa duo toko",
     "update the secret then cache it for two intervals"),
]

VOICE = "Damayanti"
RATE = "170"


def synthesize(text, path):
    """Render text to 16 kHz mono PCM with the macOS speech engine."""
    subprocess.run(
        ["say", "-v", VOICE, "-r", RATE, "-o", path,
         "--data-format=LEI16@16000", text],
        check=True,
    )


def add_noise(path, snr_db):
    """Mix in white noise at a given signal-to-noise ratio."""
    with wave.open(path, "rb") as w:
        params = w.getparams()
        frames = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)

    signal = frames.astype(np.float64)
    sig_power = np.mean(signal ** 2)
    if sig_power == 0:
        return
    noise_power = sig_power / (10 ** (snr_db / 10))
    noise = np.random.normal(0, np.sqrt(noise_power), signal.shape)
    mixed = np.clip(signal + noise, -32768, 32767).astype(np.int16)

    with wave.open(path, "wb") as w:
        w.setparams(params)
        w.writeframes(mixed.tobytes())


def normalize(text):
    keep = "abcdefghijklmnopqrstuvwxyz "
    text = "".join(c for c in text.lower() if c in keep)
    return text.split()


def wer(reference, hypothesis):
    """Standard Levenshtein word error rate."""
    r, h = normalize(reference), normalize(hypothesis)
    if not r:
        return 0.0 if not h else 1.0
    d = np.zeros((len(r) + 1, len(h) + 1), dtype=np.int32)
    d[:, 0] = np.arange(len(r) + 1)
    d[0, :] = np.arange(len(h) + 1)
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            cost = 0 if r[i - 1] == h[j - 1] else 1
            d[i, j] = min(d[i - 1, j] + 1, d[i, j - 1] + 1, d[i - 1, j - 1] + cost)
    return d[len(r), len(h)] / len(r)


def run(model_size="base", snr_db=None, verbose=False):
    print("=" * 78)
    print("KONA ACOUSTIC A/B  --  word error rate vs terse English")
    print(f"voice={VOICE} rate={RATE} model={model_size} "
          f"noise={'none' if snr_db is None else f'{snr_db} dB SNR'}")
    print("=" * 78)

    if not shutil.which("say"):
        sys.exit("This benchmark needs the macOS 'say' speech engine.")

    print(f"Loading Whisper '{model_size}'...")
    model = whisper.load_model(model_size)
    prompt = get_lexicon_prompt()

    conditions = {
        "English (terse)": [],
        "Kona (no prompt)": [],
        "Kona (lexicon prompt)": [],
    }

    tmp = tempfile.mkdtemp(prefix="kona-wer-")
    try:
        for i, (kona, english) in enumerate(PAIRS):
            for label, text, init in (
                ("English (terse)", english, None),
                ("Kona (no prompt)", kona, None),
                ("Kona (lexicon prompt)", kona, prompt),
            ):
                path = os.path.join(tmp, f"{label[:4]}_{i}.wav")
                synthesize(text, path)
                if snr_db is not None:
                    add_noise(path, snr_db)
                out = model.transcribe(path, language="en", initial_prompt=init,
                                       fp16=False)
                heard = out["text"].strip()
                score = wer(text, heard)
                conditions[label].append(score)
                if verbose:
                    print(f"  [{label}] want: {text}")
                    print(f"  [{label}] got : {heard.lower()}  WER={score:.2f}")
            print(f"  pair {i + 1}/{len(PAIRS)} done")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("\n" + "=" * 78)
    print(f"{'Condition':<26} {'mean WER':>9} {'median':>8} {'perfect':>9}")
    print("-" * 78)
    for label, scores in conditions.items():
        arr = np.array(scores)
        print(f"{label:<26} {arr.mean():>9.3f} {np.median(arr):>8.3f} "
              f"{int((arr == 0).sum()):>6}/{len(arr)}")
    print("=" * 78)

    eng = np.mean(conditions["English (terse)"])
    kona = np.mean(conditions["Kona (lexicon prompt)"])
    if eng == 0 and kona == 0:
        verdict = "Both perfect; this setup does not discriminate. Add noise (--snr)."
    elif kona < eng:
        verdict = (f"Kona transcribes better ({kona:.3f} vs {eng:.3f}). "
                   f"This is the acoustic case for the constructed vocabulary.")
    else:
        verdict = (f"Kona transcribes WORSE ({kona:.3f} vs {eng:.3f}). "
                   f"The acoustic argument does not hold against this recogniser.")
    print(f"\nVerdict: {verdict}")
    return conditions


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", default="base")
    ap.add_argument("--snr", type=float, default=None,
                    help="add white noise at this SNR in dB (e.g. 10)")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()
    run(args.model, args.snr, args.verbose)
