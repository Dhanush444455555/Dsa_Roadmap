"""
Seed script to generate backend/app/data/problems.json and sample files.
"""
import os
import json
import re

raw_csv_data = """day,leetcode_no,title,topic,difficulty,similar_to,note,source
1,88,Merge Sorted Array,Arrays,Easy,,,leetcode_extra
1,118,Pascal's Triangle,Arrays,Easy,,,leetcode_extra
1,169,Majority Element,Arrays,Easy,,,leetcode_top100
1,448,Find All Numbers Disappeared in an Array,Arrays,Easy,,,leetcode_top100
1,31,Next Permutation,Arrays,Medium,,,leetcode_top100
1,48,Rotate Image,Arrays,Medium,,,leetcode_top100
1,53,Maximum Subarray,Arrays,Medium,,,leetcode_top100
1,54,Spiral Matrix,Arrays,Medium,,,leetcode_extra
1,73,Set Matrix Zeroes,Arrays,Medium,,,leetcode_extra
1,75,Sort Colors,Arrays,Medium,,,leetcode_top100
1,189,Rotate Array,Arrays,Medium,,,leetcode_extra
1,238,Product of Array Except Self,Arrays,Medium,,,leetcode_top100
1,287,Find the Duplicate Number,Arrays,Medium,,,leetcode_top100
1,581,Shortest Unsorted Continuous Subarray,Arrays,Medium,,,leetcode_top100
1,41,First Missing Positive,Arrays,Hard,,,leetcode_extra
2,9,Palindrome Number,Math,Easy,,,leetcode_extra
2,66,Plus One,Math,Easy,,,leetcode_extra
2,202,Happy Number,Math,Easy,,,leetcode_extra
3,1,Two Sum,Hashing,Easy,Basic Hashing / HashMap,,both
3,217,Contains Duplicate,Hashing,Easy,Basic Hashing using unordered_set,,docs
3,219,Contains Duplicate II,Hashing,Easy,Hashing + index tracking,,docs
3,242,Valid Anagram,Hashing,Easy,,,leetcode_extra
3,771,Jewels and Stones,Hashing,Easy,,,leetcode_top100
3,49,Group Anagrams,Hashing,Medium,,,leetcode_top100
3,128,Longest Consecutive Sequence,Hashing,Medium,Longest Consecutive Sequence in an Array,,both
3,325,Maximum Size Subarray Sum Equals k,Hashing,Medium,Longest Subarray with Sum K,,docs
3,525,Contiguous Array,Hashing,Medium,Similar prefix-sum technique for finding longest subarray with sum 0,,docs
3,560,Subarray Sum Equals K,Hashing,Medium,Count Subarrays with Given Sum,,both
3,930,Binary Subarrays With Sum,Hashing,Medium,Count Subarrays with Given Sum,,docs
3,974,Subarray Sums Divisible by K,Hashing,Medium,Similar prefix-sum + frequency-map technique,,docs
3,1248,Count Number of Nice Subarrays,Hashing,Medium,Similar prefix-sum/counting technique,,docs
3,2588,Count the Number of Beautiful Subarrays,Hashing,Medium,Similar XOR-prefix technique,,docs
4,13,Roman to Integer,Strings,Easy,,,docs
4,14,Longest Common Prefix,Strings,Easy,,,leetcode_extra
4,1021,Remove Outermost Parentheses,Strings,Easy,,,docs
4,1614,Maximum Nesting Depth of the Parentheses,Strings,Easy,Maximum Nesting Depth,,docs
4,3,Longest Substring Without Repeating Characters,Strings,Medium,Useful similar substring/sliding-window problem,,both
4,5,Longest Palindromic Substring,Strings,Medium,,,both
4,8,String to Integer (atoi),Strings,Medium,,,docs
4,424,Longest Repeating Character Replacement,Strings,Medium,Similar substring + frequency counting,,docs
4,438,Find All Anagrams in a String,Strings,Medium,,,leetcode_top100
4,647,Palindromic Substrings,Strings,Medium,Longest Palindromic Substring,,both
4,1358,Number of Substrings Containing All Three Characters,Strings,Medium,Count Number of Substrings,,docs
4,1781,Sum of Beauty of All Substrings,Strings,Medium,,,docs
4,76,Minimum Window Substring,Strings,Hard,Advanced substring + frequency/hash-map technique,,both
5,26,Remove Duplicates from Sorted Array,Two Pointers,Easy,,,leetcode_extra
5,125,Valid Palindrome,Two Pointers,Easy,,,leetcode_extra
5,283,Move Zeroes,Two Pointers,Easy,,,leetcode_top100
5,392,Is Subsequence,Two Pointers,Easy,,,leetcode_extra
5,11,Container With Most Water,Two Pointers,Medium,,,leetcode_top100
5,15,3Sum,Two Pointers,Medium,,,leetcode_top100
5,167,Two Sum II - Input Array Is Sorted,Two Pointers,Medium,,,leetcode_extra
6,209,Minimum Size Subarray Sum,Sliding Window,Medium,,,leetcode_extra
6,567,Permutation in String,Sliding Window,Medium,,,leetcode_extra
7,136,Single Number,Bit Manipulation,Easy,,,leetcode_top100
7,191,Number of 1 Bits,Bit Manipulation,Easy,,,leetcode_extra
7,231,Power of Two,Bit Manipulation,Easy,,,leetcode_extra
7,268,Missing Number,Bit Manipulation,Easy,,,leetcode_extra
7,338,Counting Bits,Bit Manipulation,Easy,,,leetcode_top100
7,461,Hamming Distance,Bit Manipulation,Easy,,,leetcode_top100
8,20,Valid Parentheses,Stack,Easy,,,both
8,225,Implement Stack using Queues,Stack,Easy,,imp points use swap function blw two implement queues,docs
8,232,Implement Queue using Stacks,Stack,Easy,,,docs
8,496,Next Greater Element I,Stack,Easy,,its like circular thing where we use 2n-1 in for loop and descend that and push to ans where index<n,docs
8,150,Evaluate Reverse Polish Notation,Stack,Medium,,,leetcode_extra
8,155,Min Stack,Stack,Medium,,,both
8,277,Find the Celebrity,Stack,Medium,,,docs
8,394,Decode String,Stack,Medium,,,leetcode_top100
8,402,Remove K Digits,Stack,Medium,,,docs
8,503,Next Greater Element II,Stack,Medium,,,docs
8,735,Asteroid Collision,Stack,Medium,,,docs
8,739,Daily Temperatures,Stack,Medium,,,leetcode_extra
8,901,Online Stock Span,Stack,Medium,,,docs
8,907,Sum of Subarray Minimums,Stack,Medium,,,docs
8,2104,Sum of Subarray Ranges,Stack,Medium,,,docs
8,42,Trapping Rain Water,Stack,Hard,,,both
8,84,Largest Rectangle in Histogram,Stack,Hard,,,both
8,85,Maximal Rectangle,Stack,Hard,,,both
8,239,Sliding Window Maximum,Stack,Hard,,,both
8,460,LFU Cache,Stack,Hard,,,docs
9,21,Merge Two Sorted Lists,Linked List,Easy,,,both
9,83,Remove Duplicates from Sorted List,Linked List,Easy,,,docs
9,141,Linked List Cycle,Linked List,Easy,,,both
9,160,Intersection of Two Linked Lists,Linked List,Easy,,,both
9,203,Remove Linked List Elements,Linked List,Easy,,,docs
9,206,Reverse Linked List,Linked List,Easy,,,both
9,234,Palindrome Linked List,Linked List,Easy,,,both
9,876,Middle of the Linked List,Linked List,Easy,,,docs
9,2,Add Two Numbers,Linked List,Medium,,,both
9,19,Remove Nth Node From End of List,Linked List,Medium,,,both
9,24,Swap Nodes in Pairs,Linked List,Medium,,,leetcode_extra
9,61,Rotate List,Linked List,Medium,,,docs
9,82,Remove Duplicates from Sorted List II,Linked List,Medium,,,leetcode_extra
9,92,Reverse Linked List II,Linked List,Medium,,,docs
9,138,Copy List with Random Pointer,Linked List,Medium,,,docs
9,142,Linked List Cycle II,Linked List,Medium,,,both
9,143,Reorder List,Linked List,Medium,,,leetcode_extra
9,146,LRU Cache,Linked List,Medium,,,both
9,148,Sort List,Linked List,Medium,,,both
9,328,Odd Even Linked List,Linked List,Medium,,,docs
9,430,Flatten a Multilevel Doubly Linked List,Linked List,Medium,,,docs
9,725,Split Linked List in Parts,Linked List,Medium,,,docs
9,2095,Delete the Middle Node of a Linked List,Linked List,Medium,,,docs
9,23,Merge k Sorted Lists,Linked List,Hard,,,both
9,25,Reverse Nodes in k-Group,Linked List,Hard,,,docs
10,35,Search Insert Position,Binary Search,Easy,Search insert position / Lower Bound,,docs
10,69,Sqrt(x),Binary Search,Easy,Find square root of a number,,docs
10,367,Valid Perfect Square,Binary Search,Easy,square-root binary search,,docs
10,704,Binary Search,Binary Search,Easy,,,leetcode_extra
10,744,Find Smallest Letter Greater Than Target,Binary Search,Easy,Upper Bound / Ceiling,,docs
10,2643,Row With Maximum Ones,Binary Search,Easy,Find row with maximum 1's,,docs
10,33,Search in Rotated Sorted Array,Binary Search,Medium,Search in rotated sorted array-I,,both
10,34,Find First and Last Position of Element in Sorted Array,Binary Search,Medium,First and last occurrence,,both
10,74,Search a 2D Matrix,Binary Search,Medium,Search in a 2D Matrix,,docs
10,81,Search in Rotated Sorted Array II,Binary Search,Medium,,,docs
10,153,Find Minimum in Rotated Sorted Array,Binary Search,Medium,,,docs
10,162,Find Peak Element,Binary Search,Medium,,,docs
10,240,Search a 2D Matrix II,Binary Search,Medium,Search in 2D Matrix-II,,both
10,378,Kth Smallest Element in a Sorted Matrix,Binary Search,Medium,Matrix Median,,docs
10,540,Single Element in a Sorted Array,Binary Search,Medium,Single element in sorted array,,docs
10,702,Search in a Sorted Array of Unknown Size,Binary Search,Medium,Search X in sorted array,,docs
10,875,Koko Eating Bananas,Binary Search,Medium,,,docs
10,1011,Capacity To Ship Packages Within D Days,Binary Search,Medium,,,docs
10,1283,Find the Smallest Divisor Given a Threshold,Binary Search,Medium,Find the smallest divisor,,docs
10,1482,Minimum Number of Days to Make m Bouquets,Binary Search,Medium,Minimum days to make M bouquets,,docs
10,1539,Kth Missing Positive Number,Binary Search,Medium,,,docs
10,1552,Magnetic Force Between Two Balls,Binary Search,Medium,Aggressive Cows,,docs
10,4,Median of Two Sorted Arrays,Binary Search,Hard,Median of 2 sorted arrays,,both
10,410,Split Array Largest Sum,Binary Search,Hard,Painter's Partition,,docs
10,774,Minimize Max Distance to Gas Station,Binary Search,Hard,,,docs
10,1901,Find a Peak Element II,Binary Search,Hard,Find Peak Element-II,,docs
11,17,Letter Combinations of a Phone Number,Recursion & Backtracking,Medium,,,both
11,22,Generate Parentheses,Recursion & Backtracking,Medium,,,both
11,39,Combination Sum,Recursion & Backtracking,Medium,subsequence / subset generation with a target sum,,both
11,40,Combination Sum II,Recursion & Backtracking,Medium,,,leetcode_extra
11,46,Permutations,Recursion & Backtracking,Medium,,,leetcode_top100
11,47,Permutations II,Recursion & Backtracking,Medium,,,leetcode_extra
11,50,Pow(x, n),Recursion & Backtracking,Medium,,,docs
11,77,Combinations,Recursion & Backtracking,Medium,,,leetcode_extra
11,78,Subsets,Recursion & Backtracking,Medium,Power Set,,both
11,79,Word Search,Recursion & Backtracking,Medium,,,both
11,90,Subsets II,Recursion & Backtracking,Medium,Power Set when duplicate elements are involved,,docs
11,131,Palindrome Partitioning,Recursion & Backtracking,Medium,,,docs
11,1042,Flower Planting With No Adjacent,Recursion & Backtracking,Medium,M Coloring Problem (graph coloring),,docs
11,1219,Path with Maximum Gold,Recursion & Backtracking,Medium,Rat in a Maze (grid backtracking),,docs
11,1922,Count Good Numbers,Recursion & Backtracking,Medium,,,docs
11,3211,Generate Binary Strings Without Adjacent Zeros,Recursion & Backtracking,Medium,Very similar to Generate Binary Strings Without Consecutive 1s,,docs
11,37,Sudoku Solver,Recursion & Backtracking,Hard,,,docs
11,51,N-Queens,Recursion & Backtracking,Hard,N Queen,,docs
11,52,N-Queens II,Recursion & Backtracking,Hard,N Queen, but counts solutions,,docs
11,282,Expression Add Operators,Recursion & Backtracking,Hard,,,docs
11,301,Remove Invalid Parentheses,Recursion & Backtracking,Hard,,,leetcode_top100
11,980,Unique Paths III,Recursion & Backtracking,Hard,Rat in a Maze with backtracking,,docs
11,1274,Number of Ships in a Rectangle,Recursion & Backtracking,Hard,,,docs
12,455,Assign Cookies,Greedy,Easy,,,docs
12,860,Lemonade Change,Greedy,Easy,,,docs
12,1710,Maximum Units on a Truck,Greedy,Easy,Fractional Knapsack (greedy by value/weight),,docs
12,45,Jump Game II,Greedy,Medium,,,docs
12,55,Jump Game,Greedy,Medium,Jump Game I,,both
12,56,Merge Intervals,Greedy,Medium,,,both
12,57,Insert Interval,Greedy,Medium,,,docs
12,134,Gas Station,Greedy,Medium,,,leetcode_extra
12,253,Meeting Rooms II,Greedy,Medium,Minimum number of platforms required for a railway,,both
12,406,Queue Reconstruction by Height,Greedy,Medium,,,leetcode_top100
12,435,Non-overlapping Intervals,Greedy,Medium,,,docs
12,452,Minimum Number of Arrows to Burst Balloons,Greedy,Medium,Similar interval-greedy technique,,docs
12,621,Task Scheduler,Greedy,Medium,,,leetcode_top100
12,763,Partition Labels,Greedy,Medium,,,leetcode_extra
12,1834,Single-Threaded CPU,Greedy,Medium,Shortest Job First,,docs
12,135,Candy,Greedy,Hard,,,docs
13,94,Binary Tree Inorder Traversal,Binary Tree,Easy,,,leetcode_top100
13,100,Same Tree,Binary Tree,Easy,,,leetcode_extra
13,101,Symmetric Tree,Binary Tree,Easy,,,leetcode_top100
13,104,Maximum Depth of Binary Tree,Binary Tree,Easy,,,leetcode_top100
13,108,Convert Sorted Array to Binary Search Tree,Binary Tree,Easy,,,leetcode_extra
13,110,Balanced Binary Tree,Binary Tree,Easy,,,leetcode_extra
13,111,Minimum Depth of Binary Tree,Binary Tree,Easy,,,leetcode_extra
13,112,Path Sum,Binary Tree,Easy,,,leetcode_extra
13,226,Invert Binary Tree,Binary Tree,Easy,,,leetcode_top100
13,543,Diameter of Binary Tree,Binary Tree,Easy,,,leetcode_top100
13,572,Subtree of Another Tree,Binary Tree,Easy,,,leetcode_top100
13,617,Merge Two Binary Trees,Binary Tree,Easy,,,leetcode_top100
13,102,Binary Tree Level Order Traversal,Binary Tree,Medium,,,leetcode_top100
13,103,Binary Tree Zigzag Level Order Traversal,Binary Tree,Medium,,,leetcode_extra
13,105,Construct Binary Tree from Preorder and Inorder Traversal,Binary Tree,Medium,,,leetcode_top100
13,114,Flatten Binary Tree to Linked List,Binary Tree,Medium,,,leetcode_top100
13,199,Binary Tree Right Side View,Binary Tree,Medium,,,leetcode_extra
13,236,Lowest Common Ancestor of a Binary Tree,Binary Tree,Medium,,,leetcode_top100
13,437,Path Sum III,Binary Tree,Medium,,,leetcode_top100
13,124,Binary Tree Maximum Path Sum,Binary Tree,Hard,,,leetcode_top100
13,297,Serialize and Deserialize Binary Tree,Binary Tree,Hard,,,leetcode_top100
14,270,Closest Binary Search Tree Value,Binary Search Tree,Easy,Floor/Ceil in BST,,docs
14,653,Two Sum IV — Input is a BST,Binary Search Tree,Easy,Two Sum in BST,,docs
14,700,Search in a Binary Search Tree,Binary Search Tree,Easy,Search in BST,,docs
14,783,Minimum Distance Between BST Nodes,Binary Search Tree,Easy,finding minimum values in BST,,docs
14,938,Range Sum of BST,Binary Search Tree,Easy,BST traversal / range searching,,docs
14,98,Validate Binary Search Tree,Binary Search Tree,Medium,Check if a tree is a BST,,both
14,99,Recover Binary Search Tree,Binary Search Tree,Medium,Correct BST with two nodes swapped,,docs
14,173,Binary Search Tree Iterator,Binary Search Tree,Medium,BST Iterator,,docs
14,230,Kth Smallest Element in a BST,Binary Search Tree,Medium,Kth Smallest element in BST,,docs
14,235,Lowest Common Ancestor of a Binary Search Tree,Binary Search Tree,Medium,LCA in BST,,docs
14,285,Inorder Successor in BST,Binary Search Tree,Medium,,,docs
14,333,Largest BST Subtree,Binary Search Tree,Medium,Largest BST in Binary Tree,,docs
14,450,Delete Node in a BST,Binary Search Tree,Medium,Delete a node in BST,,docs
14,538,Convert BST to Greater Tree,Binary Search Tree,Medium,,,leetcode_top100
14,701,Insert into a Binary Search Tree,Binary Search Tree,Medium,Insert a given node in BST,,docs
14,1008,Construct Binary Search Tree from Preorder Traversal,Binary Search Tree,Medium,Construct BST from preorder,,docs
14,272,Closest Binary Search Tree Value II,Binary Search Tree,Hard,Advanced BST searching / closest values,,docs
15,703,Kth Largest Element in a Stream,Heap,Easy,,,leetcode_extra
15,1046,Last Stone Weight,Heap,Easy,,,leetcode_extra
15,215,Kth Largest Element in an Array,Heap,Medium,,,leetcode_top100
15,347,Top K Frequent Elements,Heap,Medium,,,leetcode_top100
15,973,K Closest Points to Origin,Heap,Medium,,,leetcode_extra
15,295,Find Median from Data Stream,Heap,Hard,,,leetcode_extra
16,208,Implement Trie (Prefix Tree),Trie,Medium,,,leetcode_top100
16,211,Design Add and Search Words Data Structure,Trie,Medium,,,leetcode_extra
16,212,Word Search II,Trie,Hard,,,leetcode_extra
17,733,Flood Fill,Graphs,Easy,Flood Fill Algorithm,,docs
17,997,Find the Town Judge,Graphs,Easy,Similar graph degree / adjacency concept,,docs
17,1971,Find if Path Exists in Graph,Graphs,Easy,Basic graph traversal / connected components,,docs
17,130,Surrounded Regions,Graphs,Medium,,,docs
17,133,Clone Graph,Graphs,Medium,,,leetcode_extra
17,200,Number of Islands,Graphs,Medium,,,both
17,207,Course Schedule,Graphs,Medium,Topological Sort / Detect cycle in directed graph,,both
17,210,Course Schedule II,Graphs,Medium,Kahn's Algorithm / Topological Sort,,docs
17,417,Pacific Atlantic Water Flow,Graphs,Medium,,,leetcode_extra
17,542,01 Matrix,Graphs,Medium,Distance of nearest cell having 1,,docs
17,547,Number of Provinces,Graphs,Medium,,,docs
17,684,Redundant Connection,Graphs,Medium,detecting a cycle in an undirected graph,,docs
17,694,Number of Distinct Islands,Graphs,Medium,,,docs
17,721,Accounts Merge,Graphs,Medium,Accounts Merge / DSU,,docs
17,743,Network Delay Time,Graphs,Medium,Dijkstra's Algorithm,,docs
17,785,Is Graph Bipartite?,Graphs,Medium,Bipartite Graph,,docs
17,787,Cheapest Flights Within K Stops,Graphs,Medium,Cheapest flight within K stops,,docs
17,802,Find Eventual Safe States,Graphs,Medium,,,docs
17,947,Most Stones Removed with Same Row or Column,Graphs,Medium,,,docs
17,994,Rotting Oranges,Graphs,Medium,,,docs
17,1020,Number of Enclaves,Graphs,Medium,,,docs
17,1091,Shortest Path in Binary Matrix,Graphs,Medium,shortest path in an unweighted graph / binary maze,,docs
17,1319,Number of Operations to Make Network Connected,Graphs,Medium,,,docs
17,1334,Find the City With the Smallest Number of Neighbors at a Threshold,Graphs,Medium,,,docs
17,1584,Min Cost to Connect All Points,Graphs,Medium,Find MST weight,,docs
17,1631,Path With Minimum Effort,Graphs,Medium,,,docs
17,1976,Number of Ways to Arrive at Destination,Graphs,Medium,,,docs
17,126,Word Ladder II,Graphs,Hard,,,docs
17,127,Word Ladder,Graphs,Hard,Word Ladder I,,docs
17,305,Number of Islands II,Graphs,Hard,,,docs
17,778,Swim in Rising Water,Graphs,Hard,Dijkstra / minimum-effort path,,docs
17,827,Making A Large Island,Graphs,Hard,Advanced grid + component/DSU technique,,docs
18,70,Climbing Stairs,Dynamic Programming,Easy,,,both
18,121,Best Time to Buy and Sell Stock,Dynamic Programming,Easy,Stock I,,both
18,62,Unique Paths,Dynamic Programming,Medium,Grid Unique Paths,,both
18,63,Unique Paths II,Dynamic Programming,Medium,,,docs
18,64,Minimum Path Sum,Dynamic Programming,Medium,,,leetcode_top100
18,72,Edit Distance,Dynamic Programming,Medium,,,both
18,91,Decode Ways,Dynamic Programming,Medium,,,leetcode_extra
18,96,Unique Binary Search Trees,Dynamic Programming,Medium,,,leetcode_top100
18,120,Triangle,Dynamic Programming,Medium,,,docs
18,122,Best Time to Buy and Sell Stock II,Dynamic Programming,Medium,Stock II,,docs
18,139,Word Break,Dynamic Programming,Medium,,,leetcode_top100
18,152,Maximum Product Subarray,Dynamic Programming,Medium,,,leetcode_top100
18,198,House Robber,Dynamic Programming,Medium,Similar recursion idea for binary choices / subsequence selection,,both
18,213,House Robber II,Dynamic Programming,Medium,,,leetcode_extra
18,221,Maximal Square,Dynamic Programming,Medium,,,leetcode_top100
18,279,Perfect Squares,Dynamic Programming,Medium,,,leetcode_top100
18,300,Longest Increasing Subsequence,Dynamic Programming,Medium,,,both
18,309,Best Time to Buy and Sell Stock with Cooldown,Dynamic Programming,Medium,Stock with Cooldown,,both
18,322,Coin Change,Dynamic Programming,Medium,Minimum Coins,,both
18,337,House Robber III,Dynamic Programming,Medium,,,leetcode_top100
18,368,Largest Divisible Subset,Dynamic Programming,Medium,,,docs
18,377,Combination Sum IV,Dynamic Programming,Medium,,,leetcode_extra
18,416,Partition Equal Subset Sum,Dynamic Programming,Medium,subsequence/subset sum,,both
18,494,Target Sum,Dynamic Programming,Medium,subsequence with sum K,,both
18,516,Longest Palindromic Subsequence,Dynamic Programming,Medium,,,docs
18,518,Coin Change II,Dynamic Programming,Medium,,,docs
18,583,Delete Operation for Two Strings,Dynamic Programming,Medium,Minimum insertions/deletions to convert String A → B (similar),,docs
18,673,Number of Longest Increasing Subsequence,Dynamic Programming,Medium,Number of Longest Increasing Subsequences,,docs
18,714,Best Time to Buy and Sell Stock with Transaction Fee,Dynamic Programming,Medium,Stock with Transaction Fee,,docs
18,718,Maximum Length of Repeated Subarray,Dynamic Programming,Medium,Longest Common Substring,,docs
18,931,Minimum Falling Path Sum,Dynamic Programming,Medium,,,docs
18,1048,Longest String Chain,Dynamic Programming,Medium,,,docs
18,1143,Longest Common Subsequence,Dynamic Programming,Medium,,,docs
18,1277,Count Square Submatrices with All Ones,Dynamic Programming,Medium,,,docs
18,10,Regular Expression Matching,Dynamic Programming,Hard,,,leetcode_top100
18,32,Longest Valid Parentheses,Dynamic Programming,Hard,,,leetcode_top100
18,44,Wildcard Matching,Dynamic Programming,Hard,,,docs
18,115,Distinct Subsequences,Dynamic Programming,Hard,,,docs
18,123,Best Time to Buy and Sell Stock III,Dynamic Programming,Hard,Stock III,,docs
18,188,Best Time to Buy and Sell Stock IV,Dynamic Programming,Hard,Stock IV,,docs
18,312,Burst Balloons,Dynamic Programming,Hard,,,leetcode_top100
18,403,Frog Jump,Dynamic Programming,Hard,,,docs
18,1092,Shortest Common Supersequence,Dynamic Programming,Hard,,,docs
18,1235,Maximum Profit in Job Scheduling,Dynamic Programming,Hard,Job Sequencing with DP and Binary Search,,docs
18,1312,Minimum Insertion Steps to Make a String Palindrome,Dynamic Programming,Hard,Minimum insertions to make string palindrome,,docs
18,1463,Cherry Pickup II,Dynamic Programming,Hard,,,docs
18,1671,Minimum Number of Removals to Make Mountain Array,Dynamic Programming,Hard,Longest Bitonic Subsequence,,docs
18,2035,Partition Array Into Two Arrays to Minimize Sum Difference,Dynamic Programming,Hard,Partition into two subsets with minimum absolute sum difference,,docs
"""

