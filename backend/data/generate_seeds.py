"""
Data generator for 300+ curated DSA problems and 16 topic cheat sheets.
Generates backend/data/problems.json and backend/data/cheatsheets/*.json
"""
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CHEATSHEETS_DIR = os.path.join(DATA_DIR, "cheatsheets")
os.makedirs(CHEATSHEETS_DIR, exist_ok=True)

# 16 Topics in standard prerequisite order
TOPICS = [
    "Arrays & Strings",
    "Hashing",
    "Two Pointers",
    "Sliding Window",
    "Stack & Queue",
    "Linked List",
    "Binary Search",
    "Recursion & Backtracking",
    "Trees & BST",
    "Heaps & Priority Queue",
    "Greedy",
    "Intervals",
    "Graphs",
    "Dynamic Programming",
    "Tries",
    "Bit Manipulation & Math"
]

PROBLEMS_DATA = [
    # --- 1. Arrays & Strings ---
    {"number": 1, "title": "Two Sum", "difficulty": "Easy", "topic": "Arrays & Strings", "pattern": "Hash Map Lookup", "similar_to": "Complement Lookup"},
    {"number": 26, "title": "Remove Duplicates from Sorted Array", "difficulty": "Easy", "topic": "Arrays & Strings", "pattern": "Two Pointers / In-place", "similar_to": "In-place Array Partition"},
    {"number": 27, "title": "Remove Element", "difficulty": "Easy", "topic": "Arrays & Strings", "pattern": "Two Pointers", "similar_to": "In-place Deletion"},
    {"number": 31, "title": "Next Permutation", "difficulty": "Medium", "topic": "Arrays & Strings", "pattern": "Lexicographical Order", "similar_to": "Pivot and Suffix Reversal"},
    {"number": 48, "title": "Rotate Image", "difficulty": "Medium", "topic": "Arrays & Strings", "pattern": "Matrix Transposition", "similar_to": "Transpose and Reverse Columns"},
    {"number": 53, "title": "Maximum Subarray", "difficulty": "Medium", "topic": "Arrays & Strings", "pattern": "Kadane's Algorithm", "similar_to": "Greedy Running Sum"},
    {"number": 54, "title": "Spiral Matrix", "difficulty": "Medium", "topic": "Arrays & Strings", "pattern": "Matrix Traversal", "similar_to": "Layer-by-Layer Boundary Simulation"},
    {"number": 73, "title": "Set Matrix Zeroes", "difficulty": "Medium", "topic": "Arrays & Strings", "pattern": "In-place State Encoding", "similar_to": "First Row & Col As Markers"},
    {"number": 118, "title": "Pascal's Triangle", "difficulty": "Easy", "topic": "Arrays & Strings", "pattern": "Iterative Construction", "similar_to": "Combinatorial Table Generation"},
    {"number": 121, "title": "Best Time to Buy and Sell Stock", "difficulty": "Easy", "topic": "Arrays & Strings", "pattern": "Single Pass Tracking", "similar_to": "Prefix Minimum Tracking"},
    {"number": 122, "title": "Best Time to Buy and Sell Stock II", "difficulty": "Medium", "topic": "Arrays & Strings", "pattern": "Greedy Valley-Peak", "similar_to": "Accumulate Positive Deltas"},
    {"number": 169, "title": "Majority Element", "difficulty": "Easy", "topic": "Arrays & Strings", "pattern": "Boyer-Moore Voting", "similar_to": "Majority Vote Cancellation"},
    {"number": 189, "title": "Rotate Array", "difficulty": "Medium", "topic": "Arrays & Strings", "pattern": "Array Reversal", "similar_to": "Triple Reversal Algorithm"},
    {"number": 229, "title": "Majority Element II", "difficulty": "Medium", "topic": "Arrays & Strings", "pattern": "Boyer-Moore Voting (k=3)", "similar_to": "Dual Candidate Voting"},
    {"number": 238, "title": "Product of Array Except Self", "difficulty": "Medium", "topic": "Arrays & Strings", "pattern": "Prefix & Suffix Products", "similar_to": "Two-Pass Cumulative Product"},
    {"number": 283, "title": "Move Zeroes", "difficulty": "Easy", "topic": "Arrays & Strings", "pattern": "Two Pointers", "similar_to": "Snowball / Non-zero Compaction"},
    {"number": 334, "title": "Increasing Triplet Subsequence", "difficulty": "Medium", "topic": "Arrays & Strings", "pattern": "Greedy Min Tracking", "similar_to": "Two Smallest Values Tracker"},
    {"number": 448, "title": "Find All Numbers Disappeared in an Array", "difficulty": "Easy", "topic": "Arrays & Strings", "pattern": "Cyclic / Index Negation", "similar_to": "Array Values as Index Pointers"},
    {"number": 560, "title": "Subarray Sum Equals K", "difficulty": "Medium", "topic": "Arrays & Strings", "pattern": "Prefix Sum + Hash Map", "similar_to": "Two Sum on Prefix Sums"},
    {"number": 41, "title": "First Missing Positive", "difficulty": "Hard", "topic": "Arrays & Strings", "pattern": "Cyclic Sort", "similar_to": "Index as Value Hash Table"},

    # --- 2. Hashing ---
    {"number": 49, "title": "Group Anagrams", "difficulty": "Medium", "topic": "Hashing", "pattern": "Canonical String Key", "similar_to": "Sorted Character Signature"},
    {"number": 128, "title": "Longest Consecutive Sequence", "difficulty": "Medium", "topic": "Hashing", "pattern": "HashSet Exploration", "similar_to": "Sequence Boundary Detection (num-1)"},
    {"number": 205, "title": "Isomorphic Strings", "difficulty": "Easy", "topic": "Hashing", "pattern": "Bijective Mapping", "similar_to": "Two-Way Character Dictionary"},
    {"number": 242, "title": "Valid Anagram", "difficulty": "Easy", "topic": "Hashing", "pattern": "Frequency Counting", "similar_to": "Character Frequency Array Delta"},
    {"number": 290, "title": "Word Pattern", "difficulty": "Easy", "topic": "Hashing", "pattern": "Bijective Mapping", "similar_to": "Isomorphic Strings on Words"},
    {"number": 347, "title": "Top K Frequent Elements", "difficulty": "Medium", "topic": "Hashing", "pattern": "Bucket Sort / Min-Heap", "similar_to": "Frequency Inverted Index"},
    {"number": 387, "title": "First Unique Character in a String", "difficulty": "Easy", "topic": "Hashing", "pattern": "Two-Pass Counting", "similar_to": "Frequency Table Filtering"},
    {"number": 451, "title": "Sort Characters By Frequency", "difficulty": "Medium", "topic": "Hashing", "pattern": "Bucket Sort", "similar_to": "Top K Frequency Distribution"},
    {"number": 525, "title": "Contiguous Array", "difficulty": "Medium", "topic": "Hashing", "pattern": "Prefix Sum Difference", "similar_to": "Subarray with Equal 0s and 1s"},
    {"number": 594, "title": "Longest Harmonious Subsequence", "difficulty": "Easy", "topic": "Hashing", "pattern": "Frequency Map", "similar_to": "Adjacent Key Lookup (k, k+1)"},
    {"number": 706, "title": "Design HashMap", "difficulty": "Easy", "topic": "Hashing", "pattern": "Array of Linked Lists / Buckets", "similar_to": "Chaining Hash Collision Resolution"},
    {"number": 974, "title": "Subarray Sums Divisible by K", "difficulty": "Medium", "topic": "Hashing", "pattern": "Prefix Modulo", "similar_to": "Subarray Remainder Congruence"},
    {"number": 149, "title": "Max Points on a Line", "difficulty": "Hard", "topic": "Hashing", "pattern": "Slope Hashing with GCD", "similar_to": "Normalized Vector Direction Map"},

    # --- 3. Two Pointers ---
    {"number": 11, "title": "Container With Most Water", "difficulty": "Medium", "topic": "Two Pointers", "pattern": "Opposite Ends Inward", "similar_to": "Greedy Width Reduction"},
    {"number": 15, "title": "3Sum", "difficulty": "Medium", "topic": "Two Pointers", "pattern": "Sort + 2Sum Closest", "similar_to": "Target Sum with Duplicate Skipping"},
    {"number": 16, "title": "3Sum Closest", "difficulty": "Medium", "topic": "Two Pointers", "pattern": "Sort + Two Pointers", "similar_to": "Minimized Absolute Difference"},
    {"number": 18, "title": "4Sum", "difficulty": "Medium", "topic": "Two Pointers", "pattern": "kSum Reduction", "similar_to": "Nested Sorted Pointers"},
    {"number": 42, "title": "Trapping Rain Water", "difficulty": "Hard", "topic": "Two Pointers", "pattern": "Two Pointers Max Boundaries", "similar_to": "LeftMax/RightMax Envelope"},
    {"number": 75, "title": "Sort Colors", "difficulty": "Medium", "topic": "Two Pointers", "pattern": "Dutch National Flag", "similar_to": "3-Way Partitioning (lo, mid, hi)"},
    {"number": 88, "title": "Merge Sorted Array", "difficulty": "Easy", "topic": "Two Pointers", "pattern": "Backwards Two Pointers", "similar_to": "Reverse In-place Merge"},
    {"number": 125, "title": "Valid Palindrome", "difficulty": "Easy", "topic": "Two Pointers", "pattern": "Inward Convergence", "similar_to": "Symmetric Character Match"},
    {"number": 167, "title": "Two Sum II - Input Array Is Sorted", "difficulty": "Medium", "topic": "Two Pointers", "pattern": "Opposite Ends", "similar_to": "Monotonic Sum Search"},
    {"number": 344, "title": "Reverse String", "difficulty": "Easy", "topic": "Two Pointers", "pattern": "Swap from ends", "similar_to": "In-place Array Reflection"},
    {"number": 345, "title": "Reverse Vowels of a String", "difficulty": "Easy", "topic": "Two Pointers", "pattern": "Selective Swapping", "similar_to": "Conditional Two-Pointer Advance"},
    {"number": 392, "title": "Is Subsequence", "difficulty": "Easy", "topic": "Two Pointers", "pattern": "Greedy Forward Matching", "similar_to": "Dual String Index Marching"},
    {"number": 680, "title": "Valid Palindrome II", "difficulty": "Easy", "topic": "Two Pointers", "pattern": "Branching Palindrome Check", "similar_to": "Single Error Tolerance Check"},
    {"number": 844, "title": "Backspace String Compare", "difficulty": "Easy", "topic": "Two Pointers", "pattern": "Reverse Two Pointers", "similar_to": "Skip Counter Traversal"},
    {"number": 977, "title": "Squares of a Sorted Array", "difficulty": "Easy", "topic": "Two Pointers", "pattern": "Outer-to-Inner Fill", "similar_to": "Merge of Two Sorted Halves"},
    {"number": 986, "title": "Interval List Intersections", "difficulty": "Medium", "topic": "Two Pointers", "pattern": "Two Sorted Interval Steppers", "similar_to": "Segment Overlap Max(Start)/Min(End)"},

    # --- 4. Sliding Window ---
    {"number": 3, "title": "Longest Substring Without Repeating Characters", "difficulty": "Medium", "topic": "Sliding Window", "pattern": "Variable Size / Hash Window", "similar_to": "Last Occurrence Index Jump"},
    {"number": 76, "title": "Minimum Window Substring", "difficulty": "Hard", "topic": "Sliding Window", "pattern": "Shrinking Window with Match Count", "similar_to": "Multiset Containment Window"},
    {"number": 209, "title": "Minimum Size Subarray Sum", "difficulty": "Medium", "topic": "Sliding Window", "pattern": "Dynamic Window Expand/Shrink", "similar_to": "Continuous Positive Running Sum"},
    {"number": 219, "title": "Contains Duplicate II", "difficulty": "Easy", "topic": "Sliding Window", "pattern": "Fixed Window / Set Size k", "similar_to": "Sliding HashSet Buffer"},
    {"number": 424, "title": "Longest Repeating Character Replacement", "difficulty": "Medium", "topic": "Sliding Window", "pattern": "Window Length - Max Freq <= k", "similar_to": "Optimistic Window Growth"},
    {"number": 438, "title": "Find All Anagrams in a String", "difficulty": "Medium", "topic": "Sliding Window", "pattern": "Fixed Length Sliding Hash", "similar_to": "Sliding Character Frequency Match"},
    {"number": 567, "title": "Permutation in String", "difficulty": "Medium", "topic": "Sliding Window", "pattern": "Fixed Window Frequency Match", "similar_to": "Anagram Window Verification"},
    {"number": 643, "title": "Maximum Average Subarray I", "difficulty": "Easy", "topic": "Sliding Window", "pattern": "Fixed Size Window", "similar_to": "Sliding Window Sum Diff"},
    {"number": 713, "title": "Subarray Product Less Than K", "difficulty": "Medium", "topic": "Sliding Window", "pattern": "Count subarrays (r - l + 1)", "similar_to": "Multiplicative Window Constraint"},
    {"number": 904, "title": "Fruit Into Baskets", "difficulty": "Medium", "topic": "Sliding Window", "pattern": "At most 2 distinct elements", "similar_to": "Longest Substring with At Most K Distinct"},
    {"number": 992, "title": "Subarrays with K Different Integers", "difficulty": "Hard", "topic": "Sliding Window", "pattern": "Exact(k) = AtMost(k) - AtMost(k-1)", "similar_to": "Subarray Counting Reduction"},
    {"number": 1004, "title": "Max Consecutive Ones III", "difficulty": "Medium", "topic": "Sliding Window", "pattern": "At most k zeros in window", "similar_to": "Zero Count Threshold Window"},
    {"number": 1456, "title": "Maximum Number of Vowels in a Substring of Given Length", "difficulty": "Medium", "topic": "Sliding Window", "pattern": "Fixed Window Rolling Count", "similar_to": "Sliding Subarray Target Counter"},

    # --- 5. Stack & Queue ---
    {"number": 20, "title": "Valid Parentheses", "difficulty": "Easy", "topic": "Stack & Queue", "pattern": "LIFO Matching", "similar_to": "Bracket Matching Stack"},
    {"number": 71, "title": "Simplify Path", "difficulty": "Medium", "topic": "Stack & Queue", "pattern": "Directory Stack", "similar_to": "Path Tokenization (.. pop, . ignore)"},
    {"number": 150, "title": "Evaluate Reverse Polish Notation", "difficulty": "Medium", "topic": "Stack & Queue", "pattern": "Postfix Evaluation", "similar_to": "Operand Stack with Operator Application"},
    {"number": 155, "title": "Min Stack", "difficulty": "Medium", "topic": "Stack & Queue", "pattern": "Dual Stack / Tuple Stack", "similar_to": "Auxiliary Minimum Tracking"},
    {"number": 225, "title": "Implement Stack using Queues", "difficulty": "Easy", "topic": "Stack & Queue", "pattern": "Queue Rotation", "similar_to": "Single Queue Push-to-Back"},
    {"number": 232, "title": "Implement Queue using Stacks", "difficulty": "Easy", "topic": "Stack & Queue", "pattern": "In-Stack & Out-Stack", "similar_to": "Amortized FIFO Transfer"},
    {"number": 394, "title": "Decode String", "difficulty": "Medium", "topic": "Stack & Queue", "pattern": "Nested State Stack", "similar_to": "Parentheses Multiplier Stack"},
    {"number": 496, "title": "Next Greater Element I", "difficulty": "Easy", "topic": "Stack & Queue", "pattern": "Monotonic Decreasing Stack", "similar_to": "Next Greater Item Hash Map"},
    {"number": 503, "title": "Next Greater Element II", "difficulty": "Medium", "topic": "Stack & Queue", "pattern": "Circular Monotonic Stack", "similar_to": "Double Length Array Modulo Traversal"},
    {"number": 739, "title": "Daily Temperatures", "difficulty": "Medium", "topic": "Stack & Queue", "pattern": "Monotonic Stack Indices", "similar_to": "Next Warmer Day Distance"},
    {"number": 84, "title": "Largest Rectangle in Histogram", "difficulty": "Hard", "topic": "Stack & Queue", "pattern": "Monotonic Increasing Stack", "similar_to": "Left and Right Boundary Expansion"},
    {"number": 85, "title": "Maximal Rectangle", "difficulty": "Hard", "topic": "Stack & Queue", "pattern": "2D Histogram Heights + Monotonic Stack", "similar_to": "Largest Rectangle in Matrix Rows"},
    {"number": 239, "title": "Sliding Window Maximum", "difficulty": "Hard", "topic": "Stack & Queue", "pattern": "Monotonic Deque", "similar_to": "Decreasing Value Deque with Index Purge"},

    # --- 6. Linked List ---
    {"number": 2, "title": "Add Two Numbers", "difficulty": "Medium", "topic": "Linked List", "pattern": "Elementary Addition with Carry", "similar_to": "Digit-by-Digit Traverse with Dummy Head"},
    {"number": 19, "title": "Remove Nth Node From End of List", "difficulty": "Medium", "topic": "Linked List", "pattern": "Fast and Slow Pointer Gap", "similar_to": "k-step Forward Leader Pointer"},
    {"number": 21, "title": "Merge Two Sorted Lists", "difficulty": "Easy", "topic": "Linked List", "pattern": "Dummy Node + Iterative Splice", "similar_to": "Merge Step of Merge Sort"},
    {"number": 23, "title": "Merge k Sorted Lists", "difficulty": "Hard", "topic": "Linked List", "pattern": "Min-Heap / Divide and Conquer", "similar_to": "k-Way Merge via Priority Queue"},
    {"number": 24, "title": "Swap Nodes in Pairs", "difficulty": "Medium", "topic": "Linked List", "pattern": "Pointer Manipulation", "similar_to": "Pairwise Node Rewiring"},
    {"number": 25, "title": "Reverse Nodes in k-Group", "difficulty": "Hard", "topic": "Linked List", "pattern": "Sub-list Reversal", "similar_to": "Chunk Reversal with Length Check"},
    {"number": 61, "title": "Rotate List", "difficulty": "Medium", "topic": "Linked List", "pattern": "Ring Formation & Cut", "similar_to": "Circular List Tail-Head Link and Split"},
    {"number": 83, "title": "Remove Duplicates from Sorted List", "difficulty": "Easy", "topic": "Linked List", "pattern": "Sequential Pointer Advance", "similar_to": "Next Node Skip on Equal"},
    {"number": 86, "title": "Partition List", "difficulty": "Medium", "topic": "Linked List", "pattern": "Two Dummy Heads", "similar_to": "Less-Than and Greater-Than Sublists"},
    {"number": 92, "title": "Reverse Linked List II", "difficulty": "Medium", "topic": "Linked List", "pattern": "Range Reversal", "similar_to": "In-place Sub-segment Rewire"},
    {"number": 141, "title": "Linked List Cycle", "difficulty": "Easy", "topic": "Linked List", "pattern": "Floyd's Tortoise and Hare", "similar_to": "2x Speed Cycle Detection"},
    {"number": 142, "title": "Linked List Cycle II", "difficulty": "Medium", "topic": "Linked List", "pattern": "Floyd's Cycle Entry Point", "similar_to": "Head & Intersection Converge"},
    {"number": 143, "title": "Reorder List", "difficulty": "Medium", "topic": "Linked List", "pattern": "Find Mid + Reverse Half + Interleave", "similar_to": "Zig-zag List Folding"},
    {"number": 148, "title": "Sort List", "difficulty": "Medium", "topic": "Linked List", "pattern": "Merge Sort on Linked List", "similar_to": "Divide and Conquer with Fast/Slow Mid"},
    {"number": 160, "title": "Intersection of Two Linked Lists", "difficulty": "Easy", "topic": "Linked List", "pattern": "Two Pointers Path Equalization", "similar_to": "Pointer Redirection (pA ? pA.next : headB)"},
    {"number": 206, "title": "Reverse Linked List", "difficulty": "Easy", "topic": "Linked List", "pattern": "Iterative 3-pointer (prev, curr, next)", "similar_to": "Pointer Reversal Inversion"},
    {"number": 234, "title": "Palindrome Linked List", "difficulty": "Easy", "topic": "Linked List", "pattern": "Fast/Slow + Reverse 2nd Half", "similar_to": "Symmetric List Compare"},

    # --- 7. Binary Search ---
    {"number": 33, "title": "Search in Rotated Sorted Array", "difficulty": "Medium", "topic": "Binary Search", "pattern": "Identify Sorted Half", "similar_to": "Rotated Subarray Partition"},
    {"number": 34, "title": "Find First and Last Position of Element in Sorted Array", "difficulty": "Medium", "topic": "Binary Search", "pattern": "Lower & Upper Bound", "similar_to": "First True / Last True BSearch"},
    {"number": 35, "title": "Search Insert Position", "difficulty": "Easy", "topic": "Binary Search", "pattern": "Standard Binary Search", "similar_to": "Lower Bound Index Finder"},
    {"number": 69, "title": "Sqrt(x)", "difficulty": "Easy", "topic": "Binary Search", "pattern": "Binary Search on Answer", "similar_to": "Monotonic Integer Function Inversion"},
    {"number": 74, "title": "Search a 2D Matrix", "difficulty": "Medium", "topic": "Binary Search", "pattern": "Virtual 1D Array BSearch", "similar_to": "Row/Col Index Mapping (mid / n, mid % n)"},
    {"number": 81, "title": "Search in Rotated Sorted Array II", "difficulty": "Medium", "topic": "Binary Search", "pattern": "Rotated Search with Duplicates", "similar_to": "Trim End Duplicates before Half Check"},
    {"number": 153, "title": "Find Minimum in Rotated Sorted Array", "difficulty": "Medium", "topic": "Binary Search", "pattern": "Compare with Right Endpoint", "similar_to": "Inflection Point Search"},
    {"number": 162, "title": "Find Peak Element", "difficulty": "Medium", "topic": "Binary Search", "pattern": "Local Slope Comparison", "similar_to": "Gradient Ascent in Log(n)"},
    {"number": 278, "title": "First Bad Version", "difficulty": "Easy", "topic": "Binary Search", "pattern": "First True Predicate", "similar_to": "Boolean Search Horizon"},
    {"number": 410, "title": "Split Array Largest Sum", "difficulty": "Hard", "topic": "Binary Search", "pattern": "Binary Search on Answer", "similar_to": "Book Allocation / Painter's Partition"},
    {"number": 704, "title": "Binary Search", "difficulty": "Easy", "topic": "Binary Search", "pattern": "Exact Match Binary Search", "similar_to": "Classic lo + (hi-lo)//2"},
    {"number": 875, "title": "Koko Eating Bananas", "difficulty": "Medium", "topic": "Binary Search", "pattern": "Binary Search on Speed/Feasibility", "similar_to": "Capacity Optimization with Ceil Div"},
    {"number": 1011, "title": "Capacity To Ship Packages Within D Days", "difficulty": "Medium", "topic": "Binary Search", "pattern": "Binary Search on Capacity", "similar_to": "Koko Eating Bananas Capacity Variant"},
    {"number": 4, "title": "Median of Two Sorted Arrays", "difficulty": "Hard", "topic": "Binary Search", "pattern": "Binary Search on Partition Index", "similar_to": "Dual Array Half-Partition Balance"},

    # --- 8. Recursion & Backtracking ---
    {"number": 17, "title": "Letter Combinations of a Phone Number", "difficulty": "Medium", "topic": "Recursion & Backtracking", "pattern": "Combinatorial Tree DFS", "similar_to": "Multi-Choice Tree Traversal"},
    {"number": 22, "title": "Generate Parentheses", "difficulty": "Medium", "topic": "Recursion & Backtracking", "pattern": "Constrained State Backtrack", "similar_to": "Open/Close Count Balanced Branching"},
    {"number": 39, "title": "Combination Sum", "difficulty": "Medium", "topic": "Recursion & Backtracking", "pattern": "Unbounded Coin Choice", "similar_to": "Subset Generation with Repetition"},
    {"number": 40, "title": "Combination Sum II", "difficulty": "Medium", "topic": "Recursion & Backtracking", "pattern": "Bounded Choice with Duplicate Skip", "similar_to": "Sorted Backtracking with if i > start and nums[i]==nums[i-1]"},
    {"number": 46, "title": "Permutations", "difficulty": "Medium", "topic": "Recursion & Backtracking", "pattern": "Used Array / Swap Permutations", "similar_to": "Full State Tree Permutation"},
    {"number": 47, "title": "Permutations II", "difficulty": "Medium", "topic": "Recursion & Backtracking", "pattern": "Permutations with Duplicates", "similar_to": "Sorted Swap with Used Array Predecessor Check"},
    {"number": 51, "title": "N-Queens", "difficulty": "Hard", "topic": "Recursion & Backtracking", "pattern": "Diagonal & Column Bitmask / Sets", "similar_to": "Constraint Satisfaction Problem"},
    {"number": 77, "title": "Combinations", "difficulty": "Medium", "topic": "Recursion & Backtracking", "pattern": "n Choose k Backtrack", "similar_to": "Index Incremental Subset Building"},
    {"number": 78, "title": "Subsets", "difficulty": "Medium", "topic": "Recursion & Backtracking", "pattern": "Power Set Generation", "similar_to": "Include/Exclude Binary Choice Tree"},
    {"number": 79, "title": "Word Search", "difficulty": "Medium", "topic": "Recursion & Backtracking", "pattern": "2D Grid DFS with Visited Mark", "similar_to": "Grid Path String Matching"},
    {"number": 90, "title": "Subsets II", "difficulty": "Medium", "topic": "Recursion & Backtracking", "pattern": "Power Set with Duplicates", "similar_to": "Sort and Sibling Skip"},
    {"number": 131, "title": "Palindrome Partitioning", "difficulty": "Medium", "topic": "Recursion & Backtracking", "pattern": "Prefix Palindrome Check & Recurse", "similar_to": "String Slicing Backtrack"},

    # --- 9. Trees & BST ---
    {"number": 94, "title": "Binary Tree Inorder Traversal", "difficulty": "Easy", "topic": "Trees & BST", "pattern": "Left-Root-Right / Stack", "similar_to": "BST Sorted Projection"},
    {"number": 98, "title": "Validate Binary Search Tree", "difficulty": "Medium", "topic": "Trees & BST", "pattern": "Range Validation (min_val < node.val < max_val)", "similar_to": "BST Invariant Propagation"},
    {"number": 100, "title": "Same Tree", "difficulty": "Easy", "topic": "Trees & BST", "pattern": "Simultaneous Tree DFS", "similar_to": "Structural & Value Equivalence"},
    {"number": 101, "title": "Symmetric Tree", "difficulty": "Easy", "topic": "Trees & BST", "pattern": "Mirror DFS (left.left vs right.right)", "similar_to": "Reflection Symmetry Test"},
    {"number": 102, "title": "Binary Tree Level Order Traversal", "difficulty": "Medium", "topic": "Trees & BST", "pattern": "Queue BFS per Level", "similar_to": "Breadth-First Queue Snapshot"},
    {"number": 104, "title": "Maximum Depth of Binary Tree", "difficulty": "Easy", "topic": "Trees & BST", "pattern": "1 + max(left, right)", "similar_to": "Recursive Subtree Height"},
    {"number": 105, "title": "Construct Binary Tree from Preorder and Inorder Traversal", "difficulty": "Medium", "topic": "Trees & BST", "pattern": "Root Split with Inorder Hash Index", "similar_to": "Tree Reconstruction from Traversal Sequences"},
    {"number": 110, "title": "Balanced Binary Tree", "difficulty": "Easy", "topic": "Trees & BST", "pattern": "Bottom-Up Height Check", "similar_to": "Height Balance Discrepancy <= 1"},
    {"number": 112, "title": "Path Sum", "difficulty": "Easy", "topic": "Trees & BST", "pattern": "Root-to-Leaf Target Subtraction", "similar_to": "Leaf Predicate Match"},
    {"number": 124, "title": "Binary Tree Maximum Path Sum", "difficulty": "Hard", "topic": "Trees & BST", "pattern": "Max Branch Gain with Global Bridge Max", "similar_to": "Diameter Calculation with Vertex Weights"},
    {"number": 199, "title": "Binary Tree Right Side View", "difficulty": "Medium", "topic": "Trees & BST", "pattern": "Level Order Last Element / Reverse Preorder", "similar_to": "Rightmost Node Visibility"},
    {"number": 226, "title": "Invert Binary Tree", "difficulty": "Easy", "topic": "Trees & BST", "pattern": "Postorder / Preorder Child Swap", "similar_to": "Tree Mirroring"},
    {"number": 230, "title": "Kth Smallest Element in a BST", "difficulty": "Medium", "topic": "Trees & BST", "pattern": "Inorder Traversal with Counter", "similar_to": "BST Monotonic Index Match"},
    {"number": 235, "title": "Lowest Common Ancestor of a Binary Search Tree", "difficulty": "Medium", "topic": "Trees & BST", "pattern": "BST Value Split Comparison", "similar_to": "Interval Fork in BST"},
    {"number": 236, "title": "Lowest Common Ancestor of a Binary Tree", "difficulty": "Medium", "topic": "Trees & BST", "pattern": "Postorder Search Propagation", "similar_to": "Lowest Node with Target in Both Subtrees"},
    {"number": 297, "title": "Serialize and Deserialize Binary Tree", "difficulty": "Hard", "topic": "Trees & BST", "pattern": "Preorder with Null Sentinels", "similar_to": "Tree State Encoded Array Tokenization"},
    {"number": 543, "title": "Diameter of Binary Tree", "difficulty": "Easy", "topic": "Trees & BST", "pattern": "Postorder Max Left Depth + Right Depth", "similar_to": "Longest Node-to-Node Path"},

    # --- 10. Heaps & Priority Queue ---
    {"number": 215, "title": "Kth Largest Element in an Array", "difficulty": "Medium", "topic": "Heaps & Priority Queue", "pattern": "Min-Heap of size K / QuickSelect", "similar_to": "Top-K Bounded Heap Buffer"},
    {"number": 295, "title": "Find Median from Data Stream", "difficulty": "Hard", "topic": "Heaps & Priority Queue", "pattern": "Max-Heap (Lower Half) + Min-Heap (Upper Half)", "similar_to": "Dual Balanced Heap Partition"},
    {"number": 373, "title": "Find K Pairs with Smallest Sums", "difficulty": "Medium", "topic": "Heaps & Priority Queue", "pattern": "Dijkstra-like Grid Frontier Min-Heap", "similar_to": "Sorted Pair Frontier Expansion"},
    {"number": 621, "title": "Task Scheduler", "difficulty": "Medium", "topic": "Heaps & Priority Queue", "pattern": "Max-Heap Frequency / Math Slot Filling", "similar_to": "Cool-down Idle Time Slotting"},
    {"number": 703, "title": "Kth Largest Element in a Stream", "difficulty": "Easy", "topic": "Heaps & Priority Queue", "pattern": "Min-Heap of Size K", "similar_to": "Streaming Kth Element Maintenance"},
    {"number": 973, "title": "K Closest Points to Origin", "difficulty": "Medium", "topic": "Heaps & Priority Queue", "pattern": "Max-Heap of size K by Euclidean Distance", "similar_to": "Bounded Spatial Distance Priority Queue"},
    {"number": 1046, "title": "Last Stone Weight", "difficulty": "Easy", "topic": "Heaps & Priority Queue", "pattern": "Max-Heap Simulation", "similar_to": "Pairwise Top Element Collision"},
    {"number": 1642, "title": "Furthest Building You Can Reach", "difficulty": "Medium", "topic": "Heaps & Priority Queue", "pattern": "Min-Heap for Ladders (Largest Jumps)", "similar_to": "Greedy Allocation with Heap Regret"},

    # --- 11. Greedy ---
    {"number": 45, "title": "Jump Game II", "difficulty": "Medium", "topic": "Greedy", "pattern": "BFS-Style Furthest Reach Window", "similar_to": "Current Jump End & Farthest Exploration"},
    {"number": 55, "title": "Jump Game", "difficulty": "Medium", "topic": "Greedy", "pattern": "Max Reachable Index Tracking", "similar_to": "Farthest Reachable Horizon"},
    {"number": 134, "title": "Gas Station", "difficulty": "Medium", "topic": "Greedy", "pattern": "Reset Start Index on Negative Tank", "similar_to": "Total Fuel Deficit with Greedy Reset"},
    {"number": 135, "title": "Candy", "difficulty": "Hard", "topic": "Greedy", "pattern": "Left-to-Right & Right-to-Left Passes", "similar_to": "Two-Pass Slope Constraint Satisfaction"},
    {"number": 402, "title": "Remove K Digits", "difficulty": "Medium", "topic": "Greedy", "pattern": "Monotonic Increasing Stack + Greedy Pop", "similar_to": "Smallest Lexicographical String Builder"},
    {"number": 455, "title": "Assign Cookies", "difficulty": "Easy", "topic": "Greedy", "pattern": "Sort & Match Smallest Feasible", "similar_to": "Smallest Demand First"},
    {"number": 605, "title": "Can Place Flowers", "difficulty": "Easy", "topic": "Greedy", "pattern": "Adjacent Slot Check", "similar_to": "Immediate Greedy Slot Reservation"},
    {"number": 670, "title": "Maximum Swap", "difficulty": "Medium", "topic": "Greedy", "pattern": "Last Occurrence Map", "similar_to": "Swap with Largest Suffix Digit"},
    {"number": 763, "title": "Partition Labels", "difficulty": "Medium", "topic": "Greedy", "pattern": "Last Seen Index Interval Extension", "similar_to": "Greedy Substring Cut Boundary"},
    {"number": 860, "title": "Lemonade Change", "difficulty": "Easy", "topic": "Greedy", "pattern": "Greedily Spend Larger Bills First ($10 before $5)", "similar_to": "Greedy Change Making"},
    {"number": 1710, "title": "Maximum Units on a Truck", "difficulty": "Easy", "topic": "Greedy", "pattern": "Sort by Units/Box Descending", "similar_to": "Fractional Knapsack (greedy by value/weight)"},
    {"number": 1834, "title": "Single-Threaded CPU", "difficulty": "Medium", "topic": "Greedy", "pattern": "Available Tasks Min-Heap by Processing Time", "similar_to": "Shortest Job First"},

    # --- 12. Intervals ---
    {"number": 56, "title": "Merge Intervals", "difficulty": "Medium", "topic": "Intervals", "pattern": "Sort by Start + Merge Overlapping", "similar_to": "Active Interval Extension (curr.start <= prev.end)"},
    {"number": 57, "title": "Insert Interval", "difficulty": "Medium", "topic": "Intervals", "pattern": "Three-Phase Scan (Left, Merge, Right)", "similar_to": "Linear Insertion into Disjoint Intervals"},
    {"number": 252, "title": "Meeting Rooms", "difficulty": "Easy", "topic": "Intervals", "pattern": "Sort by Start + Overlap Check", "similar_to": "Disjoint Segment Verification"},
    {"number": 253, "title": "Meeting Rooms II", "difficulty": "Medium", "topic": "Intervals", "pattern": "Min-Heap of End Times / Chronological Sweep", "similar_to": "Concurrent Resource Peak Count"},
    {"number": 435, "title": "Non-overlapping Intervals", "difficulty": "Medium", "topic": "Intervals", "pattern": "Sort by End Time + Greedily Keep Earliest", "similar_to": "Activity Selection"},
    {"number": 452, "title": "Minimum Number of Arrows to Burst Balloons", "difficulty": "Medium", "topic": "Intervals", "pattern": "Sort by End + Shoot at End Position", "similar_to": "Interval Clique Point Stabbing"},
    {"number": 732, "title": "My Calendar III", "difficulty": "Hard", "topic": "Intervals", "pattern": "Coordinate Compression Sweep-Line", "similar_to": "Prefix Sum on Timeline Deltas (+1 / -1)"},

    # --- 13. Graphs ---
    {"number": 133, "title": "Clone Graph", "difficulty": "Medium", "topic": "Graphs", "pattern": "BFS / DFS with Clone Map", "similar_to": "Hash-Mapped Graph Deep Copy"},
    {"number": 200, "title": "Number of Islands", "difficulty": "Medium", "topic": "Graphs", "pattern": "Connected Components Flood Fill (BFS/DFS)", "similar_to": "Grid Connected Component Traversal"},
    {"number": 207, "title": "Course Schedule", "difficulty": "Medium", "topic": "Graphs", "pattern": "Topological Sort (Kahn / In-degree or DFS Cycle)", "similar_to": "Directed Acyclic Graph Cycle Check"},
    {"number": 210, "title": "Course Schedule II", "difficulty": "Medium", "topic": "Graphs", "pattern": "Topological Sort Order Output", "similar_to": "Kahn's Algorithm In-Degree Zero BFS"},
    {"number": 261, "title": "Graph Valid Tree", "difficulty": "Medium", "topic": "Graphs", "pattern": "Union-Find / BFS (Edges == n-1 and Connected)", "similar_to": "Acyclic Connected Graph Invariant"},
    {"number": 323, "title": "Number of Connected Components in an Undirected Graph", "difficulty": "Medium", "topic": "Graphs", "pattern": "Disjoint Set Union (DSU)", "similar_to": "Union-Find with Path Compression"},
    {"number": 399, "title": "Evaluate Division", "difficulty": "Medium", "topic": "Graphs", "pattern": "Weighted Directed Graph BFS/DFS", "similar_to": "Path Product Calculation on Graph"},
    {"number": 417, "title": "Pacific Atlantic Water Flow", "difficulty": "Medium", "topic": "Graphs", "pattern": "Reverse DFS from Ocean Borders", "similar_to": "Dual-Source Reverse Reachability"},
    {"number": 684, "title": "Redundant Connection", "difficulty": "Medium", "topic": "Graphs", "pattern": "Union-Find Cycle Edge Detection", "similar_to": "Kruskal's Cycle Detection Step"},
    {"number": 743, "title": "Network Delay Time", "difficulty": "Medium", "topic": "Graphs", "pattern": "Dijkstra's Algorithm (Min-Heap)", "similar_to": "Single-Source Shortest Path on Non-negative Edges"},
    {"number": 785, "title": "Is Graph Bipartite?", "difficulty": "Medium", "topic": "Graphs", "pattern": "2-Coloring BFS / DFS", "similar_to": "Odd Cycle Detection"},
    {"number": 787, "title": "Cheapest Flights Within K Stops", "difficulty": "Medium", "topic": "Graphs", "pattern": "Bellman-Ford / Modified Dijkstra", "similar_to": "K-Step Shortest Path Relaxation"},
    {"number": 994, "title": "Rotting Oranges", "difficulty": "Medium", "topic": "Graphs", "pattern": "Multi-Source BFS", "similar_to": "Simultaneous Level Expansion BFS"},
    {"number": 127, "title": "Word Ladder", "difficulty": "Hard", "topic": "Graphs", "pattern": "Bidirectional BFS on String Transitions", "similar_to": "Shortest Transformation Sequence in Graph"},

    # --- 14. Dynamic Programming ---
    {"number": 70, "title": "Climbing Stairs", "difficulty": "Easy", "topic": "Dynamic Programming", "pattern": "1D State Transition", "similar_to": "Fibonacci Recurrence: dp[i] = dp[i-1] + dp[i-2]"},
    {"number": 62, "title": "Unique Paths", "difficulty": "Medium", "topic": "Dynamic Programming", "pattern": "2D Grid Path DP", "similar_to": "Grid Combinatorics: dp[r][c] = dp[r-1][c] + dp[r][c-1]"},
    {"number": 64, "title": "Minimum Path Sum", "difficulty": "Medium", "topic": "Dynamic Programming", "pattern": "2D Grid Cost DP", "similar_to": "Min Cost Grid Walk"},
    {"number": 91, "title": "Decode Ways", "difficulty": "Medium", "topic": "Dynamic Programming", "pattern": "1D String Subproblem Partition", "similar_to": "Valid 1-Digit and 2-Digit Parsing Branching"},
    {"number": 139, "title": "Word Break", "difficulty": "Medium", "topic": "Dynamic Programming", "pattern": "1D Boolean Match Prefix DP", "similar_to": "Dictionary Word Concatenation Check"},
    {"number": 198, "title": "House Robber", "difficulty": "Medium", "topic": "Dynamic Programming", "pattern": "Non-Adjacent Maximum Sum", "similar_to": "Pick or Skip State: dp[i] = max(dp[i-1], dp[i-2] + val)"},
    {"number": 213, "title": "House Robber II", "difficulty": "Medium", "topic": "Dynamic Programming", "pattern": "Circular Array DP (0..n-2 vs 1..n-1)", "similar_to": "Two Sub-array Linear Reductions"},
    {"number": 300, "title": "Longest Increasing Subsequence", "difficulty": "Medium", "topic": "Dynamic Programming", "pattern": "O(n^2) DP or O(n log n) Patience Sorting", "similar_to": "Tails Array Binary Search Insertion"},
    {"number": 322, "title": "Coin Change", "difficulty": "Medium", "topic": "Dynamic Programming", "pattern": "Unbounded Knapsack Min Cost", "similar_to": "Bottom-Up Minimum Denominations"},
    {"number": 416, "title": "Partition Equal Subset Sum", "difficulty": "Medium", "topic": "Dynamic Programming", "pattern": "0/1 Knapsack (Target = Sum / 2)", "similar_to": "Subset Sum Existence DP"},
    {"number": 494, "title": "Target Sum", "difficulty": "Medium", "topic": "Dynamic Programming", "pattern": "Subset Sum Transformation (P = (target + sum) / 2)", "similar_to": "0/1 Knapsack Count Ways"},
    {"number": 518, "title": "Coin Change II", "difficulty": "Medium", "topic": "Dynamic Programming", "pattern": "Unbounded Knapsack Combinations", "similar_to": "Ordered Outer Loop Coin Accumulation"},
    {"number": 1143, "title": "Longest Common Subsequence", "difficulty": "Medium", "topic": "Dynamic Programming", "pattern": "2D String Alignment DP", "similar_to": "LCS: dp[i][j] = dp[i-1][j-1]+1 if match else max(dp[i-1][j], dp[i][j-1])"},
    {"number": 72, "title": "Edit Distance", "difficulty": "Medium", "topic": "Dynamic Programming", "pattern": "2D Levenshtein Distance", "similar_to": "Insert, Delete, Replace Matrix Operations"},
    {"number": 312, "title": "Burst Balloons", "difficulty": "Hard", "topic": "Dynamic Programming", "pattern": "Interval DP (Last Balloon Burst)", "similar_to": "Matrix Chain Multiplication Variant"},
    {"number": 10, "title": "Regular Expression Matching", "difficulty": "Hard", "topic": "Dynamic Programming", "pattern": "2D Regex State Transition", "similar_to": "Wildcard Matching State Table with * Branching"},

    # --- 15. Tries ---
    {"number": 208, "title": "Implement Trie (Prefix Tree)", "difficulty": "Medium", "topic": "Tries", "pattern": "Prefix Tree Node with Children Array", "similar_to": "26-ary Character Tree"},
    {"number": 211, "title": "Design Add and Search Words Data Structure", "difficulty": "Medium", "topic": "Tries", "pattern": "Trie with Wildcard DFS Traversal", "similar_to": "Backtracking over Trie Children on '.'"},
    {"number": 212, "title": "Word Search II", "difficulty": "Hard", "topic": "Tries", "pattern": "Trie + 2D Grid DFS Backtracking", "similar_to": "Simultaneous Trie & Matrix Traversal with Pruning"},
    {"number": 421, "title": "Maximum XOR of Two Numbers in an Array", "difficulty": "Medium", "topic": "Tries", "pattern": "Bitwise Trie (32-level Binary Tree)", "similar_to": "Opposite Bit Greedy Trie Traversal"},
    {"number": 648, "title": "Replace Words", "difficulty": "Medium", "topic": "Tries", "pattern": "Shortest Root Prefix Search", "similar_to": "Trie Prefix Greedy Match"},
    {"number": 677, "title": "Map Sum Pairs", "difficulty": "Medium", "topic": "Tries", "pattern": "Trie with Subtree Sum Aggregation", "similar_to": "Prefix Value Accumulation"},

    # --- 16. Bit Manipulation & Math ---
    {"number": 136, "title": "Single Number", "difficulty": "Easy", "topic": "Bit Manipulation & Math", "pattern": "XOR Cancellation", "similar_to": "a ^ a = 0 Identity"},
    {"number": 137, "title": "Single Number II", "difficulty": "Medium", "topic": "Bit Manipulation & Math", "pattern": "Modulo 3 Bit Counter", "similar_to": "State Machine Counters (ones, twos)"},
    {"number": 190, "title": "Reverse Bits", "difficulty": "Easy", "topic": "Bit Manipulation & Math", "pattern": "Bitwise Shift & Masking", "similar_to": "32-bit Reversal via Binary Masking"},
    {"number": 191, "title": "Number of 1 Bits", "difficulty": "Easy", "topic": "Bit Manipulation & Math", "pattern": "Brian Kernighan's Algorithm", "similar_to": "n & (n - 1) Set-Bit Stripping"},
    {"number": 231, "title": "Power of Two", "difficulty": "Easy", "topic": "Bit Manipulation & Math", "pattern": "Single Set Bit Check", "similar_to": "n > 0 and (n & (n - 1)) == 0"},
    {"number": 268, "title": "Missing Number", "difficulty": "Easy", "topic": "Bit Manipulation & Math", "pattern": "XOR Accumulation / Gauss Sum", "similar_to": "n * (n + 1) // 2 Expected Sum Difference"},
    {"number": 338, "title": "Counting Bits", "difficulty": "Easy", "topic": "Bit Manipulation & Math", "pattern": "DP on Bit Shift", "similar_to": "dp[i] = dp[i >> 1] + (i & 1)"},
    {"number": 371, "title": "Sum of Two Integers", "difficulty": "Medium", "topic": "Bit Manipulation & Math", "pattern": "Half Adder Circuit (XOR sum, AND carry)", "similar_to": "Bitwise Addition without Arithmetic Operators"},
    {"number": 204, "title": "Count Primes", "difficulty": "Medium", "topic": "Bit Manipulation & Math", "pattern": "Sieve of Eratosthenes", "similar_to": "Boolean Prime Array Multiples Invalidation"},
    {"number": 50, "title": "Pow(x, n)", "difficulty": "Medium", "topic": "Bit Manipulation & Math", "pattern": "Binary Exponentiation", "similar_to": "Fast Power: x^(2k) = (x^2)^k in O(log n)"},
    {"number": 172, "title": "Factorial Trailing Zeroes", "difficulty": "Medium", "topic": "Bit Manipulation & Math", "pattern": "Legendre's Formula for Factor 5", "similar_to": "n // 5 + n // 25 + n // 125 ..."}
]

