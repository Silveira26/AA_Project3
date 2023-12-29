class Results:
    def __init__(self, counts):
        self.counts = counts

    def mean(self, letter=None):
        if letter:
            return self.counts.get(letter, 0)
        return sum(self.counts.values()) / len(self.counts) if self.counts else 0

    def variance(self, letter=None):
        mean_value = self.mean(letter)
        if letter:
            return (self.counts.get(letter, 0) - mean_value) ** 2
        return sum((x - mean_value) ** 2 for x in self.counts.values()) / len(self.counts) if self.counts else 0

    def standard_deviation(self, letter=None):
        return self.variance(letter) ** 0.5

    def absolute_error(self, letter=None, exact_counts=None):
        if letter:
            return abs(self.counts.get(letter, 0) - exact_counts.get(letter, 0))
        return sum(abs(self.counts.get(k, 0) - exact_counts.get(k, 0)) for k in exact_counts) / len(exact_counts)

    def relative_error(self, letter=None, exact_counts=None):
        if letter:
            exact_count = exact_counts.get(letter, 0)
            return (abs(self.counts.get(letter, 0) - exact_count) / exact_count) if exact_count != 0 else None
        return sum(abs(self.counts.get(k, 0) - exact_counts.get(k, 0)) / exact_counts[k] for k in exact_counts if exact_counts[k] != 0) / len(exact_counts)

    def accuracy_ratio(self, letter=None, exact_counts=None):
        if letter:
            exact_count = exact_counts.get(letter, 0)
            return (self.counts.get(letter, 0) / exact_count) if exact_count != 0 else None
        return sum(self.counts.get(k, 0) / exact_counts[k] for k in exact_counts if exact_counts[k] != 0) / len(exact_counts)

    def smallest_counter_value(self):
        return min(self.counts.values()) if self.counts else 0

    def largest_counter_value(self):
        return max(self.counts.values()) if self.counts else 0
    
    def normalized_absolute_errors(self, exact_counts, letter=None):
        if letter:
            return abs(self.counts.get(letter, 0) - exact_counts.get(letter, 0))
        return {ltr: abs(self.counts.get(ltr, 0) - exact_counts.get(ltr, 0)) for ltr in exact_counts}

    def relative_errors(self, exact_counts, letter=None):
        if letter:
            return abs(self.counts.get(letter, 0) - exact_counts.get(letter, 0)) / exact_counts.get(letter, 1)
        total_error = sum(abs(self.counts.get(k, 0) - exact_counts.get(k, 0)) for k in exact_counts)
        total_exact_count = sum(exact_counts.values())
        return total_error / total_exact_count

    def error_statistics(self, letter=None, exact_counts=None):
        norm_abs_errors = self.normalized_absolute_errors(exact_counts, letter)
        rel_errors = self.relative_errors(exact_counts, letter)

        if letter:
            return {
                'Normalized Absolute Error': norm_abs_errors,
                'Relative Error': rel_errors
            }

        return {
            'Normalized Absolute Error Stats': {
                'Lowest': min(norm_abs_errors.values()),
                'Highest': max(norm_abs_errors.values()),
                'Average': sum(norm_abs_errors.values()) / len(norm_abs_errors)
            },
            'Relative Error Stat': rel_errors
        }

    def get_statistics(self, letter=None, exact_counts=None):
        stats = {
            'Mean': self.mean(letter),
            'Variance': self.variance(letter),
            'Standard Deviation': self.standard_deviation(letter),
            'Smallest Counter Value': self.smallest_counter_value(),
            'Largest Counter Value': self.largest_counter_value()
        }

        if exact_counts:
            stats.update({
                'Mean Absolute Error': self.absolute_error(letter, exact_counts),
                'Mean Relative Error': self.relative_error(letter, exact_counts),
                'Mean Accuracy Ratio': self.accuracy_ratio(letter, exact_counts),
                'Error Statistics': self.error_statistics(letter, exact_counts)
            })

        return stats
