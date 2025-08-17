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

def build_allowed_patterns():
    from itertools import permutations
    def eq(p, K):
        r = K
        S = set()
        for x in p:
            if x <= r and x not in S:
                r -= x
                S.add(x)
        r = K
        T = set()
        for x in reversed(p):
            if x <= r and x not in T:
                r -= x
                T.add(x)
        return S == T
    P3 = []
    for p in __import__('itertools').permutations([1,2,3]):
        if eq(p,3):
            P3.append(list(p))
    P6 = []
    for p in __import__('itertools').permutations([1,2,3,4,5,6]):
        if eq(p,6):
            P6.append(list(p))
    return P3, P6

PATS3, PATS6 = build_allowed_patterns()

MAXN = 200000 + 5
fact = [1]* (MAXN)
invfact = [1]* (MAXN)
for i in range(1, MAXN):
    fact[i] = fact[i-1] * i % mod
invfact[-1] = pow(fact[-1], mod-2, mod)
for i in range(MAXN-1, 0, -1):
    invfact[i-1] = invfact[i] * i % mod

def nCk(n,k):
    if n < 0 or k < 0 or k > n: return 0
    return fact[n] * invfact[k] % mod * invfact[n-k] % mod

def count_for_patterns(N, arr, M, patterns):
    pos = [-1] * (M+1)
    present = [False]*(M+1)
    free = [1 if x==-1 else 0 for x in arr]
    pref = [0]*(N+1)
    for i in range(N):
        pref[i+1] = pref[i] + free[i]
        v = arr[i]
        if 1 <= v <= M:
            pos[v] = i
            present[v] = True
    U = pref[N]
    missing = [v for v in range(1,M+1) if not present[v]]
    cM = len(missing)
    total = 0
    for pat in patterns:
        fixed_idx_pos = []
        for idx, v in enumerate(pat):
            if present[v]:
                fixed_idx_pos.append((idx, pos[v]))
        ok = True
        for i in range(1, len(fixed_idx_pos)):
            if fixed_idx_pos[i-1][1] >= fixed_idx_pos[i][1]:
                ok = False
                break
        if not ok:
            continue
        last_idx = -1
        last_pos = -1
        ways = 1
        fps = fixed_idx_pos + [(M, N)]
        ptr = 0
        while ptr < len(fps):
            nxt_idx, nxt_pos = fps[ptr]
            need = 0
            for j in range(last_idx+1, nxt_idx):
                if not present[pat[j]]:
                    need += 1
            avail = pref[nxt_pos] - pref[last_pos+1]
            ways = ways * nCk(avail, need) % mod
            last_idx, last_pos = nxt_idx, nxt_pos
            ptr += 1
        total = (total + ways) % mod
    total = total * fact[U - cM] % mod
    return total

def solve():
    t = II()
    out = []
    for _ in range(t):
        n = II()
        a = LI()
        ans = 0
        ans = (ans + count_for_patterns(n, a, 3, PATS3)) % mod
        ans = (ans + count_for_patterns(n, a, 6, PATS6)) % mod
        out.append(str(ans))
    print("\n".join(out))

if __name__ == "__main__":
    solve()