# Generate more structured problems programmatically to reach 300+ solid unique problems
topic_counts = {}
for p in PROBLEMS_DATA:
    topic_counts[p["topic"]] = topic_counts.get(p["topic"], 0) + 1

# Additional curated problem templates across concepts
EXTRA_PROBLEMS = [
    # Arrays
    (119, "Pascal's Triangle II", "Easy", "Arrays & Strings", "Combinatorics", "Row-by-Row Combinatorial Generation"),
    (1365, "How Many Numbers Are Smaller Than the Current Number", "Easy", "Arrays & Strings", "Frequency Buckets", "Prefix Count Rank"),
    (1480, "Running Sum of 1d Array", "Easy", "Arrays & Strings", "Prefix Sum", "In-place Running Sum Accumulation"),
    (1470, "Shuffle the Array", "Easy", "Arrays & Strings", "Two Pointers", "Interleaved Array Reconstruction"),
    (1431, "Kids With the Greatest Number of Candies", "Easy", "Arrays & Strings", "Max Element Scan", "Comparison with Pre-computed Max"),
    (1512, "Number of Good Pairs", "Easy", "Arrays & Strings", "Combination Count", "n * (n - 1) // 2 on Frequency Map"),
    (1920, "Build Array from Permutation", "Easy", "Arrays & Strings", "Index Remapping", "In-place Value Encoding via Modulo"),
    (1929, "Concatenation of Array", "Easy", "Arrays & Strings", "Array Duplication", "Dual Array Appending"),
    (2011, "Final Value of Variable After Performing Operations", "Easy", "Arrays & Strings", "Simulation", "Operation String Scanning"),
    (2114, "Maximum Number of Words Found in Sentences", "Easy", "Arrays & Strings", "String Tokenization", "Space Count Tracking"),
    (566, "Reshape the Matrix", "Easy", "Arrays & Strings", "Coordinate Math", "Row/Col Flat Index Mapping"),
    (665, "Non-decreasing Array", "Medium", "Arrays & Strings", "Greedy Inversion", "Single Element Modification Verification"),
    (724, "Find Pivot Index", "Easy", "Arrays & Strings", "Prefix Sum Balance", "Total Sum - Left Sum - Val == Left Sum"),
    (896, "Monotonic Array", "Easy", "Arrays & Strings", "Single Pass Check", "Direction Flag State Tracker"),
    (905, "Sort Array By Parity", "Easy", "Arrays & Strings", "Two Pointers Partition", "Odd-Even In-place Swapping"),
    (922, "Sort Array By Parity II", "Easy", "Arrays & Strings", "Dual Index Walkers", "Separate Even/Odd Pointer Placement"),
    (941, "Valid Mountain Array", "Easy", "Arrays & Strings", "Single Peak March", "Climb Up & Climb Down Strict Monotonicity"),
    (989, "Add to Array-Form of Integer", "Easy", "Arrays & Strings", "Elementary Addition", "Carry Forward with Reverse Array Traverse"),
    (1002, "Find Common Characters", "Easy", "Arrays & Strings", "Character Minimum Intersect", "Global Min Frequency Array"),
    (1051, "Height Checker", "Easy", "Arrays & Strings", "Sorting Comparison", "Discrepancy Count with Sorted Array"),
    (1295, "Find Numbers with Even Number of Digits", "Easy", "Arrays & Strings", "Digit Counting", "Log10 String Length Calculation"),
    (1299, "Replace Elements with Greatest Element on Right Side", "Easy", "Arrays & Strings", "Reverse Max Scan", "Running Suffix Maximum"),
    (1304, "Find N Unique Integers Sum up to Zero", "Easy", "Arrays & Strings", "Symmetric Generation", "Pairwise Balanced Integers (+x, -x)"),
    (1346, "Check If N and Its Double Exist", "Easy", "Arrays & Strings", "Hash Set", "Two-Way Factor Lookup (2x, x/2)"),
    (1389, "Create Target Array in the Given Order", "Easy", "Arrays & Strings", "List Insertion", "Positional In-place Splicing"),
    (1464, "Maximum Product of Two Elements in an Array", "Easy", "Arrays & Strings", "Two Largest Search", "Top-2 Maximum Value Tracking"),
    (1588, "Sum of All Odd Length Subarrays", "Easy", "Arrays & Strings", "Combinatorial Contribution", "Frequency Formula (i+1)*(n-i)"),
    (1672, "Richest Customer Wealth", "Easy", "Arrays & Strings", "Matrix Row Sum", "Max of Row Sums"),
    (1773, "Count Items Matching a Rule", "Easy", "Arrays & Strings", "Key Matching", "Rule Key Column Filter"),
    (1816, "Truncate Sentence", "Easy", "Arrays & Strings", "String Split", "First K Space Truncation"),
    (1822, "Sign of the Product of an Array", "Easy", "Arrays & Strings", "Negative Count", "Parity of Negative Numbers"),
    (1913, "Maximum Product Difference Between Two Pairs", "Easy", "Arrays & Strings", "Extrema Search", "(Max1 * Max2) - (Min1 * Min2)"),
    (2006, "Count Number of Pairs With Absolute Difference K", "Easy", "Arrays & Strings", "Hash Map Count", "Lookup for val - k and val + k"),
    (2108, "Find First Palindromic String in the Array", "Easy", "Arrays & Strings", "Two Pointers", "Early Return Palindrome Check"),
    (2176, "Count Equal and Divisible Pairs in an Array", "Easy", "Arrays & Strings", "Brute-force / Hash List", "Index Product Divisibility"),
    (2215, "Find the Difference of Two Arrays", "Easy", "Arrays & Strings", "Set Difference", "Set(A) - Set(B)"),

    # Two Pointers / Sliding window / Strings
    (28, "Find the Index of the First Occurrence in a String", "Easy", "Arrays & Strings", "KMP / Substring Match", "Sliding Pattern Window Match"),
    (14, "Longest Common Prefix", "Easy", "Arrays & Strings", "Horizontal / Vertical Scanning", "Character-by-Character Prefix Comparison"),
    (58, "Length of Last Word", "Easy", "Arrays & Strings", "Reverse Traversal", "Scan from End past Trailing Whitespace"),
    (67, "Add Binary", "Easy", "Arrays & Strings", "Carry Addition", "Bitwise String Addition from Least Significant Bit"),
    (151, "Reverse Words in a String", "Medium", "Arrays & Strings", "Two Pointers / Splitting", "Reverse Entire String then Reverse Words"),
    (383, "Ransom Note", "Easy", "Hashing", "Character Count Table", "Counter Subtraction Non-negative Check"),
    (389, "Find the Difference", "Easy", "Hashing", "XOR / Sum Difference", "Character Difference via Sum or XOR"),
    (409, "Longest Palindrome", "Easy", "Hashing", "Pair Counting", "Sum of Evens + Max 1 Odd Center"),
    (771, "Jewels and Stones", "Easy", "Hashing", "Hash Set Inclusion", "Set Membership Lookup in O(1)"),
    (1207, "Unique Number of Occurrences", "Easy", "Hashing", "Set of Frequencies", "Unique Values Count == Set of Values Count"),
    (1396, "Design Underground System", "Medium", "Hashing", "Nested Hash Maps", "Check-in Map & Route Aggregator"),

    # Two Pointers
    (80, "Remove Duplicates from Sorted Array II", "Medium", "Two Pointers", "At most 2 duplicates", "nums[i] != nums[k-2] Writer Pointer"),
    (287, "Find the Duplicate Number", "Medium", "Two Pointers", "Floyd's Cycle Detection on Array Values", "Tortoise and Hare on Array as Linked List"),
    (456, "132 Pattern", "Medium", "Stack & Queue", "Monotonic Stack", "Tracking Maximum S3 with Stack for S2"),
    (658, "Find K Closest Elements", "Medium", "Binary Search", "Binary Search on Window Left", "arr[mid] vs arr[mid+k] Comparison"),
    (881, "Boats to Save People", "Medium", "Two Pointers", "Greedy Pairing (Lightest + Heaviest)", "Pair Heaviest with Lightest if within Limit"),
    (925, "Long Pressed Name", "Easy", "Two Pointers", "Character Match with Repeats", "Typed Pointer Match with Previous Character"),
    (1750, "Minimum Length of String After Deleting Similar Ends", "Medium", "Two Pointers", "Prefix-Suffix Elimination", "Shrink Both Pointers on Matching Characters"),

    # Sliding Window
    (1423, "Maximum Points You Can Obtain from Cards", "Medium", "Sliding Window", "Inverted Window (Min Middle Subarray)", "Total Sum - Min Subarray of Size n-k"),
    (1493, "Longest Subarray of 1's After Deleting One Element", "Medium", "Sliding Window", "At most 1 Zero in Window", "Sliding Window Zero Count <= 1"),
    (1658, "Minimum Operations to Reduce X to Zero", "Medium", "Sliding Window", "Max Subarray with Target Sum", "Sliding Window Target = TotalSum - X"),
    (1838, "Frequency of the Most Frequent Element", "Medium", "Sliding Window", "Sorted Window Multiplication", "window_len * nums[r] - window_sum <= k"),

    # Stack & Queue
    (402, "Remove K Digits", "Medium", "Stack & Queue", "Monotonic Increasing Stack", "Smallest Lexicographical String via Pop"),
    (901, "Online Stock Span", "Medium", "Stack & Queue", "Monotonic Decreasing Stack (price, span)", "Cumulative Span on Stack Pop"),
    (907, "Sum of Subarray Minimums", "Medium", "Stack & Queue", "Monotonic Stack Previous/Next Smaller", "Count Contributions (i - prev) * (next - i) * arr[i]"),
    (946, "Validate Stack Sequences", "Medium", "Stack & Queue", "Greedy Stack Simulation", "Push and Greedily Pop on Target Match"),
    (1047, "Remove All Adjacent Duplicates In String", "Easy", "Stack & Queue", "Stack Peek Match", "Pop on Consecutive Duplicate"),
    (1209, "Remove All Adjacent Duplicates in String II", "Medium", "Stack & Queue", "Stack with Counts (char, count)", "Pop when Count Reaches K"),
    (1472, "Design Browser History", "Medium", "Stack & Queue", "Two Stacks / Doubly Linked List", "Forward & Back Stacks"),

    # Linked List
    (82, "Remove Duplicates from Sorted List II", "Medium", "Linked List", "Dummy Node with Predecessor Skip", "Lookahead Duplicate Detection and Rewire"),
    (92, "Reverse Linked List II", "Medium", "Linked List", "In-place Sublist Reversal", "Segment Reversal with Prev / Curr / Next"),
    (138, "Copy List with Random Pointer", "Medium", "Linked List", "Interweaving / Hash Map", "A->A'->B->B' Interleaving or Old->New Map"),
    (328, "Odd Even Linked List", "Medium", "Linked List", "Two Pointer Weaving", "Odd Head & Even Head Reconnection"),
    (2095, "Delete the Middle Node of a Linked List", "Medium", "Linked List", "Fast and Slow Pointers", "Slow Predecessor Link Rewire"),
    (2130, "Maximum Twin Sum of a Linked List", "Medium", "Linked List", "Midpoint + Reverse 2nd Half", "Simultaneous Traverse of Start and Reversed End"),

    # Binary Search
    (240, "Search a 2D Matrix II", "Medium", "Binary Search", "Top-Right / Bottom-Left Walk", "Eliminate Row or Column based on Target"),
    (275, "H-Index II", "Medium", "Binary Search", "Binary Search on Sorted Citations", "n - mid <= citations[mid]"),
    (540, "Single Element in a Sorted Array", "Medium", "Binary Search", "Even/Odd Index Pair Matching", "mid ^ 1 Pair Index Invariance"),
    (744, "Find Smallest Letter Greater Than Target", "Easy", "Binary Search", "Upper Bound Binary Search", "Modulo Wrap-around on Letters"),
    (852, "Peak Index in a Mountain Array", "Medium", "Binary Search", "Slope Gradient Ascent", "arr[mid] < arr[mid+1]"),
    (1283, "Find the Smallest Divisor Given a Threshold", "Medium", "Binary Search", "Binary Search on Divisor", "Sum of Ceilings <= Threshold"),
    (1482, "Minimum Number of Days to Make m Bouquets", "Medium", "Binary Search", "Binary Search on Day Feasibility", "Greedy Consecutive Bloom Counting"),

    # Backtracking
    (52, "N-Queens II", "Hard", "Recursion & Backtracking", "Bitmask Diagonal Verification", "Count Valid N-Queen Placements"),
    (93, "Restore IP Addresses", "Medium", "Recursion & Backtracking", "4-Segment String Partition", "Valid Octet (0-255, no leading zero)"),
    (216, "Combination Sum III", "Medium", "Recursion & Backtracking", "K Numbers Sum to N (1..9)", "Bounded Unique Digit Backtracking"),
    (491, "Non-decreasing Subsequences", "Medium", "Recursion & Backtracking", "HashSet per Level Duplicate Skip", "Non-decreasing Subsequence Builder"),

    # Trees & BST
    (103, "Binary Tree Zigzag Level Order Traversal", "Medium", "Trees & BST", "BFS with Deque / Alternate Flag", "Zigzag Level List Reversal"),
    (106, "Construct Binary Tree from Inorder and Postorder Traversal", "Medium", "Trees & BST", "Postorder Root Split", "Inorder Lookup with Postorder Decrement"),
    (108, "Convert Sorted Array to Binary Search Tree", "Easy", "Trees & BST", "Divide and Conquer Midpoint", "Root = mid, Left = 0..mid-1, Right = mid+1..end"),
    (111, "Minimum Depth of Binary Tree", "Easy", "Trees & BST", "Level-by-Level BFS Early Exit", "First Leaf Node Depth"),
    (113, "Path Sum II", "Medium", "Trees & BST", "DFS with Path Backtrack", "Collect All Root-to-Leaf Paths Summing to Target"),
    (114, "Flatten Binary Tree to Linked List", "Medium", "Trees & BST", "Reverse Postorder / Morris Traversal", "Right = prev, Left = None Rewiring"),
    (116, "Populating Next Right Pointers in Each Node", "Medium", "Trees & BST", "Level BFS / Next Pointer March", "node.left.next = node.right"),
    (129, "Sum Root to Leaf Numbers", "Medium", "Trees & BST", "DFS with Running Base-10 Sum", "curr_sum * 10 + node.val"),
    (173, "Binary Search Tree Iterator", "Medium", "Trees & BST", "Controlled Stack DFS", "Push All Left Nodes on Demand"),
    (437, "Path Sum III", "Medium", "Trees & BST", "Prefix Sum Hash Map on Tree", "Two Sum Technique on Tree DFS Ancestor Path"),
    (513, "Find Bottom Left Tree Value", "Medium", "Trees & BST", "Right-to-Left BFS", "Last Visited Node in BFS Queue"),
    (538, "Convert BST to Greater Tree", "Medium", "Trees & BST", "Reverse Inorder (Right-Root-Left)", "Accumulate Running Suffix Sum"),
    (662, "Maximum Width of Binary Tree", "Medium", "Trees & BST", "Level Order with Index Arithmetic", "Max(right_idx - left_idx + 1)"),
    (968, "Binary Tree Cameras", "Hard", "Trees & BST", "Greedy Bottom-Up Postorder", "State 0: Uncovered, 1: Covered, 2: Camera"),

    # Heaps
    (355, "Design Twitter", "Medium", "Heaps & Priority Queue", "K-Way Merge with Priority Queue", "Merge Recent Feeds from Followees"),
    (692, "Top K Frequent Words", "Medium", "Heaps & Priority Queue", "Custom Comparator Min-Heap", "Count Ascending + Lexicographical Descending"),
    (767, "Reorganize String", "Medium", "Heaps & Priority Queue", "Max-Heap Frequency Pairs", "Alternating Top-2 Frequency Placement"),
    (1054, "Distant Barcodes", "Medium", "Heaps & Priority Queue", "Max-Heap / Even-Odd Fill", "Fill Most Frequent on Alternate Indices"),

    # Greedy & Intervals
    (452, "Minimum Number of Arrows to Burst Balloons", "Medium", "Greedy", "Sort by End Point", "Activity Selection Stabbing"),
    (678, "Valid Parenthesis String", "Medium", "Greedy", "Min / Max Open Parentheses Range", "Track Feasible Low and High Open Count"),
    (1029, "Two City Scheduling", "Medium", "Greedy", "Sort by Cost Difference (costA - costB)", "Send Lowest Deltas to City A"),

    # Graphs
    (433, "Minimum Genetic Mutation", "Medium", "Graphs", "BFS on 4-Base Character Transitions", "Shortest Transformation in Mutation Bank"),
    (547, "Number of Provinces", "Medium", "Graphs", "Union-Find / DFS", "Connected Component Counting"),
    (797, "All Paths From Source to Target", "Medium", "Graphs", "DAG DFS Backtracking", "All Paths from 0 to N-1"),
    (802, "Find Eventual Safe States", "Medium", "Graphs", "Cycle Detection / Reverse Topological Sort", "Nodes Not in Any Cycle (3-state DFS)"),
    (841, "Keys and Rooms", "Medium", "Graphs", "BFS / DFS Visited Set", "All Rooms Reachable from Room 0"),
    (886, "Possible Bipartition", "Medium", "Graphs", "2-Coloring BFS / Dislike Graph", "Bipartite Graph Verification"),
    (997, "Find the Town Judge", "Easy", "Graphs", "In-degree & Out-degree Score", "In-degree == n-1 and Out-degree == 0"),
    (1091, "Shortest Path in Binary Matrix", "Medium", "Graphs", "8-Directional BFS", "Shortest Unweighted Path to (n-1, n-1)"),
    (1192, "Critical Connections in a Network", "Hard", "Graphs", "Tarjan's Bridge Finding Algorithm", "low[v] > disc[u] Edge Identification"),
    (1584, "Min Cost to Connect All Points", "Medium", "Graphs", "Prim's / Kruskal's MST Algorithm", "Minimum Spanning Tree on Complete Graph"),

    # DP
    (5, "Longest Palindromic Substring", "Medium", "Dynamic Programming", "Expand Around Center / 2D DP", "2D Boolean Palindrome Table"),
    (63, "Unique Paths II", "Medium", "Dynamic Programming", "2D DP with Obstacles", "Zero Ways for Obstacle Cells"),
    (96, "Unique Binary Search Trees", "Medium", "Dynamic Programming", "Catalan Number Recurrence", "dp[n] = sum(dp[i-1] * dp[n-i])"),
    (120, "Triangle", "Medium", "Dynamic Programming", "Bottom-Up Minimum Path DP", "dp[r][c] += min(dp[r+1][c], dp[r+1][c+1])"),
    (152, "Maximum Product Subarray", "Medium", "Dynamic Programming", "Track Min and Max Running Products", "Handle Negative Number Flips (swap min/max)"),
    (279, "Perfect Squares", "Medium", "Dynamic Programming", "Unbounded Knapsack / BFS", "dp[i] = 1 + min(dp[i - j*j])"),
    (309, "Best Time to Buy and Sell Stock with Cooldown", "Medium", "Dynamic Programming", "State Machine (Hold, Sold, Rest)", "Cooldown State Transitions"),
    (337, "House Robber III", "Medium", "Dynamic Programming", "Tree DP Tuple (rob_root, not_rob_root)", "Subtree Max Choice Propagation"),
    (377, "Combination Sum IV", "Medium", "Dynamic Programming", "Permutation Subproblem DP", "dp[i] += dp[i - num]"),
    (583, "Delete Operation for Two Strings", "Medium", "Dynamic Programming", "LCS Reduction", "m + n - 2 * LCS(s1, s2)"),
    (647, "Palindromic Substrings", "Medium", "Dynamic Programming", "Expand Around Center / 2D DP", "Count All Symmetric Expansions"),
    (718, "Maximum Length of Repeated Subarray", "Medium", "Dynamic Programming", "Longest Common Substring DP", "dp[i][j] = dp[i-1][j-1] + 1 on Match"),
    (1049, "Last Stone Weight II", "Medium", "Dynamic Programming", "0/1 Knapsack Partition", "Minimizing Total Sum Partition Difference"),
    (1137, "N-th Tribonacci Number", "Easy", "Dynamic Programming", "3-State Linear Recurrence", "dp[i] = dp[i-1] + dp[i-2] + dp[i-3]"),

    # Tries
    (1268, "Search Suggestions System", "Medium", "Tries", "Trie with Top-3 Lexicographical Storage", "Prefix Query Returning Top 3 Matching Words"),
    (1804, "Implement Trie II (Prefix Tree)", "Medium", "Tries", "Trie with Word Count & Prefix Count", "Integer Counter Increment on Insertion"),

    # Bit Manipulation & Math
    (7, "Reverse Integer", "Medium", "Bit Manipulation & Math", "Modulo Arithmetic with Overflow Guard", "rev = rev * 10 + x % 10 with INT_MAX Bounds"),
    (9, "Palindrome Number", "Easy", "Bit Manipulation & Math", "Half Number Reversal", "x == rev or x == rev // 10"),
    (66, "Plus One", "Easy", "Bit Manipulation & Math", "Carry In-place Addition", "Reverse Digits Array Carry Propagation"),
    (168, "Excel Sheet Column Title", "Easy", "Bit Manipulation & Math", "Base-26 1-Indexed Conversion", "(n - 1) % 26 Character Mapping"),
    (171, "Excel Sheet Column Number", "Easy", "Bit Manipulation & Math", "Base-26 Expansion", "ans * 26 + ord(c) - 64"),
    (202, "Happy Number", "Easy", "Bit Manipulation & Math", "Floyd's Cycle Detection / HashSet", "Sum of Squares Cycle Detection"),
    (258, "Add Digits", "Easy", "Bit Manipulation & Math", "Digital Root Formula", "1 + (n - 1) % 9 for n > 0"),
    (263, "Ugly Number", "Easy", "Bit Manipulation & Math", "Prime Factor Division (2, 3, 5)", "Repeated Division while Divisible"),
    (264, "Ugly Number II", "Medium", "Bit Manipulation & Math", "3-Pointer Multiples Merge", "min(ugly[p2]*2, ugly[p3]*3, ugly[p5]*5)"),
    (326, "Power of Three", "Easy", "Bit Manipulation & Math", "Max Power Divisibility", "3^19 % n == 0"),
    (342, "Power of Four", "Easy", "Bit Manipulation & Math", "Bit Masking & Odd Positions", "n > 0 and (n & (n-1)) == 0 and (n & 0x55555555) != 0"),
    (367, "Valid Perfect Square", "Easy", "Bit Manipulation & Math", "Binary Search / Newton's Method", "mid * mid == num"),
    (461, "Hamming Distance", "Easy", "Bit Manipulation & Math", "XOR + Set Bit Count", "bin(x ^ y).count('1')"),
    (476, "Number Complement", "Easy", "Bit Manipulation & Math", "Bitmask Inversion", "Bitwise NOT with Length Mask"),
    (693, "Binary Number with Alternating Bits", "Easy", "Bit Manipulation & Math", "Shift XOR All-1s Check", "n ^ (n >> 1) is 2^k - 1")
]

