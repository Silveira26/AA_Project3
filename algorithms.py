import random
import time

class FixedProbabilityCounter:
    def __init__(self):
        pass

    def estimate_counts(self, text, exact_counts):
        start_time = time.time()
        estimated_counts = {}
        for letter in text:
            if letter.isalpha() and random.random() < 0.5:  # 50% probability
                letter = letter.upper()
                estimated_counts[letter] = estimated_counts.get(letter, 0) + 1

        errors = calculate_errors(exact_counts, estimated_counts)
        end_time = time.time()
        return estimated_counts, errors, end_time - start_time


class SpaceSavingCount:
    def __init__(self, k):
        self.k = k
        self.counts = {}

    def process(self, stream, exact_counts):
        start_time = time.time()
        for letter in stream:
            if letter.isalpha():
                letter = letter.upper()
                if letter in self.counts:
                    self.counts[letter] += 1
                elif len(self.counts) < self.k:
                    self.counts[letter] = 1
                else:
                    min_letter = min(self.counts, key=self.counts.get)
                    self.counts[letter] = self.counts.pop(min_letter) + 1

        errors = calculate_errors(exact_counts, self.counts)
        end_time = time.time()
        return self.counts, errors, end_time - start_time


def exact_letter_count(text):
    start_time = time.time()
    counts = {}
    for letter in text:
        if letter.isalpha():
            letter = letter.upper()
            counts[letter] = counts.get(letter, 0) + 1
    end_time = time.time()
    return counts, end_time - start_time

def calculate_errors(exact_counts, estimated_counts):
    absolute_errors = {}
    relative_errors = {}
    for letter in set(exact_counts) | set(estimated_counts):
        exact = exact_counts.get(letter, 0)
        estimated = estimated_counts.get(letter, 0)
        absolute_errors[letter] = abs(exact - estimated)
        if exact != 0:
            relative_error = (abs(exact - estimated) / exact) * 100
            relative_errors[letter] = f"{relative_error:.2f}%"
        else:
            relative_errors[letter] = '0.00%'
    return {'absolute': absolute_errors, 'relative': relative_errors}