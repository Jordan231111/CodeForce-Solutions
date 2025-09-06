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


def compute_Ts(n:int):
    inv2 = (mod+1)//2
    s1 = [0]*(n+1)
    s2 = [0]*(n+1)
    for i in range(1, n+1):
        s1[i] = (s1[i-1] + i) % mod
        s2[i] = (s2[i-1] + i*i) % mod
    sumB_total = s1[n]
    Ts = [0]*(n+1)
    for L in range(2, n+1):
        K = L-1
        Q = (n + L - 1) // L
        SumA = 0
        SumA2 = 0
        SumAB = 0
        for q in range(1, Q+1):
            l = (q-1)*L + 1
            r = n if q*L > n else q*L
            cnt = r - l + 1
            sumB = (s1[r] - s1[l-1]) % mod
            sumB2 = (s2[r] - s2[l-1]) % mod
            SumA = (SumA + sumB - q*cnt) % mod
            SumA2 = (SumA2 + sumB2 - (2*q % mod)*sumB + (q*q % mod)*cnt) % mod
            SumAB = (SumAB + sumB2 - q*sumB) % mod
        Ts[L] = ( (L*inv2 % mod) * ((SumA2 + SumA) % mod) + (K % mod) * (n % mod) % mod * sumB_total % mod - (K % mod) * SumAB % mod ) % mod
    return Ts


def solve():
    t = II()
    cache = {}
    out = []
    for _ in range(t):
        n = II()
        p = LI()
        vis = [0]*(n+1)
        cnt = DD(int)
        for i in range(1, n+1):
            if vis[i]:
                continue
            cur = i
            l = 0
            while not vis[cur]:
                vis[cur] = 1
                cur = p[cur-1]
                l += 1
            if l >= 2:
                cnt[l] += 1
        if n not in cache:
            cache[n] = compute_Ts(n)
        Ts = cache[n]
        ans = 0
        for L, c in cnt.items():
            ans = (ans + c * Ts[L]) % mod
        out.append(str(ans))
    print('\n'.join(out))


if __name__ == '__main__':
    solve()


