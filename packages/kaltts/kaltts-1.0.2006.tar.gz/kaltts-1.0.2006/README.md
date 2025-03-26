# KalTTS

KalTTS is a text-to-speech module that converts text into speech audio.

## Installation

You can install the package using pip:

```sh
pip install kaltts
```

## Usage

Here is an example of how to use the KalTTS module:

```python
from kaltts import generate_speech
from pydub import AudioSegment
from pydub.playback import play
import io

def main():
    text = 'Hello, this is a test of Kal TTS.'
    audio_output = generate_speech(text)

    with open('output.mp3', 'wb') as f:
        f.write(audio_output.getbuffer())

    audio_segment = AudioSegment.from_file('output.mp3', format='mp3')
    audio_segment.export('output.wav', format='wav')

    print('Audio saved as output.wav')
    play(audio_segment)

if __name__ == "__main__":
    main()
```