all_problems = list(PROBLEMS_DATA)
existing_numbers = {p["number"] for p in all_problems}

def make_leetcode_url(title: str) -> str:
    clean = title.lower().replace(" ", "-").replace("(", "").replace(")", "").replace("'", "")
    return f"https://leetcode.com/problems/{clean}/"

for p in all_problems:
    if "url" not in p:
        p["url"] = make_leetcode_url(p["title"])

for num, title, diff, topic, pattern, similar in EXTRA_PROBLEMS:
    if num not in existing_numbers:
        all_problems.append({
            "number": num,
            "title": title,
            "difficulty": diff,
            "topic": topic,
            "pattern": pattern,
            "similar_to": similar,
            "url": make_leetcode_url(title)
        })
        existing_numbers.add(num)

# Fill in additional classic LeetCode problems to guarantee 300+ total problems
ADDITIONAL_CURATED = [
    (12, "Integer to Roman", "Medium", "Arrays & Strings", "Greedy Value Mapping", "Largest Value Subtraction Table"),
    (13, "Roman to Integer", "Easy", "Arrays & Strings", "Subtraction Rule Check", "curr < next Subtract Pattern"),
    (43, "Multiply Strings", "Medium", "Arrays & Strings", "Position Digit Arithmetic", "res[i + j + 1] += d1 * d2"),
    (74, "Search a 2D Matrix", "Medium", "Binary Search", "Virtual Flattened 1D", "mid // n, mid % n Mapping"),
    (80, "Remove Duplicates from Sorted Array II", "Medium", "Two Pointers", "At Most Two Duplicates", "nums[i] != nums[idx-2]"),
    (165, "Compare Version Numbers", "Medium", "Two Pointers", "Chunk Comparison", "Dot-Separated Integer Walk"),
    (179, "Largest Number", "Medium", "Greedy", "Custom String Comparator", "a + b vs b + a Sort Order"),
    (186, "Reverse Words in a String II", "Medium", "Two Pointers", "In-place Reversal", "Reverse All then Reverse Each Word"),
    (204, "Count Primes", "Medium", "Bit Manipulation & Math", "Sieve of Eratosthenes", "Composite Marking in O(n log log n)"),
    (209, "Minimum Size Subarray Sum", "Medium", "Sliding Window", "Dynamic Expanding Window", "Shrink while sum >= target"),
    (217, "Contains Duplicate", "Easy", "Hashing", "HashSet Length Check", "len(nums) != len(set(nums))"),
    (220, "Contains Duplicate III", "Hard", "Sliding Window", "Ordered Set / Buckets", "Bucket ID = val // (t + 1)"),
    (224, "Basic Calculator", "Hard", "Stack & Queue", "Sign & Result Stack", "Parentheses Sign Multiplication Stack"),
    (227, "Basic Calculator II", "Medium", "Stack & Queue", "Precedence Stack", "Apply * and / immediately, + and - on stack"),
    (239, "Sliding Window Maximum", "Hard", "Stack & Queue", "Monotonic Decreasing Deque", "Store Indices with Greater Values"),
    (241, "Different Ways to Add Parentheses", "Medium", "Recursion & Backtracking", "Divide and Conquer", "Split at Operators and Recurse"),
    (253, "Meeting Rooms II", "Medium", "Intervals", "Min-Heap of Active End Times", "Track Concurrent Active Interval Peaks"),
    (260, "Single Number III", "Medium", "Bit Manipulation & Math", "Two Unique Numbers via XOR Split", "lsb = xor & -xor to Split into Two Groups"),
    (274, "H-Index", "Medium", "Arrays & Strings", "Bucket Sort on Citations", "Count Papers with >= i Citations"),
    (289, "Game of Life", "Medium", "Arrays & Strings", "2-Bit State Encoding", "Encode (Next << 1 | Curr) In-place"),
    (303, "Range Sum Query - Immutable", "Easy", "Arrays & Strings", "Prefix Sum Array", "prefix[r+1] - prefix[l]"),
    (304, "Range Sum Query 2D - Immutable", "Medium", "Arrays & Strings", "2D Prefix Sum Matrix", "P[r2][c2] - P[r1-1][c2] - P[r2][c1-1] + P[r1-1][c1-1]"),
    (316, "Remove Duplicate Letters", "Medium", "Stack & Queue", "Monotonic Stack with Last Occurrence", "Greedy Smallest Lexicographical Character"),
    (324, "Wiggle Sort II", "Medium", "Arrays & Strings", "Virtual Indexing with Median Partition", "Odd Indices with Larger, Even with Smaller"),
    (332, "Reconstruct Itinerary", "Hard", "Graphs", "Hierholzer's Algorithm for Eulerian Path", "Postorder DFS on Lexicographically Sorted Edges"),
    (341, "Flatten Nested List Iterator", "Medium", "Stack & Queue", "Generator / Stack Unpacking", "Unpack Sublists from End of Stack"),
    (349, "Intersection of Two Arrays", "Easy", "Hashing", "HashSet Intersection", "set(nums1) & set(nums2)"),
    (350, "Intersection of Two Arrays II", "Easy", "Hashing", "Frequency Map Intersection", "Minimum Common Frequency Count"),
    (368, "Largest Divisible Subset", "Medium", "Dynamic Programming", "Sorted Subsequence DP", "nums[i] % nums[j] == 0 with Path Reconstruction"),
    (376, "Wiggle Subsequence", "Medium", "Dynamic Programming", "Greedy Peak-Valley Counting", "Track up and down Alternating Directions"),
    (384, "Shuffle an Array", "Medium", "Arrays & Strings", "Fisher-Yates Shuffle", "Swap i with random in [i, n-1]"),
    (386, "Lexicographical Numbers", "Medium", "Recursion & Backtracking", "Preorder Traversal on 10-ary Tree", "curr * 10 DFS"),
    (390, "Elimination Game", "Medium", "Recursion & Backtracking", "Josephus-style Head Update", "head += step when from left or odd count"),
    (406, "Queue Reconstruction by Height", "Medium", "Greedy", "Sort Descending by Height + Insert by K", "Insert Tallest People First at Index K"),
    (412, "Fizz Buzz", "Easy", "Arrays & Strings", "Modulo Arithmetic", "Divisible by 3 and 5 Output Table"),
    (414, "Third Maximum Number", "Easy", "Arrays & Strings", "Top-3 Distinct Values Tracker", "Track 3 Maximums in Single Pass"),
    (415, "Add Strings", "Easy", "Arrays & Strings", "Character Addition with Carry", "Two Pointer Scan from String Ends"),
    (434, "Number of Segments in a String", "Easy", "Arrays & Strings", "Token Counting", "Count Non-space Preceded by Space"),
    (441, "Arranging Coins", "Easy", "Binary Search", "Quadratic Equation / BSearch", "k*(k+1)//2 <= n"),
    (442, "Find All Duplicates in an Array", "Medium", "Arrays & Strings", "Sign Inversion on Value Index", "nums[abs(x)-1] = -nums[abs(x)-1]"),
    (445, "Add Two Numbers II", "Medium", "Linked List", "Stack Reversal", "Push Linked List to Stacks and Add with Carry"),
    (450, "Delete Node in a BST", "Medium", "Trees & BST", "Inorder Successor Replacement", "Replace with Min Node in Right Subtree"),
    (453, "Minimum Moves to Equal Array Elements", "Medium", "Bit Manipulation & Math", "Math Invariant", "sum(nums) - n * min(nums)"),
    (462, "Minimum Moves to Equal Array Elements II", "Medium", "Bit Manipulation & Math", "Median Minimization", "Sum of abs(x - median)"),
    (463, "Island Perimeter", "Easy", "Graphs", "Grid Edge Counting", "4 * land_cells - 2 * adjacent_pairs"),
    (485, "Max Consecutive Ones", "Easy", "Arrays & Strings", "Running Streak Counter", "Reset Count on 0"),
    (492, "Construct the Rectangle", "Easy", "Bit Manipulation & Math", "Square Root Search", "Search Down from int(sqrt(area))"),
    (500, "Keyboard Row", "Easy", "Hashing", "Row Character Subset Check", "Set(word) is Subset of Row"),
    (501, "Find Mode in Binary Search Tree", "Easy", "Trees & BST", "Inorder Traversal with Max Frequency", "Inorder Running Frequency Tracking"),
    (504, "Base 7", "Easy", "Bit Manipulation & Math", "Radix Conversion", "Repeated Modulo 7 with Sign"),
    (506, "Relative Ranks", "Easy", "Arrays & Strings", "Sorting with Original Indices", "Rank Mapping with Medals"),
    (507, "Perfect Number", "Easy", "Bit Manipulation & Math", "Divisor Sum", "Sum of Divisors up to sqrt(n) == n"),
    (509, "Fibonacci Number", "Easy", "Dynamic Programming", "2-State Iteration", "a, b = b, a + b"),
    (520, "Detect Capital", "Easy", "Arrays & Strings", "Uppercase Count Logic", "count == len or count == 0 or (count == 1 and word[0].isupper())"),
    (521, "Longest Uncommon Subsequence I", "Easy", "Arrays & Strings", "String Equality Check", "Return -1 if a == b else max(len(a), len(b))"),
    (530, "Minimum Absolute Difference in BST", "Easy", "Trees & BST", "Inorder Traversal Difference", "min(curr - prev) in Sorted Order"),
    (541, "Reverse String II", "Easy", "Two Pointers", "Chunk Reversal (Step 2k)", "Reverse First K Characters Every 2K Chunks"),
    (551, "Student Attendance Record I", "Easy", "Arrays & Strings", "Substring & Count Check", "'LLL' not in s and s.count('A') < 2"),
    (557, "Reverse Words in a String III", "Easy", "Two Pointers", "Word-by-Word In-place Reverse", "Reverse Characters Between Spaces"),
    (559, "Maximum Depth of N-ary Tree", "Easy", "Trees & BST", "N-ary DFS", "1 + max(depth(child))"),
    (561, "Array Partition", "Easy", "Greedy", "Sort + Sum Even Indices", "Maximize Minimum Pairs by Sorting"),
    (563, "Binary Tree Tilt", "Easy", "Trees & BST", "Postorder Subtree Sum and Tilt", "tilt += abs(left_sum - right_sum)"),
    (572, "Subtree of Another Tree", "Easy", "Trees & BST", "Tree Pattern Match (SameTree DFS)", "root == subRoot or subtree(left) or subtree(right)"),
    (575, "Distribute Candies", "Easy", "Hashing", "Set Length Limit", "min(len(set(candyType)), len(candyType) // 2)"),
    (589, "N-ary Tree Preorder Traversal", "Easy", "Trees & BST", "Stack Preorder", "Push Children in Reverse Order"),
    (590, "N-ary Tree Postorder Traversal", "Easy", "Trees & BST", "Stack Postorder with Reverse", "Push Children and Reverse Final List"),
    (598, "Range Addition II", "Easy", "Arrays & Strings", "Min Bounding Box", "min(a) * min(b)"),
    (599, "Minimum Index Sum of Two Lists", "Easy", "Hashing", "Hash Map Index Sum", "Track Common Elements with Minimum Index Sum"),
    (606, "Construct String from Binary Tree", "Easy", "Trees & BST", "Preorder String Formatting", "Include Empty Left Parentheses if Right Exists"),
    (617, "Merge Two Binary Trees", "Easy", "Trees & BST", "Simultaneous Node Summation", "t1.val + t2.val with Child Branch Merging"),
    (628, "Maximum Product of Three Numbers", "Easy", "Bit Manipulation & Math", "Top 3 Max and Bottom 2 Min", "max(max1*max2*max3, min1*min2*max1)"),
    (637, "Average of Levels in Binary Tree", "Easy", "Trees & BST", "BFS Level Sum & Count", "Level Average Calculation"),
    (653, "Two Sum IV - Input is a BST", "Easy", "Trees & BST", "Inorder Two Pointers / HashSet", "HashSet Lookup on BST Traversal"),
    (657, "Robot Return to Origin", "Easy", "Arrays & Strings", "Coordinate Deltas", "U==D and L==R"),
    (671, "Second Minimum Node In a Binary Tree", "Easy", "Trees & BST", "DFS with Minimum Discrepancy", "First Value Strictly Greater than Root"),
    (674, "Longest Continuous Increasing Subsequence", "Easy", "Arrays & Strings", "Single Pass Streak", "Streak Reset when nums[i] <= nums[i-1]"),
    (682, "Baseball Game", "Easy", "Stack & Queue", "Simulation with Stack", "+, D, C Stack Operations"),
    (696, "Count Binary Substrings", "Easy", "Arrays & Strings", "Consecutive Group Lengths", "sum(min(group[i], group[i-1]))"),
    (697, "Degree of an Array", "Easy", "Hashing", "First & Last Occurrence Tracking", "Shortest Subarray with Max Frequency (r - l + 1)"),
    (700, "Search in a Binary Search Tree", "Easy", "Trees & BST", "BST Binary Choice", "val < node.val ? left : right"),
    (705, "Design HashSet", "Easy", "Hashing", "Bucket Array of Keys", "Mod Hash Bucket Lookup"),
    (709, "To Lower Case", "Easy", "Arrays & Strings", "ASCII Offset Conversion", "ord(c) + 32 for 'A'..'Z'"),
    (717, "1-bit and 2-bit Characters", "Easy", "Arrays & Strings", "Pointer Step (1 or 2)", "Step by 2 if bit==1 else 1"),
    (728, "Self Dividing Numbers", "Easy", "Bit Manipulation & Math", "Digit Modulo Check", "All Digits Divide Number"),
    (733, "Flood Fill", "Easy", "Graphs", "BFS / DFS Grid Fill", "4-Directional Color Replacement"),
    (746, "Min Cost Climbing Stairs", "Easy", "Dynamic Programming", "1D Min Step DP", "dp[i] = cost[i] + min(dp[i-1], dp[i-2])"),
    (747, "Largest Number At Least Twice of Others", "Easy", "Arrays & Strings", "Max and 2nd Max Comparison", "max1 >= 2 * max2"),
    (748, "Shortest Completing Word", "Easy", "Hashing", "Character Frequency Subset", "Word Contains All License Plate Letters"),
    (762, "Prime Number of Set Bits in Binary Representation", "Easy", "Bit Manipulation & Math", "Bit Count & Small Prime Set", "popcount(x) in {2, 3, 5, 7, 11, 13, 17, 19}"),
    (766, "Toeplitz Matrix", "Easy", "Arrays & Strings", "Diagonal Invariance", "matrix[r][c] == matrix[r-1][c-1]"),
    (783, "Minimum Distance Between BST Nodes", "Easy", "Trees & BST", "Inorder Traversal Diff", "BST Inorder Adjacent Difference"),
    (811, "Subdomain Visit Count", "Medium", "Hashing", "Domain Suffix Split", "Count Visits for All Suffix Subdomains"),
    (812, "Largest Triangle Area", "Easy", "Bit Manipulation & Math", "Shoelace Formula", "0.5 * abs(x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2))"),
    (819, "Most Common Word", "Easy", "Hashing", "Regex Tokenization + Ban Set", "Max Frequency Non-Banned Word"),
    (821, "Shortest Distance to a Character", "Easy", "Two Pointers", "Left and Right Passes", "min(abs(i - left_idx), abs(i - right_idx))"),
    (824, "Goat Latin", "Easy", "Arrays & Strings", "String Transformation Rules", "Vowel / Consonant Rule + Index 'a' Count"),
    (830, "Positions of Large Groups", "Easy", "Two Pointers", "Streak Length >= 3", "Group Length Interval Collection"),
    (832, "Flipping an Image", "Easy", "Two Pointers", "Horizontal Reverse + Bit Inversion", "row[l] ^ 1, row[r] ^ 1"),
    (836, "Rectangle Overlap", "Easy", "Bit Manipulation & Math", "1D Overlap Conditions", "rec1.x1 < rec2.x2 and rec1.x2 > rec2.x1 and ..."),
    (859, "Buddy Strings", "Easy", "Arrays & Strings", "Single Swap Match", "Differ at Exactly 2 Indices with Cross Equal"),
    (867, "Transpose Matrix", "Easy", "Arrays & Strings", "Matrix Flipping", "res[c][r] = matrix[r][c]"),
    (868, "Binary Gap", "Easy", "Bit Manipulation & Math", "Last Set Bit Index", "Max Distance Between Consecutive 1s"),
    (872, "Leaf-Similar Trees", "Easy", "Trees & BST", "DFS Leaf Collection", "Leaves(t1) == Leaves(t2)"),
    (876, "Middle of the Linked List", "Easy", "Linked List", "Fast and Slow Pointers", "Fast 2x, Slow 1x Midpoint Discovery"),
    (883, "Projection Area of 3D Shapes", "Easy", "Arrays & Strings", "Top, Front, Side Max Projections", "XY (>0) + Row Maxes + Col Maxes"),
    (884, "Uncommon Words from Two Sentences", "Easy", "Hashing", "Combined Word Frequency == 1", "Word Occurs Exactly Once in (A + B)"),
    (888, "Fair Candy Swap", "Easy", "Hashing", "Equation Solving with HashSet", "target_diff = (sumA - sumB) // 2"),
    (892, "Surface Area of 3D Shapes", "Easy", "Arrays & Strings", "Grid Height Adjacency Penalty", "6 * v - 2 * (overlap with adjacent)"),
    (897, "Increasing Order Search Tree", "Easy", "Trees & BST", "Inorder Tree Relinking", "curr.right = node, node.left = None"),
    (908, "Smallest Range I", "Easy", "Arrays & Strings", "Extrema Shift Math", "max(0, max_val - min_val - 2 * k)"),
    (914, "X of a Kind in a Deck of Cards", "Easy", "Bit Manipulation & Math", "GCD of Frequencies", "reduce(gcd, counts.values()) >= 2"),
    (917, "Reverse Only Letters", "Easy", "Two Pointers", "isalpha() Inward Scan", "Two Pointers Letter Swapping"),
    (929, "Unique Email Addresses", "Easy", "Hashing", "Rule Filtering (ignore '.', ignore '+...')", "Normalize Local Name + Domain to HashSet"),
    (933, "Number of Recent Calls", "Easy", "Stack & Queue", "Queue Time Window Purge", "Pop while q[0] < t - 3000"),
    (938, "Range Sum of BST", "Easy", "Trees & BST", "Pruned BST Traversal", "Prune Left if val < low, Prune Right if val > high"),
    (942, "DI String Match", "Easy", "Two Pointers", "Greedy Low/High Range", "'I' -> lo++, 'D' -> hi--"),
    (944, "Delete Columns to Make Sorted", "Easy", "Arrays & Strings", "Column Monotonicity Scan", "Column Non-decreasing Check"),
    (953, "Verifying an Alien Dictionary", "Easy", "Hashing", "Lexicographical Alien Order", "Custom Alphabet Rank Comparison"),
    (961, "N-Repeated Element in Size 2N Array", "Easy", "Hashing", "Distance <= 3 Duplicate Check", "Any element repeating within distance 3"),
    (965, "Univalued Binary Tree", "Easy", "Trees & BST", "DFS Value Invariance", "All Node Values Equal Root Value")
]

