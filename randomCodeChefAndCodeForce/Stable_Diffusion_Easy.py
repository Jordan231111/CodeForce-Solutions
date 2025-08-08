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

def even_stable(a, l, r):
    m = r - l + 1
    dp0 = [0]*16
    dp1 = [0]*16
    for yl in (0,1):
        for yr in (0,1):
            s = (yl<<1) | (yr<<2)
            if yl|yr:
                dp1[s] = 1
            else:
                dp0[s] = 1
    steps = m//2
    for t in range(steps):
        L = l + t
        R = r - t
        l2 = 1 if L>l and a[L-1]==2 else 0
        r2 = 1 if L<r and a[L+1]==2 else 0
        rl2 = 1 if R>l and a[R-1]==2 else 0
        rr2 = 1 if R<r and a[R+1]==2 else 0
        last = t == steps-1
        if not last:
            ndp0 = [0]*16
            ndp1 = [0]*16
        found = 0
        for zf in (0,1):
            dp = dp1 if zf else dp0
            for s in range(16):
                if dp[s]==0:
                    continue
                b0 = s & 1
                b1 = (s>>1)&1
                b2 = (s>>2)&1
                b3 = (s>>3)&1
                if L+1 < R-1:
                    for x in (0,1):
                        bl = b1 + l2*b0 + r2*x
                        for y in (0,1):
                            br = b2 + rl2*y + rr2*b3
                            if bl==br:
                                ns = b1 | (x<<1) | (y<<2) | (b2<<3)
                                if zf | x | y:
                                    ndp1[ns] = 1
                                else:
                                    ndp0[ns] = 1
                elif L+1 == R-1:
                    for x in (0,1):
                        bl = b1 + l2*b0 + r2*x
                        br = b2 + rl2*x + rr2*b3
                        if bl==br:
                            ns = b1 | (x<<1) | (x<<2) | (b2<<3)
                            if zf | x:
                                ndp1[ns] = 1
                            else:
                                ndp0[ns] = 1
                else:
                    x = b2
                    y = b1
                    bl = b1 + l2*b0 + r2*x
                    br = b2 + rl2*y + rr2*b3
                    if bl==br and zf:
                        return 1
        if last:
            return 0
        dp0, dp1 = ndp0, ndp1
    return 0

def solve():
    t = II()
    out = []
    for _ in range(t):
        n = II()
        a = LI()
        ans = 0
        for i in range(n):
            for j in range(i, n):
                m = j - i + 1
                if m & 1:
                    ans += 1
                else:
                    ans += even_stable(a, i, j)
        out.append(str(ans))
    print("\n".join(out))

if __name__ == "__main__":
    solve()


