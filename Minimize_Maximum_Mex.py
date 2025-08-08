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
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        freq = [0]*(n+2)
        A = [0]*n
        B = [0]*n
        # read array A and count frequencies
        for i in range(n):
            v = int(data[idx+i])
            A[i] = v
            freq[v] += 1
        idx += n
        # read array B and count frequencies
        for i in range(n):
            v = int(data[idx+i])
            B[i] = v
            freq[v] += 1
        idx += n

        forced = [False]*(n+2)  # value forced to appear in both arrays
        for i in range(n):
            if A[i] == B[i]:
                forced[A[i]] = True

        presenceA = [False]*(n+2)
        presenceB = [False]*(n+2)
        # place forced values in both arrays
        for v in range(n+1):
            if forced[v]:
                presenceA[v] = presenceB[v] = True

        turn = 0  # 0 -> assign to A, 1 -> assign to B alternately for optional values
        for v in range(n+1):
            if forced[v] or freq[v] == 0:
                continue
            # optional value (appears >=1 but not forced)
            if turn == 0:
                presenceA[v] = True
            else:
                presenceB[v] = True
            turn ^= 1

        mexA = 0
        while presenceA[mexA]:
            mexA += 1
        mexB = 0
        while presenceB[mexB]:
            mexB += 1
        ans = mexA if mexA > mexB else mexB
        out.append(str(ans))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()

