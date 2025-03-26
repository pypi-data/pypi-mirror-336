import numpy as np
import os
from src.model import create_tacotron2_model
from src.data_processing import normalize_text, text_to_phonemes, extract_audio_features
import yaml

def train_model(config_path):
    # Load configuration
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    vocab_size = config['vocab_size']
    embedding_dim = config['embedding_dim']
    lstm_units = config['lstm_units']
    max_decoder_length = config['max_decoder_length']
    epochs = config['epochs']

    model = create_tacotron2_model(vocab_size, embedding_dim, lstm_units, max_decoder_length)

    # Load preprocessed data
    normalized_text_dir = 'data/processed/normalized_text/'
    phonemes_dir = 'data/processed/phonemes/'
    audio_features_dir = 'data/processed/audio_features/'

    normalized_texts = []
    phonemes_list = []
    audio_features_list = []

    # Load normalized texts
    for filename in os.listdir(normalized_text_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(normalized_text_dir, filename), 'r') as file:
                normalized_texts.append(file.read())

    # Load phonemes
    for filename in os.listdir(phonemes_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(phonemes_dir, filename), 'r') as file:
                phonemes_list.append(file.read())

    # Load audio features
    for filename in os.listdir(audio_features_dir):
        if filename.endswith('.npy'):
            audio_features_list.append(np.load(os.path.join(audio_features_dir, filename)))

    # Convert lists to numpy arrays
    normalized_texts = np.array(normalized_texts)
    phonemes_list = np.array(phonemes_list)
    audio_features_list = np.array(audio_features_list)

    # Train the model
    model.fit([normalized_texts, phonemes_list], audio_features_list, epochs=epochs)

if __name__ == "__main__":
    train_model('config/config.yaml')