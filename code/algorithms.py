import random
import time

class FixedProbabilityCounter:
    def __init__(self):
        pass

    def estimate_counts(self, text):
        start_time = time.time()
        estimated_counts = {}
        for letter in text:
            if letter.isalpha() and random.random() < 0.5:
                estimated_counts[letter] = estimated_counts.get(letter, 0) + 1

        for letter in estimated_counts:
            estimated_counts[letter] *= 1 / 0.5 

        end_time = time.time()
        return estimated_counts, end_time - start_time


class SpaceSavingCount:
    def __init__(self, k):
        self.k = k
        self.counts = {}

    def process(self, stream):
        start_time = time.time()
        for letter in stream:
            if letter.isalpha():
                if letter in self.counts:
                    self.counts[letter] += 1
                elif len(self.counts) < self.k:
                    self.counts[letter] = 1
                else:
                    min_letter = min(self.counts, key=self.counts.get)
                    self.counts[letter] = self.counts.pop(min_letter) + 1

        end_time = time.time()
        return self.counts, end_time - start_time


def exact_letter_count(text):
    start_time = time.time()
    counts = {}
    for letter in text:
        if letter.isalpha():
            counts[letter] = counts.get(letter, 0) + 1
    end_time = time.time()
    return counts, end_time - start_time