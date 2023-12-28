from algorithms import FixedProbabilityCounter, SpaceSavingCount, exact_letter_count
import json

def process_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def main():
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
        results['exact_counts'] = {
            'counts': exact_counts,
            'execution_time': exact_time
        }

        # Fixed Probability Counter
        fpc = FixedProbabilityCounter()
        estimated_counts, errors, fpc_time = fpc.estimate_counts(text, exact_counts)
        results['fixed_probability'] = {
            'estimated_counts': estimated_counts,
            'errors': errors,
            'execution_time': fpc_time
        }

        # SpaceSavingCount for different k values
        for k in [3, 5, 10]:
            ssc = SpaceSavingCount(k)
            estimated_counts, errors, ssc_time = ssc.process(text, exact_counts)
            results[f'space_saving_k_{k}'] = {
                'estimated_counts': estimated_counts,
                'errors': errors,
                'execution_time': ssc_time
            }

        # Saving results to individual JSON files
        file_name = 'results/' + language + '.json'
        with open(file_name, 'w', encoding='utf-8') as results_file:
            json.dump(results, results_file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()