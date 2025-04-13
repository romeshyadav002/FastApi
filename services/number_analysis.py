import numpy as np

def analyze_numbers(numbers: list[float]):
    arr = np.array(numbers)
    return {
        "sum": float(np.sum(arr)),
        "mean": float(np.mean(arr)),
        "std_dev": float(np.std(arr))
    }

