import numpy as np
from .model import create_tacotron2_model
from .vocoder import griffin_lim
import yaml

def generate_speech(input_text, config_path='config/config.yaml'):
    # Load configuration
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    vocab_size = config['vocab_size']
    embedding_dim = config['embedding_dim']
    lstm_units = config['lstm_units']

    # Load model
    model = create_tacotron2_model(vocab_size, embedding_dim, lstm_units)
    model.load_weights('models/tts_model.h5')

    # Dummy input for illustration
    input_data = np.random.randint(1, vocab_size, size=(1, 10))
    decoder_inputs = np.random.rand(1, 10, 80)
    audio_features = model.predict([input_data, decoder_inputs])

    # Convert features back to audio using Griffin-Lim
    waveform = griffin_lim(audio_features[0])

    return waveform
