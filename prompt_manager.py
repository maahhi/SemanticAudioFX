import json

SYSTEM_INSTRUCTION = """
You are an expert audio engineer. Your task is to translate natural language descriptions of audio effects and environments into specific parameters for a digital audio processing chain.

You have access to the following audio effects units (plugins):

1. **Reverb**: Creates space and ambience.
   - Params: room_size (0.0-1.0), damping (0.0-1.0), wet_level (0.0-1.0), dry_level (0.0-1.0), width (0.0-1.0)
2. **Compressor**: Controls dynamic range.
   - Params: threshold_db (-60 to 0), ratio (1.0 to 20.0), attack_ms (0.1 to 100), release_ms (10 to 1000)
3. **HighShelf**: Boosts or cuts frequencies above a cutoff.
   - Params: cutoff_frequency_hz (20 to 20000), gain_db (-24 to 24), q (0.1 to 10)
4. **LowShelf**: Boosts or cuts frequencies below a cutoff.
   - Params: cutoff_frequency_hz (20 to 20000), gain_db (-24 to 24), q (0.1 to 10)
5. **PeakFilter**: Boosts or cuts a specific frequency band.
   - Params: cutoff_frequency_hz (20 to 20000), gain_db (-24 to 24), q (0.1 to 10)
6. **Distortion**: Adds grit and saturation.
   - Params: drive_db (0 to 50)
7. **Delay**: Adds echoes.
    - Params: delay_seconds (0.0 to 2.0), feedback (0.0 to 1.0), mix (0.0 to 1.0)
8. **Chorus**: Adds modulation and thickness.
    - Params: rate_hz (0.1 to 10), depth (0.0 to 1.0), centre_delay_ms (1 to 20), feedback (0.0 to 1.0), mix (0.0 to 1.0)
9. **Phaser**: Adds sweeping modulation.
    - Params: rate_hz (0.01 to 10), depth (0.0 to 1.0), centre_frequency_hz (100 to 5000), feedback (0.0 to 1.0), mix (0.0 to 1.0)
10. **Gain**: Adjusts volume.
    - Params: gain_db (-60 to 24)

### Output Format
You must respond with a valid JSON object containing an "effect_chain" list. Each item in the list must have a "type" (one of the bold names above, case-insensitive) and "params" object. Include a "reason" field explaining your design.

Example JSON Structure:
{
  "effect_chain": [
    {
      "type": "low_shelf",
      "params": {"cutoff_frequency_hz": 200, "gain_db": -5}
    },
    {
      "type": "reverb",
      "params": {"room_size": 0.8, "wet_level": 0.4}
    }
  ],
  "reason": "Cutting low end to clear mud and adding reverb for a spacious feel."
}

Do not include markdown formatting like ```json ... ```. Just return the raw JSON string.
CRITICAL: Do NOT use mathematical expressions (e.g., "24 - 16") in the JSON values. You must calculate the value yourself and output a single number (e.g., 8.0).
"""

FEW_SHOT_EXAMPLES = [
    {
        "input": "Make it sound like a telephone call.",
        "output": {
            "effect_chain": [
                {
                    "type": "high_shelf",
                    "params": {"cutoff_frequency_hz": 4000, "gain_db": -24.0, "q": 1.0}
                },
                {
                    "type": "low_shelf",
                    "params": {"cutoff_frequency_hz": 400, "gain_db": -24.0, "q": 1.0}
                },
                {
                    "type": "distortion",
                    "params": {"drive_db": 10.0}
                },
                 {
                    "type": "compressor",
                    "params": {"threshold_db": -15.0, "ratio": 4.0}
                }
            ],
            "reason": "Telephone audio has limited bandwidth (approx 400Hz to 4kHz) and is often heavily compressed and slightly distorted."
        }
    },
    {
        "input": "A large, empty cathedral.",
        "output": {
            "effect_chain": [
                {
                    "type": "reverb",
                    "params": {
                        "room_size": 0.95,
                        "damping": 0.2,
                        "wet_level": 0.6,
                        "dry_level": 0.5,
                        "width": 1.0
                    }
                },
                {
                    "type": "delay",
                    "params": {
                         "delay_seconds": 0.4,
                         "feedback": 0.3,
                         "mix": 0.2
                    }
                }
            ],
             "reason": "Cathedrals have very long decay times (high room_size) and are very reflective (low damping). A touch of pre-delay adds to the sense of scale."
        }
    },
    {
        "input": "Radio broadcast from the 1950s.",
        "output": {
            "effect_chain": [
                {
                     "type": "high_shelf",
                     "params": {"cutoff_frequency_hz": 5000, "gain_db": -15.0}
                },
                 {
                     "type": "low_shelf",
                     "params": {"cutoff_frequency_hz": 150, "gain_db": -10.0}
                },
                {
                    "type": "distortion",
                    "params": {"drive_db": 5.0}
                },
                {
                    "type": "gain",
                    "params": {"gain_db": 2.0}
                }
            ],
            "reason": "Vintage radio is band-limited but not as aggressively as a telephone. Slight saturation (distortion) adds vintage warmth."
        }
    },
    {
        "input": "Deep underwater sound.",
        "output": {
             "effect_chain": [
                {
                    "type": "low_shelf",
                    "params": {"cutoff_frequency_hz": 1000, "gain_db": 12.0}
                },
                {
                    "type": "high_shelf",
                    "params": {"cutoff_frequency_hz": 500, "gain_db": -24.0}
                },
                 {
                    "type": "reverb",
                     "params": {"room_size": 0.3, "wet_level": 0.5, "damping": 0.9}
                 }
            ],
            "reason": "Water absorbs high frequencies rapidly, so we boost lows and cut highs aggressively. Heavy damping in reverb simulates the density of water."
        }
    }
]


def build_prompt(user_text: str, audio_features: dict = None) -> str:
    """Methods to construct the full prompt interaction."""
    
    prompt = f"{SYSTEM_INSTRUCTION}\n\n# Examples\n"
    
    for ex in FEW_SHOT_EXAMPLES:
        prompt += f"Input: \"{ex['input']}\"\nOutput: {json.dumps(ex['output'])}\n\n"

    # Add Audio Context if available
    audio_context = ""
    if audio_features:
        audio_context = "Audio Analysis:\n"
        for key, value in audio_features.items():
            audio_context += f"- {key}: {value}\n"
        audio_context += "\n"
        
    prompt += f"# Current Task\n{audio_context}Input: \"{user_text}\"\nOutput:"
    
    return prompt
