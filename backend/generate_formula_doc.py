"""
Script to create the ultimate DSA Formulas & Tricks Master Document (.docx and .md).
"""
import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_dsa_formulas_doc():
    doc = Document()

    # Title
    title = doc.add_heading('DSA Formulas, Patterns & Tricks Master Document', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    p_sub = doc.add_paragraph('Comprehensive High-Yield Cheatsheet for Technical Coding Interviews')
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph('Upload this document to your Google Drive folder or share it with peers for fast revision.')
    doc.add_paragraph('—' * 40)

    # Section 1
    doc.add_heading('1. Time Complexity & Constraint Analysis Rules', level=1)
    doc.add_paragraph(
        'Before writing any code, examine input constraint N to deduce target time complexity:\n'
        '• N <= 10 -> O(N!) or O(N^2 * 2^N) [Permutations, Backtracking, Traveling Salesperson]\n'
        '• N <= 20 -> O(2^N) [Subsets, Exponential Backtracking]\n'
        '• N <= 500 -> O(N^3) [Floyd-Warshall, 3D Dynamic Programming, Matrix Chain]\n'
        '• N <= 2,000 -> O(N^2) [Nested loops, 2D Grid DP, Insertion/Selection Sort]\n'
        '• N <= 100,000 -> O(N log N) [Merge Sort, Heap, Binary Search over N elements, Balanced BST]\n'
        '• N <= 1,000,000 -> O(N) [Two Pointers, Sliding Window, Prefix Sum, Monotonic Stack, Hash Table]\n'
        '• N <= 10^9 or 10^18 -> O(log N) or O(sqrt(N)) [Binary Search on Answer, Prime Checking, Fast Exponentiation]'
    )

    # Section 2
    doc.add_heading('2. Bit Manipulation Magic & Invariants', level=1)
    doc.add_paragraph(
        'Essential Bitwise Identities:\n'
        '• Check if X is a Power of 2: (x > 0) and (x & (x - 1) == 0)\n'
        '• Clear the lowest set bit (rightmost 1): x = x & (x - 1) [Used in Brian Kernighan bit count]\n'
        '• Isolate the lowest set bit: lowest = x & (-x)\n'
        '• Multiply by 2^k: x << k | Divide by 2^k: x >> k\n'
        '• Check k-th bit (0-indexed): (x >> k) & 1\n'
        '• Set k-th bit: x |= (1 << k)\n'
        '• Clear k-th bit: x &= ~(1 << k)\n'
        '• Toggle k-th bit: x ^= (1 << k)\n'
        '• XOR Cancellation Invariant: x ^ x = 0, x ^ 0 = x (Key for Single Number problems)'
    )

    # Section 3
    doc.add_heading('3. Arrays & Hashing High-Yield Tricks', level=1)
    doc.add_paragraph(
        '• Prefix Sum Subarray Rule: Sum of subarray arr[i...j] = Prefix[j] - Prefix[i - 1].\n'
        '  To find number of subarrays with sum K: maintain HashMap of prefix sum frequencies.\n'
        '• Kadane\'s Algorithm (Max Subarray Sum):\n'
        '  current_max = max(arr[i], current_max + arr[i]); global_max = max(global_max, current_max)\n'
        '• Boyer-Moore Voting Algorithm (Majority Element > N/2):\n'
        '  Keep candidate and count. If count == 0, candidate = num. If num == candidate count++ else count--.\n'
        '• Dutch National Flag (3-way partition: 0s, 1s, 2s):\n'
        '  Three pointers (low, mid, high). Swap arr[low], arr[mid] if 0; swap arr[mid], arr[high] if 2.'
    )

    # Section 4
    doc.add_heading('4. Two Pointers & Sliding Window Framework', level=1)
    doc.add_paragraph(
        '• Opposite Direction (Sorted Arrays):\n'
        '  left = 0, right = n - 1. If sum < target: left++. If sum > target: right--.\n'
        '• Fast & Slow Pointers (Floyd\'s Cycle Finding):\n'
        '  slow moves 1 step, fast moves 2 steps. If they meet -> cycle exists.\n'
        '  Cycle entry node formula: Reset slow = head, keep fast at meeting point, move both 1 step until they collide.\n'
        '• Variable-Size Sliding Window (Longest/Shortest Subarray):\n'
        '  for right in range(n):\n'
        '      add arr[right] to window_state\n'
        '      while window_state violates condition:\n'
        '          remove arr[left] from window_state; left++\n'
        '      update_ans(right - left + 1)'
    )

    # Section 5
    doc.add_heading('5. Binary Search Invariants & Patterns', level=1)
    doc.add_paragraph(
        '• Safe Mid Calculation (Prevents 32-bit Integer Overflow):\n'
        '  mid = low + (high - low) // 2\n'
        '• Lower Bound (First index where arr[i] >= target):\n'
        '  while low <= high:\n'
        '      if arr[mid] >= target: ans = mid; high = mid - 1\n'
        '      else: low = mid + 1\n'
        '• Binary Search on Answer Space (Min/Max Optimization, e.g. Koko Eating Bananas):\n'
        '  1. Identify range: [min_feasible, max_feasible]\n'
        '  2. Define monotonic predicate function: is_valid(speed)\n'
        '  3. Binary search on speed: if is_valid(mid): ans = mid; high = mid - 1 else: low = mid + 1'
    )

    # Section 6
    doc.add_heading('6. Monotonic Stack & Queue Rules', level=1)
    doc.add_paragraph(
        '• Next Greater Element / Stock Span:\n'
        '  Maintain a monotonically decreasing stack of indices or values.\n'
        '  Whenever current element > stack.top(), pop and resolve the answer for stack.top().\n'
        '• Largest Rectangle in Histogram / Trapping Rain Water:\n'
        '  Push indices onto stack. Pop when current height is lower to compute width = (current_idx - stack.peek() - 1).'
    )

    # Section 7
    doc.add_heading('7. Trees & Binary Search Trees (BST)', level=1)
    doc.add_paragraph(
        '• Inorder of BST is ALWAYS strictly ascending.\n'
        '• Tree Height = 1 + max(height(left), height(right))\n'
        '• Tree Diameter = max(left_height + right_height) across all nodes\n'
        '• Lowest Common Ancestor (LCA) in BST:\n'
        '  If both p, q < root.val -> search root.left\n'
        '  If both p, q > root.val -> search root.right\n'
        '  Else -> root is the split point (LCA).'
    )

    # Section 8
    doc.add_heading('8. Graph Algorithms & Shortest Path Formulas', level=1)
    doc.add_paragraph(
        '• BFS: Queue-based. Guaranteed shortest path in unweighted graphs.\n'
        '• Dijkstra\'s Algorithm: Min-Priority Queue on distance. Time: O((V + E) log V). Does NOT work on negative edges.\n'
        '• Bellman-Ford: Relax all E edges V - 1 times. Detects negative weight cycles. Time: O(V * E).\n'
        '• Topological Sort (DAG only):\n'
        '  Kahn\'s Algorithm: Compute in-degree for all vertices. Push 0 in-degree vertices to Queue. Decrement neighbors.\n'
        '• Disjoint Set Union (DSU / Union-Find):\n'
        '  With Path Compression + Union by Rank, nearly O(1) amortized: find(i) = (parent[i] == i ? i : parent[i] = find(parent[i]))'
    )

    # Section 9
    doc.add_heading('9. Dynamic Programming Core Archetypes', level=1)
    doc.add_paragraph(
        '• 0/1 Knapsack (Each item chosen at most once):\n'
        '  dp[w] = max(dp[w], val[i] + dp[w - weight[i]]), iterate w backwards from Capacity down to weight[i].\n'
        '• Unbounded Knapsack (Coin Change, items can be reused):\n'
        '  dp[w] = min(dp[w], 1 + dp[w - coin]), iterate w forwards from coin to Capacity.\n'
        '• Longest Increasing Subsequence (LIS):\n'
        '  O(N log N) using patience sorting: for num in arr: idx = bisect_left(tails, num); tails[idx] = num.\n'
        '• Longest Common Subsequence (LCS):\n'
        '  if s1[i-1] == s2[j-1]: dp[i][j] = 1 + dp[i-1][j-1] else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n'
        '• Matrix / Grid Traversal:\n'
        '  dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])'
    )

    os.makedirs("uploads", exist_ok=True)
    docx_path = "uploads/DSA_Formulas_and_Tricks_Master.docx"
    doc.save(docx_path)
    print("Saved DOCX:", docx_path)

    # Also save Markdown version
    md_content = """# DSA Formulas, Patterns & Tricks Master Document
*Comprehensive High-Yield Cheatsheet for Technical Coding Interviews*

---

## 1. Time Complexity & Constraint Analysis Rules
Before writing any code, examine input constraint N:
- **N <= 10**: $O(N!)$ or $O(N^2 \\cdot 2^N)$ [Permutations, Traveling Salesperson, Backtracking]
- **N <= 20**: $O(2^N)$ [Subsets, Combination Sum]
- **N <= 500**: $O(N^3)$ [Floyd-Warshall, 3D Dynamic Programming]
- **N <= 2,000**: $O(N^2)$ [Nested loops, 2D Grid DP]
- **N <= 100,000**: $O(N \\log N)$ [Sorting, Heap, Binary Search over array]
- **N <= 1,000,000**: $O(N)$ [Two Pointers, Sliding Window, Monotonic Stack, Prefix Sum]
- **N <= 10^9 or 10^18**: $O(\\log N)$ or $O(\\sqrt{N})$ [Binary Search on Answer Space, Fast Exponentiation]

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
- **Tree Diameter**: $\\max(left\\_depth + right\\_depth)$ across all nodes.
- **LCA in BST**: First node where $p$ and $q$ split to different branches.

---

## 8. Graph Shortest Path & DSU
- **BFS**: Unweighted graph shortest path in $O(V + E)$.
- **Dijkstra**: Non-negative weights with Min-Heap in $O((V + E) \\log V)$.
- **Kahn's Topological Sort**: Process vertices with in-degree 0 in a Queue.
- **DSU Path Compression**: `find(i): parent[i] = find(parent[i])`

---

## 9. Dynamic Programming Archetypes
- **0/1 Knapsack**: `dp[w] = max(dp[w], val + dp[w - wt])` iterating backwards in 1D array.
- **Unbounded Knapsack**: Coin Change, iterate forwards in 1D array.
- **LIS in $O(N \\log N)$**: Patience Sorting with `bisect_left`.
- **LCS / Edit Distance**: 2D table tracking character matches.
"""
    with open("uploads/DSA_Formulas_and_Tricks_Master.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    print("Saved MD: uploads/DSA_Formulas_and_Tricks_Master.md")

if __name__ == "__main__":
    create_dsa_formulas_doc()
