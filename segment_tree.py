#!/usr/bin/env python3
"""
segment_tree.py

A classic iterative segment tree implementation supporting:
 - point_update(index, new_value)
 - range_sum(l, r)  # sum over [l, r) (r exclusive)
"""

from typing import List

class SegmentTree:
    def __init__(self, data: List[int]):
        n = len(data)
        self.n = 1
        while self.n < n:
            self.n <<= 1
        self.tree = [0] * (2*self.n)
        for i, val in enumerate(data):
            self.tree[self.n + i] = val
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2*i] + self.tree[2*i + 1]

    def point_update(self, idx: int, value: int) -> None:
        i = self.n + idx
        self.tree[i] = value
        i >>= 1
        while i:
            self.tree[i] = self.tree[2*i] + self.tree[2*i + 1]
            i >>= 1

    def range_sum(self, l: int, r: int) -> int:
        # [l, r)
        res = 0
        l += self.n; r += self.n
        while l < r:
            if l & 1:
                res += self.tree[l]
                l += 1
            if r & 1:
                r -= 1
                res += self.tree[r]
            l >>= 1; r >>= 1
        return res

# Quick test
if __name__ == "__main__":
    import random, time
    n = 5000
    data = [random.randint(0,1000) for _ in range(n)]
    st = SegmentTree(data)
    # random operations test
    for _ in range(1000):
        if random.random() < 0.5:
            idx = random.randrange(0, n)
            st.point_update(idx, random.randint(0,1000))
        else:
            l = random.randrange(0, n)
            r = random.randrange(l+1, min(n, l+100)+1)
            _ = st.range_sum(l, r)
    print("Basic randomized test completed.")
