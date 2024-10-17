# Task 1.1
# Multiple classes with inheritance
# The Sample class satisfies the conditions of the task

import math
import numpy as np


# Σ equivalent in Python
def sigma(end: int, func, start: int = 0):
    result = 0
    for i in range(start, end):
        result += func(i)

    return result


def choose(number_of_successes: int, number_of_rolls: int):
    numerator = math.factorial(number_of_rolls)
    denominator = (
        math.factorial(number_of_successes)
        * math.factorial(number_of_rolls - number_of_successes)
    )
    return numerator / denominator


def get_probability(
    num_of_possibilities_per_roll: int,
    num_of_successes: int,
    num_of_rolls: int
):
    possible_outcome_count = num_of_possibilities_per_roll**num_of_rolls
    return choose(num_of_successes, num_of_rolls) / possible_outcome_count


# Beasley-Springer / Moro Approximation formula
# I'm not looking at z score tables...
def get_z_score(percentage: float):
    p = ((1 - percentage) / 2) + percentage
    t = math.sqrt(-2 * math.log(1 - p))
    c = [2.515517, 0.802853, 0.010328]
    d = [1.432788, 0.189269, 0.001308]

    return t - (
        (c[0] + c[1]*t + c[2]*t**2)
        / (1 + d[0]*t + d[1]*t**2 + d[2]*t**3)
    )


class Dataset:
    def __init__(self, data: np.ndarray):
        assert isinstance(data, np.ndarray), (
            "Data must be a numpy array."
        )
        self.size = len(data)
        self.data = data

    # Σ / n
    def get_mean(self):
        result = sigma(
            self.size,
            lambda i: self.data[i]
        )
        return result / self.size

    def get_variance(self):
        result = sigma(
            self.size,
            lambda i, mean=self.get_mean(): (
                (self.data[i] - mean)**2
            )
        )

        return result / (self.size - 1)

    # Standard deviation is the root of the variance
    def get_standard_deviation(self):
        return math.sqrt(self.get_variance())

    def get_standard_error(self):
        return self.get_standard_deviation() / math.sqrt(self.size)


# Create new sample of dataset of x size, with random values
class Sample(Dataset):
    def __init__(self, parent_dataset: np.ndarray, sample_size: int):
        assert isinstance(parent_dataset, np.ndarray), (
            "parent_dataset must be of type \"np.ndarray\"."
        )
        assert len(parent_dataset.data) >= sample_size, (
            "New sample size must be <= full dataset size."
        )
        # Fetch random values
        data = parent_dataset.copy()
        np.random.shuffle(data)
        data = data[0:sample_size]

        super().__init__(data)
        self._parent_dataset = parent_dataset

    def get_confidence_interval(self, confidence_level: float):
        mean = self.get_mean()
        Z = get_z_score(confidence_level)
        standard_deviation = self.get_standard_deviation()
        root_of_n = math.sqrt(self.size)
        return {
            "lower bound": mean - Z * (standard_deviation / root_of_n),
            "upper bound": mean + Z * (standard_deviation / root_of_n)
        }

    def get_standard_error(self):
        return self.get_standard_deviation() / math.sqrt(self.size)


# Choose to create as many samples as you want from a dataset
# No duplicates
# Completely random sampling
class Samples:
    def __init__(
        self,
        parent_dataset: np.ndarray,
        sample_size: int,
        num_of_samples: int
    ):
        assert isinstance(parent_dataset, np.ndarray), (
            "parent_dataset must be of type \"np.ndarray\"."
        )
        assert len(parent_dataset.data) >= sample_size * num_of_samples, (
            "Sample size * num of samples must be <= than dataset's size."
        )
        self._parent_dataset = parent_dataset
        self.num_of_samples = num_of_samples
        self.sample_size = sample_size

        samples = np.empty(num_of_samples, dtype=object)

        data = parent_dataset.copy()
        np.random.shuffle(data)
        for i in range(0, num_of_samples):
            samples[i] = Sample(
                data[sample_size * i:sample_size * i + sample_size],
                sample_size
            )

        self.samples = samples

    def get_standard_error(self):
        mean_data = np.empty(self.num_of_samples, dtype=float)
        for i in range(0, self.num_of_samples):
            mean_data[i] = self.samples[i].get_mean()

        mean_data = Dataset(mean_data)

        return mean_data.get_standard_deviation()

    def get_confidence_interval(self, confidence_level: float):
        mean_of_means = sigma(
            self.num_of_samples,
            lambda i: self.samples[i].get_mean()
        )
        mean_of_means /= self.num_of_samples
        Z = get_z_score(confidence_level)
        standard_error = self.get_standard_error()

        return {
            "lower bound": mean_of_means - Z * standard_error,
            "upper bound": mean_of_means + Z * standard_error
        }
