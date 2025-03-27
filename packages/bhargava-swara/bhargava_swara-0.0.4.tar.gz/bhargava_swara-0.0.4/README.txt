# Bhargava Swara
A Python library for analyzing Indian classical music, including raga, tala, tempo, tradition, ornaments, and full analysis.


## Prerequisites
- **Gemini API Key:** This library uses Google's Gemini API for music analysis. You’ll need to:
  1. Sign up for a Google Cloud account.
  2. Enable the Generative AI API in the Google Cloud Console.
  3. Create an API key in the "Credentials" section.
  See [Google’s Generative AI Docs](https://cloud.google.com/generative-ai/docs) for details.


## Installation
```bash
pip install bhargava_swara



USAGE

from bhargava_swara import (
    analyze_raga,
    analyze_tala,
    analyze_tempo,
    analyze_tradition,
    analyze_ornaments,
    analyze_music_full
)

# Set your Gemini API key
api_key = "YOUR_API_KEY"
audio = "path/to/audio.wav"

# Individual analyses
print(f"Raga: {analyze_raga(audio, api_key)}")
print(f"Tala: {analyze_tala(audio, api_key)}")
print(f"Tempo: {analyze_tempo(audio, api_key)}")
print(f"Tradition: {analyze_tradition(audio, api_key)}")
print(f"Ornaments: {analyze_ornaments(audio, api_key)}")

# Full analysis
print(f"Full Analysis:\n{analyze_music_full(audio, api_key)}")