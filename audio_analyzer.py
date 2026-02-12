import librosa
import numpy as np
import os

def analyze_audio(file_path: str, duration_limit: float = 30.0) -> dict:
    """
    Analyzes an audio file and returns a dictionary of features.
    
    Args:
        file_path: Path to the audio file.
        duration_limit: Limit analysis to the first N seconds to speed up processing.
        
    Returns:
        dict: A dictionary containing extracted audio features.
    """
    try:
        # Load audio (load only the first few seconds for speed)
        y, sr = librosa.load(file_path, sr=None, duration=duration_limit)
        
        # 1. Basic Info
        duration = librosa.get_duration(y=y, sr=sr)
        
        # 2. Loudness (RMS)
        rms = librosa.feature.rms(y=y)
        avg_rms = float(np.mean(rms))
        
        # 3. Brightness (Spectral Centroid)
        # High centroid = brighter/sharper sound (e.g., speech sibilance, cymbals)
        # Low centroid = darker/muffled sound (e.g., bass, hum)
        cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        avg_centroid = float(np.mean(cent))
        
        # 4. Zero Crossing Rate (Noise/Percussiveness vs Tonal)
        # High ZCR often indicates noise or unvoiced speech
        zcr = librosa.feature.zero_crossing_rate(y)
        avg_zcr = float(np.mean(zcr))
        
        # 5. Tempo (BPM)
        # librosa 0.10+ returns a scalar for tempo
        tempo = librosa.feature.tempo(y=y, sr=sr)
        if isinstance(tempo, np.ndarray):
            tempo = tempo[0]
        tempo = float(tempo)
        
        # 6. Spectral Bandwidth
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        avg_bw = float(np.mean(spec_bw))

        # Basic Classification Heuristic (Very rough)
        # Music often has stable rhythm and harmonic content. Speech has high variability.
        content_hint = "Unknown"
        if avg_zcr > 0.1:
            content_hint = "High Noise/Unvoiced Speech"
        elif avg_centroid < 1000:
            content_hint = "Low Frequency/Dark"
        else:
            content_hint = "Balanced/Tonal"

        return {
            "duration_seconds": round(duration, 2),
            "sample_rate": sr,
            "tempo_bpm": round(tempo, 1),
            "avg_loudness_rms": round(avg_rms, 4),
            "spectral_centroid_brightness": round(avg_centroid, 1),
            "zero_crossing_rate": round(avg_zcr, 4),
            "spectral_bandwidth": round(avg_bw, 1),
            "content_descriptor": content_hint
        }
        
    except Exception as e:
        print(f"Warning: Audio analysis failed: {e}")
        return {"error": str(e)}
