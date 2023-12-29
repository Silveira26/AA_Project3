import io
import os
import string
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def generate_gutenberg_markers(file_name):
    """
    Generate Project Gutenberg start and end markers based on the file name.
    :param file_name: The name of the file
    :return: A tuple containing the start and end markers
    """
    base_name = os.path.basename(file_name).split('.')[0] # Get the base name without extension
    title = base_name.replace('_', ' ').upper() # Replace underscores with spaces and convert to uppercase
    start_marker = f"*** START OF THE PROJECT GUTENBERG EBOOK {title} ***"
    end_marker = f"*** END OF THE PROJECT GUTENBERG EBOOK {title} ***"
    return start_marker, end_marker

def correct_text_file(language, input_file, output_file):
    """
    This function corrects a text file by removing Project Gutenberg headers,
    stop words, punctuation, and converting all words to uppercase.
    :param language: The language of the text file
    :param input_file: The input file name
    :param output_file: The output file name
    :return: None
    """
    # Initialize stop words
    stop_words = set(stopwords.words(language))

    # Check if the output directory exists, create it if not
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the input file
    with open(input_file, "r", encoding="utf-8") as file1:
        # Read the file content
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

        # Tokenize the text
        words = word_tokenize(content)

        # Open the output file
        with open(output_file, 'w', encoding="utf-8") as appendFile:
            # Process each word
            for word in words:
                # Check if the word is not a stop word and not a punctuation
                if word.lower() not in stop_words and word not in string.punctuation:
                    # Convert to uppercase and write to the file
                    appendFile.write(word.upper() + " ")

def main():
    # Process English
    correct_text_file('english', 'original_texts/Around the World in Eighty Days.txt', 'corrected_texts/Around the World in Eighty Days.txt')

    # Process Italian
    correct_text_file('italian', 'original_texts/Il giro del mondo in ottanta giorni.txt', 'corrected_texts/Il giro del mondo in ottanta giorni.txt')

    # Process German
    correct_text_file('german', 'original_texts/De reis om de wereld in tachtig dagen.txt', 'corrected_texts/De reis om de wereld in tachtig dagen.txt')

    # Process French
    correct_text_file('french', 'original_texts/Le tour du monde en quatre-vingts jours.txt', 'corrected_texts/Le tour du monde en quatre-vingts jours.txt')

if __name__ == "__main__":
    main()
