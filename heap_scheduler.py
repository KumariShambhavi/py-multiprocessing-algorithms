#!/usr/bin/env python3
"""
heap_scheduler.py

Simple min-heap scheduler using heapq. Keeps a counter to preserve insertion order
for equal-priority tasks.
"""

import heapq
from typing import Any, List, Tuple

class MinHeapScheduler:
    def __init__(self):
        self._heap: List[Tuple[int,int,str,Any]] = []
        self._counter = 0
    def add_task(self, priority: int, task_id: str, payload: Any=None) -> None:
        heapq.heappush(self._heap, (priority, self._counter, task_id, payload))
        self._counter += 1
    def pop_task(self):
        if not self._heap:
            return None
        priority, _, task_id, payload = heapq.heappop(self._heap)
        return priority, task_id, payload
    def __len__(self):
        return len(self._heap)

# Example usage:
if __name__ == "__main__":
    sched = MinHeapScheduler()
    tasks = [(5, "t1"), (1, "t2"), (5, "t3"), (2, "t4")]
    for p,t in tasks:
        sched.add_task(p, t)
    while len(sched):
        print(sched.pop_task())
