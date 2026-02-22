import essentia.standard as es
import numpy as np

def analyze_track(path):
    loader = es.MonoLoader(filename=path)
    audio = loader()

    rhythm = es.RhythmExtractor2013(method="multifeature")
    bpm, beats, _, _, _ = rhythm(audio)

    loudness = es.LoudnessEBUR128()(audio)
    energy = np.mean(audio ** 2)

    # Phrase boundaries (approx every 8 bars)
    seconds_per_beat = 60 / bpm
    phrase_length = seconds_per_beat * 32  # 32 beats = 8 bars (4/4)

    return {
        "bpm": float(bpm),
        "beats": beats.tolist(),
        "phrase_length": phrase_length,
        "energy": float(energy),
        "lufs": float(loudness)
    }