def generate_slug(title):
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title.lower())
    slug = re.sub(r'[\s_]+', '-', slug).strip('-')
    return slug

topic_prereqs = {
    "Arrays": [],
    "Math": ["Arrays"],
    "Hashing": ["Arrays"],
    "Strings": ["Arrays"],
    "Two Pointers": ["Arrays"],
    "Sliding Window": ["Arrays", "Two Pointers"],
    "Bit Manipulation": ["Math"],
    "Stack": ["Arrays", "Linked List"],
    "Queue": ["Arrays", "Linked List"],
    "Linked List": ["Pointers"],
    "Binary Search": ["Arrays", "Two Pointers"],
    "Recursion & Backtracking": ["Stack"],
    "Greedy": ["Arrays", "Sorting"],
    "Binary Tree": ["Recursion & Backtracking"],
    "Binary Search Tree": ["Binary Tree", "Binary Search"],
    "Heap": ["Binary Tree", "Arrays"],
    "Trie": ["Strings", "Binary Tree"],
    "Graphs": ["Recursion & Backtracking", "Queue", "Stack"],
    "Dynamic Programming": ["Recursion & Backtracking", "Arrays"]
}

default_similar = {
    "Jump Game": "Greedy Reachability",
    "Jump Game II": "BFS / Greedy Step Count",
    "Best Time to Buy and Sell Stock": "Single-Pass Peak-Valley / Kadane's Variant",
    "Linked List Cycle": "Floyd's Tortoise and Hare Cycle Detection",
    "Reverse Linked List": "Iterative Pointer Reversal",
    "Binary Search": "Divide and Conquer Search",
    "Koko Eating Bananas": "Binary Search on Answer Range",
    "Last Stone Weight": "Max Heap Simulation",
    "Maximum Units on a Truck": "Fractional Knapsack (Greedy by Value/Weight)",
    "Single-Threaded CPU": "Shortest Job First (Min-Heap Event Simulation)",
    "Two Sum": "HashMap Complement Lookup",
    "3Sum": "Two Pointers on Sorted Array",
    "Valid Parentheses": "LIFO Stack Matching",
    "Merge Intervals": "Sorting + Interval Merging",
    "Number of Islands": "Connected Components BFS/DFS",
    "Course Schedule": "Topological Sort / Kahn's Algorithm / Cycle Detection",
    "Climbing Stairs": "Fibonacci Dynamic Programming",
    "Coin Change": "Unbounded Knapsack DP",
    "Longest Increasing Subsequence": "Patience Sorting / 1D DP",
    "Trapping Rain Water": "Two Pointers / Monotonic Stack Elevation",
    "LRU Cache": "Doubly Linked List + HashMap",
    "Word Search": "Backtracking Grid DFS",
    "Search in Rotated Sorted Array": "Modified Binary Search with Sorted Half Detection"
}

