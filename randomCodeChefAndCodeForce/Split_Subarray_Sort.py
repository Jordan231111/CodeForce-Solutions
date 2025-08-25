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
from array import array

class Wavelet:
    __slots__ = ('lo','hi','b','l','r')
    def __init__(self, data, lo, hi):
        self.lo = lo
        self.hi = hi
        n = len(data)
        self.b = array('I', [0]*(n+1))
        if lo == hi or n == 0:
            self.l = None
            self.r = None
            return
        mid = (lo + hi) >> 1
        left = []
        right = []
        c = 0
        for i in range(n):
            x = data[i]
            if x <= mid:
                c += 1
                left.append(x)
            else:
                right.append(x)
            self.b[i+1] = c
        self.l = Wavelet(left, lo, mid)
        self.r = Wavelet(right, mid+1, hi)
    def lte(self, l, r, k):
        if l > r or k < self.lo:
            return 0
        if self.hi <= k:
            return r - l + 1
        lb = self.b[l-1]
        rb = self.b[r]
        return self.l.lte(lb+1, rb, k) + self.r.lte(l - lb, r - rb, k)
    def kth(self, l, r, k):
        if l > r:
            return 0
        if self.lo == self.hi:
            return self.lo
        lb = self.b[l-1]
        rb = self.b[r]
        cnt = rb - lb
        if k <= cnt:
            return self.l.kth(lb+1, rb, k)
        else:
            return self.r.kth(l - lb, r - rb, k - cnt)

def build_sparse_min(a):
    n = len(a) - 1
    lg = [0]*(n+2)
    for i in range(2, n+2):
        lg[i] = lg[i>>1] + 1
    K = lg[n if n>0 else 1]
    st = [array('I', [0]*(n+1)) for _ in range(K+1)]
    row0 = st[0]
    for i in range(1, n+1):
        row0[i] = a[i]
    j = 1
    while (1<<j) <= n:
        prev = st[j-1]
        cur = st[j]
        span = 1<<(j-1)
        upto = n - (1<<j) + 1
        for i in range(1, upto+1):
            v1 = prev[i]
            v2 = prev[i+span]
            cur[i] = v1 if v1 <= v2 else v2
        j += 1
    return lg, st

def range_min(lg, st, l, r):
    if l > r:
        return 1000001001
    k = lg[r - l + 1]
    row = st[k]
    a = row[l]
    b = row[r - (1<<k) + 1]
    return a if a <= b else b

def build_sparse_max(a):
    n = len(a) - 1
    lg = [0]*(n+2)
    for i in range(2, n+2):
        lg[i] = lg[i>>1] + 1
    K = lg[n if n>0 else 1]
    st = [array('I', [0]*(n+1)) for _ in range(K+1)]
    row0 = st[0]
    for i in range(1, n+1):
        row0[i] = a[i]
    j = 1
    while (1<<j) <= n:
        prev = st[j-1]
        cur = st[j]
        span = 1<<(j-1)
        upto = n - (1<<j) + 1
        for i in range(1, upto+1):
            v1 = prev[i]
            v2 = prev[i+span]
            cur[i] = v1 if v1 >= v2 else v2
        j += 1
    return lg, st

def range_max(lg, st, l, r):
    if l > r:
        return 0
    k = lg[r - l + 1]
    row = st[k]
    a = row[l]
    b = row[r - (1<<k) + 1]
    return a if a >= b else b

def solve():
    data = io.BytesIO(os.read(0, os.fstat(0).st_size)).read().split()
    it = 0
    t = int(data[it]); it += 1
    out_lines = []
    for _ in range(t):
        n = int(data[it]); it += 1
        K = int(data[it]); it += 1
        q = int(data[it]); it += 1
        A = [0]*(n+1)
        for i in range(1, n+1):
            A[i] = int(data[it]); it += 1
        lgmx, stmx = build_sparse_max(A)
        wt = Wavelet(A[1:], 1, n)
        size = 1
        while size < n+2:
            size <<= 1
        seg = [0]*(size<<1)
        def seg_set(idx, val):
            p = idx + size - 1
            if seg[p] < val:
                seg[p] = val
                p >>= 1
                while p:
                    a = seg[p<<1]
                    b = seg[p<<1|1]
                    seg[p] = a if a >= b else b
                    p >>= 1
        def seg_query(l, r):
            if l > r:
                return 0
            l += size - 1
            r += size - 1
            resl = 0
            resr = 0
            while l <= r:
                if l & 1:
                    v = seg[l]
                    if v > resl:
                        resl = v
                    l += 1
                if not (r & 1):
                    v = seg[r]
                    if v > resr:
                        resr = v
                    r -= 1
                l >>= 1
                r >>= 1
            return resl if resl >= resr else resr
        e0 = [0]*(n+2)
        cur_end = 0
        for i in range(1, n+1):
            endi = i + K - 1
            if endi > n:
                endi = n
            while cur_end < endi:
                cur_end += 1
                seg_set(A[cur_end], cur_end)
            e = i
            while True:
                lm = range_max(lgmx, stmx, i, e)
                rpos = seg_query(1, lm)
                if rpos <= e:
                    break
                e = rpos
            e0[i] = e
        LOG = (n+2).bit_length()
        up = [[0]*(n+2) for _ in range(LOG)]
        le = [[0]*(n+2) for _ in range(LOG)]
        su = [[0]*(n+2) for _ in range(LOG)]
        for i in range(1, n+1):
            up[0][i] = e0[i] + 1
            le[0][i] = e0[i]
            su[0][i] = e0[i] - i + 1
        up[0][n+1] = n+1
        le[0][n+1] = n
        su[0][n+1] = 0
        for k in range(1, LOG):
            upk_1 = up[k-1]
            lek_1 = le[k-1]
            suk_1 = su[k-1]
            upk = up[k]
            lek = le[k]
            suk = su[k]
            for i in range(1, n+2):
                v = upk_1[i]
                upk[i] = upk_1[v]
                lek[i] = lek_1[v] if v <= n else lek_1[i]
                suk[i] = suk_1[i] + (suk_1[v] if v <= n+1 else 0)
        def advance_to_R(i, R):
            s = 0
            u = i
            for k in range(LOG-1, -1, -1):
                if u <= n and le[k][u] <= R:
                    s += su[k][u]
                    u = up[k][u]
            return u, s
        def find_block_at_rank(i, R, X):
            u = i
            rem = X
            for k in range(LOG-1, -1, -1):
                if u <= n and le[k][u] <= R and su[k][u] < rem:
                    rem -= su[k][u]
                    u = up[k][u]
            return u, rem
        ans = [0]*q
        for qi in range(q):
            L = int(data[it]); it += 1
            R = int(data[it]); it += 1
            X = int(data[it]); it += 1
            m = R - L + 1
            if m <= K:
                ans[qi] = wt.kth(L, R, X)
                continue
            uAfter, Sfull = advance_to_R(L, R)
            if X <= Sfull:
                blk, pth = find_block_at_rank(L, R, X)
                ans[qi] = wt.kth(blk, e0[blk], pth)
            else:
                pth = X - Sfull
                ans[qi] = wt.kth(uAfter, R, pth)
        out_lines.append(" ".join(str(x) for x in ans))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
