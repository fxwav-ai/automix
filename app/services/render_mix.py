import librosa
import soundfile as sf
import numpy as np

from app.services.analysis import analyze_track
from app.services.vocals import vocal_activity
from app.services.loudness import normalize_lufs

SR = 44100

def load(path):
    return librosa.load(path, sr=SR, mono=True)

def mix_tracks(paths, output_path):
    final_audio = None
    base_bpm = None

    for i, path in enumerate(paths):
        y, sr = load(path)
        meta = analyze_track(path)

        if i == 0:
            base_bpm = meta["bpm"]
            final_audio = y
            continue

        # BPM match
        stretch_rate = meta["bpm"] / base_bpm
        y = librosa.effects.time_stretch(y, stretch_rate)

        # Phrase-locked transition
        fade_len = int(meta["phrase_length"] * sr)
        fade_len = min(fade_len, len(final_audio), len(y))

        fade_out = np.linspace(1, 0, fade_len)
        fade_in = np.linspace(0, 1, fade_len)

        # Vocal safety
        if vocal_activity(final_audio[-fade_len:]):
            fade_len = int(fade_len * 0.5)

        final_audio[-fade_len:] *= fade_out
        y[:fade_len] *= fade_in

        final_audio = np.concatenate([final_audio, y])

    final_audio = normalize_lufs(final_audio, SR)
    sf.write(output_path, final_audio, SR)