def parse_csv_and_enrich():
    lines = raw_csv_data.strip().split('\n')[1:]
    problems = []
    
    for idx, line in enumerate(lines, start=1):
        parts = [p.strip() for p in line.split(',')]
        if len(parts) < 5:
            continue
        day = int(parts[0]) if parts[0].isdigit() else 1
        lc_no = int(parts[1]) if parts[1].isdigit() else idx
        title = parts[2]
        topic = parts[3]
        difficulty = parts[4].capitalize()
        similar_to = parts[5] if len(parts) > 5 and parts[5] else default_similar.get(title, f"{topic} Pattern")
        note = parts[6] if len(parts) > 6 and parts[6] else ""
        source = parts[7] if len(parts) > 7 and parts[7] else "built_in"
        
        slug = generate_slug(title)
        
        prereqs = topic_prereqs.get(topic, ["Basic Programming"])
        topics_list = [topic]
        if "Tree" in topic and topic != "Binary Tree":
            topics_list.append("Tree")
        if topic == "Dynamic Programming":
            topics_list.append("Algorithms")
        if topic in ["Two Pointers", "Sliding Window"]:
            topics_list.append("Arrays")
            
        estimated_minutes = 20 if difficulty == "Easy" else 35 if difficulty == "Medium" else 55
        
        prob = {
            "id": idx,
            "leetcode_number": lc_no,
            "title": title,
            "slug": slug,
            "difficulty": difficulty,
            "topics": topics_list,
            "subtopics": [f"{topic} Core", f"{difficulty} Level"],
            "source": source,
            "description": f"Standard {difficulty} LeetCode #{lc_no} problem focusing on {topic}.",
            "similar_problems": [similar_to] if similar_to else [],
            "similar_concept": similar_to,
            "prerequisites": prereqs,
            "estimated_minutes": estimated_minutes,
            "note": note,
            "suggested_day": day
        }
        problems.append(prob)
        
    return problems

