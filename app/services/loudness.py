import pyloudnorm as pyln
import numpy as np

def normalize_lufs(audio, sr, target_lufs=-14.0):
    meter = pyln.Meter(sr)
    loudness = meter.integrated_loudness(audio)
    normalized = pyln.normalize.loudness(audio, loudness, target_lufs)
    return normalized