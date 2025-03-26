import re
from num2words import num2words
import librosa
import numpy as np
import os
import pickle
from collections import defaultdict

# Dictionary-based pronunciation
CMU_DICT_URL = "http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/cmudict-0.7b"

def normalize_text(text):
    # Convert text to lowercase
    text = text.lower()
    # Expand common abbreviations
    text = re.sub(r'\bdr\b', 'doctor', text)
    text = re.sub(r'\bmr\b', 'mister', text)
    text = re.sub(r'\bmrs\b', 'missus', text)
    text = re.sub(r'\bms\b', 'miss', text)
    # Convert numbers to words
    text = re.sub(r'\d+', lambda m: num2words(int(m.group())), text)
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    return text

def load_cmu_dict(dict_path=None):
    """Load the CMU Pronouncing Dictionary."""
    pronounce_dict = {}

    # If a dictionary file is provided, use it
    if dict_path and os.path.exists(dict_path):
        dict_file = dict_path
    else:
        # Otherwise, check if we've already downloaded it
        dict_file = "cmudict-0.7b"
        if not os.path.exists(dict_file):
            print("Downloading CMU Pronouncing Dictionary...")
            try:
                import urllib.request
                urllib.request.urlretrieve(CMU_DICT_URL, dict_file)
            except Exception as e:
                print(f"Failed to download dictionary: {e}")
                return {}

    try:
        with open(dict_file, 'r', encoding='latin-1') as f:
            for line in f:
                if line.startswith(';;;'):
                    continue
                if not line.strip():
                    continue

                parts = line.strip().split('  ')
                if len(parts) < 2:
                    continue

                word = parts[0].lower()
                # Remove the trailing numbers from words with multiple pronunciations
                if word[-1].isdigit() and word[-2] == '(':
                    word = word[:-3]

                pronounce = parts[1]
                pronounce_dict[word] = pronounce
    except Exception as e:
        print(f"Error loading dictionary: {e}")

    return pronounce_dict

class LetterToSoundModel:
    """Simple N-gram based Letter-to-Sound model."""

    def __init__(self, cmu_dict=None, n=4, model_path='lts_model.pkl'):
        self.n = n  # Context window size
        self.model_path = model_path
        self.grapheme_to_phoneme_map = defaultdict(list)

        # Try to load a pre-trained model
        if os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    self.grapheme_to_phoneme_map = pickle.load(f)
                print(f"Loaded LTS model from {model_path}")
                return
            except Exception as e:
                print(f"Error loading LTS model: {e}")

        # If we couldn't load a model and we have a dictionary, train a new model
        if cmu_dict:
            self.train(cmu_dict)

    def train(self, cmu_dict):
        """Train the LTS model from a pronunciation dictionary."""
        print("Training Letter-to-Sound model...")

        # Process each word in the dictionary
        for word, pronunciation in cmu_dict.items():
            # Skip words with non-alphabetic characters
            if not word.isalpha():
                continue

            # Prepare the word with padding
            padded_word = '_' * (self.n - 1) + word + '_' * (self.n - 1)

            # Extract n-gram features and map to phonemes
            for i in range(len(word)):
                # Get the context window
                context = padded_word[i:i+self.n*2-1]

                # Add the mapping from this context to the corresponding phoneme
                phoneme = pronunciation.split()[i] if i < len(pronunciation.split()) else '_'
                self.grapheme_to_phoneme_map[context].append(phoneme)

        # Save the model
        try:
            with open(self.model_path, 'wb') as f:
                pickle.dump(self.grapheme_to_phoneme_map, f)
            print(f"Saved LTS model to {self.model_path}")
        except Exception as e:
            print(f"Error saving LTS model: {e}")

    def predict(self, word):
        """Predict pronunciation for an unknown word."""
        if not word.isalpha():
            return " ".join([letter for letter in word])  # Simple fallback for non-alphabetic words

        # Prepare the word with padding
        padded_word = '_' * (self.n - 1) + word + '_' * (self.n - 1)

        # Generate phonemes for each letter
        phonemes = []
        for i in range(len(word)):
            context = padded_word[i:i+self.n*2-1]

            # Find the most frequent phoneme for this context
            if context in self.grapheme_to_phoneme_map:
                predictions = self.grapheme_to_phoneme_map[context]
                # Get the most common phoneme
                phoneme = max(set(predictions), key=predictions.count)
                phonemes.append(phoneme)
            else:
                # Fallback for unknown contexts
                if word[i] in 'aeiou':
                    phonemes.append(word[i].upper() + "H")  # Simple vowel with stress
                else:
                    phonemes.append(word[i].upper())  # Simple consonant

        return " ".join(phonemes)

def text_to_phonemes(text, dict_path=None, custom_dict=None):
    """Convert text to phonemes using CMU dictionary and LTS model for unknown words."""
    # Normalize the text first
    text = normalize_text(text)

    # Load the pronunciation dictionary
    cmu_dict = load_cmu_dict(dict_path)

    if not cmu_dict:
        return "Error: Could not load pronunciation dictionary"

    # Add custom dictionary entries if provided
    if custom_dict:
        cmu_dict.update(custom_dict)

    # Create or load the LTS model
    lts_model = LetterToSoundModel(cmu_dict)

    # Split text into words
    words = text.strip().split()

    # Convert each word to phonemes
    phonemes = []
    unknown_words = []

    for word in words:
        if word in cmu_dict:
            phonemes.append(cmu_dict[word])
        else:
            # Use the LTS model for unknown words
            predicted_phonemes = lts_model.predict(word)
            phonemes.append(predicted_phonemes)
            unknown_words.append(word)

    # Report unknown words
    if unknown_words:
        print(f"Used LTS model for {len(unknown_words)} words: {', '.join(unknown_words)}")

    # Join all phonemes
    result = " ".join(phonemes)

    return result

def extract_audio_features(file_path):
    # Load audio file
    y, sr = librosa.load(file_path)
    # Extract Mel-spectrogram
    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=80)
    # Convert to decibels
    log_mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)
    return log_mel_spectrogram
