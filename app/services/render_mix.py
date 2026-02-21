import librosa
import soundfile as sf
import numpy as np

TARGET_SR = 44100

def load_audio(path):
    y, sr = librosa.load(path, sr=TARGET_SR, mono=True)
    return y, sr

def match_bpm(y, sr, target_bpm):
    bpm, _ = librosa.beat.beat_track(y=y, sr=sr)
    rate = bpm / target_bpm if bpm > 0 else 1.0
    return librosa.effects.time_stretch(y, rate)

def mix_tracks(track_paths, output_path):
    mixed = None
    target_bpm = None

    for i, path in enumerate(track_paths):
        y, sr = load_audio(path)
        bpm, _ = librosa.beat.beat_track(y=y, sr=sr)

        if i == 0:
            target_bpm = bpm
            mixed = y
        else:
            y = match_bpm(y, sr, target_bpm)

            # 8-second DJ-style overlap
            fade_len = 8 * sr
            fade_len = min(fade_len, len(mixed), len(y))

            fade_out = np.linspace(1, 0, fade_len)
            fade_in = np.linspace(0, 1, fade_len)

            mixed[-fade_len:] = mixed[-fade_len:] * fade_out
            y[:fade_len] = y[:fade_len] * fade_in

            mixed = np.concatenate([mixed, y])

    sf.write(output_path, mixed, TARGET_SR)