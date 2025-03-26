import numpy as np
import os
import librosa

def normalize_text(text):
    # Implement text normalization logic here
    normalized_text = text.lower().strip()
    return normalized_text

def text_to_phonemes(text, lts_model):
    # Convert text to phonemes using the letter-to-sound model
    phonemes = lts_model.predict(text)
    return phonemes

def extract_audio_features(audio_path):
    # Load audio file and extract features
    audio, sr = librosa.load(audio_path, sr=None)
    audio_features = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=80)
    return audio_features

def load_normalized_texts(normalized_text_dir):
    normalized_texts = []
    for filename in os.listdir(normalized_text_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(normalized_text_dir, filename), 'r') as file:
                normalized_texts.append(file.read())
    return normalized_texts

def load_phonemes(phonemes_dir):
    phonemes_list = []
    for filename in os.listdir(phonemes_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(phonemes_dir, filename), 'r') as file:
                phonemes_list.append(file.read().strip().split())
    return phonemes_list

def load_audio_features(audio_features_dir):
    audio_features_list = []
    for filename in os.listdir(audio_features_dir):
        if filename.endswith('.npy'):
            features = np.load(os.path.join(audio_features_dir, filename))
            audio_features_list.append(features)
    return audio_features_list