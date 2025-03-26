from src.tts_project.synthesize import generate_speech
from src.tts_project.train import train_model

def main():
    # Example usage of the TTS model
    text = "Hello, this is a test of the Kal TTS model."
    
    # Generate speech from text
    audio_output = generate_speech(text, config_path='config/config.yaml')
    audio_output.save("output.wav")

    # Train the model
    train_model(config_path='config/config.yaml')

if __name__ == "__main__":
    main()