from pedalboard import (
    Pedalboard, 
    Reverb, 
    Compressor, 
    HighShelfFilter, 
    LowShelfFilter, 
    PeakFilter, 
    Gain,
    Delay,
    Chorus,
    Distortion,
    Phaser
)
import soundfile as sf
import numpy as np

def apply_pedalboard_effects(input_path: str, output_path: str, effects_config: dict):
    """
    Applies audio effects using Pedalboard based on the provided configuration.
    
    Args:
        input_path: Path to the input audio file.
        output_path: Path to save the processed audio.
        effects_config: Dictionary containing 'effect_chain' list of effect definitions.
    """
    # Load audio
    audio, sample_rate = sf.read(input_path)
    
    # Define the board
    board = Pedalboard()
    
    # Parse effects from config
    # Expecting effects_config to be like: {'effect_chain': [{'type': 'reverb', 'params': {...}}, ...]}
    # OR for backward compatibility with the simple plan: {'effect': 'reverb', 'parameters': {...}}
    
    chain_data = []
    if 'effect_chain' in effects_config:
        chain_data = effects_config['effect_chain']
    elif 'effect' in effects_config:
        # Single effect mode
        chain_data = [{'type': effects_config['effect'], 'params': effects_config.get('parameters', {})}]
        
    for effect_item in chain_data:
        effect_type = effect_item.get('type', '').lower()
        params = effect_item.get('params', {})
        
        plugin = None
        
        try:
            if effect_type == 'reverb':
                plugin = Reverb(
                    room_size=float(params.get('room_size', 0.5)),
                    damping=float(params.get('damping', 0.5)),
                    wet_level=float(params.get('wet_level', 0.33)),
                    dry_level=float(params.get('dry_level', 0.6)),
                    width=float(params.get('width', 1.0)),
                    freeze_mode=float(params.get('freeze_mode', 0.0))
                )
            elif effect_type == 'compressor':
                plugin = Compressor(
                    threshold_db=float(params.get('threshold_db', -10)),
                    ratio=float(params.get('ratio', 2.0)),
                    attack_ms=float(params.get('attack_ms', 10)),
                    release_ms=float(params.get('release_ms', 100))
                )
            elif effect_type == 'high_shelf':
                plugin = HighShelfFilter(
                    cutoff_frequency_hz=float(params.get('cutoff_frequency_hz', 4000)),
                    gain_db=float(params.get('gain_db', 0)),
                    q=float(params.get('q', 0.707))
                )
            elif effect_type == 'low_shelf':
                plugin = LowShelfFilter(
                    cutoff_frequency_hz=float(params.get('cutoff_frequency_hz', 400)),
                    gain_db=float(params.get('gain_db', 0)),
                    q=float(params.get('q', 0.707))
                )
            elif effect_type == 'peaking' or effect_type == 'peak':
                plugin = PeakFilter(
                    cutoff_frequency_hz=float(params.get('cutoff_frequency_hz', 1000)),
                    gain_db=float(params.get('gain_db', 0)),
                    q=float(params.get('q', 0.707))
                )
            elif effect_type == 'delay':
                plugin = Delay(
                    delay_seconds=float(params.get('delay_seconds', 0.5)),
                    feedback=float(params.get('feedback', 0.2)),
                    mix=float(params.get('mix', 0.5))
                )
            elif effect_type == 'chorus':
                 plugin = Chorus(
                    rate_hz=float(params.get('rate_hz', 1.0)),
                    depth=float(params.get('depth', 0.25)),
                    centre_delay_ms=float(params.get('centre_delay_ms', 7.0)),
                    feedback=float(params.get('feedback', 0.0)),
                    mix=float(params.get('mix', 0.5))
                 )
            elif effect_type == 'distortion':
                plugin = Distortion(
                    drive_db=float(params.get('drive_db', 25.0))
                )
            elif effect_type == 'phaser':
                plugin = Phaser(
                    rate_hz=float(params.get('rate_hz', 1.0)),
                    depth=float(params.get('depth', 0.5)),
                    centre_frequency_hz=float(params.get('centre_frequency_hz', 1300.0)),
                    feedback=float(params.get('feedback', 0.0)),
                    mix=float(params.get('mix', 0.5))
                )
            elif effect_type == 'gain':
                plugin = Gain(
                    gain_db=float(params.get('gain_db', 0.0))
                )

            if plugin:
                board.append(plugin)
            else:
                print(f"Warning: Unknown effect type '{effect_type}'")
                
        except Exception as e:
            print(f"Error creating effect '{effect_type}': {e}")

    # Run the audio through the board
    processed_audio = board(audio, sample_rate)
    
    # Save output
    sf.write(output_path, processed_audio, sample_rate)
    return True
