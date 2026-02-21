import librosa
import numpy as np

def analyze_track(path: str):
    y, sr = librosa.load(path, sr=None)

    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    rms = np.mean(librosa.feature.rms(y=y))

    return {
        "bpm": float(tempo),
        "energy": float(rms),
        "duration": librosa.get_duration(y=y, sr=sr)
    }