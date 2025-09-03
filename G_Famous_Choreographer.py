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

import os, io

def splitmix64(x):
    x = (x + 0x9e3779b97f4a7c15) & ((1<<64)-1)
    z = x
    z ^= (z >> 30)
    z = (z * 0xbf58476d1ce4e5b9) & ((1<<64)-1)
    z ^= (z >> 27)
    z = (z * 0x94d049bb133111eb) & ((1<<64)-1)
    z ^= (z >> 31)
    return z & ((1<<64)-1)

def build_prefix_both(rows_bytes, n, m, powX, powY, mask):
    W = m + 1
    Sf = [0] * ((n + 1) * W)
    Sg = [0] * ((n + 1) * W)
    seed = (n<<32) ^ (m<<1) ^ 0x123456789ABCDEF
    z = [0]*26
    s0 = seed ^ 0xDEADBEEFCAFEBABE
    for i in range(26):
        s0 = splitmix64(s0 + 0x9e3779b97f4a7c15)
        z[i] = s0 or 1
    for i in range(n):
        rowPow = powX[i]
        row_f = rows_bytes[i]
        row_g = rows_bytes[n-1-i]
        o1 = (i+1)*W
        o0 = i*W
        for j in range(m):
            w = ((z[row_f[j]-97] * rowPow) & mask)
            w = (w * powY[j]) & mask
            Sf[o1 + j + 1] = (Sf[o0 + j + 1] + Sf[o1 + j] - Sf[o0 + j] + w) & mask
            wg = ((z[row_g[m-1-j]-97] * rowPow) & mask)
            wg = (wg * powY[j]) & mask
            Sg[o1 + j + 1] = (Sg[o0 + j + 1] + Sg[o1 + j] - Sg[o0 + j] + wg) & mask
    return Sf, Sg, z

def build_prefix_rev(rows_bytes, n, m, powX, powY, mask, z):
    W = m + 1
    S = [0] * ((n + 1) * W)
    for i in range(n):
        rowPow = powX[i]
        o1 = (i+1)*W
        o0 = i*W
        src_row = rows_bytes[n-1-i]
        for j in range(m):
            w = ((z[src_row[m-1-j]-97] * rowPow) & mask)
            w = (w * powY[j]) & mask
            S[o1 + j + 1] = (S[o0 + j + 1] + S[o1 + j] - S[o0 + j] + w) & mask
    return S

def rect_hash(S, W, r0, c0, h, w, mask):
    i1 = r0
    j1 = c0
    i2 = r0 + h
    j2 = c0 + w
    return (S[i2*W + j2] - S[i1*W + j2] - S[i2*W + j1] + S[i1*W + j1]) & mask

def solve():
    data = io.BytesIO(os.read(0, os.fstat(0).st_size)).read().split()
    it = iter(data)
    t = int(next(it))
    out_lines = []
    MASK = (1<<64) - 1
    for _ in range(t):
        n = int(next(it)); m = int(next(it))
        rows = [next(it) for __ in range(n)]
        powX = [1]*max(1,n)
        powY = [1]*max(1,m)
        if n>1:
            seedx = (n<<17) ^ (m<<3) ^ 0xABCDEF0123456789
            bx = (splitmix64(seedx) | 1) & MASK
            for i in range(1,n):
                powX[i] = (powX[i-1] * bx) & MASK
        if m>1:
            seedy = (n<<7) ^ (m<<23) ^ 0x102030405060708
            by = (splitmix64(seedy) | 1) & MASK
            for j in range(1,m):
                powY[j] = (powY[j-1] * by) & MASK
        Sf, Sg, z = build_prefix_both(rows, n, m, powX, powY, MASK)
        W = m + 1
        minK = (n-1)*m + (m-1)*n + (n-1)*(m-1)
        Sfl = Sf; Sgl = Sg; powXl = powX; powYl = powY; mask = MASK
        for ad in range(n):
            if ad*m >= minK:
                break
            rem = minK - 1 - ad*m
            if rem < 0:
                break
            denom = n + ad
            cd_lim = rem // denom
            if cd_lim > m-1:
                cd_lim = m-1
            h = n - ad
            for cd in range(cd_lim+1):
                if ad*m + cd*denom >= minK:
                    break
                w = m - cd
                rr_range = (0,) if ad == 0 else (0,1)
                cc_range = (0,) if cd == 0 else (0,1)
                found = False
                for rr in rr_range:
                    fr0 = ad if rr == 1 else 0
                    gr0 = 0 if rr == 1 else ad
                    i1 = fr0; i2 = fr0 + h
                    r1 = i1*W; r2 = i2*W
                    i1g = gr0; i2g = gr0 + h
                    rg1 = i1g*W; rg2 = i2g*W
                    for cc in cc_range:
                        fc0 = cd if cc == 1 else 0
                        gc0 = 0 if cc == 1 else cd
                        j1 = fc0; j2 = fc0 + w
                        hf = (Sfl[r2 + j2] - Sfl[r1 + j2] - Sfl[r2 + j1] + Sfl[r1 + j1]) & mask
                        j1g = gc0; j2g = gc0 + w
                        hg = (Sgl[rg2 + j2g] - Sgl[rg1 + j2g] - Sgl[rg2 + j1g] + Sgl[rg1 + j1g]) & mask
                        v1 = (hf * powXl[gr0]) & mask; v1 = (v1 * powYl[gc0]) & mask
                        v2 = (hg * powXl[fr0]) & mask; v2 = (v2 * powYl[fc0]) & mask
                        if v1 == v2:
                            K = ad*m + cd*n + ad*cd
                            if K < minK:
                                minK = K
                            found = True
                            break
                    if found:
                        break
                if minK == 0:
                    break
            if minK == 0:
                break
        out_lines.append(str(minK))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()


