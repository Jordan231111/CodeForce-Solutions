# input
import sys
input = sys.stdin.readline
II = lambda : int(input())
MI = lambda : map(int, input().split())
LI = lambda : [int(a) for a in input().split()]
SI = lambda : input().rstrip()
LLI = lambda n : [[int(a) for a in input().split()] for _ in range(n)]
LSI = lambda n : [input().rstrip() for _ in range(n)]
MI_1 = lambda : map(lambda x:int(x)-1, input().split())
LI_1 = lambda : [int(a)-1 for a in input().split()]

def graph(n:int, m:int, dir:bool=False, index:int=-1) -> list[set[int]]:
    edge = [set() for i in range(n+1+index)]
    for _ in range(m):
        a,b = map(int, input().split())
        a += index
        b += index
        edge[a].add(b)
        if not dir:
            edge[b].add(a)
    return edge

def graph_w(n:int, m:int, dir:bool=False, index:int=-1) -> list[set[tuple]]:
    edge = [set() for i in range(n+1+index)]
    for _ in range(m):
        a,b,c = map(int, input().split())
        a += index
        b += index
        edge[a].add((b,c))
        if not dir:
            edge[b].add((a,c))
    return edge

mod = 998244353
inf = 1001001001001001001
ordalp = lambda s : ord(s)-65 if s.isupper() else ord(s)-97
ordallalp = lambda s : ord(s)-39 if s.isupper() else ord(s)-97
yes = lambda : print("Yes")
no = lambda : print("No")
yn = lambda flag : print("Yes" if flag else "No")
def acc(a:list[int]):
    sa = [0]*(len(a)+1)
    for i in range(len(a)):
        sa[i+1] = a[i] + sa[i]
    return sa

prinf = lambda ans : print(ans if ans < 1000001001001001001 else -1)
alplow = "abcdefghijklmnopqrstuvwxyz"
alpup = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alpall = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
URDL = {'U':(-1,0), 'R':(0,1), 'D':(1,0), 'L':(0,-1)}
DIR_4 = [[-1,0],[0,1],[1,0],[0,-1]]
DIR_8 = [[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]]
DIR_BISHOP = [[-1,1],[1,1],[1,-1],[-1,-1]]
prime60 = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59]
sys.set_int_max_str_digits(0)
# sys.setrecursionlimit(10**6)
# import pypyjit
# pypyjit.set_param('max_unroll_recursion=-1')

from collections import defaultdict,deque
from heapq import heappop,heappush
from bisect import bisect_left,bisect_right
DD = defaultdict
BSL = bisect_left
BSR = bisect_right

def solve():
    n = II()
    p = LI()
    # Optimal algorithm: compute for each position the number of larger elements preceding (B) and following (A).
    # Minimal inversions equals sum of min(A_i, B_i).
    if n == 1:
        print(0)
        return

    # Fenwick Tree helper functions
    bit = [0] * (n + 2)
    def bit_add(i):
        while i < len(bit):
            bit[i] += 1
            i += i & -i
    def bit_sum(i):
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s

    # Compute B_i: number of earlier elements greater than p[i]
    B = [0] * n
    for idx, val in enumerate(p):
        less_or_equal = bit_sum(val)
        B[idx] = idx - less_or_equal  # elements before idx minus those <= val gives count greater than val
        bit_add(val)

    # Reset BIT to compute A_i: number of later elements greater than p[i]
    bit = [0] * (n + 2)
    A = [0] * n
    total_seen = 0
    for idx in range(n - 1, -1, -1):
        val = p[idx]
        greater_later = total_seen - bit_sum(val)  # elements already seen to the right that are > val
        A[idx] = greater_later
        bit_add(val)
        total_seen += 1

    # Minimal inversions is sum of min(A_i, B_i)
    ans = 0
    for a, b in zip(A, B):
        ans += a if a < b else b
    print(ans)
    return
    
    if n == 1:
        print(0)
        return
    
    def count_inversions(arr):
        """Count inversions in array efficiently"""
        def merge_sort_and_count(arr, temp, left, right):
            inv_count = 0
            if left < right:
                mid = (left + right) // 2
                inv_count += merge_sort_and_count(arr, temp, left, mid)
                inv_count += merge_sort_and_count(arr, temp, mid + 1, right)
                inv_count += merge_and_count(arr, temp, left, mid, right)
            return inv_count
        
        def merge_and_count(arr, temp, left, mid, right):
            i, j, k = left, mid + 1, left
            inv_count = 0
            
            while i <= mid and j <= right:
                if arr[i] <= arr[j]:
                    temp[k] = arr[i]
                    i += 1
                else:
                    temp[k] = arr[j]
                    inv_count += (mid - i + 1)
                    j += 1
                k += 1
            
            while i <= mid:
                temp[k] = arr[i]
                i += 1
                k += 1
            
            while j <= right:
                temp[k] = arr[j]
                j += 1
                k += 1
            
            for i in range(left, right + 1):
                arr[i] = temp[i]
            
            return inv_count
        
        arr_copy = arr[:]
        temp = [0] * len(arr)
        return merge_sort_and_count(arr_copy, temp, 0, len(arr) - 1)
    
    # For small n, use brute force to find optimal solution
    if n <= 20:
        min_inv = float('inf')
        
        # Try all 2^n possibilities
        for mask in range(1 << n):
            result = []
            for i in range(n):
                if mask & (1 << i):
                    # Mirror
                    result.append(2 * n - p[i])
                else:
                    # Stay
                    result.append(p[i])
            
            inv = count_inversions(result)
            min_inv = min(min_inv, inv)
        
        print(min_inv)
        return
    
    # Final optimal algorithm based on analytical proof
    strategies = []
    
    # Strategy 1: Smart greedy based on observed patterns
    # From analysis: prefer to keep smaller values, mirror larger ones
    values_with_idx = [(p[i], i) for i in range(n)]
    values_with_idx.sort()
    
    # Try different split points, but optimize for large n
    if n <= 1000:
        # For moderate n, try all split points
        split_points = range(n + 1)
    else:
        # For large n, try only promising split points
        split_points = [0, n//4, n//2, 3*n//4, n]
        # Add some points around median
        median = n // 2
        split_points.extend(range(max(0, median - 5), min(n + 1, median + 6)))
        split_points = sorted(set(split_points))
    
    for split in split_points:
        result = [0] * n
        for i in range(split):
            val, idx = values_with_idx[i]
            result[idx] = val  # Stay
        for i in range(split, n):
            val, idx = values_with_idx[i]
            result[idx] = 2 * n - val  # Mirror
        strategies.append(count_inversions(result))
    
    # Strategy 2: Threshold-based approach (limited thresholds for large n)
    if n <= 500:
        threshold_range = range(1, n + 1)
    else:
        # For large n, try only some key thresholds
        threshold_range = [1, n//4, n//2, 3*n//4, n]
    
    for threshold in threshold_range:
        result = []
        for i in range(n):
            if p[i] <= threshold:
                result.append(p[i])  # Stay
            else:
                result.append(2 * n - p[i])  # Mirror
        strategies.append(count_inversions(result))
    
    # Strategy 3: Mirror values above median
    median = (n + 1) // 2
    result = []
    for i in range(n):
        if p[i] <= median:
            result.append(p[i])  # Stay
        else:
            result.append(2 * n - p[i])  # Mirror
    strategies.append(count_inversions(result))
    
    print(min(strategies))

t = II()
for _ in range(t):
    solve()
