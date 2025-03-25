import numpy as np


class DataProcessor:
    def __init__(self, data):
        self.data = data

    def calculate_stats(self, column):
        values = self.data[column]
        return {
            "mean": np.mean(values),
            "median": np.median(values),
            "std": np.std(values),
        }
