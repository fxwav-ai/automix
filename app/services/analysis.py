import librosa
import numpy as np

def analyze_track(path):
    # Load audio (first 2 minutes)
    y, sr = librosa.load(path, sr=22050, mono=True, duration=120)

    # --- BPM detection ---
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)

    # --- RMS energy ---
    rms = librosa.feature.rms(y=y)
    energy = float(np.mean(rms))

    # --- Beat times in seconds ---
    beat_times = librosa.frames_to_time(beats, sr=sr).tolist()

    # --- Phrase length (8 bars in 4/4) ---
    seconds_per_beat = 60 / tempo
    phrase_length = seconds_per_beat * 32  # 8 bars * 4 beats

    # --- Track duration ---
    duration = librosa.get_duration(y=y, sr=sr)

    # --- Key detection ---
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_mean = chroma.mean(axis=1)
    key_index = int(np.argmax(chroma_mean))
    keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    key = keys[key_index]

    return {
        "bpm": float(tempo),
        "key": key,
        "beats": beat_times,
        "phrase_length": float(phrase_length),
        "energy": energy,
        "duration": float(duration)
    }