import json
import json
import sys
from llm_client import query_llama
from prompt_manager import build_prompt

TEST_CASES = [
    {
        "input": "A giant speaking in a massive, echoing cave.",
        "reasoning": "To simulate a giant, we need to emphasize low frequencies (LowShelf boost). For the cave, we need a large Reverb with long decay (high room_size). A small Delay helps simulate reflections.",
        "expected_pedalboard_inputs": [
            {"type": "low_shelf", "params": {"cutoff_frequency_hz": 200, "gain_db": 6.0}},
            {"type": "reverb", "params": {"room_size": 0.9, "wet_level": 0.5}},
            {"type": "delay", "params": {"delay_seconds": 0.3}}
        ]
    },
    {
        "input": "A broken radio transmission from a spaceship.",
        "reasoning": "Radio requires bandwidth limiting (HighShelf cut, LowShelf cut). 'Broken' implies Distortion. 'Spaceship' might suggest some background ambience or slight Reverb/Delay, but the radio effect is dominant.",
        "expected_pedalboard_inputs": [
            {"type": "high_shelf", "params": {"cutoff_frequency_hz": 3000, "gain_db": -12.0}},
            {"type": "low_shelf", "params": {"cutoff_frequency_hz": 300, "gain_db": -12.0}},
            {"type": "distortion", "params": {"drive_db": 15.0}}
        ]
    },
    {
        "input": "An underwater announcement.",
        "reasoning": "Water absorbs high frequencies, so aggressive HighShelf cut. LowShelf boost to make it muddy. Reverb with high damping to simulate density.",
        "expected_pedalboard_inputs": [
            {"type": "high_shelf", "params": {"cutoff_frequency_hz": 600, "gain_db": -20.0}},
            {"type": "low_shelf", "params": {"cutoff_frequency_hz": 1000, "gain_db": 6.0}},
            {"type": "reverb", "params": {"room_size": 0.4, "damping": 0.9}}
        ]
    },
    {
        "input": "A robot malfunction.",
        "reasoning": "Robotic sounds often use Chorus or Phaser for modulation. 'Malfunction' implies Distortion or rapid stuttering (short Delay).",
        "expected_pedalboard_inputs": [
            {"type": "phaser", "params": {"rate_hz": 5.0, "depth": 0.8}},
            {"type": "distortion", "params": {"drive_db": 10.0}},
            {"type": "delay", "params": {"delay_seconds": 0.05, "feedback": 0.7}}
        ]
    }
]

def run_tests():
    print("Running Audio FX Generation Tests...\n")
    
    for i, test_case in enumerate(TEST_CASES):
        print(f"--- Test Case {i+1}: {test_case['input']} ---")
        
        # Generte Prompt
        prompt = build_prompt(test_case['input'])
        
        # Query LLM
        print("Querying LLM...")
        try:
            response_text = query_llama(prompt)
        except Exception as e:
            print(f"Error querying LLM: {e}")
            continue
            
        # Parse Response
        try:
            # Basic cleanup
            cleaned_response = response_text.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            
            llm_config = json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            print(f"Raw Response: {response_text}")
            continue

        # Validating
        print("\n[Comparison]")
        print(f"My Reasoning:      {test_case['reasoning']}")
        print(f"LLM Reasoning:     {llm_config.get('reason', 'N/A')}")
        
        print("\n[Effect Chain]")
        print("Expected (Key Effects):")
        print(json.dumps(test_case['expected_pedalboard_inputs'], indent=2))
        
        print("LLM Generated:")
        print(json.dumps(llm_config.get('effect_chain', []), indent=2))
        
        # Simple match check (Check if expected effect types are present)
        expected_types = [eff['type'].lower() for eff in test_case['expected_pedalboard_inputs']]
        generated_types = [eff['type'].lower() for eff in llm_config.get('effect_chain', [])]
        
        missing = [t for t in expected_types if t not in generated_types]
        
        if not missing:
            print(f"\n✅ SUCCESS: All expected effect types {expected_types} present.")
        else:
            print(f"\n⚠️  PARTIAL: Missing effect types: {missing}")
            
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    run_tests()
