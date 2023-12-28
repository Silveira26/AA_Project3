import json
import matplotlib.pyplot as plt
import numpy as np
import os
from collections import defaultdict

def load_results(filename, results_folder='results'):
    with open(os.path.join(results_folder, filename), 'r', encoding='utf-8') as file:
        return json.load(file)

def plot_letter_frequency(exact_counts, language, charts_folder='charts'):
    letters, counts = zip(*sorted(exact_counts.items()))
    plt.figure(figsize=(15, 8))
    plt.bar(letters, counts)
    plt.xlabel('Letter')
    plt.ylabel('Frequency')
    plt.title(f'Letter Frequency in {language}')
    plt.savefig(os.path.join(charts_folder, f'letter_frequency_{language}.png'))
    plt.close()

def plot_letter_frequency_all_languages(all_results, charts_folder='charts'):
    plt.figure(figsize=(15, 8))

    all_letters = set()
    for results in all_results.values():
        all_letters.update(results['exact_counts']['counts'].keys())

    sorted_letters = sorted(all_letters)

    for language, results in all_results.items():
        counts = results['exact_counts']['counts']
        frequencies = [counts.get(letter, 0) for letter in sorted_letters]
        plt.plot(sorted_letters, frequencies, marker='o', linestyle='-', label=language)

    # Identify the top 4 most frequent letters across all languages
    overall_counts = defaultdict(int)
    for results in all_results.values():
        for letter, count in results['exact_counts']['counts'].items():
            overall_counts[letter] += count

    top_4_letters = sorted(overall_counts, key=overall_counts.get, reverse=True)[:4]

    # Annotate the top 4 letters on the plot
    for letter in top_4_letters:
        max_count = max([results['exact_counts']['counts'].get(letter, 0) for results in all_results.values()])
        plt.annotate(f'Top: {letter}', (letter, max_count), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9, color='red')

    plt.xlabel('Letter')
    plt.ylabel('Frequency')
    plt.title('Letter Frequency Comparison Across Languages')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(charts_folder, 'letter_frequency_all_languages.png'))
    plt.close()

def plot_error_analysis(results, language, k_values, charts_folder='charts'):
    # Gather all letters from the relative errors for all k_values
    letters = set()
    for k in k_values:
        letters.update(results[f'space_saving_k_{k}']['errors']['relative'].keys())
    
    # Sort the letters
    sorted_letters = sorted(letters)

    plt.figure(figsize=(15, 8))
    for k in k_values:
        key = f'space_saving_k_{k}'
        # Sort the errors according to the sorted letters
        errors = [float(results[key]['errors']['relative'].get(letter, '0').rstrip('%')) for letter in sorted_letters]
        plt.plot(sorted_letters, errors, marker='o', linestyle='-', label=f'k={k}')
    
    plt.xlabel('Letter')
    plt.ylabel('Relative Error (%)')
    plt.title(f'Error Analysis for {language} (Space Saving Algorithm)')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(charts_folder, f'error_analysis_{language}_k_values.png'))
    plt.close()

def plot_absolute_error_analysis(results, language, k_values, charts_folder='charts'):
    # Gather all letters from the absolute errors for all k_values
    letters = set()
    for k in k_values:
        letters.update(results[f'space_saving_k_{k}']['errors']['absolute'].keys())

    # Sort the letters
    sorted_letters = sorted(letters)

    plt.figure(figsize=(15, 8))
    for k in k_values:
        key = f'space_saving_k_{k}'
        # Sort the errors according to the sorted letters
        errors = [results[key]['errors']['absolute'].get(letter, 0) for letter in sorted_letters]
        plt.plot(sorted_letters, errors, marker='o', linestyle='-', label=f'k={k}')

    plt.xlabel('Letter')
    plt.ylabel('Absolute Error')
    plt.title(f'Absolute Error Analysis for {language} (Space Saving Algorithm)')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(charts_folder, f'absolute_error_analysis_{language}_k_values.png'))
    plt.close()

def plot_execution_times_comparison(all_results, charts_folder='charts'):
    languages = all_results.keys()
    algorithms = ['exact_counts', 'fixed_probability', 'space_saving_k_3', 'space_saving_k_5', 'space_saving_k_10']
    execution_times = defaultdict(list)

    for algorithm in algorithms:
        for language in languages:
            execution_times[algorithm].append(all_results[language][algorithm]['execution_time'])

    plt.figure(figsize=(15, 8))
    x = range(len(languages))
    for algorithm, times in execution_times.items():
        plt.plot(x, times, marker='o', linestyle='-', label=algorithm)
    plt.xticks(x, languages)
    plt.xlabel('Language')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Execution Times Comparison Across Algorithms and Languages')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(charts_folder, 'execution_times_comparison.png'))
    plt.close()

