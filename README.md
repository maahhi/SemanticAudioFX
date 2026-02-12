# Text-to-Audio FX

Transform your audio files using text descriptions powered by Llama 3 on Groq.

## Overview
This project allows you to apply audio effects (reverb, delay, distortion, eq, etc.) to an input audio file by simply describing the desired effect in natural language. It analyzes the input audio features to make informed decisions about the effects chain.

## Setup

1.  **Clone the repository** (if applicable) and navigate to the project directory.

2.  **Create a Virtual Environment** (recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Setup**:
    Copy the example environment file and add your Groq API key:
    ```bash
    cp .env.example .env
    ```
    Open `.env` and set `GROQ_API_KEY` to your key.

## Usage

### Basic Usage
The main script requires an input file, a text description, and an output path.

```bash
python main.py --input inputs/Recording.wav --text "Make it sound like a telephone call" --output outputs/telephone_effect.wav
```

### Verbose Mode
Use the `--verbose` flag to see the audio analysis results, the raw LLM response, and the parsed effect parameters.

```bash
python main.py --input inputs/beep.wav --text "Add a massive cathedral reverb" --output outputs/reverb_beep.wav --verbose
```

### Examples

**1. Telephone Effect:**
> "Make it sound like a vintage telephone call with limited bandwidth and some noise."

**2. Underwater:**
> "The sound is coming from deep underwater, muffled and distant."

<video src="https://github.com/maahhi/SemanticAudioFX/raw/main/samples/beep.mp4" controls="controls"></video>
**3. Sci-Fi Robot:**
> "Transform the voice into a malfunction robot with stuttering and metallic resonance."
<video src="https://github.com/maahhi/SemanticAudioFX/raw/main/samples/rec_robo.mp4" controls="controls"></video>
## Audio Analysis & Dynamic Prompts

The system automatically analyzes the input audio before generating effects. This allows you to write "dynamic" prompts that adapt to the specific characteristics of the audio file.

**Analyzed Features:**
- **Tempo (BPM)**: The speed of the track.
- **Brightness (Spectral Centroid)**: How "bright" or "dark" the audio sounds.
- **Loudness (RMS)**: The volume level.
- **Content Type**: Heuristic guess (e.g., "Balanced/Tonal" vs "High Noise").

**Example Dynamic Prompts:**
<video src="https://github.com/maahhi/SemanticAudioFX/raw/main/samples/beep.mp4" controls="controls"></video>
1.  **Tempo-Synced Delay:**
    > "Add a delay echo. The delay time should be exactly 60 divided by the detected BPM."
    *   *Result*: If input is 120 BPM, delay will be 0.5s. If 100 BPM, delay will be 0.6s.
<video src="https://github.com/maahhi/SemanticAudioFX/raw/main/samples/beep_temposync.mp4" controls="controls"></video>
2.  **Adaptive EQ:**
    > "If the audio is dark (low centroid), brighten it with a high shelf. If it is already bright, make it warmer."
    *   *Result*: The system checks the `spectral_centroid_brightness` and applies EQ accordingly.

3.  **Smart Normalization:**
    > "Check the loudness. If it is below -20dB, add gain to bring it up to standard levels."

## Project Structure

- `inputs/`: Directory for source audio files.
- `outputs/`: Directory for generated audio files.
- `main.py`: Main entry point for the application.
- `audio_analyzer.py`: Analyzes input audio features.
- `audio_processor.py`: Applies effects using Pedalboard.
- `llm_client.py`: Handles communication with Groq API.
- `prompt_manager.py`: Constructs prompts for the LLM.
