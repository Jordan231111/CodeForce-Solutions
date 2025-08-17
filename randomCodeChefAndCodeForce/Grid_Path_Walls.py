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

def nCr_prepare(n):
    fact = [1]*(n+1)
    for i in range(1,n+1):
        fact[i] = fact[i-1]*i%mod
    invfact = [1]*(n+1)
    invfact[n] = pow(fact[n], mod-2, mod)
    for i in range(n,0,-1):
        invfact[i-1] = invfact[i]*i%mod
    return fact, invfact

def nCr(n,k,fact,invfact):
    if k<0 or k>n or n<0:
        return 0
    return fact[n]*invfact[k]%mod*invfact[n-k]%mod

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    t = next(it)
    cases = []
    maxd = 0
    for _ in range(t):
        h = next(it); w = next(it); k = next(it)
        cases.append((h,w,k))
        d = h + w - 2
        if d > maxd:
            maxd = d
    fact, invfact = nCr_prepare(maxd if maxd>0 else 1)
    inv2 = (mod+1)//2
    out = []
    for h,w,k in cases:
        d = h + w - 2
        nsp = nCr(d, h-1, fact, invfact)
        outside = (2*(h-1)%mod)*((w-1)%mod)%mod
        if k < d:
            out.append('0')
        elif k == d:
            out.append(str(nsp))
        elif k == d+1:
            ans = nsp * outside % mod
            out.append(str(ans))
        else:
            c2 = outside * ((outside-1)%mod) % mod
            c2 = c2 * inv2 % mod
            pairs = (d-1)%mod * nCr(d-2, h-2, fact, invfact) % mod
            ans = (nsp * c2 - pairs) % mod
            out.append(str(ans))
    sys.stdout.write("\n".join(out))

if __name__ == '__main__':
    main()


