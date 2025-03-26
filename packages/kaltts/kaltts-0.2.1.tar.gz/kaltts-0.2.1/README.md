# Kal Text-to-Speech (TTS) Synthesis

## 📦 Overview
Kal TTS is a Text-to-Speech synthesis model that converts text input into natural-sounding speech. This project utilizes deep learning techniques to generate audio from text, making it suitable for various applications such as virtual assistants, audiobooks, and more.

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Odeneho-Calculus/KTTS_v1_model
   cd KTTS_v1_model
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### Text-to-Speech Synthesis
```python
from src.synthesize import generate_speech

text = "Hello, this is a test of Kal TTS."
audio_output = generate_speech(text)
audio_output.save("output.wav")
```

### Training a New Model
```python
from src.train import train_tts_model

train_tts_model(
    data_path="data/processed/",
    config_path="config/config.yaml"
)
```

## 🧠 Workflow

1. **Text Normalization**: Standardize input text
2. **Phoneme Conversion**: Transform text to phonetic representation
3. **Feature Extraction**: Generate audio features
4. **Model Training**: Train TTS models using extracted features
5. **Speech Synthesis**: Generate audio from text input

## 📊 Performance Metrics

- Supported Languages: English (expandable)
- Sampling Rate: Configurable (default: 22050 Hz)
- Model Architectures: Neural TTS, Vocoder-based synthesis

## 📞 Contact

kalculusGuy - [calculus069@gmail.com](mailto:calculus069@gmail.com)

Project Link: [https://github.com/Odeneho-Calculus/KTTS_v1_model](https://github.com/Odeneho-Calculus/KTTS_v1_model)