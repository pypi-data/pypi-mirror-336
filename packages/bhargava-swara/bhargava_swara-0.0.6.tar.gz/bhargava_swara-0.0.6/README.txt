Bhargava Swara
=============

A Python library for analyzing and visualizing Indian classical music, including raga, tala, tempo, tradition, ornaments, full analysis, and mel-frequency spectrograms.

Prerequisites
-------------

- **Gemini API Key:** This library uses Google's Gemini API for music analysis. You'll need to:
  1. Sign up for a Google Cloud account.
  2. Enable the Generative AI API in the Google Cloud Console.
  3. Create an API key in the "Credentials" section.
  See Google's Generative AI Docs (https://cloud.google.com/generative-ai/docs) for details.

- **Audio Files:** Supported formats include WAV and MP3 for spectrogram generation.

Installation
------------

Install the library using pip:

    pip install bhargava_swara

Usage
-----

### Music Analysis

Analyze various aspects of Indian classical music using the Gemini API.

```python
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


# Mel-Frequency Spectrogram Generation
# Generate a mel-frequency spectrogram to visualize the frequency content of an audio file over time.

from bhargava_swara import generate_mel_spectrogram

# Define input and output paths
audio = "path/to/audio.wav"
output = "path/to/output_mel_spectrogram.png"

# Generate the spectrogram
generate_mel_spectrogram(audio, output, n_mels=128, fmax=8000)
print("Mel spectrogram generated successfully!")

audio: Path to the input audio file (e.g., WAV or MP3).
output: Path to save the PNG file (e.g., "spectrogram.png").
n_mels: Number of mel bands (default: 128).
fmax: Maximum frequency in Hz (default: 8000).


Dependencies
google-generativeai>=0.1.0
librosa>=0.10.0
matplotlib>=3.7.0
numpy>=1.24.0


Contributing
Contributions are welcome! Please submit a pull request or open an issue on the GitHub repository (if available).

License
This library is licensed under the MIT License. See the LICENSE file for details.