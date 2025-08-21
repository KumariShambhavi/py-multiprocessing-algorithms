"""
Matrix multiplier using multiprocessing.Pool
Generates speedup curves across core counts
"""

import multiprocessing as mp
import numpy as np
import time
import pandas as pd
import matplotlib.pyplot as plt
import psutil
from pathlib import Path

MATRIX_SIZE = 160   # set to 500 for full experiment
REPEATS = 30        # set to 500 for full experiment
OUTPUT_DIR = Path("results")
OUTPUT_DIR.mkdir(exist_ok=True)

def multiply_matrices(seed: int) -> float:
    """Generate two random matrices and multiply them."""
    np.random.seed(seed)
    A = np.random.rand(MATRIX_SIZE, MATRIX_SIZE)
    B = np.random.rand(MATRIX_SIZE, MATRIX_SIZE)
    C = A @ B
    return float(np.sum(C))  # return dummy value to force computation

def run_experiment():
    cores = list(range(1, mp.cpu_count() + 1))
    times = {}

    for c in cores:
        with mp.Pool(processes=c) as pool:
            start = time.perf_counter()
            pool.map(multiply_matrices, range(REPEATS))
            elapsed = time.perf_counter() - start
            times[c] = elapsed
            print(f"{c} cores: {elapsed:.2f}s (CPU util ~ {psutil.cpu_percent(interval=1)}%)")

    # Save results
    df = pd.DataFrame(list(times.items()), columns=["Cores", "Time"])
    df.to_csv(OUTPUT_DIR / "matrix_speedup.csv", index=False)

    # Plot
    plt.plot(df["Cores"], df["Time"], marker="o")
    plt.xlabel("CPU Cores")
    plt.ylabel("Execution Time (s)")
    plt.title("Matrix Multiplication Speedup (Pool.map)")
    plt.grid(True)
    plt.savefig(OUTPUT_DIR / "matrix_speedup.png")
    print("Results saved in 'results/'")

if __name__ == "__main__":
    run_experiment()
