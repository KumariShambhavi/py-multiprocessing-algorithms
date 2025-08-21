#!/usr/bin/env python3
"""
matrix_experiments.py

Run matrix multiplication experiments with two parallelization approaches:
  - multiprocessing.Pool.map
  - multiprocessing.Process + Queue

Adjust MATRIX_SIZE and REPEATS for your machine. For the full assignment set:
  MATRIX_SIZE = 500
  REPEATS = 500

Be mindful of memory: storing many matrices consumes RAM. Generate matrices on the fly
if necessary.

Requires: numpy, psutil, matplotlib, pandas
"""

from __future__ import annotations
import multiprocessing as mp
import numpy as np
import time
import psutil
import matplotlib.pyplot as plt
import csv
from typing import List, Tuple, Dict, Any
import argparse
import os

def matmul_pair(pair: Tuple[np.ndarray, np.ndarray]) -> np.ndarray:
    a, b = pair
    return a.dot(b)

def run_pool(matrix_size: int, repeats: int, workers: int) -> float:
    rng = np.random.default_rng(12345)
    # Option A: pre-generate (may use lots of memory)
    pairs = [(rng.standard_normal((matrix_size, matrix_size)),
              rng.standard_normal((matrix_size, matrix_size)))
             for _ in range(repeats)]
    start = time.perf_counter()
    with mp.Pool(processes=workers) as pool:
        _ = pool.map(matmul_pair, pairs)
    return time.perf_counter() - start

def process_worker(in_q: mp.Queue, out_q: mp.Queue) -> None:
    while True:
        item = in_q.get()
        if item is None:
            break
        idx, a, b = item
        out_q.put((idx, a.dot(b)))

def run_process_queue(matrix_size: int, repeats: int, workers: int) -> float:
    rng = np.random.default_rng(12345)
    matrices = [(rng.standard_normal((matrix_size, matrix_size)),
                 rng.standard_normal((matrix_size, matrix_size)))
                for _ in range(repeats)]
    in_q = mp.Queue()
    out_q = mp.Queue()
    procs = [mp.Process(target=process_worker, args=(in_q, out_q)) for _ in range(workers)]
    for p in procs:
        p.start()
    start = time.perf_counter()
    for i, (a,b) in enumerate(matrices):
        in_q.put((i,a,b))
    for _ in procs:
        in_q.put(None)  # sentinel
    collected = 0
    while collected < repeats:
        out_q.get()
        collected += 1
    elapsed = time.perf_counter() - start
    for p in procs:
        p.join()
    return elapsed

def sample_cpu_during(func, *args, sample_interval: float=0.05):
    """
    Run the function while sampling CPU percent using psutil.
    Returns (result, cpu_samples)
    """
    import threading
    samples = []
    done_flag = [False]
    def sampler():
        while not done_flag[0]:
            samples.append(psutil.cpu_percent(interval=sample_interval))
    t = threading.Thread(target=sampler)
    t.start()
    try:
        result = func(*args)
    finally:
        done_flag[0] = True
        t.join()
    return result, samples

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix-size", type=int, default=160)
    parser.add_argument("--repeats", type=int, default=30)
    parser.add_argument("--max-workers", type=int, default=min(mp.cpu_count(), 4))
    parser.add_argument("--out-dir", type=str, default="pm_results")
    args = parser.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    pool_results = {}
    proc_results = {}
    for w in range(1, args.max_workers+1):
        t_pool, cpu_pool = sample_cpu_during(run_pool, args.matrix_size, args.repeats, w)
        t_proc, cpu_proc = sample_cpu_during(run_process_queue, args.matrix_size, args.repeats, w)
        pool_results[w] = t_pool
        proc_results[w] = t_proc
        print(f"Workers={w}: pool={t_pool:.3f}s, proc_queue={t_proc:.3f}s")

    # Save CSV and plot
    import pandas as pd
    df = pd.DataFrame({
        "workers": list(pool_results.keys()),
        "pool_time_s": list(pool_results.values()),
        "proc_time_s": list(proc_results.values())
    })
    csv_path = os.path.join(args.out_dir, "matrix_speedup.csv")
    df.to_csv(csv_path, index=False)

    plt.figure()
    plt.plot(df["workers"], df["pool_time_s"], marker='o', label="Pool.map")
    plt.plot(df["workers"], df["proc_time_s"], marker='o', label="Process+Queue")
    plt.xlabel("Number of worker processes")
    plt.ylabel("Execution time (s)")
    plt.title(f"Matrix mult speedup (size={args.matrix_size}, repeats={args.repeats})")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(args.out_dir, "matrix_speedup.png"))
    print("Saved results to", args.out_dir)

if __name__ == "__main__":
    main()
