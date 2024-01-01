import json
import matplotlib.pyplot as plt
import numpy as np
import os
from collections import defaultdict

def load_results(filename, results_folder='../results'):
    with open(os.path.join(results_folder, filename), 'r', encoding='utf-8') as file:
        return json.load(file)

def plot_letter_frequency(counts, language, charts_folder='../charts'):
    letters, frequencies = zip(*sorted(counts.items()))
    plt.figure(figsize=(15, 8))
    plt.bar(letters, frequencies)
    plt.xlabel('Letter')
    plt.ylabel('Frequency')
    plt.title(f'Letter Frequency in {language}')
    plt.savefig(os.path.join(charts_folder, f'letter_frequency_{language}.png'))
    plt.close()

def plot_letter_frequency_all_languages(all_results, charts_folder='../charts'):
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

def plot_algorithm_execution_times(all_results, charts_folder='../charts'):
    languages = all_results.keys()
    algorithms = ['exact_counts', 'fixed_probability_avg', 'space_saving_k_3', 'space_saving_k_5', 'space_saving_k_10']
    execution_times = {alg: [] for alg in algorithms}

    for language in languages:
        for alg in algorithms:
            execution_times[alg].append(all_results[language].get(alg, {}).get('execution_time', 0))

    plt.figure(figsize=(15, 8))
    x = np.arange(len(languages))
    bar_width = 0.15

    for i, alg in enumerate(algorithms):
        plt.bar(x + i * bar_width, execution_times[alg], bar_width, label=alg.replace('_', ' ').title())

    plt.xlabel('Language')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Comparison of Algorithm Execution Times Across Languages')
    plt.xticks(x + bar_width * len(algorithms) / 2, languages)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(charts_folder, 'algorithm_execution_times.png'))
    plt.close()

def plot_error_statistics(result, language, charts_folder='../charts'):
    algorithms = ['fixed_probability_avg', 'space_saving_k_3', 'space_saving_k_5', 'space_saving_k_10']
    error_types = ['Normalized Absolute Error', 'Relative Error']  # Updated key names

    plt.figure(figsize=(15, 8))
    for error_type in error_types:
        error_values = []
        for alg in algorithms:
            error_stats = result[alg]['statistics_E']['Error Statistics']
            error_value = error_stats.get(error_type, 0)
            error_values.append(error_value)

        plt.plot(algorithms, error_values, marker='o', linestyle='-', label=error_type)

    plt.xlabel('Algorithm')
    plt.ylabel('Error Value')  # Changed from 'Error (%)' to 'Error Value'
    plt.title(f'Error Analysis for {language} (Letter E)')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(charts_folder, f'error_analysis_{language}.png'))
    plt.close()

def plot_execution_times(result, language, charts_folder='../charts'):
    algorithms = ['exact_counts', 'fixed_probability_avg', 'space_saving_k_3', 'space_saving_k_5', 'space_saving_k_10']
    execution_times = [result[alg]['execution_time'] for alg in algorithms]

    plt.figure(figsize=(15, 8))
    plt.bar(algorithms, execution_times)
    plt.xlabel('Algorithm')
    plt.ylabel('Execution Time (seconds)')
    plt.title(f'Execution Times for {language}')
    plt.grid(True)
    plt.savefig(os.path.join(charts_folder, f'execution_times_{language}.png'))
    plt.close()

def plot_mean_absolute_error(all_results, charts_folder='../charts'):
    algorithms = ['fixed_probability_avg', 'space_saving_k_3', 'space_saving_k_5', 'space_saving_k_10']
    plt.figure(figsize=(15, 8))

    for language, results in all_results.items():
        values = [results[alg]['statistics'].get('Mean Absolute Error', 0) for alg in algorithms]
        plt.plot(algorithms, values, marker='o', linestyle='-', label=language)

    plt.xlabel('Algorithm')
    plt.ylabel('Mean Absolute Error')
    plt.title('Mean Absolute Error Across Languages')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(charts_folder, 'mean_absolute_error_across_languages.png'))
    plt.close()

def plot_mean_relative_error(all_results, charts_folder='../charts'):
    algorithms = ['fixed_probability_avg', 'space_saving_k_3', 'space_saving_k_5', 'space_saving_k_10']
    plt.figure(figsize=(15, 8))

    for language, results in all_results.items():
        values = [results[alg]['statistics'].get('Mean Relative Error', 0) for alg in algorithms]
        plt.plot(algorithms, values, marker='o', linestyle='-', label=language)

    plt.xlabel('Algorithm')
    plt.ylabel('Mean Relative Error')
    plt.title('Mean Relative Error Across Languages')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(charts_folder, 'mean_relative_error_across_languages.png'))
    plt.close()

def plot_mean_accuracy_ratio(all_results, charts_folder='../charts'):
    algorithms = ['fixed_probability_avg', 'space_saving_k_3', 'space_saving_k_5', 'space_saving_k_10']
    plt.figure(figsize=(15, 8))

    for language, results in all_results.items():
        values = [results[alg]['statistics'].get('Mean Accuracy Ratio', 0) for alg in algorithms]
        plt.plot(algorithms, values, marker='o', linestyle='-', label=language)

    plt.xlabel('Algorithm')
    plt.ylabel('Mean Accuracy Ratio')
    plt.title('Mean Accuracy Ratio Across Languages')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(charts_folder, 'mean_accuracy_ratio_across_languages.png'))
    plt.close()

def main():
    languages = ['English', 'Italian', 'German', 'French']
    file_names = [f'{lang}.json' for lang in languages]
    all_results = {lang: load_results(file_name) for lang, file_name in zip(languages, file_names)}

    os.makedirs('../charts', exist_ok=True)

    plot_letter_frequency_all_languages(all_results)
    plot_algorithm_execution_times(all_results)
    plot_mean_absolute_error(all_results)
    plot_mean_relative_error(all_results)
    plot_mean_accuracy_ratio(all_results)

    for language, results in all_results.items():
        plot_letter_frequency(results['exact_counts']['counts'], language)
        plot_error_statistics(results, language)
        plot_execution_times(results, language)

if __name__ == "__main__":
    main()
