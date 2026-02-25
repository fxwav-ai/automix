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

        # Proper tempo match
        stretch_rate = base_bpm / meta["bpm"]
        stretch_rate = max(0.96, min(1.04, stretch_rate))
        y = librosa.effects.time_stretch(y, stretch_rate)

        # Phrase-based fade length
        fade_len = int(meta["phrase_length"] * sr)
        fade_len = min(fade_len, len(final_audio), len(y))

        # Equal-power crossfade
        fade_out = np.cos(np.linspace(0, np.pi/2, fade_len))
        fade_in  = np.sin(np.linspace(0, np.pi/2, fade_len))

        a = final_audio
        b = y

        a_tail = a[-fade_len:]
        b_head = b[:fade_len]

        # Vocal safety adjustment
        if vocal_activity(a_tail):
            fade_len = int(fade_len * 0.5)
            a_tail = a[-fade_len:]
            b_head = b[:fade_len]
            fade_out = np.cos(np.linspace(0, np.pi/2, fade_len))
            fade_in  = np.sin(np.linspace(0, np.pi/2, fade_len))

        blended = (a_tail * fade_out) + (b_head * fade_in)

        final_audio = np.concatenate([
            a[:-fade_len],
            blended,
            b[fade_len:]
        ])

    final_audio = normalize_lufs(final_audio, SR)
    sf.write(output_path, final_audio, SR)