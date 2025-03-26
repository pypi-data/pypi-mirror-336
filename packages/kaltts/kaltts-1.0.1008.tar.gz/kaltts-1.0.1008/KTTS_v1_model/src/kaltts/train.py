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

    # Check if data is loaded correctly
    print(f"Loaded {len(normalized_texts)} normalized text files.")
    print(f"Loaded {len(phonemes_list)} phoneme files.")
    print(f"Loaded {len(audio_features_list)} audio feature files.")

    # Ensure sequence lengths match
    sequence_length = min(audio_features_list[0].shape[1], max_decoder_length)
    input_data = np.random.randint(1, vocab_size, size=(len(normalized_texts), sequence_length))
    decoder_inputs = np.random.rand(len(normalized_texts), sequence_length, 80)
    output_data = np.array([af[:, :sequence_length].T for af in audio_features_list])

    # Adjust validation_split based on the number of samples
    validation_split = 0.1 if len(normalized_texts) > 1 else 0

    # Train the model
    model.fit([input_data, decoder_inputs], output_data, epochs=epochs, batch_size=32, validation_split=validation_split)

    # Save the trained model
    model.save('tts_model.h5')
    print("Model training complete. Model saved as 'tts_model.h5'.")

if __name__ == "__main__":
    train_model('config/config.yaml')