if __name__ == "__main__":
    problems = parse_csv_and_enrich()
    
    os.makedirs("app/data", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    os.makedirs("uploads", exist_ok=True)
    
    with open("app/data/problems.json", "w", encoding="utf-8") as f:
        json.dump(problems, f, indent=2)
        
    with open("data/problems.json", "w", encoding="utf-8") as f:
        json.dump(problems, f, indent=2)
        
    # Write sample files for upload testing
    # 1. Sample TXT
    sample_txt_content = """DSA Preparation Sheet - Core Problems
55 — Jump Game
121 — Best Time to Buy and Sell Stock
141 — Linked List Cycle
206 — Reverse Linked List
704 — Binary Search
875 — Koko Eating Bananas
1046 — Last Stone Weight
1710 — Maximum Units on a Truck
1834 — Single-Threaded CPU
1 — Two Sum
15 — 3Sum
20 — Valid Parentheses
53 — Maximum Subarray
200 — Number of Islands
300 — Longest Increasing Subsequence
"""
    with open("uploads/sample_dsa_sheet.txt", "w", encoding="utf-8") as f:
        f.write(sample_txt_content)
        
    # 2. Sample CSV
    sample_csv_content = """leetcode_number,title,difficulty,topic,similar_concept
55,Jump Game,Medium,Greedy,Greedy Reachability
121,Best Time to Buy and Sell Stock,Easy,Dynamic Programming,Stock I
141,Linked List Cycle,Easy,Linked List,Floyd Tortoise and Hare
206,Reverse Linked List,Easy,Linked List,Pointer Reversal
704,Binary Search,Easy,Binary Search,Divide and Conquer
875,Koko Eating Bananas,Medium,Binary Search,Binary Search on Answer
1046,Last Stone Weight,Easy,Heap,Max Heap Simulation
1710,Maximum Units on a Truck,Easy,Greedy,Fractional Knapsack
1834,Single-Threaded CPU,Medium,Greedy,Shortest Job First
"""
    with open("uploads/sample_dsa_sheet.csv", "w", encoding="utf-8") as f:
        f.write(sample_csv_content)
        
    # Try generating sample docx and pdf if libraries are present
    try:
        from docx import Document
        doc = Document()
        doc.add_heading('My DSA Target Problems Sheet', 0)
        doc.add_paragraph('Here are the problems selected for preparation:')
        for item in [
            "55 — Jump Game (Medium, Greedy)",
            "121 — Best Time to Buy and Sell Stock (Easy, DP)",
            "141 — Linked List Cycle (Easy, Linked List)",
            "206 — Reverse Linked List (Easy, Linked List)",
            "704 — Binary Search (Easy, Binary Search)",
            "875 — Koko Eating Bananas (Medium, Binary Search)",
            "1046 — Last Stone Weight (Easy, Heap)",
            "1710 — Maximum Units on a Truck (Easy, Greedy)",
            "1834 — Single-Threaded CPU (Medium, Greedy/Heap)",
            "1 — Two Sum (Easy, Hashing)",
            "200 — Number of Islands (Medium, Graphs)"
        ]:
            doc.add_paragraph(item, style='List Bullet')
        doc.save("uploads/sample_dsa_sheet.docx")
    except Exception as e:
        print("Docx creation skipped:", e)
        
    print(f"Successfully generated {len(problems)} enriched problems in data files!")
