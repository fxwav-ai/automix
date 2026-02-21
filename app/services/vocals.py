import librosa
import numpy as np

def vocal_activity(y):
    spec = np.abs(librosa.stft(y))
    centroid = librosa.feature.spectral_centroid(S=spec)

    # High centroid ≈ vocal presence
    return np.mean(centroid) > 2500