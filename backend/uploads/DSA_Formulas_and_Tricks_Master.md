# DSA Formulas, Patterns & Tricks Master Document
*Comprehensive High-Yield Cheatsheet for Technical Coding Interviews*

---

## 1. Time Complexity & Constraint Analysis Rules
Before writing any code, examine input constraint N:
- **N <= 10**: $O(N!)$ or $O(N^2 \cdot 2^N)$ [Permutations, Traveling Salesperson, Backtracking]
- **N <= 20**: $O(2^N)$ [Subsets, Combination Sum]
- **N <= 500**: $O(N^3)$ [Floyd-Warshall, 3D Dynamic Programming]
- **N <= 2,000**: $O(N^2)$ [Nested loops, 2D Grid DP]
- **N <= 100,000**: $O(N \log N)$ [Sorting, Heap, Binary Search over array]
- **N <= 1,000,000**: $O(N)$ [Two Pointers, Sliding Window, Monotonic Stack, Prefix Sum]
- **N <= 10^9 or 10^18**: $O(\log N)$ or $O(\sqrt{N})$ [Binary Search on Answer Space, Fast Exponentiation]

---

## 2. Bit Manipulation Magic & Invariants
- **Check Power of 2**: `(x > 0) && ((x & (x - 1)) == 0)`
- **Clear Lowest Set Bit**: `x = x & (x - 1)`
- **Isolate Lowest Set Bit**: `x & (-x)`
- **Check k-th bit**: `(x >> k) & 1`
- **Set k-th bit**: `x |= (1 << k)`
- **Clear k-th bit**: `x &= ~(1 << k)`
- **Toggle k-th bit**: `x ^= (1 << k)`
- **XOR Rule**: `x ^ x = 0`, `x ^ 0 = x`

---

## 3. Arrays & Hashing High-Yield Tricks
- **Prefix Sum Subarray Rule**: $Sum(i...j) = Prefix[j] - Prefix[i - 1]$. Maintain frequency map of prefix sums for target $K$.
- **Kadane's Algorithm**: `curr_max = max(arr[i], curr_max + arr[i])`
- **Boyer-Moore Voting**: Find majority element (> N/2) in $O(N)$ time, $O(1)$ space.
- **Dutch National Flag**: 3 pointers (`low`, `mid`, `high`) partition in-place.

---

## 4. Two Pointers & Sliding Window Framework
- **Opposite Pointers**: Sorted arrays, Two Sum II, 3Sum, Container with Most Water.
- **Fast & Slow**: Floyd's Cycle Detection. Meeting point + restart from head finds cycle entrance.
- **Sliding Window Template**:
  ```python
  left = 0
  for right in range(len(arr)):
      add_to_window(arr[right])
      while window_invalid():
          remove_from_window(arr[left])
          left += 1
      update_best(right - left + 1)
  ```

---

## 5. Binary Search Invariants & Patterns
- **Safe Mid**: `mid = low + (high - low) // 2`
- **Binary Search on Answer Space**:
  1. Identify monotonic bounds $[L, R]$.
  2. Write `is_possible(mid) -> bool`.
  3. Narrow search window based on feasibility test.

---

## 6. Monotonic Stack & Queue Rules
- **Next Greater Element**: Decreasing stack. Pop smaller elements when a larger element arrives.
- **Largest Rectangle in Histogram**: Compute width using indices from monotonic stack.

---

## 7. Trees & BSTs
- **Inorder Traversal of BST**: Always strictly ascending order.
- **Tree Diameter**: $\max(left\_depth + right\_depth)$ across all nodes.
- **LCA in BST**: First node where $p$ and $q$ split to different branches.

---

## 8. Graph Shortest Path & DSU
- **BFS**: Unweighted graph shortest path in $O(V + E)$.
- **Dijkstra**: Non-negative weights with Min-Heap in $O((V + E) \log V)$.
- **Kahn's Topological Sort**: Process vertices with in-degree 0 in a Queue.
- **DSU Path Compression**: `find(i): parent[i] = find(parent[i])`

---

## 9. Dynamic Programming Archetypes
- **0/1 Knapsack**: `dp[w] = max(dp[w], val + dp[w - wt])` iterating backwards in 1D array.
- **Unbounded Knapsack**: Coin Change, iterate forwards in 1D array.
- **LIS in $O(N \log N)$**: Patience Sorting with `bisect_left`.
- **LCS / Edit Distance**: 2D table tracking character matches.
