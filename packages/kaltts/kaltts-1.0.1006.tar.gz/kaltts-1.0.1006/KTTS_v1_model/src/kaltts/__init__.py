from .synthesize import generate_speech
from .train import train_model
from .data_processing import normalize_text, text_to_phonemes, extract_audio_features
from .model import create_tacotron2_model
from .vocoder import griffin_lim