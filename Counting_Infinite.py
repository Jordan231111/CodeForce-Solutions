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

def prepare_factorials(n:int):
    fact=[1]*(n+1)
    for i in range(1,n+1):
        fact[i]=fact[i-1]*i%mod
    invfact=[1]*(n+1)
    invfact[n]=pow(fact[n],mod-2,mod)
    for i in range(n,0,-1):
        invfact[i-1]=invfact[i]*i%mod
    return fact,invfact

def solve_case(N:int,K:int,fact:list[int],invfact:list[int]):
    if 2*K>N:
        return pow(K%mod,N,mod)
    S_prev=[0]*(K+1)
    S_prev[0]=1
    diag=[0]*(K+1)
    for n in range(1,N+1):
        S_curr=[0]*(K+1)
        lim=min(n,K)
        for k in range(1,lim+1):
            S_curr[k]=(S_prev[k-1]+k*S_prev[k])%mod
        S_prev=S_curr
        s=N-n
        if 0<=s<=K:
            diag[s]=S_prev[K-s]
    factK=fact[K]
    def falling(n,s):
        return fact[n]*invfact[n-s]%mod
    total=0
    for s in range(K+1):
        sign=-1 if s&1 else 1
        term=invfact[s]*falling(N,s)%mod
        term=term*diag[s]%mod
        if sign==1:
            total=(total+term)%mod
        else:
            total=(total-term)%mod
    invalid=factK*total%mod
    return (pow(K%mod,N,mod)-invalid)%mod

def main():
    T=II()
    cases=[tuple(MI()) for _ in range(T)]
    maxN=max(n for n,_ in cases)
    fact,invfact=prepare_factorials(maxN)
    for N,K in cases:
        print(solve_case(N,K,fact,invfact))

if __name__=="__main__":
    main()
