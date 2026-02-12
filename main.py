
import argparse
import sys
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from llm_client import query_llama
from prompt_manager import build_prompt
from audio_processor import apply_pedalboard_effects
from audio_analyzer import analyze_audio

def main():
    parser = argparse.ArgumentParser(description="Text-to-Audio FX: Enrich audio based on text description.")
    parser.add_argument("--input", required=True, help="Path to input audio file")
    parser.add_argument("--text", required=True, help="Description of the desired effect")
    parser.add_argument("--output", required=True, help="Path to save output audio file")
    parser.add_argument("--verbose", action="store_true", help="Print debug info")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(1)
        
    # Check for API key
    if not os.environ.get("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY environment variable is not set.")
        print("Please export GROQ_API_KEY='your_api_key'")
        sys.exit(1)

    # 0. Analyze Audio
    print(f"Analyzing audio: '{args.input}'...")
    audio_features = analyze_audio(args.input)
    if "error" in audio_features:
        print(f"Warning: Audio analysis failed: {audio_features['error']}")
        audio_features = None
    else:
        print("Audio Analysis Results:")
        for k, v in audio_features.items():
            print(f"  - {k}: {v}")

    # 1. Generate Prompt
    print(f"Generating prompt for: '{args.text}'...")
    prompt = build_prompt(args.text, audio_features)
    
    # 2. Query LLM
    print("Querying Llama 3 via Groq...")
    try:
        response_text = query_llama(prompt)
        if args.verbose:
            print("Raw LLM Response:")
            print(response_text)
    except Exception as e:
        print(f"Error querying LLM: {e}")
        sys.exit(1)
        
    # 3. Parse JSON
    print("Parsing parameters...")
    try:
        # cleanup markdown code blocks if present (despite instruction)
        cleaned_response = response_text.strip()
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]
        
        effects_config = json.loads(cleaned_response)
        
        if args.verbose:
            print("Parsed Config:")
            print(json.dumps(effects_config, indent=2))
            
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from LLM: {e}")
        print("Raw response was:", response_text)
        sys.exit(1)

    # 4. Apply Effects
    print(f"Applying effects to '{args.input}'...")
    try:
        success = apply_pedalboard_effects(args.input, args.output, effects_config)
        if success:
            print(f"Successfully saved to '{args.output}'")
            if "reason" in effects_config:
                print(f"Effect Reasoning: {effects_config['reason']}")
    except Exception as e:
        print(f"Error applying effects: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
