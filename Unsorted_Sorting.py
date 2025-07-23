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
import io
import os
fact = [1]
for i in range(1,101):
    fact.append(fact[-1]*i%mod)
invfact = [pow(f,mod-2,mod) for f in fact]
def compute_number(N,L,X):
    if L <= 1:
        return 0
    if L > N:
        return fact[N-1]%mod
    W = N - L +1
    dp = [[[[0 for _ in range(3)] for _ in range(N+1)] for _ in range(N+1)] for _ in range(2)]
    cur = 0
    dp[cur][0][0][0] =1
    for s in range(W):
        nxt = 1-cur
        for q in range(N+1):
            for r in range(N+1):
                for t in range(3):
                    dp[nxt][q][r][t] =0
        cur_s = s+1
        for q in range(N+1):
            for r in range(N+1):
                for t in range(3):
                    val = dp[cur][q][r][t]
                    if val ==0:
                        continue
                    close_val = val
                    close_q = q
                    close_r = r
                    close_t = t
                    if r >0 and cur_s > q+1:
                        eff = r-1 if t==1 else r
                        if eff <0:
                            continue
                        close_val = val * invfact[eff] % mod
                        close_q =0
                        close_r =0
                        close_t =0
                    next_q = close_q
                    next_r = close_r
                    next_t = close_t
                    dp[nxt][next_q][next_r][next_t] = (dp[nxt][next_q][next_r][next_t] + close_val) % mod
                    place_val = close_val * (mod -1) % mod
                    new_min = cur_s
                    new_max = cur_s + L -1
                    if new_max >N:
                        continue
                    new_t_temp = -1
                    if new_max <X:
                        new_t_temp =0
                    elif cur_s >X:
                        new_t_temp =2
                    elif cur_s ==X:
                        new_t_temp =1
                    else:
                        continue
                    if new_t_temp ==-1:
                        continue
                    if close_r ==0:
                        new_q = new_max
                        new_r = L
                        new_t = new_t_temp
                    else:
                        if cur_s > close_q +1:
                            new_q = new_max
                            new_r = L
                            new_t = new_t_temp
                        else:
                            old_min = close_q - close_r +1
                            merged_min = min(old_min, cur_s)
                            merged_max = max(close_q, new_max)
                            merged_r = merged_max - merged_min +1
                            contains = (merged_min <=X <= merged_max)
                            has_left = (merged_min <X)
                            if contains and has_left:
                                continue
                            merged_t = -1
                            if not contains:
                                if merged_max <X:
                                    merged_t =0
                                else:
                                    merged_t =2
                            else:
                                merged_t =1
                            new_q = merged_max
                            new_r = merged_r
                            new_t = merged_t
                    dp[nxt][new_q][new_r][new_t] = (dp[nxt][new_q][new_r][new_t] + place_val) % mod
        cur = nxt
    total =0
    for q in range(N+1):
        for r in range(N+1):
            for t in range(3):
                val = dp[cur][q][r][t]
                if val ==0:
                    continue
                if r==0:
                    total = (total + val) % mod
                else:
                    eff = r-1 if t==1 else r
                    if eff<0:
                        continue
                    total = (total + val * invfact[eff] % mod) % mod
    ans = total * fact[N-1] % mod
    return ans
t=II()
for _ in range(t):
    n,k,x=MI()
    if k>n:
        print(0)
        continue
    m = n - k
    num = compute_number(n, m+1, x)
    num2 = compute_number(n, m, x) if m>0 else 0
    ans = (num - num2) % mod
    print(ans)