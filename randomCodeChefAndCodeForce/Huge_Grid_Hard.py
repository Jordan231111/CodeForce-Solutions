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


def precompute_factorials(max_n: int, mod: int):
    fac = [1] * (max_n + 1)
    ifac = [1] * (max_n + 1)
    for i in range(1, max_n + 1):
        fac[i] = fac[i-1] * i % mod
    ifac[max_n] = pow(fac[max_n], mod - 2, mod)
    for i in range(max_n - 1, -1, -1):
        ifac[i] = ifac[i+1] * (i+1) % mod
    return fac, ifac


def C(n: int, k: int, fac, ifac):
    if k < 0 or k > n or n < 0:
        return 0
    return fac[n] * ifac[k] % mod * ifac[n-k] % mod


def solve():
    t = II()
    Ns = []
    As = []
    totalN = 0
    for _ in range(t):
        n = II()
        s = SI()
        Ns.append(n)
        As.append(s)
        totalN += n
    maxN = max(Ns) if Ns else 0
    # factorials up to 2*maxN
    fac, ifac = precompute_factorials(2*maxN + 5, mod)

    out_lines = []
    for case in range(t):
        n = Ns[case]
        s = As[case]
        a = [1 if ch == '1' else 0 for ch in s]

        # collect internal constrained indices (1..n-1) where A_t=1
        ones = [i+1 for i in range(n-1) if a[i] == 1]

        # helper for gap transition matrix application
        def apply_gap(vec0_a: int, vec0_b: int, g: int):
            if g == 0:
                na = (2*vec0_a + vec0_b) % mod
                nb = (vec0_a + 2*vec0_b) % mod
                return na, nb
            val = C(2*g, g, fac, ifac)
            ssum = (vec0_a + vec0_b) % mod
            na = val * ssum % mod
            nb = na
            return na, nb

        if not ones:
            if a[-1] == 1:
                if n == 1:
                    out_lines.append('1')
                else:
                    ans = (2 * C(2*n - 4, n - 2, fac, ifac)) % mod
                    out_lines.append(str(ans))
            else:
                ans = C(2*n - 2, n - 1, fac, ifac)
                out_lines.append(str(ans % mod))
            continue

        # initialize vector at first one
        t1 = ones[0]
        if t1 == 1:
            vr = 1
            vd = 1
        else:
            g0 = t1 - 1
            # number of ways to get to posR/posD at t1 with minimal at t1
            base = (2 * C(2*(g0-1), g0-1, fac, ifac)) % mod  # 2 * C(2*t1-4, t1-2)
            vr = base
            vd = base

        # process subsequent ones
        for idx in range(len(ones) - 1):
            tcur = ones[idx]
            tnext = ones[idx+1]
            g = tnext - tcur - 1
            vr, vd = apply_gap(vr, vd, g)

        # finalize to the end
        tL = ones[-1]
        if a[-1] == 1:
            g_end = (n - 1) - tL
            if g_end == 0:
                ans = (vr + vd) % mod
            else:
                mul = (2 * C(2*g_end - 1, g_end, fac, ifac)) % mod
                ans = ( (vr + vd) % mod ) * mul % mod
            out_lines.append(str(ans))
        else:
            # free tail
            g_end = (n - 1) - tL
            # ways from posR (tL, tL+1) to (n, n)
            waysR = C(2*g_end + 1, g_end + 1, fac, ifac)
            # ways from posD (tL+1, tL) to (n, n)
            waysD = C(2*g_end + 1, g_end, fac, ifac)
            ans = (vr * waysR + vd * waysD) % mod
            out_lines.append(str(ans))

    print('\n'.join(out_lines))


if __name__ == '__main__':
    solve()


