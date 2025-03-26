import os
import numpy as np
from src.data_processing import normalize_text, text_to_phonemes, extract_audio_features

# Custom dictionary for common words in your domain
CUSTOM_DICT = {
    "ananse": "AH0 N AE1 N S EH0",
    "dimnyimlira": "D IH0 M N Y IH1 M L IH0 R AH0",
    "dosey": "D OW1 S EY0", 
    "flatters": "F L AE1 T ER0 Z",
    "ananses": "AH0 N AE1 N S EH0 Z",
    "egoistic": "EH2 G OW0 IH1 S T IH0 K",
    "dispossession": "D IH2 S P AH0 Z EH1 SH AH0 N",
    "sensitizing": "S EH1 N S IH0 T AY2 Z IH0 NG"
}

def main():
    while True:
        print("\n--- TTS Data Preprocessing Menu ---")
        print("1. Normalize Text")
        print("2. Convert Text to Phonemes")
        print("3. Extract Audio Features")
        print("4. Add to Custom Dictionary")
        print("5. Exit")
        choice = input("Select an option: ")
        if choice == '1':
            normalize_text_menu()
        elif choice == '2':
            text_to_phonemes_menu()
        elif choice == '3':
            extract_audio_features_menu()
        elif choice == '4':
            add_to_custom_dictionary()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

def normalize_text_menu():
    input_dir = 'data/raw_text/'
    output_dir = 'data/processed/normalized_text/'
    
    # Ensure directories exist
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # Check if input directory has files
    if not os.listdir(input_dir):
        print(f"No text files found in {input_dir}. Please add .txt files and try again.")
        return
    
    file_count = 0
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as file:
                text = file.read()
            normalized_text = normalize_text(text)
            output_filename = f'normalized_{filename}'
            with open(os.path.join(output_dir, output_filename), 'w', encoding='utf-8') as file:
                file.write(normalized_text)
            file_count += 1
    
    print(f"Text normalization complete. Processed {file_count} files.")

def text_to_phonemes_menu():
    input_dir = 'data/processed/normalized_text/'
    output_dir = 'data/processed/phonemes/'
    
    # Ensure directories exist
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # Check if input directory has files
    if not os.listdir(input_dir):
        print(f"No normalized text files found in {input_dir}. Run text normalization first.")
        return
    
    # Load custom dictionary from file if it exists
    if os.path.exists('custom_dict.txt'):
        try:
            with open('custom_dict.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split('  ', 1)
                        if len(parts) == 2:
                            word, phonemes = parts
                            CUSTOM_DICT[word] = phonemes
            print(f"Loaded {len(CUSTOM_DICT)} entries from custom dictionary.")
        except Exception as e:
            print(f"Error loading custom dictionary: {e}")
    
    file_count = 0
    unknown_words_total = set()
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as file:
                text = file.read()
            
            # Track unknown words for this file
            unknown_words_before = set()
            for word in text.lower().split():
                if word.isalpha() and word not in CUSTOM_DICT:
                    unknown_words_before.add(word)
            
            phonemes = text_to_phonemes(text, custom_dict=CUSTOM_DICT)
            
            output_filename = f'phonemes_{filename}'
            with open(os.path.join(output_dir, output_filename), 'w', encoding='utf-8') as file:
                file.write(phonemes)
            file_count += 1
            
            # Add to total unknown words
            unknown_words_total.update(unknown_words_before)
    
    print(f"Phoneme conversion complete. Processed {file_count} files.")
    if unknown_words_total:
        print(f"Used LTS model for {len(unknown_words_total)} unique unknown words.")
        print("Consider adding frequently used words to the custom dictionary.")

def extract_audio_features_menu():
    input_dir = 'data/audio/'
    output_dir = 'data/processed/audio_features/'
    
    # Ensure directories exist
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # Check if input directory has files
    if not os.listdir(input_dir):
        print(f"No audio files found in {input_dir}. Please add .wav files and try again.")
        return
    
    file_count = 0
    for filename in os.listdir(input_dir):
        if filename.endswith('.wav'):
            file_path = os.path.join(input_dir, filename)
            print(f"Processing {filename}...")
            try:
                features = extract_audio_features(file_path)
                output_filename = f'audio_features_{os.path.splitext(filename)[0]}.npy'
                np.save(os.path.join(output_dir, output_filename), features)
                file_count += 1
                print(f"  Feature shape: {features.shape}")
            except Exception as e:
                print(f"  Error processing {filename}: {e}")
    
    print(f"Audio feature extraction complete. Processed {file_count} files.")

def add_to_custom_dictionary():
    # Ensure the custom dictionary file exists
    if not os.path.exists('custom_dict.txt'):
        with open('custom_dict.txt', 'w', encoding='utf-8') as f:
            for word, pron in CUSTOM_DICT.items():
                f.write(f"{word}  {pron}\n")
    
    print("\n--- Custom Dictionary Management ---")
    print("1. Add a single word")
    print("2. Batch import from file")
    print("3. View current custom dictionary")
    print("4. Back to main menu")
    
    choice = input("Select an option: ")
    
    if choice == '1':
        word = input("Enter the word to add: ").lower()
        pronunciation = input("Enter the pronunciation (in CMU format, e.g., 'K AE1 T'): ")
        
        # Add to the runtime dictionary
        CUSTOM_DICT[word] = pronunciation
        
        # Save to the file
        with open('custom_dict.txt', 'a', encoding='utf-8') as f:
            f.write(f"{word}  {pronunciation}\n")
        
        print(f"Added '{word}' with pronunciation '{pronunciation}' to custom dictionary.")
    
    elif choice == '2':
        filename = input("Enter the path to the import file (format: word<tab>pronunciation): ")
        try:
            count = 0
            with open(filename, 'r', encoding='utf-8') as infile, open('custom_dict.txt', 'a', encoding='utf-8') as outfile:
                for line in infile:
                    if line.strip():
                        parts = line.strip().split('\t')
                        if len(parts) == 2:
                            word, pron = parts
                            word = word.lower()
                            CUSTOM_DICT[word] = pron
                            outfile.write(f"{word}  {pron}\n")
                            count += 1
            print(f"Imported {count} words to the custom dictionary.")
        except Exception as e:
            print(f"Error importing from file: {e}")
    
    elif choice == '3':
        print("\nCurrent Custom Dictionary:")
        print("--------------------------")
        for word, pron in sorted(CUSTOM_DICT.items()):
            print(f"{word}: {pron}")
        print(f"Total entries: {len(CUSTOM_DICT)}")
    
    elif choice == '4':
        return
    
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()