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

**3. Sci-Fi Robot:**
> "Transform the voice into a malfunction robot with stuttering and metallic resonance."

## Project Structure

- `inputs/`: Directory for source audio files.
- `outputs/`: Directory for generated audio files (ignored by git).
- `main.py`: Main entry point for the application.
- `audio_analyzer.py`: Analyzes input audio features.
- `audio_processor.py`: Applies effects using Pedalboard.
- `llm_client.py`: Handles communication with Groq API.
- `prompt_manager.py`: Constructs prompts for the LLM.