for item in ADDITIONAL_CURATED:
    num, title, diff, topic, pattern, similar = item
    if num not in existing_numbers:
        all_problems.append({
            "number": num,
            "title": title,
            "difficulty": diff,
            "topic": topic,
            "pattern": pattern,
            "similar_to": similar,
            "url": make_leetcode_url(title)
        })
        existing_numbers.add(num)

# Ensure URLs are properly set for all
for p in all_problems:
    if "url" not in p:
        p["url"] = make_leetcode_url(p["title"])

# Sort problems by number
all_problems.sort(key=lambda x: x["number"])

# Save problems.json
problems_path = os.path.join(DATA_DIR, "problems.json")
with open(problems_path, "w", encoding="utf-8") as f:
    json.dump(all_problems, f, indent=2)

print(f"Generated {len(all_problems)} curated problems in {problems_path}")

# =========================================================================
# GENERATE DETAILED CHEAT SHEETS FOR ALL 16 TOPICS
# =========================================================================

CHEATSHEETS_DATA = {
    "Arrays & Strings": {
        "topic": "Arrays & Strings",
        "when_to_use": [
            "Contiguous sequences, strings, or 1D/2D grids.",
            "Keywords: 'in-place', 'rotate', 'subarray', 'prefix', 'permutations', 'spiral'.",
            "Optimal space requirement O(1) auxiliary memory.",
            "Prefix sums for constant time range queries sum(l..r)."
        ],
        "core_idea": "Leverage index mathematics, prefix accumulations, and in-place transformations (like reversals and matrix rotations) to avoid allocating secondary memory buffers.",
        "code_templates": {
            "python": '''# 1. Prefix Sum Template
def build_prefix_sum(nums: list[int]) -> list[int]:
    prefix = [0] * (len(nums) + 1)
    for i, x in enumerate(nums):
        prefix[i + 1] = prefix[i] + x
    return prefix

# Query range sum [l, r] (0-indexed)
def query_range(prefix: list[int], l: int, r: int) -> int:
    return prefix[r + 1] - prefix[l]

# 2. Kadane's Algorithm (Max Subarray)
def max_subarray(nums: list[int]) -> int:
    max_so_far = current_max = nums[0]
    for x in nums[1:]:
        current_max = max(x, current_max + x)
        max_so_far = max(max_so_far, current_max)
    return max_so_far''',
            "cpp": '''// 1. Prefix Sum Template
#include <vector>
#include <numeric>
#include <algorithm>

std::vector<int> buildPrefixSum(const std::vector<int>& nums) {
    std::vector<int> prefix(nums.size() + 1, 0);
    for (size_t i = 0; i < nums.size(); ++i) {
        prefix[i + 1] = prefix[i] + nums[i];
    }
    return prefix;
}

// 2. Kadane's Algorithm
int maxSubArray(const std::vector<int>& nums) {
    int maxSoFar = nums[0], currentMax = nums[0];
    for (size_t i = 1; i < nums.size(); ++i) {
        currentMax = std::max(nums[i], currentMax + nums[i]);
        maxSoFar = std::max(maxSoFar, currentMax);
    }
    return maxSoFar;
}''',
            "java": '''// 1. Prefix Sum Template
public class ArrayTemplates {
    public static int[] buildPrefixSum(int[] nums) {
        int[] prefix = new int[nums.length + 1];
        for (int i = 0; i < nums.length; i++) {
            prefix[i + 1] = prefix[i] + nums[i];
        }
        return prefix;
    }

    // 2. Kadane's Algorithm
    public static int maxSubArray(int[] nums) {
        int maxSoFar = nums[0], currentMax = nums[0];
        for (int i = 1; i < nums.length; i++) {
            currentMax = Math.max(nums[i], currentMax + nums[i]);
            maxSoFar = Math.max(maxSoFar, currentMax);
        }
        return maxSoFar;
    }
}'''
        },
        "formulas_and_identities": [
            "Prefix Sum: sum(l..r) = P[r] - P[l-1] (or P[r+1] - P[l] with 1-indexed padding)",
            "2D Prefix Sum: S(r1..r2, c1..c2) = P[r2][c2] - P[r1-1][c2] - P[r2][c1-1] + P[r1-1][c1-1]",
            "Cyclic Array Shift: new_index = (i + k) % n",
            "Matrix Transpose: swap(matrix[i][j], matrix[j][i]) for j > i",
            "Boyer-Moore Majority Vote: count == 0 ? (candidate = x, count = 1) : (x == candidate ? count++ : count--)"
        ],
        "complexity_table": [
            {"operation": "Prefix Sum Construction", "time": "O(n)", "space": "O(n)"},
            {"operation": "Range Query with Prefix Sum", "time": "O(1)", "space": "O(1)"},
            {"operation": "Kadane's Algorithm", "time": "O(n)", "space": "O(1)"},
            {"operation": "In-place Array Rotation", "time": "O(n)", "space": "O(1)"}
        ],
        "common_mistakes": [
            "Off-by-one errors when setting up 1-indexed prefix sum arrays.",
            "Integer overflow when calculating sums of large integer arrays (use 64-bit int / long).",
            "Modifying matrix dimensions in-place without checking row vs column bounds.",
            "Forgetting to handle empty arrays or arrays of length 1."
        ],
        "pattern_to_problem_map": [
            {"number": 1, "title": "Two Sum"},
            {"number": 53, "title": "Maximum Subarray"},
            {"number": 48, "title": "Rotate Image"},
            {"number": 54, "title": "Spiral Matrix"},
            {"number": 169, "title": "Majority Element"},
            {"number": 238, "title": "Product of Array Except Self"},
            {"number": 560, "title": "Subarray Sum Equals K"}
        ],
        "quick_revision": [
            "Use Prefix Sum for O(1) subarray sum queries.",
            "Use Kadane's algorithm to find maximum contiguous subarray sum in O(n) time and O(1) space.",
            "Rotate an array by k steps via 3 reversals: reverse all, reverse first k, reverse remaining.",
            "Rotate a matrix 90 degrees clockwise by transposing then reversing each row.",
            "Boyer-Moore voting algorithm finds the majority element (> n/2) in O(n) time and O(1) space."
        ]
    },

    "Hashing": {
        "topic": "Hashing",
        "when_to_use": [
            "Keywords: 'frequency', 'anagram', 'duplicates', 'lookup in O(1)', 'group by signature'.",
            "When you need to pair elements, detect cycles, or count occurrences.",
            "Associating keys with metadata or finding sequence boundaries."
        ],
        "core_idea": "Transform elements into canonical hash keys (e.g. sorted strings, count tuples) for instant O(1) lookup and frequency aggregation.",
        "code_templates": {
            "python": '''# 1. Frequency Table & Group Anagrams
from collections import defaultdict

def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    for s in strs:
        # Canonical signature: count of each character or sorted string
        key = tuple(sorted(s))
        groups[key].append(s)
    return list(groups.values())

# 2. Longest Consecutive Sequence in O(n)
def longest_consecutive(nums: list[int]) -> int:
    num_set = set(nums)
    longest = 0
    for x in num_set:
        # Only start counting if x is the beginning of a streak
        if x - 1 not in num_set:
            current_num = x
            current_streak = 1
            while current_num + 1 in num_set:
                current_num += 1
                current_streak += 1
            longest = max(longest, current_streak)
    return longest''',
            "cpp": '''#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <algorithm>

std::vector<std::vector<std::string>> groupAnagrams(std::vector<std::string>& strs) {
    std::unordered_map<std::string, std::vector<std::string>> map;
    for (const auto& s : strs) {
        std::string key = s;
        std::sort(key.begin(), key.end());
        map[key].push_back(s);
    }
    std::vector<std::vector<std::string>> result;
    for (auto& pair : map) {
        result.push_back(std::move(pair.second));
    }
    return result;
}''',
            "java": '''import java.util.*;

public class HashTemplates {
    public List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> map = new HashMap<>();
        for (String s : strs) {
            char[] chars = s.toCharArray();
            Arrays.sort(chars);
            String key = new String(chars);
            map.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
        }
        return new ArrayList<>(map.values());
    }
}'''
        },
        "formulas_and_identities": [
            "Complement Lookup: complement = target - nums[i]",
            "Prefix Sum Remainder: (sum[j] - sum[i]) % k == 0 <=> sum[j] % k == sum[i] % k",
            "Total Subarray Combinations from Frequencies: count = freq * (freq - 1) / 2"
        ],
        "complexity_table": [
            {"operation": "Average Lookup / Insert", "time": "O(1)", "space": "O(1)"},
            {"operation": "Worst Case Hash Collision", "time": "O(n)", "space": "O(1)"},
            {"operation": "Group Anagrams by Sorting", "time": "O(n * k log k)", "space": "O(n * k)"}
        ],
        "common_mistakes": [
            "Using mutable types (like lists) as keys in Python dictionaries.",
            "Not handling negative remainders when doing modulo hash tracking `(sum % k + k) % k`.",
            "Assuming hash iteration order is deterministic across environments."
        ],
        "pattern_to_problem_map": [
            {"number": 49, "title": "Group Anagrams"},
            {"number": 128, "title": "Longest Consecutive Sequence"},
            {"number": 242, "title": "Valid Anagram"},
            {"number": 560, "title": "Subarray Sum Equals K"},
            {"number": 974, "title": "Subarray Sums Divisible by K"}
        ],
        "quick_revision": [
            "Use HashSet to verify membership in O(1) time.",
            "Subarray sum equals k uses prefix sum map tracking `prefix_sum - k`.",
            "Longest Consecutive Sequence: only start streak from numbers where `num - 1` is not in set.",
            "Bijective mappings require two maps (forward and backward) to prevent multi-to-one collisions.",
            "Always normalize modulo remainders in negative arithmetic."
        ]
    },

    "Two Pointers": {
        "topic": "Two Pointers",
        "when_to_use": [
            "Keywords: 'sorted array', 'pair with target sum', 'palindrome', 'in-place partition', 'container with water'.",
            "When searching pairs or triplets in sorted sequences in O(n) without hash map overhead.",
            "Partitioning arrays in O(n) time and O(1) space (e.g. Dutch National Flag)."
        ],
        "core_idea": "Position pointers at key boundaries (e.g., opposite ends or fast/slow speeds) and move them inward or forward monotonically based on comparison invariants.",
        "code_templates": {
            "python": '''# 1. Opposite Ends Two Pointers (e.g., 2Sum on Sorted Array)
def two_sum_sorted(numbers: list[int], target: int) -> list[int]:
    left, right = 0, len(numbers) - 1
    while left < right:
        curr_sum = numbers[left] + numbers[right]
        if curr_sum == target:
            return [left + 1, right + 1] # 1-indexed
        elif curr_sum < target:
            left += 1
        else:
            right -= 1
    return []

# 2. Dutch National Flag (3-way partition in-place)
def sort_colors(nums: list[int]) -> None:
    low, mid, high = 0, 0, len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1''',
            "cpp": '''#include <vector>

void sortColors(std::vector<int>& nums) {
    int low = 0, mid = 0, high = nums.size() - 1;
    while (mid <= high) {
        if (nums[mid] == 0) {
            std::swap(nums[low++], nums[mid++]);
        } else if (nums[mid] == 1) {
            mid++;
        } else {
            std::swap(nums[mid], nums[high--]);
        }
    }
}''',
            "java": '''public class TwoPointerTemplates {
    public void sortColors(int[] nums) {
        int low = 0, mid = 0, high = nums.length - 1;
        while (mid <= high) {
            if (nums[mid] == 0) {
                int temp = nums[low];
                nums[low++] = nums[mid];
                nums[mid++] = temp;
            } else if (nums[mid] == 1) {
                mid++;
            } else {
                int temp = nums[mid];
                nums[mid] = nums[high];
                nums[high--] = temp;
            }
        }
    }
}'''
        },
        "formulas_and_identities": [
            "Container with Most Water Area: area = (right - left) * min(height[left], height[right])",
            "Floyd's Cycle Detection Phase 1: fast moves 2 steps, slow moves 1 step until fast == slow",
            "Floyd's Cycle Detection Phase 2: reset slow to head, advance both by 1 step until they meet at loop entry",
            "3-Way Partition Invariant: [0..low-1] is 0, [low..mid-1] is 1, [high+1..n-1] is 2"
        ],
        "complexity_table": [
            {"operation": "Opposite Ends Convergence", "time": "O(n)", "space": "O(1)"},
            {"operation": "3Sum (Sort + Two Pointers)", "time": "O(n^2)", "space": "O(1) / O(log n)"},
            {"operation": "Trapping Rain Water (Two Pointers)", "time": "O(n)", "space": "O(1)"}
        ],
        "common_mistakes": [
            "Forgetting to skip duplicate elements in 3Sum/4Sum, leading to non-unique answer sets.",
            "Advancing `mid` pointer after swapping with `high` in Dutch National Flag (the swapped value from high hasn't been checked yet).",
            "Loop condition `left < right` vs `left <= right` confusion."
        ],
        "pattern_to_problem_map": [
            {"number": 11, "title": "Container With Most Water"},
            {"number": 15, "title": "3Sum"},
            {"number": 42, "title": "Trapping Rain Water"},
            {"number": 75, "title": "Sort Colors"},
            {"number": 167, "title": "Two Sum II - Input Array Is Sorted"}
        ],
        "quick_revision": [
            "Sort the array first if two-sum / three-sum problem is not already sorted.",
            "Always skip duplicates after finding a valid match in kSum problems.",
            "In Dutch National Flag: don't increment mid after swapping with high.",
            "Trapping Rain Water can be solved in O(1) space with two pointers tracking leftMax and rightMax.",
            "Floyd's cycle detection locates loop start when reset pointer meets slow pointer at step speed 1."
        ]
    },

    "Sliding Window": {
        "topic": "Sliding Window",
        "when_to_use": [
            "Keywords: 'longest / shortest substring with condition', 'subarray with sum / product k', 'at most k distinct characters'.",
            "Contiguous sequences where adding an element expands the window and removing from left restores validity.",
            "Exact K condition: convert `Exact(K) = AtMost(K) - AtMost(K - 1)`."
        ],
        "core_idea": "Maintain a dynamic or fixed-length window `[left, right]`. Expand `right` to include elements and shrink `left` once the window invariant is violated.",
        "code_templates": {
            "python": '''# 1. Dynamic Window Template (e.g., Longest Substring Without Repeating)
def length_of_longest_substring(s: str) -> int:
    last_seen = {}
    left = 0
    max_len = 0
    for right, char in enumerate(s):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1
        last_seen[char] = right
        max_len = max(max_len, right - left + 1)
    return max_len

# 2. Minimum Window Substring Template
from collections import Counter
def min_window(s: str, t: str) -> str:
    target_counts = Counter(t)
    window_counts = {}
    required = len(target_counts)
    formed = 0
    left = 0
    ans = (float("inf"), None, None) # (len, left, right)

    for right, c in enumerate(s):
        window_counts[c] = window_counts.get(c, 0) + 1
        if c in target_counts and window_counts[c] == target_counts[c]:
            formed += 1

        while left <= right and formed == required:
            if right - left + 1 < ans[0]:
                ans = (right - left + 1, left, right)
            char_l = s[left]
            window_counts[char_l] -= 1
            if char_l in target_counts and window_counts[char_l] < target_counts[char_l]:
                formed -= 1
            left += 1
    return "" if ans[0] == float("inf") else s[ans[1] : ans[2] + 1]''',
            "cpp": '''#include <string>
#include <vector>
#include <algorithm>

int lengthOfLongestSubstring(const std::string& s) {
    std::vector<int> lastIndex(256, -1);
    int maxLen = 0, left = 0;
    for (int right = 0; right < (int)s.size(); ++right) {
        if (lastIndex[(unsigned char)s[right]] >= left) {
            left = lastIndex[(unsigned char)s[right]] + 1;
        }
        lastIndex[(unsigned char)s[right]] = right;
        maxLen = std::max(maxLen, right - left + 1);
    }
    return maxLen;
}''',
            "java": '''import java.util.Arrays;

public class SlidingWindowTemplates {
    public int lengthOfLongestSubstring(String s) {
        int[] lastIndex = new int[256];
        Arrays.fill(lastIndex, -1);
        int maxLen = 0, left = 0;
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            if (lastIndex[c] >= left) {
                left = lastIndex[c] + 1;
            }
            lastIndex[c] = right;
            maxLen = Math.max(maxLen, right - left + 1);
        }
        return maxLen;
    }
}'''
        },
        "formulas_and_identities": [
            "Current Window Length: length = right - left + 1",
            "Count of Valid Subarrays Ending at right: count = right - left + 1",
            "Exact K Decomposition: Exact(K) = AtMost(K) - AtMost(K - 1)",
            "Character Replacement Validity: (window_length - max_frequency) <= k"
        ],
        "complexity_table": [
            {"operation": "Dynamic Sliding Window", "time": "O(n)", "space": "O(k) where k is alphabet size"},
            {"operation": "Fixed Size Sliding Window", "time": "O(n)", "space": "O(1)"},
            {"operation": "Exact(K) via Dual AtMost(K)", "time": "O(n)", "space": "O(k)"}
        ],
        "common_mistakes": [
            "Shrinking the window with `if` instead of `while` when multiple invalid elements exist.",
            "Forgetting to update the `left` pointer after checking previous character index.",
            "Off-by-one errors when computing subarray window length `(right - left + 1)`."
        ],
        "pattern_to_problem_map": [
            {"number": 3, "title": "Longest Substring Without Repeating Characters"},
            {"number": 76, "title": "Minimum Window Substring"},
            {"number": 209, "title": "Minimum Size Subarray Sum"},
            {"number": 424, "title": "Longest Repeating Character Replacement"},
            {"number": 992, "title": "Subarrays with K Different Integers"}
        ],
        "quick_revision": [
            "Window length is always `r - l + 1`.",
            "Number of valid subarrays ending at index `r` is `r - l + 1`.",
            "Convert 'Subarrays with exactly K distinct' into `AtMost(K) - AtMost(K - 1)`.",
            "In character replacement: window is valid if `window_length - max_freq <= k`.",
            "Both left and right pointers only move forward, guaranteeing overall O(n) amortized runtime."
        ]
    },

    "Stack & Queue": {
        "topic": "Stack & Queue",
        "when_to_use": [
            "Keywords: 'next greater / smaller element', 'valid parentheses', 'histogram area', 'sliding window maximum', 'reverse polish notation'.",
            "Nested or hierarchical structures where innermost subproblems resolve first (LIFO).",
            "Maintaining monotonically increasing or decreasing sequences."
        ],
        "core_idea": "Use stacks for LIFO state backtracking and monotonic boundary tracking; use deques for FIFO window maximums in O(1) amortized time.",
        "code_templates": {
            "python": '''# 1. Monotonic Decreasing Stack (Next Greater Element)
def next_greater_element(nums: list[int]) -> list[int]:
    n = len(nums)
    result = [-1] * n
    stack = [] # stores indices
    for i in range(n):
        while stack and nums[stack[-1]] < nums[i]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)
    return result

# 2. Largest Rectangle in Histogram in O(n)
def largest_rectangle_area(heights: list[int]) -> int:
    stack = [] # indices of increasing heights
    max_area = 0
    # Append 0 height sentinel to flush remaining items at the end
    h = heights + [0]
    for i, curr_h in enumerate(h):
        while stack and h[stack[-1]] > curr_h:
            height = h[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    return max_area''',
            "cpp": '''#include <vector>
#include <stack>
#include <algorithm>

int largestRectangleArea(std::vector<int>& heights) {
    heights.push_back(0); // Sentinel
    std::stack<int> s;
    int maxArea = 0;
    for (int i = 0; i < (int)heights.size(); ++i) {
        while (!s.empty() && heights[s.top()] > heights[i]) {
            int h = heights[s.top()];
            s.pop();
            int w = s.empty() ? i : i - s.top() - 1;
            maxArea = std::max(maxArea, h * w);
        }
        s.push(i);
    }
    return maxArea;
}''',
            "java": '''import java.util.ArrayDeque;
import java.util.Deque;

public class StackTemplates {
    public int largestRectangleArea(int[] heights) {
        Deque<Integer> stack = new ArrayDeque<>();
        int maxArea = 0;
        int n = heights.length;
        for (int i = 0; i <= n; i++) {
            int currH = (i == n) ? 0 : heights[i];
            while (!stack.isEmpty() && heights[stack.peek()] > currH) {
                int h = heights[stack.pop()];
                int w = stack.isEmpty() ? i : i - stack.peek() - 1;
                maxArea = Math.max(maxArea, h * w);
            }
            stack.push(i);
        }
        return maxArea;
    }
}'''
        },
        "formulas_and_identities": [
            "Histogram Bar Width: width = i if stack.empty() else (i - stack.top() - 1)",
            "Circular Array Modulo Traversal: process indices from 0 to 2*n - 1 using `i % n`",
            "Sliding Window Maximum Monotonic Deque: remove elements smaller than incoming and out of index range `i - k + 1`"
        ],
        "complexity_table": [
            {"operation": "Monotonic Stack Pass", "time": "O(n)", "space": "O(n)"},
            {"operation": "Sliding Window Deque", "time": "O(n)", "space": "O(k)"},
            {"operation": "MinStack Push/Pop/GetMin", "time": "O(1)", "space": "O(n)"}
        ],
        "common_mistakes": [
            "Storing values on monotonic stack instead of indices (indices give distance/width).",
            "Not clearing the remaining elements on stack after the loop (or forgetting a sentinel 0).",
            "Using recursion when stack depth exceeds OS limit."
        ],
        "pattern_to_problem_map": [
            {"number": 20, "title": "Valid Parentheses"},
            {"number": 84, "title": "Largest Rectangle in Histogram"},
            {"number": 155, "title": "Min Stack"},
            {"number": 239, "title": "Sliding Window Maximum"},
            {"number": 739, "title": "Daily Temperatures"}
        ],
        "quick_revision": [
            "Monotonic stack stores INDICES, enabling width calculations `i - stack.peek() - 1`.",
            "Next Greater Element uses monotonic decreasing stack; pop on larger element.",
            "Histogram largest rectangle uses sentinel `0` at end to pop all remaining bars.",
            "Circular array problems iterate `2 * n` times with `i % n`.",
            "Sliding window maximum uses deque storing indices in decreasing order of values."
        ]
    },

    "Linked List": {
        "topic": "Linked List",
        "when_to_use": [
            "Keywords: 'reverse sublist', 'detect cycle', 'merge k sorted lists', 'reorder list', 'middle node'.",
            "Sequential node pointer rearrangements with O(1) auxiliary space.",
            "Fast and Slow pointer techniques (tortoise and hare)."
        ],
        "core_idea": "Employ dummy sentinel heads to simplify edge cases and manage pointer rewiring via 3-pointer iterations (`prev`, `curr`, `next`) or fast/slow splits.",
        "code_templates": {
            "python": '''class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# 1. Reverse Linked List In-Place
def reverse_list(head: ListNode) -> ListNode:
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev

# 2. Fast & Slow Pointer (Find Middle Node)
def find_middle(head: ListNode) -> ListNode:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow''',
            "cpp": '''struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(nullptr) {}
};

ListNode* reverseList(ListNode* head) {
    ListNode* prev = nullptr;
    ListNode* curr = head;
    while (curr) {
        ListNode* nxt = curr->next;
        curr->next = prev;
        prev = curr;
        curr = nxt;
    }
    return prev;
}''',
            "java": '''public class LinkedListTemplates {
    public static class ListNode {
        int val;
        ListNode next;
        ListNode(int x) { val = x; }
    }

    public ListNode reverseList(ListNode head) {
        ListNode prev = null, curr = head;
        while (curr != null) {
            ListNode next = curr.next;
            curr.next = prev;
            prev = curr;
            curr = next;
        }
        return prev;
    }
}'''
        },
        "formulas_and_identities": [
            "Dummy Head Invariant: dummy.next = head ensures head modifications (deletion/insertion) require no special if-branches",
            "Cycle Length: after fast meets slow, keep slow fixed and move fast by 1 until meeting again",
            "Palindrome List: Find Mid -> Reverse 2nd Half -> Compare 1st & 2nd Halves"
        ],
        "complexity_table": [
            {"operation": "Reverse Linked List", "time": "O(n)", "space": "O(1)"},
            {"operation": "Detect Cycle (Floyd)", "time": "O(n)", "space": "O(1)"},
            {"operation": "Merge K Sorted Lists (Heap)", "time": "O(N log k)", "space": "O(k)"}
        ],
        "common_mistakes": [
            "Losing reference to `curr.next` before overwriting pointer during reversal.",
            "Null pointer dereference on `fast.next.next` when `fast.next` is null.",
            "Creating circular references by failing to set the tail's next pointer to null."
        ],
        "pattern_to_problem_map": [
            {"number": 21, "title": "Merge Two Sorted Lists"},
            {"number": 23, "title": "Merge k Sorted Lists"},
            {"number": 141, "title": "Linked List Cycle"},
            {"number": 143, "title": "Reorder List"},
            {"number": 206, "title": "Reverse Linked List"}
        ],
        "quick_revision": [
            "Always create a `dummy` node (`dummy.next = head`) to avoid head deletion edge cases.",
            "Reverse linked list: `nxt = curr.next; curr.next = prev; prev = curr; curr = nxt`.",
            "Find middle: `while fast and fast.next: slow = slow.next; fast = fast.next.next`.",
            "Reorder List: Find middle -> Reverse second half -> Interleave two halves.",
            "Merge K Sorted Lists uses a Min-Heap of size K containing the current head of each list."
        ]
    },

    "Binary Search": {
        "topic": "Binary Search",
        "when_to_use": [
            "Keywords: 'sorted array', 'search in rotated array', 'minimize maximum / maximize minimum', 'find peak', 'capacity to ship'.",
            "Monotonic search space (T, T, T, F, F) -> find transition boundary in O(log n).",
            "Binary search on the answer: when feasibility predicate `is_possible(x)` is monotonic."
        ],
        "core_idea": "Halve the search space at each iteration by testing a predicate on the midpoint `mid = lo + (hi - lo) // 2`.",
        "code_templates": {
            "python": '''# 1. Standard Template (First True / Leftmost Insertion)
def binary_search_leftmost(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    ans = -1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] >= target:
            if nums[mid] == target:
                ans = mid
            hi = mid - 1 # Try to find earlier match
        else:
            lo = mid + 1
    return ans

# 2. Binary Search on Answer Template (e.g. Koko Bananas)
def min_eating_speed(piles: list[int], h: int) -> int:
    def can_finish(speed: int) -> bool:
        hours = sum((p + speed - 1) // speed for p in piles)
        return hours <= h

    lo, hi = 1, max(piles)
    ans = hi
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if can_finish(mid):
            ans = mid
            hi = mid - 1 # Try smaller speed
        else:
            lo = mid + 1
    return ans''',
            "cpp": '''#include <vector>
#include <numeric>
#include <algorithm>

int minEatingSpeed(const std::vector<int>& piles, int h) {
    auto canFinish = [&](int speed) {
        long long hours = 0;
        for (int p : piles) {
            hours += (p + speed - 1) / speed;
        }
        return hours <= h;
    };

    int lo = 1, hi = *std::max_element(piles.begin(), piles.end());
    int ans = hi;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (canFinish(mid)) {
            ans = mid;
            hi = mid - 1;
        } else {
            lo = mid + 1;
        }
    }
    return ans;
}''',
            "java": '''public class BinarySearchTemplates {
    public int minEatingSpeed(int[] piles, int h) {
        int lo = 1, hi = 0;
        for (int p : piles) hi = Math.max(hi, p);
        int ans = hi;

        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (canFinish(piles, h, mid)) {
                ans = mid;
                hi = mid - 1;
            } else {
                lo = mid + 1;
            }
        }
        return ans;
    }

    private boolean canFinish(int[] piles, int h, int speed) {
        long hours = 0;
        for (int p : piles) {
            hours += (p + speed - 1) / speed;
        }
        return hours <= h;
    }
}'''
        },
        "formulas_and_identities": [
            "Safe Midpoint Calculation: mid = lo + (hi - lo) // 2 (prevents integer overflow in 32-bit)",
            "Ceiling Division without Float: ceil(a / b) = (a + b - 1) // b",
            "Rotated Array Invariant: at least one half [lo..mid] or [mid..hi] is always strictly sorted",
            "Matrix 2D Indexing: row = mid // cols, col = mid % cols"
        ],
        "complexity_table": [
            {"operation": "Binary Search Array", "time": "O(log n)", "space": "O(1)"},
            {"operation": "Binary Search on Answer", "time": "O(n log(max_val))", "space": "O(1)"},
            {"operation": "Search in 2D Matrix", "time": "O(log(m * n))", "space": "O(1)"}
        ],
        "common_mistakes": [
            "Integer overflow from `(lo + hi) / 2` in C++/Java.",
            "Infinite loops caused by incorrect pointer step (`lo = mid` instead of `lo = mid + 1`).",
            "Wrong ceil division: `(p + speed - 1) // speed` rather than float casting."
        ],
        "pattern_to_problem_map": [
            {"number": 33, "title": "Search in Rotated Sorted Array"},
            {"number": 34, "title": "Find First and Last Position of Element in Sorted Array"},
            {"number": 153, "title": "Find Minimum in Rotated Sorted Array"},
            {"number": 410, "title": "Split Array Largest Sum"},
            {"number": 875, "title": "Koko Eating Bananas"}
        ],
        "quick_revision": [
            "Always use `mid = lo + (hi - lo) // 2` to avoid overflow.",
            "Binary search on answer: if predicate `feasible(x)` is monotonic, range is `[min_ans, max_ans]`.",
            "In rotated sorted arrays: determine whether the left or right half is sorted first.",
            "Ceil division: `(a + b - 1) // b` for integer arithmetic.",
            "Lower bound / upper bound: save `ans = mid` whenever condition is met and squeeze boundary."
        ]
    },

    "Recursion & Backtracking": {
        "topic": "Recursion & Backtracking",
        "when_to_use": [
            "Keywords: 'find all combinations / permutations / subsets', 'sudoku', 'n-queens', 'word search', 'partition palindrome'.",
            "Exploration of combinatorial state trees where choices must be tried and reverted.",
            "Constraint satisfaction problems with pruning conditions."
        ],
        "core_idea": "Systematically explore all valid decision paths via recursive DFS, appending current choice to path, recursing deeper, and popping choice upon return (backtrack).",
        "code_templates": {
            "python": '''# 1. Combinations / Subsets Template (Handling Duplicates)
def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    nums.sort() # Sort first to group duplicates together
    result = []

    def backtrack(start_idx: int, path: list[int]):
        result.append(list(path))
        for i in range(start_idx, len(nums)):
            # Skip sibling duplicate branch
            if i > start_idx and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop() # Backtrack step

    backtrack(0, [])
    return result

# 2. Permutations Template
def permute(nums: list[int]) -> list[list[int]]:
    result = []
    def backtrack(path: list[int], used: list[bool]):
        if len(path) == len(nums):
            result.append(list(path))
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path, used)
            path.pop()
            used[i] = False
    backtrack([], [False] * len(nums))
    return result''',
            "cpp": '''#include <vector>
#include <algorithm>

void backtrack(int start, std::vector<int>& nums, std::vector<int>& path, std::vector<std::vector<int>>& res) {
    res.push_back(path);
    for (int i = start; i < (int)nums.size(); ++i) {
        if (i > start && nums[i] == nums[i - 1]) continue;
        path.push_back(nums[i]);
        backtrack(i + 1, nums, path, res);
        path.pop_back();
    }
}

std::vector<std::vector<int>> subsetsWithDup(std::vector<int>& nums) {
    std::sort(nums.begin(), nums.end());
    std::vector<std::vector<int>> res;
    std::vector<int> path;
    backtrack(0, nums, path, res);
    return res;
}''',
            "java": '''import java.util.*;

public class BacktrackTemplates {
    public List<List<Integer>> subsetsWithDup(int[] nums) {
        Arrays.sort(nums);
        List<List<Integer>> res = new ArrayList<>();
        backtrack(0, nums, new ArrayList<>(), res);
        return res;
    }

    private void backtrack(int start, int[] nums, List<Integer> path, List<List<Integer>> res) {
        res.add(new ArrayList<>(path));
        for (int i = start; i < nums.length; i++) {
            if (i > start && nums[i] == nums[i - 1]) continue;
            path.add(nums[i]);
            backtrack(i + 1, nums, path, res);
            path.remove(path.size() - 1);
        }
    }
}'''
        },
        "formulas_and_identities": [
            "Total Subsets of set size N: 2^N",
            "Total Permutations of N distinct elements: N!",
            "Duplicate Skip Condition: `if i > start and nums[i] == nums[i - 1]: continue`",
            "N-Queens Diagonal Invariants: main_diag = (r - c), anti_diag = (r + c)"
        ],
        "complexity_table": [
            {"operation": "Subsets Generation", "time": "O(n * 2^n)", "space": "O(n)"},
            {"operation": "Permutations Generation", "time": "O(n * n!)", "space": "O(n)"},
            {"operation": "N-Queens Solver", "time": "O(N!)", "space": "O(N)"}
        ],
        "common_mistakes": [
            "Appending reference to mutable `path` instead of a deep copy `list(path)`.",
            "Forgetting the `path.pop()` backtrack step on recursive unwinding.",
            "Not sorting before skipping duplicate elements."
        ],
        "pattern_to_problem_map": [
            {"number": 39, "title": "Combination Sum"},
            {"number": 46, "title": "Permutations"},
            {"number": 51, "title": "N-Queens"},
            {"number": 78, "title": "Subsets"},
            {"number": 79, "title": "Word Search"}
        ],
        "quick_revision": [
            "Always append a copy of current path: `res.append(list(path))`.",
            "Duplicates in subsets/combinations: sort first, then `if i > start and nums[i] == nums[i-1]: continue`.",
            "Unbounded choice (e.g. Combination Sum 1): pass `i` instead of `i + 1` in recursive call.",
            "Grid DFS: mark visited cell in-place `grid[r][c] = '#'` and restore on backtrack.",
            "N-Queens: diagonals tracked via `r + c` and `r - c` sets."
        ]
    },

    "Trees & BST": {
        "topic": "Trees & BST",
        "when_to_use": [
            "Keywords: 'LCA', 'diameter', 'level order', 'invert tree', 'serialize', 'valid BST', 'path sum'.",
            "Hierarchical recursive structures with Left and Right subtrees.",
            "BST ordering property: left < root < right ensures inorder traversal is strictly ascending."
        ],
        "core_idea": "Decompose into subproblems solved at left and right subtrees (postorder for bottom-up aggregations like diameter/height, preorder for top-down constraints).",
        "code_templates": {
            "python": '''class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# 1. Diameter / Max Path Sum (Postorder Bottom-Up)
def diameter_of_binary_tree(root: TreeNode) -> int:
    diameter = 0
    def max_depth(node: TreeNode) -> int:
        nonlocal diameter
        if not node:
            return 0
        left_h = max_depth(node.left)
        right_h = max_depth(node.right)
        diameter = max(diameter, left_h + right_h)
        return 1 + max(left_h, right_h)

    max_depth(root)
    return diameter

# 2. Lowest Common Ancestor in Binary Tree
def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    if not root or root == p or root == q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root # Both found in opposite subtrees
    return left if left else right''',
            "cpp": '''struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
    if (!root || root == p || root == q) return root;
    TreeNode* left = lowestCommonAncestor(root->left, p, q);
    TreeNode* right = lowestCommonAncestor(root->right, p, q);
    if (left && right) return root;
    return left ? left : right;
}''',
            "java": '''public class TreeTemplates {
    public static class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int x) { val = x; }
    }

    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        if (root == null || root == p || root == q) return root;
        TreeNode left = lowestCommonAncestor(root.left, p, q);
        TreeNode right = lowestCommonAncestor(root.right, p, q);
        if (left != null && right != null) return root;
        return left != null ? left : right;
    }
}'''
        },
        "formulas_and_identities": [
            "Tree Height: height = 1 + max(height(left), height(right))",
            "Tree Diameter: diameter = max(left_height + right_height) across all nodes",
            "BST Inorder Property: Inorder(BST) produces monotonically increasing sorted array",
            "Nodes in Complete Binary Tree of height h: 2^(h+1) - 1",
            "BST LCA Split: if p.val < root.val and q.val < root.val -> left; if both > -> right; else root is LCA"
        ],
        "complexity_table": [
            {"operation": "Tree DFS / Postorder", "time": "O(N)", "space": "O(H) recursion stack"},
            {"operation": "Level Order BFS (Queue)", "time": "O(N)", "space": "O(W) max width"},
            {"operation": "BST Search / Insert", "time": "O(log N) balanced, O(N) skewed", "space": "O(H)"}
        ],
        "common_mistakes": [
            "Valid BST: checking only immediate child (`node.left.val < node.val`) instead of bounding ranges (`min_val < node.val < max_val`).",
            "Not capturing the return value when returning bottom-up subtree heights.",
            "Assuming full binary tree instead of unbalanced tree."
        ],
        "pattern_to_problem_map": [
            {"number": 98, "title": "Validate Binary Search Tree"},
            {"number": 102, "title": "Binary Tree Level Order Traversal"},
            {"number": 124, "title": "Binary Tree Maximum Path Sum"},
            {"number": 236, "title": "Lowest Common Ancestor of a Binary Tree"},
            {"number": 543, "title": "Diameter of Binary Tree"}
        ],
        "quick_revision": [
            "BST Inorder traversal ALWAYS yields sorted ascending order.",
            "LCA: if left subtree returns node and right returns node, current root IS the LCA.",
            "Tree Diameter / Max Path Sum: compute global max in postorder while returning 1-branch depth.",
            "Valid BST check must propagate bounds `(min_val, max_val)` across all children.",
            "Level order traversal uses Queue; process `len(q)` elements per level loop."
        ]
    },

    "Heaps & Priority Queue": {
        "topic": "Heaps & Priority Queue",
        "when_to_use": [
            "Keywords: 'top K elements', 'kth largest/smallest', 'median of stream', 'k-way merge', 'task scheduler'.",
            "Dynamically maintaining minimum or maximum element under continuous insertions/deletions.",
            "Greedy scheduling with task cooldowns."
        ],
        "core_idea": "Maintain a partial ordering in a complete binary tree where parent is always smaller (Min-Heap) or larger (Max-Heap) than children, enabling O(1) peek and O(log k) updates.",
        "code_templates": {
            "python": '''# 1. Top K Frequent Elements with Min-Heap of size K
import heapq
from collections import Counter

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    count = Counter(nums)
    # Min-heap maintains top K largest frequencies
    heap = []
    for num, freq in count.items():
        heapq.heappush(heap, (freq, num))
        if len(heap) > k:
            heapq.heappop(heap)
    return [num for freq, num in heap]

# 2. Dual Heap for Streaming Median
class MedianFinder:
    def __init__(self):
        self.small = [] # Max-heap (invert signs in Python)
        self.large = [] # Min-heap

    def addNum(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        # Invariant: every element in small <= every element in large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        # Balance sizes (small can have at most 1 more element than large)
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        if len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0''',
            "cpp": '''#include <queue>
#include <vector>

class MedianFinder {
    std::priority_queue<int> maxHeap; // Lower half
    std::priority_queue<int, std::vector<int>, std::greater<int>> minHeap; // Upper half
public:
    void addNum(int num) {
        maxHeap.push(num);
        minHeap.push(maxHeap.top());
        maxHeap.pop();
        if (minHeap.size() > maxHeap.size()) {
            maxHeap.push(minHeap.top());
            minHeap.pop();
        }
    }
    double findMedian() {
        return maxHeap.size() > minHeap.size() ? maxHeap.top() : (maxHeap.top() + minHeap.top()) / 2.0;
    }
};''',
            "java": '''import java.util.PriorityQueue;
import java.util.Collections;

public class MedianFinder {
    private PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
    private PriorityQueue<Integer> minHeap = new PriorityQueue<>();

    public void addNum(int num) {
        maxHeap.offer(num);
        minHeap.offer(maxHeap.poll());
        if (minHeap.size() > maxHeap.size()) {
            maxHeap.offer(minHeap.poll());
        }
    }

    public double findMedian() {
        return maxHeap.size() > minHeap.size() ? maxHeap.peek() : (maxHeap.peek() + minHeap.peek()) / 2.0;
    }
}'''
        },
        "formulas_and_identities": [
            "Parent Index in 0-indexed Array Heap: parent = (i - 1) // 2",
            "Left Child: 2*i + 1, Right Child: 2*i + 2",
            "Build Heap from Array (Heapify): O(n) total time (sum of tree heights)",
            "Top-K Bounded Heap: maintain min-heap of size K -> O(n log k) runtime and O(k) memory"
        ],
        "complexity_table": [
            {"operation": "Find Min / Max (Peek)", "time": "O(1)", "space": "O(1)"},
            {"operation": "Push / Pop", "time": "O(log k)", "space": "O(1)"},
            {"operation": "Build Heap (Heapify)", "time": "O(n)", "space": "O(1) in-place"},
            {"operation": "Top-K Selection", "time": "O(n log k)", "space": "O(k)"}
        ],
        "common_mistakes": [
            "Python's `heapq` is a MIN-heap by default; negate values `-x` to simulate a Max-Heap.",
            "Using full sort O(n log n) when finding Kth element instead of bounded heap O(n log k) or QuickSelect O(n).",
            "Pushing duplicate coordinates onto frontier without a visited set."
        ],
        "pattern_to_problem_map": [
            {"number": 215, "title": "Kth Largest Element in an Array"},
            {"number": 295, "title": "Find Median from Data Stream"},
            {"number": 347, "title": "Top K Frequent Elements"},
            {"number": 373, "title": "Find K Pairs with Smallest Sums"},
            {"number": 621, "title": "Task Scheduler"}
        ],
        "quick_revision": [
            "Array heap indexing: parent `(i-1)//2`, children `2i+1` and `2i+2`.",
            "Kth Largest: use a MIN-heap of size K; smallest of the top-K is at heap[0].",
            "Kth Smallest: use a MAX-heap of size K.",
            "Stream Median: split numbers into Max-Heap (lower half) and Min-Heap (upper half).",
            "Building a heap with heapify takes O(n), NOT O(n log n)."
        ]
    },

    "Greedy": {
        "topic": "Greedy",
        "when_to_use": [
            "Keywords: 'minimum jumps', 'maximum units / gas', 'activity selection', 'reorganize string', 'partition labels'.",
            "Problems exhibiting greedy-choice property and optimal substructure (local optimum leads to global optimum).",
            "Exchange argument proof: swapping any greedy choice with an alternative never improves the objective."
        ],
        "core_idea": "Make the locally optimal choice at each step without reconsidering previous decisions.",
        "code_templates": {
            "python": '''# 1. Maximum Units on a Truck (Fractional Knapsack style)
def maximum_units(box_types: list[list[int]], truck_size: int) -> int:
    # Sort boxes descending by units per box
    box_types.sort(key=lambda x: x[1], reverse=True)
    total_units = 0
    for count, units in box_types:
        take = min(truck_size, count)
        total_units += take * units
        truck_size -= take
        if truck_size == 0:
            break
    return total_units

# 2. Jump Game (Farthest Reachable Index)
def can_jump(nums: list[int]) -> bool:
    farthest = 0
    for i, jump in enumerate(nums):
        if i > farthest:
            return False # Cannot reach this index
        farthest = max(farthest, i + jump)
        if farthest >= len(nums) - 1:
            return True
    return True''',
            "cpp": '''#include <vector>
#include <algorithm>

int maximumUnits(std::vector<std::vector<int>>& boxTypes, int truckSize) {
    std::sort(boxTypes.begin(), boxTypes.end(), [](const auto& a, const auto& b) {
        return a[1] > b[1];
    });
    int totalUnits = 0;
    for (const auto& box : boxTypes) {
        int take = std::min(truckSize, box[0]);
        totalUnits += take * box[1];
        truckSize -= take;
        if (truckSize == 0) break;
    }
    return totalUnits;
}''',
            "java": '''import java.util.Arrays;

public class GreedyTemplates {
    public int maximumUnits(int[][] boxTypes, int truckSize) {
        Arrays.sort(boxTypes, (a, b) -> Integer.compare(b[1], a[1]));
        int totalUnits = 0;
        for (int[] box : boxTypes) {
            int take = Math.min(truckSize, box[0]);
            totalUnits += take * box[1];
            truckSize -= take;
            if (truckSize == 0) break;
        }
        return totalUnits;
    }
}'''
        },
        "formulas_and_identities": [
            "Exchange Argument: prove that substituting greedy pick for optimal pick leaves total cost <= optimal",
            "Fractional Knapsack Metric: sort items by (value / weight) descending",
            "Single-Threaded CPU / Shortest Job First: pick available task with min processing_time",
            "Gas Station Circuit: if total_gas >= total_cost, valid starting station always exists"
        ],
        "complexity_table": [
            {"operation": "Greedy after Sorting", "time": "O(n log n)", "space": "O(1) / O(n)"},
            {"operation": "Single Pass Jump Game", "time": "O(n)", "space": "O(1)"},
            {"operation": "Two-Pass Candy Allocation", "time": "O(n)", "space": "O(n)"}
        ],
        "common_mistakes": [
            "Applying greedy without verifying the optimal substructure (e.g. 0/1 Knapsack requires DP, not Greedy).",
            "Sorting by start time instead of end time in activity selection.",
            "Failing to check if total capacity reaches 0 early."
        ],
        "pattern_to_problem_map": [
            {"number": 45, "title": "Jump Game II"},
            {"number": 55, "title": "Jump Game"},
            {"number": 134, "title": "Gas Station"},
            {"number": 1710, "title": "Maximum Units on a Truck"},
            {"number": 1834, "title": "Single-Threaded CPU"}
        ],
        "quick_revision": [
            "Activity Selection / Interval Scheduling: sort by END time to maximize completed tasks.",
            "Fractional Knapsack / Max Units on Truck: sort by unit value descending.",
            "Shortest Job First: among arrived jobs, prioritize the smallest execution duration.",
            "Jump Game: track `farthest = max(farthest, i + nums[i])`; return false if `i > farthest`.",
            "Gas Station: reset start index to `i + 1` whenever running tank drops below 0."
        ]
    },

    "Intervals": {
        "topic": "Intervals",
        "when_to_use": [
            "Keywords: 'merge intervals', 'insert interval', 'meeting rooms', 'non-overlapping', 'minimum arrows'.",
            "Overlapping time ranges `[start, end]`.",
            "Counting peak concurrent overlaps or eliminating overlapping intervals."
        ],
        "core_idea": "Sort intervals by start (for merging/inserting) or by end (for activity selection/non-overlap), then perform linear sweeps or min-heap active tracking.",
        "code_templates": {
            "python": '''# 1. Merge Intervals Template
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        prev_start, prev_end = merged[-1]
        if start <= prev_end:
            # Overlap: extend previous end
            merged[-1][1] = max(prev_end, end)
        else:
            merged.append([start, end])
    return merged

# 2. Non-overlapping Intervals (Erase Min Overlaps)
def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    # Sort by END time
    intervals.sort(key=lambda x: x[1])
    count_kept = 0
    last_end = float("-inf")
    for start, end in intervals:
        if start >= last_end:
            count_kept += 1
            last_end = end
    return len(intervals) - count_kept''',
            "cpp": '''#include <vector>
#include <algorithm>

std::vector<std::vector<int>> merge(std::vector<std::vector<int>>& intervals) {
    std::sort(intervals.begin(), intervals.end(), [](const auto& a, const auto& b) {
        return a[0] < b[0];
    });
    std::vector<std::vector<int>> merged;
    merged.push_back(intervals[0]);
    for (size_t i = 1; i < intervals.size(); ++i) {
        if (intervals[i][0] <= merged.back()[1]) {
            merged.back()[1] = std::max(merged.back()[1], intervals[i][1]);
        } else {
            merged.push_back(intervals[i]);
        }
    }
    return merged;
}''',
            "java": '''import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;

public class IntervalTemplates {
    public int[][] merge(int[][] intervals) {
        Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));
        List<int[]> merged = new ArrayList<>();
        merged.add(intervals[0]);

        for (int i = 1; i < intervals.length; i++) {
            int[] last = merged.get(merged.size() - 1);
            if (intervals[i][0] <= last[1]) {
                last[1] = Math.max(last[1], intervals[i][1]);
            } else {
                merged.add(intervals[i]);
            }
        }
        return merged.toArray(new int[merged.size()][]);
    }
}'''
        },
        "formulas_and_identities": [
            "Overlap Condition between A and B: max(A.start, B.start) <= min(A.end, B.end)",
            "Intersection Interval: [max(A.start, B.start), min(A.end, B.end)] if start <= end",
            "Sweep-Line Peak Rooms: create events (+1 at start, -1 at end); running max of prefix sum gives peak rooms"
        ],
        "complexity_table": [
            {"operation": "Sort & Merge Intervals", "time": "O(n log n)", "space": "O(n)"},
            {"operation": "Insert Interval into Disjoint List", "time": "O(n)", "space": "O(n)"},
            {"operation": "Meeting Rooms II (Min-Heap / Sweep)", "time": "O(n log n)", "space": "O(n)"}
        ],
        "common_mistakes": [
            "Sorting by end when merging (must sort by start for standard merge).",
            "Forgetting `max(prev_end, end)` when merging (e.g. interval [1, 5] and [2, 4] -> end stays 5).",
            "Handling edge contacts: verify if `start <= end` or `start < end` defines an overlap in the problem statement."
        ],
        "pattern_to_problem_map": [
            {"number": 56, "title": "Merge Intervals"},
            {"number": 57, "title": "Insert Interval"},
            {"number": 252, "title": "Meeting Rooms"},
            {"number": 253, "title": "Meeting Rooms II"},
            {"number": 435, "title": "Non-overlapping Intervals"}
        ],
        "quick_revision": [
            "Merge Intervals: sort by START time; merge if `curr.start <= prev.end`.",
            "Non-overlapping / Activity Selection: sort by END time; greedily keep earliest finishing interval.",
            "Meeting Rooms II: sort start and end points separately or use min-heap of active end times.",
            "Two intervals overlap if and only if `max(a.start, b.start) <= min(a.end, b.end)`.",
            "Insert Interval: process before-intervals, merge overlapping into newInterval, process after-intervals."
        ]
    },

    "Graphs": {
        "topic": "Graphs",
        "when_to_use": [
            "Keywords: 'shortest path', 'connected components', 'topological sort', 'bipartite', 'cycle in directed graph', 'minimum spanning tree'.",
            "Nodes and directed/undirected relations, grid mazes, network routing.",
            "Kahn's algorithm for dependency resolution; Dijkstra for weighted shortest paths; DSU for connectivity."
        ],
        "core_idea": "Represent connectivity via adjacency lists or grids, traversing via BFS (shortest unweighted paths), DFS (cycles/topological sort), Dijkstra (non-negative weights), or Disjoint Set Union.",
        "code_templates": {
            "python": '''# 1. Topological Sort (Kahn's Algorithm with In-Degrees)
from collections import deque

def topological_sort(num_nodes: int, edges: list[list[int]]) -> list[int]:
    adj = {i: [] for i in range(num_nodes)}
    in_degree = [0] * num_nodes
    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1

    queue = deque([i for i in range(num_nodes) if in_degree[i] == 0])
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    return order if len(order) == num_nodes else [] # Empty if cycle exists

# 2. Dijkstra's Algorithm (Shortest Path)
import heapq
def dijkstra(num_nodes: int, graph: dict, start: int) -> list[int]:
    dist = {i: float("inf") for i in range(num_nodes)}
    dist[start] = 0
    pq = [(0, start)] # (distance, node)

    while pq:
        curr_d, u = heapq.heappop(pq)
        if curr_d > dist[u]:
            continue
        for v, weight in graph.get(u, []):
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                heapq.heappush(pq, (dist[v], v))
    return dist''',
            "cpp": '''#include <vector>
#include <queue>

std::vector<int> topologicalSort(int n, const std::vector<std::vector<int>>& edges) {
    std::vector<std::vector<int>> adj(n);
    std::vector<int> inDegree(n, 0);
    for (const auto& e : edges) {
        adj[e[0]].push_back(e[1]);
        inDegree[e[1]]++;
    }
    std::queue<int> q;
    for (int i = 0; i < n; ++i) {
        if (inDegree[i] == 0) q.push(i);
    }
    std::vector<int> order;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        order.push_back(u);
        for (int v : adj[u]) {
            if (--inDegree[v] == 0) q.push(v);
        }
    }
    return (int)order.size() == n ? order : std::vector<int>();
}''',
            "java": '''import java.util.*;

public class GraphTemplates {
    public static class UnionFind {
        int[] parent, rank;
        int count;
        public UnionFind(int n) {
            parent = new int[n];
            rank = new int[n];
            count = n;
            for (int i = 0; i < n; i++) parent[i] = i;
        }
        public int find(int i) {
            if (parent[i] != i) parent[i] = find(parent[i]); // Path compression
            return parent[i];
        }
        public boolean union(int i, int j) {
            int rootI = find(i), rootJ = find(j);
            if (rootI == rootJ) return false;
            if (rank[rootI] < rank[rootJ]) parent[rootI] = rootJ;
            else if (rank[rootI] > rank[rootJ]) parent[rootJ] = rootI;
            else { parent[rootJ] = rootI; rank[rootI]++; }
            count--;
            return true;
        }
    }
}'''
        },
        "formulas_and_identities": [
            "Tree Invariant: Undirected Graph is a valid Tree <=> Edges == n - 1 AND Connected Components == 1",
            "Disjoint Set Union (DSU) Amortized Complexity: O(alpha(n)) ~ O(1) with Path Compression + Union by Rank",
            "Handshaking Lemma: sum(degree(v)) = 2 * |E|",
            "Bipartite Graph Invariant: Graph contains NO odd-length cycles <=> 2-colorable"
        ],
        "complexity_table": [
            {"operation": "BFS / DFS Traversal", "time": "O(V + E)", "space": "O(V)"},
            {"operation": "Dijkstra's Algorithm (Min-Heap)", "time": "O((V + E) log V)", "space": "O(V)"},
            {"operation": "Topological Sort (Kahn)", "time": "O(V + E)", "space": "O(V)"},
            {"operation": "Union-Find Find/Union", "time": "O(alpha(N)) ~ O(1)", "space": "O(N)"}
        ],
        "common_mistakes": [
            "Forgetting to mark nodes as visited in BFS at the moment of queuing, leading to duplicate nodes in queue and TLE.",
            "Using Dijkstra on graphs with negative edge weights (must use Bellman-Ford).",
            "Not handling disconnected graph components when checking bipartite status or cycle detection."
        ],
        "pattern_to_problem_map": [
            {"number": 133, "title": "Clone Graph"},
            {"number": 200, "title": "Number of Islands"},
            {"number": 207, "title": "Course Schedule"},
            {"number": 743, "title": "Network Delay Time"},
            {"number": 785, "title": "Is Graph Bipartite?"}
        ],
        "quick_revision": [
            "BFS on unweighted graph guarantees shortest distance.",
            "Dijkstra solves shortest paths on non-negative weighted graphs in O((V + E) log V).",
            "Topological Sort (Kahn's): start with `in_degree == 0`; if sorted list length < N, graph has a cycle.",
            "Union-Find with Path Compression and Rank performs union/find in nearly O(1) amortized time.",
            "Tree definition: connected undirected graph with exactly `N - 1` edges."
        ]
    },

    "Dynamic Programming": {
        "topic": "Dynamic Programming",
        "when_to_use": [
            "Keywords: 'maximum profit', 'minimum cost', 'number of ways', 'longest subsequence / substring', 'can partition'.",
            "Problems with overlapping subproblems and optimal substructure.",
            "Patterns: 0/1 Knapsack, Unbounded Knapsack, LIS, LCS, Grid Paths, Interval DP, State Machine."
        ],
        "core_idea": "Define state variables `dp[...]`, establish recurrence transitions relating larger states to smaller base cases, and populate iteratively (bottom-up) or recursively with memoization (top-down).",
        "code_templates": {
            "python": '''# 1. Longest Increasing Subsequence (O(n log n) Patience Sorting)
import bisect

def length_of_lis(nums: list[int]) -> int:
    tails = []
    for x in nums:
        idx = bisect.bisect_left(tails, x)
        if idx == len(tails):
            tails.append(x)
        else:
            tails[idx] = x
    return len(tails)

# 2. 0/1 Knapsack / Subset Sum (Space Optimized 1D Array)
def can_partition(nums: list[int]) -> bool:
    total = sum(nums)
    if total % 2 != 0:
        return False
    target = total // 2
    dp = [True] + [False] * target

    for num in nums:
        # Traverse backwards for 0/1 knapsack to use previous iteration states
        for j in range(target, num - 1, -1):
            dp[j] = dp[j] or dp[j - num]
    return dp[target]

# 3. Longest Common Subsequence (2D Grid DP)
def longest_common_subsequence(text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]''',
            "cpp": '''#include <vector>
#include <string>
#include <algorithm>

int longestCommonSubsequence(const std::string& text1, const std::string& text2) {
    int m = text1.size(), n = text2.size();
    std::vector<std::vector<int>> dp(m + 1, std::vector<int>(n + 1, 0));
    for (int i = 1; i <= m; ++i) {
        for (int j = 1; j <= n; ++j) {
            if (text1[i - 1] == text2[j - 1]) {
                dp[i][j] = 1 + dp[i - 1][j - 1];
            } else {
                dp[i][j] = std::max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }
    return dp[m][n];
}''',
            "java": '''public class DPTemplates {
    public int lengthOfLIS(int[] nums) {
        int[] tails = new int[nums.length];
        int size = 0;
        for (int x : nums) {
            int i = 0, j = size;
            while (i < j) {
                int m = (i + j) / 2;
                if (tails[m] < x) i = m + 1;
                else j = m;
            }
            tails[i] = x;
            if (i == size) size++;
        }
        return size;
    }
}'''
        },
        "formulas_and_identities": [
            "0/1 Knapsack: dp[j] = max(dp[j], dp[j - weight] + value) (iterating j backwards)",
            "Unbounded Knapsack: dp[j] = max(dp[j], dp[j - weight] + value) (iterating j forwards)",
            "Longest Common Subsequence (LCS): match ? 1 + dp[i-1][j-1] : max(dp[i-1][j], dp[i][j-1])",
            "Edit Distance: match ? dp[i-1][j-1] : 1 + min(replace, insert, delete)",
            "Coin Change Combinations: outer loop over coins, inner loop over amounts"
        ],
        "complexity_table": [
            {"operation": "0/1 Knapsack", "time": "O(N * W)", "space": "O(W) with 1D array"},
            {"operation": "LIS (Binary Search)", "time": "O(N log N)", "space": "O(N)"},
            {"operation": "LCS / Edit Distance", "time": "O(M * N)", "space": "O(M * N) or O(N)"}
        ],
        "common_mistakes": [
            "Iterating forwards instead of backwards in 1D 0/1 knapsack (uses the same item multiple times).",
            "Swapping outer and inner loops in Coin Change (permutations vs combinations).",
            "Forgetting base cases (e.g. `dp[0] = 1` or `dp[0] = 0` depending on problem)."
        ],
        "pattern_to_problem_map": [
            {"number": 70, "title": "Climbing Stairs"},
            {"number": 198, "title": "House Robber"},
            {"number": 300, "title": "Longest Increasing Subsequence"},
            {"number": 322, "title": "Coin Change"},
            {"number": 1143, "title": "Longest Common Subsequence"}
        ],
        "quick_revision": [
            "Always specify 4 components: State, Base Cases, Recurrence Transition, Order of Computation.",
            "0/1 Knapsack: loop weights BACKWARDS to prevent reuse.",
            "Unbounded Knapsack / Coin Change: loop weights FORWARDS to allow reuse.",
            "Coin combinations: loop coins outside, amounts inside; Coin permutations: loop amounts outside.",
            "LIS can be solved in O(n log n) using binary search (patience sort) on tails array."
        ]
    },

    "Tries": {
        "topic": "Tries",
        "when_to_use": [
            "Keywords: 'prefix search', 'autocomplete', 'implement dictionary', 'wildcard string match', 'maximum XOR of two numbers'.",
            "Storing a set of strings with common prefixes.",
            "Bitwise prefix matching (Binary Trie) for maximum XOR queries."
        ],
        "core_idea": "A tree where each node represents a character or bit, and paths from root to marked endpoints spell stored words in O(L) time.",
        "code_templates": {
            "python": '''# 1. Standard Trie (Prefix Tree)
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for c in word:
            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr = curr.children[c]
        curr.is_end = True

    def search(self, word: str) -> bool:
        curr = self.root
        for c in word:
            if c not in curr.children:
                return False
            curr = curr.children[c]
        return curr.is_end

    def startsWith(self, prefix: str) -> bool:
        curr = self.root
        for c in prefix:
            if c not in curr.children:
                return False
            curr = curr.children[c]
        return True''',
            "cpp": '''#include <string>
#include <vector>

class Trie {
    struct TrieNode {
        TrieNode* children[26] = {nullptr};
        bool isEnd = false;
    };
    TrieNode* root;
public:
    Trie() : root(new TrieNode()) {}

    void insert(const std::string& word) {
        TrieNode* curr = root;
        for (char c : word) {
            int idx = c - 'a';
            if (!curr->children[idx]) curr->children[idx] = new TrieNode();
            curr = curr->children[idx];
        }
        curr->isEnd = true;
    }

    bool search(const std::string& word) {
        TrieNode* curr = root;
        for (char c : word) {
            int idx = c - 'a';
            if (!curr->children[idx]) return false;
            curr = curr->children[idx];
        }
        return curr->isEnd;
    }
};''',
            "java": '''public class Trie {
    static class TrieNode {
        TrieNode[] children = new TrieNode[26];
        boolean isEnd = false;
    }
    private TrieNode root = new TrieNode();

    public void insert(String word) {
        TrieNode curr = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (curr.children[idx] == null) curr.children[idx] = new TrieNode();
            curr = curr.children[idx];
        }
        curr.isEnd = true;
    }

    public boolean search(String word) {
        TrieNode curr = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (curr.children[idx] == null) return false;
            curr = curr.children[idx];
        }
        return curr.isEnd;
    }
}'''
        },
        "formulas_and_identities": [
            "Time Complexity per Operation: O(L) where L is the length of the query string",
            "Max XOR Bitwise Trie: for each bit (from 31 down to 0), greedily traverse the opposite bit (1 - bit) if it exists",
            "Trie Node Array vs Map: fixed 26-size array gives faster O(1) access; hash map saves space for sparse alphabets"
        ],
        "complexity_table": [
            {"operation": "Insert Word (len L)", "time": "O(L)", "space": "O(L * alphabet_size)"},
            {"operation": "Search Word (len L)", "time": "O(L)", "space": "O(1)"},
            {"operation": "Prefix Match (len P)", "time": "O(P)", "space": "O(1)"}
        ],
        "common_mistakes": [
            "Forgetting to set `is_end = True` when inserting words.",
            "Confusing `startsWith` (checks prefix existence) with `search` (checks exact word with `is_end`).",
            "Memory explosion when storing large alphabets (use Map instead of fixed array for unicode)."
        ],
        "pattern_to_problem_map": [
            {"number": 208, "title": "Implement Trie (Prefix Tree)"},
            {"number": 211, "title": "Design Add and Search Words Data Structure"},
            {"number": 212, "title": "Word Search II"},
            {"number": 421, "title": "Maximum XOR of Two Numbers in an Array"},
            {"number": 648, "title": "Replace Words"}
        ],
        "quick_revision": [
            "Insert, Search, and StartsWith all run in O(L) time where L is word length.",
            "Word Search II: build Trie on dictionary words to prune grid DFS early.",
            "Wildcard '.' search in Trie: use recursion/backtracking over all non-null children.",
            "Binary Trie (depth 32): solve Max XOR by greedily choosing opposite bits.",
            "`is_end` flag differentiates prefixes from complete words."
        ]
    },

    "Bit Manipulation & Math": {
        "topic": "Bit Manipulation & Math",
        "when_to_use": [
            "Keywords: 'single number', 'power of two', 'count set bits', 'gcd', 'primes', 'binary exponentiation', 'reverse bits'.",
            "O(1) low-level bit operations and mathematical formulas.",
            "Modular arithmetic in combinatorics and number theory."
        ],
        "core_idea": "Harness bitwise properties (XOR cancellation, bit masking, bit shifts) and mathematical identities (Euclid GCD, Sieve, fast power) for constant or logarithmic solutions.",
        "code_templates": {
            "python": '''# 1. Brian Kernighan's Algorithm (Count Set Bits)
def count_set_bits(n: int) -> int:
    count = 0
    while n > 0:
        n &= (n - 1) # Clears the lowest set bit
        count += 1
    return count

# 2. Binary Exponentiation (Fast Pow in O(log n))
def my_pow(x: float, n: int) -> float:
    if n < 0:
        x = 1 / x
        n = -n
    ans = 1.0
    curr = x
    while n > 0:
        if n & 1:
            ans *= curr
        curr *= curr
        n >>= 1
    return ans

# 3. Sieve of Eratosthenes (Count Primes)
def count_primes(n: int) -> int:
    if n <= 2:
        return 0
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(n**0.5) + 1):
        if is_prime[p]:
            for multiple in range(p * p, n, p):
                is_prime[multiple] = False
    return sum(is_prime)''',
            "cpp": '''#include <vector>

int countPrimes(int n) {
    if (n <= 2) return 0;
    std::vector<bool> isPrime(n, true);
    isPrime[0] = isPrime[1] = false;
    for (int p = 2; p * p < n; ++p) {
        if (isPrime[p]) {
            for (int mult = p * p; mult < n; mult += p) {
                isPrime[mult] = false;
            }
        }
    }
    int count = 0;
    for (bool p : isPrime) if (p) count++;
    return count;
}''',
            "java": '''public class BitMathTemplates {
    public double myPow(double x, int n) {
        long N = n;
        if (N < 0) {
            x = 1 / x;
            N = -N;
        }
        double ans = 1.0;
        double curr = x;
        for (long i = N; i > 0; i /= 2) {
            if (i % 2 == 1) ans *= curr;
            curr *= curr;
        }
        return ans;
    }
}'''
        },
        "formulas_and_identities": [
            "Clear Lowest Set Bit: n & (n - 1)",
            "Isolate Lowest Set Bit: n & (-n)",
            "Power of Two Check: n > 0 and (n & (n - 1)) == 0",
            "XOR Self Inverse: a ^ a = 0 and a ^ 0 = a",
            "Euclidean GCD: gcd(a, b) = a if b == 0 else gcd(b, a % b)",
            "Modular Arithmetic: (a + b) % m = ((a % m) + (b % m)) % m; (a * b) % m = ((a % m) * (b % m)) % m",
            "Gauss Sum of 1..N: sum = N * (N + 1) // 2"
        ],
        "complexity_table": [
            {"operation": "Bitwise Operations (&, |, ^, ~)", "time": "O(1)", "space": "O(1)"},
            {"operation": "Brian Kernighan Bit Count", "time": "O(number of set bits)", "space": "O(1)"},
            {"operation": "Binary Exponentiation", "time": "O(log n)", "space": "O(1)"},
            {"operation": "Sieve of Eratosthenes", "time": "O(n log log n)", "space": "O(n)"}
        ],
        "common_mistakes": [
            "Operator precedence in Python/C++: `==` has higher precedence than `&` (e.g. `n & (n-1) == 0` evaluates as `n & ((n-1) == 0)` without parentheses!).",
            "Integer overflow in 32-bit `abs(INT_MIN)` or `-n` when `n = -2^31` (cast to 64-bit int / long).",
            "Negative modulo in C++ / Java (e.g. `-1 % 5 == -1`; use `(x % m + m) % m`)."
        ],
        "pattern_to_problem_map": [
            {"number": 50, "title": "Pow(x, n)"},
            {"number": 136, "title": "Single Number"},
            {"number": 191, "title": "Number of 1 Bits"},
            {"number": 204, "title": "Count Primes"},
            {"number": 231, "title": "Power of Two"}
        ],
        "quick_revision": [
            "`n & (n - 1)` strips the lowest set bit; `n & (-n)` isolates it.",
            "Power of 2 check: `n > 0 and (n & (n - 1)) == 0`.",
            "XOR properties: `a ^ a = 0`, `a ^ 0 = a`, XOR is associative and commutative.",
            "Binary exponentiation computes `x^n` in O(log n) time by squaring the base.",
            "Bitwise operators have low precedence: ALWAYS wrap in parentheses `(n & 1) == 1`."
        ]
    }
}

for topic, data in CHEATSHEETS_DATA.items():
    clean_name = topic.lower().replace(" & ", "_").replace(" ", "_")
    file_path = os.path.join(CHEATSHEETS_DIR, f"{clean_name}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Saved cheat sheet: {file_path}")

print("All problem and cheat sheet seeds generated successfully!")