def identify_top_letters(all_results, num_letters=3):
    letter_counts = {}
    for lang, results in all_results.items():
        for letter, count in results['exact_counts']['counts'].items():
            if letter.isalpha():  # Filter out non-alphabetic characters
                letter_counts[letter] = letter_counts.get(letter, 0) + count
    top_letters = sorted(letter_counts, key=letter_counts.get, reverse=True)[:num_letters]
    return top_letters

def plot_relative_error_comparison(all_results, charts_folder='charts'):
    top_letters = identify_top_letters(all_results)
    languages = all_results.keys()

    plt.figure(figsize=(15, 8))
    bar_width = 0.15
    x = np.arange(len(languages))

    for i, letter in enumerate(top_letters):
        errors = [float(all_results[lang]['fixed_probability']['errors']['relative'].get(letter, '0').rstrip('%')) 
                  for lang in languages]
        plt.bar(x + i * bar_width, errors, width=bar_width, label=f'Letter {letter}')

    plt.xlabel('Language')
    plt.ylabel('Relative Error (%)')
    plt.title('Relative Error Comparison for Top 3 Letters Across Languages')
    plt.xticks(x + bar_width, languages)
    plt.legend()
    plt.savefig(os.path.join(charts_folder, 'relative_error_top_letters_comparison.png'))
    plt.close()

def plot_most_frequent_letters_comparison(all_results, k, charts_folder='charts'):
    languages = all_results.keys()
    top_letters = {}

    for lang in languages:
        key = f'space_saving_k_{k}'
        letters, counts = zip(*sorted(all_results[lang][key]['estimated_counts'].items(), key=lambda x: x[1], reverse=True)[:5])
        top_letters[lang] = counts

    plt.figure(figsize=(15, 8))
    x = np.arange(len(languages))
    bar_width = 0.15

    for i, letter in enumerate(letters):
        plt.bar(x + i * bar_width, [top_letters[lang][i] for lang in languages], width=bar_width, label=f'Letter {letter}')

    plt.xlabel('Language')
    plt.ylabel('Estimated Count')
    plt.title(f'Top 5 Most Frequent Letters Comparison Across Languages (k={k})')
    plt.xticks(x + bar_width, languages)
    plt.legend()
    plt.savefig(os.path.join(charts_folder, f'most_frequent_letters_k_{k}_comparison.png'))
    plt.close()

def plot_counts_comparison(exact_counts, approximate_counts, language, k_values, charts_folder='charts'):
    letters = sorted(exact_counts.keys())
    exact_values = [exact_counts[letter] for letter in letters]
    approx_values = defaultdict(list)

    # Gather approximate counts from Fixed Probability Counter and Space Saving for each k
    for k in k_values:
        for letter in letters:
            approx_values[k].append(approximate_counts[f'space_saving_k_{k}']['estimated_counts'].get(letter, 0))

    bar_width = 0.15
    index = np.arange(len(letters))

    plt.figure(figsize=(15, 8))
    plt.bar(index, exact_values, bar_width, label='Exact Counts')

    for i, k in enumerate(k_values, start=1):
        plt.bar(index + i * bar_width, approx_values[k], bar_width, label=f'Approximate Counts (k={k})')

    plt.xlabel('Letter')
    plt.ylabel('Count')
    plt.title(f'Counts Comparison in {language}')
    plt.xticks(index + bar_width, letters)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(charts_folder, f'counts_comparison_{language}.png'))
    plt.close()

# Main function to generate all charts
def main():
    languages = ['English', 'Italian', 'German', 'French']
    k_values = [3, 5, 10]
    file_names = [f'{lang}.json' for lang in languages]
    all_results = {lang: load_results(file_name) for lang, file_name in zip(languages, file_names)}

    # Ensure charts folder exists
    os.makedirs('charts', exist_ok=True)

    plot_letter_frequency_all_languages(all_results)

    # Create charts for each language
    for language, results in all_results.items():
        plot_letter_frequency(results['exact_counts']['counts'], language)
        plot_error_analysis(results, language, k_values)
        plot_absolute_error_analysis(results, language, k_values)
        plot_counts_comparison(results['exact_counts']['counts'], results, language, k_values)
    
    # Create a combined chart for execution times
    plot_execution_times_comparison(all_results)

    # Plot relative error comparison across languages for top letters
    plot_relative_error_comparison(all_results)

    # Plot most frequent letters comparison across languages for each k
    for k in k_values:
        plot_most_frequent_letters_comparison(all_results, k)

if __name__ == "__main__":
    main()