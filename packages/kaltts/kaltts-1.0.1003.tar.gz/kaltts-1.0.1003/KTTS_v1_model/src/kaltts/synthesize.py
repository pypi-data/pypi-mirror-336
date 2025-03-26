from gtts import gTTS
import io

def generate_speech(text):
    # Generate speech using gTTS
    tts = gTTS(text)
    audio_output = io.BytesIO()
    tts.write_to_fp(audio_output)
    audio_output.seek(0)
    return audio_output
