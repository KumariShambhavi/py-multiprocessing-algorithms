"""
Matrix multiplier using multiprocessing.Process + Queue
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

def worker(task_queue: mp.Queue, result_queue: mp.Queue):
    while True:
        seed = task_queue.get()
        if seed is None:
            break
        np.random.seed(seed)
        A = np.random.rand(MATRIX_SIZE, MATRIX_SIZE)
        B = np.random.rand(MATRIX_SIZE, MATRIX_SIZE)
        C = A @ B
        result_queue.put(float(np.sum(C)))

def run_experiment():
    cores = list(range(1, mp.cpu_count() + 1))
    times = {}

    for c in cores:
        task_queue = mp.Queue()
        result_queue = mp.Queue()
        processes = [mp.Process(target=worker, args=(task_queue, result_queue)) for _ in range(c)]

        for p in processes:
            p.start()

        start = time.perf_counter()
        for i in range(REPEATS):
            task_queue.put(i)

        for _ in processes:
            task_queue.put(None)

        results = [result_queue.get() for _ in range(REPEATS)]
        elapsed = time.perf_counter() - start
        times[c] = elapsed

        print(f"{c} cores: {elapsed:.2f}s (CPU util ~ {psutil.cpu_percent(interval=1)}%)")

        for p in processes:
            p.join()

    # Save results
    df = pd.DataFrame(list(times.items()), columns=["Cores", "Time"])
    df.to_csv(OUTPUT_DIR / "matrix_speedup_queue.csv", index=False)

    # Plot
    plt.plot(df["Cores"], df["Time"], marker="o", color="orange")
    plt.xlabel("CPU Cores")
    plt.ylabel("Execution Time (s)")
    plt.title("Matrix Multiplication Speedup (Process + Queue)")
    plt.grid(True)
    plt.savefig(OUTPUT_DIR / "matrix_speedup_queue.png")
    print("Results saved in 'results/'")

if __name__ == "__main__":
    run_experiment()
