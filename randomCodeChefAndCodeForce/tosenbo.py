# input
import sys
# input = sys.stdin.readline
import os
import io
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

def solve(n, a, b):
    # Helper functions --------------------------------------------------
    def lsb(x: int) -> int:
        """index of least–significant set bit (0-based)"""
        return (x & -x).bit_length() - 1

    def next_value(lower: int, required: int, forbidden: int) -> int | None:
        """Minimal y ≥ lower such that:
        1. required ⊆ bits(y)
        2. bits(y) ∩ forbidden = ∅
        Returns None if impossible."""
        if required & forbidden:
            return None

        y = lower
        if y < required:
            y = required
        y |= required  # set mandatory bits

        while y & forbidden:
            k = lsb(y & forbidden)          # offending bit
            y = ((y >> (k + 1)) + 1) << (k + 1)  # bump at (k+1) and clear below
            y |= required                   # re-add mandatory bits
        return y

    # Pre-compute mandatory mask M[i] = a_{i-1} | a_i -------------------
    M = [0] * n
    for i in range(n):
        left = a[i - 1] if i else 0
        right = a[i] if i < n - 1 else 0
        M[i] = left | right

    B = [0] * n  # final values

    # Construct B incrementally, with local back-tracking when needed -----
    B[0] = next_value(max(b[0], M[0]), M[0], 0)
    if B[0] is None:
        print(-1)
        return

    for i in range(1, n):
        # We may need to back-track to i-1 if forbidden overlap occurs
        while True:
            forbidden = B[i - 1] & ~a[i - 1]        # bits that *must not* appear in B[i]
            candidate = next_value(max(b[i], M[i]), M[i], forbidden)

            if candidate is not None:
                B[i] = candidate
                break  # success for this index

            # Overlap between required and forbidden -> have to adjust B[i-1]
            overlap = M[i] & forbidden
            if overlap == 0:
                print(-1)
                return

            k = lsb(overlap)
            B[i - 1] += 1 << k  # increment to flip bit k to 0 via carry

            # Propagate fix leftwards to maintain previous relations
            j = i - 1
            while j > 0:
                extra = (B[j] & B[j - 1]) & ~a[j - 1]
                if extra == 0:
                    break
                k2 = lsb(extra)
                B[j] += 1 << k2
                j -= 1

    # Final verification -------------------------------------------------
    for i in range(n - 1):
        if (B[i] & B[i + 1]) != a[i]:
            print(-1)
            return

    if any(B[i] < b[i] for i in range(n)):
        print(-1)
        return

    print(sum(B) - sum(b))

def main():
    data = io.BytesIO(os.read(0, os.fstat(0).st_size)).read().split()
    data_ptr = 0

    def next_int():
        nonlocal data_ptr
        data_ptr += 1
        return int(data[data_ptr - 1])

    t = next_int()
    for _ in range(t):
        n = next_int()
        a = [next_int() for _ in range(n - 1)]
        b = [next_int() for _ in range(n)]
        solve(n, a, b)

if __name__ == "__main__":
    main() 