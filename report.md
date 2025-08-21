# Python Multiprocessing & Advanced Algorithms — Report

## Overview

This project explores Python multiprocessing, CPU-bound optimization, and advanced data structures (heaps, tries, segment trees) and graph algorithms. It contains practical scripts, experimental comparisons (Pool.map vs Process+Queue), a min-heap scheduler, a segment tree implementation, and a Dijkstra-based CLI for shortest-path queries.

### Sources consulted
- Official Python docs: `multiprocessing`, `heapq`, `concurrent.futures`, `timeit`.
- `psutil` documentation for CPU usage sampling.
- Algorithm references: CLRS (for asymptotic analysis), competitive programming notes (segment trees, Dijkstra).
- Blog posts: "Why Python's GIL matters", "Multiprocessing vs Threading in Python".
- StackOverflow for code patterns and practical hints (e.g., Process/Queue sentinel patterns).

## Key Concepts & Learnings

### Multiprocessing (Process, Pool, Queue)
- `multiprocessing.Process`: gives fine-grained control over processes and IPC. Useful when tasks need dedicated process lifecycle control or complex inter-process messaging.
- `multiprocessing.Pool`: convenient for map-style parallelism; handles worker lifecycle/serialization, simpler code, lower boilerplate.
- `Queue`: common pattern for producer-consumer between processes; explicit queue gives more control (task prioritization, dynamic addition), but requires more boilerplate and careful sentinel handling.

### When CPU-bound beats Threading
- Python's GIL prevents multiple native Python bytecode executions in parallel within a single process; therefore **CPU-bound** tasks should use `multiprocessing` (or native extensions, `numpy` that release GIL, or C-extensions).
- **I/O-bound** tasks often benefit from `threading` or async I/O.
- `numpy` matrix multiplication is implemented in optimized C/Fortran and often releases the GIL; so `numpy` operations can scale differently.

### Heaps, Tries, Segment Trees
- `heapq` is a binary heap based priority queue (min-heap by default). Insert/pop operations both O(log n).
- Tries (prefix trees) provide O(length_of_key) lookup/insert; good for prefix queries and dictionaries with shared prefixes.
- Segment trees support range queries and point updates in O(log n) time and O(n) memory (often using 2n-size array).
- MST and Dijkstra covered: Dijkstra is O((V+E) log V) with a binary heap; BFS/DFS are O(V+E).

### Complexity analysis (examples)
- Heap operations: insert/pop — O(log n); peek — O(1); space — O(n).
- Segment tree: build — O(n); point update — O(log n); range query — O(log n); space — O(2n) (implementation detail).
- Dijkstra (binary heap): O((V+E) log V) time; with Fibonacci heap it's O(E + V log V) but not practical for Python.

## Implementation notes and trade-offs

### Matrix multiplier (Pool vs Process+Queue)
- `Pool.map` is concise and fits batch jobs well; overhead for pickling might be significant if tasks are many and small.
- `Process+Queue` provides better control (e.g., streaming tasks, dynamic load balancing) but costs more code and careful sentinels.
- When tasks are large (e.g., big matrix multiplies) the overhead of worker management is small compared to compute; Pool often suffices.
- For truly large-scale production: prefer optimized BLAS-backed `numpy` which parallelizes in C; then multiple Python processes may not help — profile and test.

### Min-Heap Scheduler
- Use `heapq` for priority scheduling. For tasks with same priority, include a counter to preserve insertion order.
- Complexity: insert O(log n), pop O(log n), peek O(1); space O(n).

### Segment Tree
- Used for range-sum and point updates; I used a power-of-two sized backing array to simplify index math and iterative update/query.

### Dijkstra CLI
- Implemented using adjacency lists and `heapq`.
- CSV parser reads edges `city1,city2,distance`.
- CLI wraps reading CSV, building graph, running Dijkstra, and printing path and distance.
- Visualization: simple node-coordinate layout plotted with `matplotlib`. For large graphs use `networkx` or dedicated visualization tools.

## Experiments

### Matrix experiments (scaled)
- Goal: measure execution time vs number of cores for both Pool.map and Process+Queue.
- Scaled experiment used here (to fit interactive environment): matrix size 160, repeats 30, workers 1..4. Produced speedup curve and CSV.
- Observations: For small matrices or small numbers of repetitions, overhead dominates and parallelism may not help. For larger matrices, you should see decreasing time (speedup) as processes are added up to the number of physical cores.

**How to run full experiment**: change `matrix_size`, `repeats`, and `max_workers` in the provided script and run on a machine with sufficient RAM/CPU. Consider generating matrices inside workers (streaming) to avoid memory blowup.

### Min-heap & Segment tree experiments
- Measured insertion/pop workload for 50k items — very quick in CPython; consistent with O(log n).
- Ran 5k randomized segment tree operations; recorded and plotted operation time statistics.

### Dijkstra demo
- Small graph example produced and visualized path.

## Files included
- `matrix_experiments.py` — Pool vs Process/Queue implementations + CPU sampling + plotting.
- `heap_scheduler.py` — min-heap scheduler demo and complexity notes.
- `segment_tree.py` — segment tree with test bench.
- `dijkstra_cli.py` — reads CSV, runs Dijkstra, prints path; includes a small plotting helper.

## Closing thoughts
- Always profile (time, memory, CPU) with representative workloads before committing to a design.
- Use optimized libraries (NumPy, BLAS) whenever possible for heavy numeric work — often faster and simpler than hand-parallelization in Python.
- For production distributed computing, consider job schedulers or frameworks (Dask, Ray) if you need fault tolerance and large-scale data handling.

