from .model import create_tacotron2_model
from .train import train_model
from .synthesize import synthesize_speech
from .controller import main
from .vocoder import griffin_lim

__version__ = "1.0.20010"
