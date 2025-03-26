import numpy as np
from src.model import create_tacotron2_model
from src.vocoder import griffin_lim
import yaml

def generate_speech(input_text):
    config_path = 'config/config.yaml'
    
    # Load configuration
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    vocab_size = config['vocab_size']
    embedding_dim = config['embedding_dim']
    lstm_units = config['lstm_units']
    max_decoder_length = config['max_decoder_length']

    # Load model
    model = create_tacotron2_model(vocab_size, embedding_dim, lstm_units, max_decoder_length)
    model.load_weights('tts_model.h5')

    # Prepare input data
    input_data = np.random.randint(1, vocab_size, size=(1, len(input_text)))  # Dummy input for illustration
    decoder_inputs = np.random.rand(1, max_decoder_length, 80)  # Dummy decoder inputs
    audio_features = model.predict([input_data, decoder_inputs])

    # Convert features back to audio using Griffin-Lim
    waveform = griffin_lim(audio_features[0])

    return waveform