import librosa
import numpy as np

def griffin_lim(spectrogram, n_iter=60, window='hann', n_fft=1024, hop_length=None):
    # Inverse Short-Time Fourier Transform
    angles = np.exp(2j * np.pi * np.random.rand(*spectrogram.shape))

    for i in range(n_iter):
        inverse = librosa.istft(spectrogram * angles, hop_length=hop_length, window=window)
        reconstruction = librosa.stft(inverse, n_fft=n_fft, hop_length=hop_length, window=window)
        angles = np.exp(1j * np.angle(reconstruction))

    return librosa.istft(spectrogram * angles, hop_length=hop_length, window=window)
