import numpy as np
import librosa

def griffin_lim(audio_features, n_iter=60, hop_length=256):
    """Convert audio features back to waveform using Griffin-Lim algorithm."""
    # Initialize the phase to random values
    phase = np.random.rand(*audio_features.shape) * 2 * np.pi
    # Initialize the magnitude from the audio features
    magnitude = audio_features

    for _ in range(n_iter):
        # Reconstruct the complex spectrogram
        complex_spec = magnitude * np.exp(1j * phase)
        # Inverse Short-Time Fourier Transform (ISTFT) to get the waveform
        waveform = librosa.istft(complex_spec, hop_length=hop_length)
        # Recompute the magnitude
        complex_spec_new = librosa.stft(waveform, hop_length=hop_length)
        magnitude = np.abs(complex_spec_new)
        # Update the phase
        phase = np.angle(complex_spec_new)

    return waveform

def audio_to_features(audio_path, sr=22050):
    """Extract audio features from a waveform."""
    y, _ = librosa.load(audio_path, sr=sr)
    features = librosa.feature.melspectrogram(y, sr=sr)
    return features
