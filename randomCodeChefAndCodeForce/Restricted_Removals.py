# input
import sys, re

data_tokens = [tok for tok in re.findall(r'-?\d+', sys.stdin.read())]
ptr = 0

def next_int():
    global ptr
    val = int(data_tokens[ptr])
    ptr += 1
    return val

def next_bits(k: int):
    global ptr
    bits = data_tokens[ptr:ptr + k]
    ptr += k
    return ''.join(bits)

# dummy aliases kept for compatibility, though unused below
II = next_int
MI = lambda: (next_int(), next_int())


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

def main():
    t = II()
    for _ in range(t):
        n, m = MI()
        A = ''.join(input().split())  # read n bits
        B_raw = ''.join(input().split())  # read m bits
        # Extend B cyclically to length n for ease of indexing
        if m == 0:
            print(n)
            continue
        B = (B_raw * ((n + m - 1) // m))[:n]

        last_pos = {'0': -10**9, '1': -10**9}
        deletions_so_far = 0  # Mi in the editorial
        cannot_delete = 0
        for i in range(n):
            last_pos[B[i]] = i  # update latest position of B[i]
            ch = A[i]
            if last_pos[ch] >= i - deletions_so_far:
                deletions_so_far += 1  # Ai is deletable
            else:
                cannot_delete += 1      # Ai must remain
        print(cannot_delete)

if __name__ == "__main__":
    main()

