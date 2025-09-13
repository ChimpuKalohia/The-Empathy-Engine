# The-Empathy-Engine

> **Emotion-aware Text→Speech** — dynamically modulates synthesized speech so the voice sounds empathetic, expressive, and human-like.

---

## Repository

This README is tailored for the code in this repository: **The-Empathy-Engine**.

**Repository URL:** [https://github.com/ChimpuKalohia/The-Empathy-Engine](https://github.com/ChimpuKalohia/The-Empathy-Engine)

---

## Quick summary

The Empathy Engine analyzes input text to detect emotion and then alters vocal parameters (rate, pitch, volume, etc.) before synthesizing speech. The final output is a playable audio file (e.g. `.wav`, `.mp3`).

This project focuses on bridging the gap between raw TTS output and emotionally-resonant spoken responses for use in AI assistants, voice agents, and customer-facing systems.

---

## What’s included (detected in this repo)

* `emotion_classifier.py` — emotion classification utilities
* `sentiment_analysis.py` — sentiment helpers / alternate analyzer
* `tts.py` — text-to-speech glue and output generation
* `test.mp3` — example output audio

> If any filenames differ in your local copy, tell me and I’ll adapt the README or make a PR.

---

## Features (core requirements)

* **Text input** via CLI or (optionally) an HTTP API.
* **Emotion detection** with at least three categories (Positive / Neutral / Negative).
* **Vocal parameter modulation**: programmatic control over *at least two* voice parameters (e.g., rate & pitch).
* **Emotion→voice mapping**: deterministic logic maps detected emotion (and intensity) to voice parameter values.
* **Audio output**: produces a `.wav` or `.mp3` file that can be played back.

---

## Recommended stack

* **Language:** Python 3.8+
* **Emotion / sentiment:** Hugging Face Transformers (for a robust model), fallback to VADER/TextBlob for offline quick checks
* **TTS engines:**

  * Offline/local: `pyttsx3` (fast prototyping)
  * API/High-quality: ElevenLabs, Google Cloud TTS, or gTTS (note: gTTS has limited prosody control)
* **Post-processing (pitch/rate manipulation):** `librosa`, `pydub`, or `rubberband` (for audio-level pitch/time manipulation)
* **API framework (optional):** FastAPI or Flask

---

## Setup (suggested)

```bash
# clone
git clone https://github.com/ChimpuKalohia/The-Empathy-Engine.git
cd The-Empathy-Engine

# create venv
python3 -m venv venv
source venv/bin/activate

# install dependencies (example list)
pip install -r requirements.txt
# if you don't have requirements.txt, try:
# pip install fastapi uvicorn transformers torch pyttsx3 pydub librosa soundfile
```

**Environment variables** (only if you opt for remote APIs):

---

## Running (examples)

> The repository contains `tts.py` and helper modules. The commands below are generic examples — adapt them to the actual CLI in `tts.py`.

**CLI (example)**

```bash
# simple one-off from terminal
python tts.py --text "I got good news!" --out out.wav --engine pyttsx3
```

**API (example)**
Run a FastAPI/Flask wrapper (if you add it):

```bash
uvicorn api:app --reload --port 8000
```

Then:

```bash
curl -X POST "http://localhost:8000/synthesize" \
  -H "Content-Type: application/json" \
  -d '{"text":"Thanks for your patience","format":"wav"}' --output out.wav
```

---

## Emotion → Voice mapping (design notes & example)

The mapping layer sits between the classifier and the TTS engine. We recommend mapping by *emotion label* and *intensity* (probability/confidence); intensity scales how strong the parameter changes are.

**Example mapping (relative values)**

* Base voice: `rate = 1.0`, `pitch = 0 (semitones)`, `volume = 0.0` (relative adjustments)

| Emotion                 | Rate multiplier | Pitch (semitones) | Volume (relative) |
| ----------------------- | --------------: | ----------------: | ----------------: |
| Enthusiastic / Positive |            1.15 |                +3 |             +0.08 |
| Neutral                 |            1.00 |                 0 |                 0 |
| Frustrated / Negative   |            1.20 |                +2 |             +0.12 |

**Intensity scaling**
If the classifier returns an intensity between 0 and 1, multiply the delta by that intensity. Example (pseudo):

```python
def map_emotion_to_params(label, intensity=1.0, base_rate=1.0):
    if label == 'positive':
        return {
            'rate': base_rate * (1.0 + 0.15 * intensity),
            'pitch_semitones': 3 * intensity,
            'volume_delta': 0.08 * intensity,
        }
    if label == 'neutral':
        return {'rate': base_rate, 'pitch_semitones': 0, 'volume_delta': 0.0}
    if label == 'negative':
        return {
            'rate': base_rate * (1.0 + 0.20 * intensity),
            'pitch_semitones': 2 * intensity,
            'volume_delta': 0.12 * intensity,
        }
```

**Implementing pitch changes**

* If the TTS engine supports SSML and pitch/rate attributes (e.g., Google Cloud TTS), prefer that approach.
* Otherwise, synthesize neutral audio and post-process using `librosa.effects.pitch_shift` and `librosa.core.resample` or `pydub`/`rubberband` for time stretching.

---

## Post-processing pipeline (recommended)

1. Detect emotion & intensity from text.
2. Map to voice parameters.
3. Call TTS engine to produce a baseline audio file.
4. Optionally apply audio transformations (pitch shift, time stretching) to match desired parameters.
5. Export to `.wav` or `.mp3`.

---

## Bonus / Stretch ideas

* Granular emotion labels (e.g., surprise, inquisitive, concerned).
* Intensity-aware modulation — map classifier confidence to modulation magnitude.
* Web UI with live text input + embedded audio player (FastAPI + simple HTML/JS).
* Full SSML generation for engines that support it so you can control pauses, emphasis and phonetic tweaks.

---

## Notes on design choices

* Use a *classifier + mapper + TTS* split so emotion logic is engine-agnostic.
* Keep mapping deterministic and testable (unit tests for label→params mapping).
* Prefer high-quality API voices (ElevenLabs / Google) for user-facing demos; use local engines for offline testing/prototyping.

---

## Troubleshooting & limitations

* Not all TTS engines support pitch changes; you may need offline audio processing libraries.
* Audio transformations can introduce artifacts — high-quality libraries (e.g., rubberband) reduce artifacts.
* If real-time response is required, avoid heavy post-processing or use faster streaming TTS APIs.

---

## How I can help next

* I can update the repo's existing `README.md` directly or create a PR with this README.
* I can scan your code and update examples to match actual function and CLI names.
* I can add a simple FastAPI wrapper + HTML demo page and a Dockerfile.

---

## License

MIT — feel free to reuse and adapt.

---

## Contact

Repo owner: `ChimpuKalohia` (GitHub)
