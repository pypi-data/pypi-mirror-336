import numpy as np
from .model import create_tacotron2_model
from .vocoder import griffin_lim
import yaml
import os

def synthesize_speech(input_text, config_path=None):
    """
    Synthesize speech from input text using a Tacotron 2 model.

    Args:
        input_text (str): The text to convert to speech.
        config_path (str): Path to the configuration file. Defaults to internal config.

    Returns:
        waveform (np.ndarray): The synthesized audio waveform.
    """
    if config_path is None:
        # Use default configuration path
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'default_config.yaml')

    # Load configuration
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    vocab_size = config['vocab_size']
    embedding_dim = config['embedding_dim']
    lstm_units = config['lstm_units']

    # Load model
    model = create_tacotron2_model(vocab_size, embedding_dim, lstm_units)
    model.load_weights('tts_model.h5')

    # Dummy input for illustration
    input_data = np.random.randint(1, vocab_size, size=(1, 10))
    decoder_inputs = np.random.rand(1, 10, 80)
    audio_features = model.predict([input_data, decoder_inputs])

    # Convert features back to audio using Griffin-Lim
    waveform = griffin_lim(audio_features[0])

    return waveform
