import librosa
import numpy as np

def analyze_track(path):
    y, sr = librosa.load(path, sr=None)

    # BPM detection
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)

    # RMS energy
    rms = librosa.feature.rms(y=y)
    energy = float(np.mean(rms))

    # Beat times in seconds
    beat_times = librosa.frames_to_time(beats, sr=sr).tolist()

    # Phrase length (8 bars in 4/4)
    seconds_per_beat = 60 / tempo
    phrase_length = seconds_per_beat * 32

    duration = librosa.get_duration(y=y, sr=sr)

    return {
        "bpm": float(tempo),
        "beats": beat_times,
        "phrase_length": float(phrase_length),
        "energy": energy,
        "duration": float(duration)
    }