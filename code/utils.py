import os
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def generate_gutenberg_markers(file_name):
    base_name = os.path.basename(file_name).split('.')[0] # Get the base name without extension
    title = base_name.replace('_', ' ').upper() # Replace underscores with spaces and convert to uppercase
    start_marker = f"*** START OF THE PROJECT GUTENBERG EBOOK {title} ***"
    end_marker = f"*** END OF THE PROJECT GUTENBERG EBOOK {title} ***"
    return start_marker, end_marker

def correct_text_file(language, input_file, output_file):
    # Initialize stop words
    stop_words = set(stopwords.words(language))

    # Check if the output directory exists, create it if not
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, "r", encoding="utf-8") as file1:
        content = file1.read()

        # Generate Project Gutenberg markers
        start_marker, end_marker = generate_gutenberg_markers(input_file)

        # Remove Project Gutenberg header and footer
        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker, start_idx)

        if start_idx != -1 and end_idx != -1:
            content = content[start_idx + len(start_marker):end_idx]
        elif start_idx != -1:
            content = content[start_idx + len(start_marker):]
        elif end_idx != -1:
            content = content[:end_idx]

        words = word_tokenize(content)

        with open(output_file, 'w', encoding="utf-8") as appendFile:
            for word in words:
                # Check if the word is not a stop word and not a punctuation
                if word.lower() not in stop_words and word not in string.punctuation:
                    # Convert to uppercase and write to the file
                    appendFile.write(word.upper() + " ")

def main():
    correct_text_file('english', 'original_texts/Around the World in Eighty Days.txt', 'corrected_texts/Around the World in Eighty Days.txt')

    correct_text_file('italian', 'original_texts/Il giro del mondo in ottanta giorni.txt', 'corrected_texts/Il giro del mondo in ottanta giorni.txt')

    correct_text_file('german', 'original_texts/De reis om de wereld in tachtig dagen.txt', 'corrected_texts/De reis om de wereld in tachtig dagen.txt')

    correct_text_file('french', 'original_texts/Le tour du monde en quatre-vingts jours.txt', 'corrected_texts/Le tour du monde en quatre-vingts jours.txt')

if __name__ == "__main__":
    main()
