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

def precompute_fact(max_n):
    fact = [1]*(max_n+1)
    invfact = [1]*(max_n+1)
    for i in range(1, max_n+1):
        fact[i] = fact[i-1]*i % mod
    invfact[max_n] = pow(fact[max_n], mod-2, mod)
    for i in range(max_n, 0, -1):
        invfact[i-1] = invfact[i]*i % mod
    return fact, invfact

def comb(n, k, fact, invfact):
    if k < 0 or k > n or n < 0:
        return 0
    return fact[n]*invfact[k]%mod*invfact[n-k]%mod

def runs_count(total, runs, fact, invfact):
    if runs == 0:
        return 1 if total == 0 else 0
    if runs < 0 or runs > total:
        return 0
    return comb(total-1, runs-1, fact, invfact)

def solve():
    t = II()
    cases = []
    maxN = 0
    for _ in range(t):
        n,k = MI()
        cases.append(n)
        if n > maxN:
            maxN = n
    fact, invfact = precompute_fact(maxN+2)
    out = []
    for n in cases:
        q, r = divmod(n, 3)
        c0 = q
        c1 = q + (1 if r >= 1 else 0)
        c2 = q + (1 if r == 2 else 0)
        L = c1 + c2
        total = 0
        if L > 0:
            for runs in (c0-1, c0, c0+1):
                if runs < 1 or runs > L:
                    continue
                z = c0 - (runs - 1)
                if z == 0:
                    ways_zero = 1
                elif z == 1:
                    ways_zero = 2
                elif z == 2:
                    ways_zero = 1
                else:
                    continue
                A_lo = 0 if runs <= c2 else runs - c2
                A_hi = runs if runs <= c1 else c1
                Nr = 0
                for A in range(A_lo, A_hi+1):
                    term = comb(runs, A, fact, invfact)
                    term = term * runs_count(c1, A, fact, invfact) % mod
                    term = term * runs_count(c2, runs - A, fact, invfact) % mod
                    Nr = (Nr + term) % mod
                total = (total + ways_zero * Nr) % mod
        total = total * fact[c0] % mod
        total = total * fact[c1] % mod
        total = total * fact[c2] % mod
        out.append(str(total))
    print("\n".join(out))

if __name__ == "__main__":
    solve()

