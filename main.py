from algorithms import FixedProbabilityCounter, SpaceSavingCount, exact_letter_count
from results import Results
import json

def process_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def main(stats_letter='E'):
    texts = {
        'English': 'corrected_texts/Around the World in Eighty Days.txt',
        'Italian': 'corrected_texts/Il giro del mondo in ottanta giorni.txt',
        'German': 'corrected_texts/De reis om de wereld in tachtig dagen.txt',
        'French': 'corrected_texts/Le tour du monde en quatre-vingts jours.txt'
    }

    for language, path in texts.items():
        results = {}
        text = process_text(path)
        
        # Exact counts
        exact_counts, exact_time = exact_letter_count(text)
        exact_results = Results(exact_counts)
        results['exact_counts'] = {
            'counts': exact_counts,
            'execution_time': exact_time,
            'statistics': exact_results.get_statistics(),
            f'statistics_{stats_letter}': exact_results.get_statistics(stats_letter)
        }

        # Fixed Probability Counter repeated 100 times
        fpc_total_counts = {}
        fpc_total_time = 0
        for _ in range(100):
            fpc = FixedProbabilityCounter()
            estimated_counts, fpc_time = fpc.estimate_counts(text)
            fpc_total_time += fpc_time
            for letter, count in estimated_counts.items():
                fpc_total_counts[letter] = fpc_total_counts.get(letter, 0) + count
        
        # Averaging the results over 100 runs
        for letter in fpc_total_counts:
            fpc_total_counts[letter] /= 100
        fpc_avg_time = fpc_total_time / 100
        fpc_results = Results(fpc_total_counts)
        results['fixed_probability_avg'] = {
            'estimated_counts': fpc_total_counts,
            'execution_time': fpc_avg_time,
            'statistics': fpc_results.get_statistics(None, exact_counts),
            f'statistics_{stats_letter}': fpc_results.get_statistics(stats_letter, exact_counts)
        }


        # SpaceSavingCount for different k values
        for k in [3, 5, 10]:
            ssc = SpaceSavingCount(k)
            estimated_counts, ssc_time = ssc.process(text)
            ssc_results = Results(estimated_counts)
            results[f'space_saving_k_{k}'] = {
                'estimated_counts': estimated_counts,
                'execution_time': ssc_time,
                'statistics': ssc_results.get_statistics(None, exact_counts),
                f'statistics_{stats_letter}': ssc_results.get_statistics(stats_letter, exact_counts)
            }

        # Saving results to individual JSON files
        file_name = 'results/' + language + '.json'
        with open(file_name, 'w', encoding='utf-8') as results_file:
            json.dump(results, results_file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()