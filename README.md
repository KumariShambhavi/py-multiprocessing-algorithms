# PyParallel-Algorithms 🚀  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  
[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)  
[![Multiprocessing](https://img.shields.io/badge/Multiprocessing-Enabled-green.svg)]()  

## 📌 Overview
This repository contains an advanced **Python Multiprocessing and Algorithms Project**, exploring CPU-bound task optimization, multiprocessing vs. threading, and advanced data structures. It demonstrates how parallelism and efficient algorithms can drastically improve performance in real-world computational problems.

---

## 📂 Project Structure
├── matrix_pool.py # Matrix multiplier using Pool.map
├── matrix_process_queue.py # Matrix multiplier using Process + Queue
├── city_roads.csv # Sample dataset for Dijkstra’s shortest path
├── segment_tree.py # Segment tree (range-sum + point update)
├── heap_scheduler.py # Min-heap-based task scheduler
├── report.md # Detailed project documentation
├── README.md # This file
├── LICENSE # MIT License
└── results/ # Output plots (speedup curves, operation times, etc.)

yaml
Copy code

---

## ⚡ Implemented Tasks
1. **Matrix Multiplier**  
   - Parallelized 500×500 matrix multiplications using:
     - `multiprocessing.Pool.map`
     - `multiprocessing.Process + Queue`  
   - Benchmarked CPU utilization using **psutil**.  
   - Generated **speedup curves** across CPU cores.  

2. **Min-Heap Task Scheduler**  
   - Implemented using Python’s `heapq`.  
   - Prioritizes tasks by deadline/priority.  
   - Includes **time & space complexity analysis**.  

3. **Segment Tree**  
   - Supports **range-sum queries** and **point updates**.  
   - Tested with **10,000 random operations**.  
   - Visualized **operation times**.  

4. **Shortest Path CLI (Dijkstra’s Algorithm)**  
   - Reads from `city_roads.csv`.  
   - Computes shortest paths between cities.  
   - Visualizes the **shortest path graph**.  

---

## 📊 Results & Visuals
- ✅ **Speedup Curve (Matrix Multiplier)**  
- ✅ **Heap Scheduler Performance Graph**  
- ✅ **Segment Tree Operation Times**  
- ✅ **Shortest Path Visualization**  

*(All plots available in `/results` folder)*  

---

## 🛠️ Technologies Used
- **Python 3.12+**  
- **multiprocessing** (Pool, Process, Queue)  
- **heapq** (Min-Heap)  
- **Matplotlib / NetworkX** (Visualizations)  
- **psutil** (CPU Utilization Tracking)  

---

## 📈 Complexity Highlights
- **Heap Scheduler:**  
  - Insert → `O(log n)`  
  - Pop (next task) → `O(log n)`  
- **Segment Tree:**  
  - Range Query → `O(log n)`  
  - Update → `O(log n)`  
- **Dijkstra’s Algorithm:**  
  - With Min-Heap → `O((V + E) log V)`  

---

## 📜 License
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.  

---

## 🤝 Contributing
Contributions are welcome! Feel free to fork the repo, submit issues, or open PRs to improve the project.  

---

## 👩‍💻 Author
**Kumari Shambhavi**  

---
