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
from collections import defaultdict,deque
from heapq import heappop,heappush
from bisect import bisect_left,bisect_right
DD = defaultdict
BSL = bisect_left
BSR = bisect_right

P = 1000000007

def solve():
    P = 1000000007
    t = II()
    res = []
    for _ in range(t):
        n = II()
        mat = [SI() for _ in range(n)]
        half = n >> 1
        # total combinations
        total = 1
        row_counts = [row.count('1') for row in mat]
        for c in row_counts:
            total = (total * c) % P
        if half == 1:
            # arrays are not good only when both elements are identical
            cnt_ident = 0
            r0, r1 = mat[0], mat[1]
            for j in range(n):
                if r0[j] == '1' and r1[j] == '1':
                    cnt_ident += 1
            bad = cnt_ident % P
            res.append(str((total - bad) % P))
            continue
        # precompute per row delta frequency
        max_val = n
        max_diff = half * max_val  # maximum possible positive diff
        size = max_diff + 1
        dp = [0]*(size)
        # first row (index 0)
        a_idx = 0
        b_idx = half
        freq0 = [0]*(2*max_val+1)  # shift by +max_val to handle negative
        shift = max_val
        row_a = mat[a_idx]
        row_b = mat[b_idx]
        for i in range(n):
            if row_a[i]=='1':
                for j in range(n):
                    if row_b[j]=='1':
                        delta = (i+1) - (j+1)
                        if delta>=0:
                            freq0[delta+shift] += 1
        for d_idx in range(shift, 2*max_val+1):
            cnt = freq0[d_idx]
            if cnt:
                dp[d_idx-shift] = cnt % P
        # process middle rows
        for idx in range(1, half-1):
            row_a = mat[idx]
            row_b = mat[idx+half]
            # compute delta frequency for this row
            freq_dict = {}
            for i in range(n):
                if row_a[i]=='1':
                    val_a = i+1
                    for j in range(n):
                        if row_b[j]=='1':
                            delta = val_a - (j+1)
                            freq_dict[delta] = freq_dict.get(delta,0)+1
            if not freq_dict:
                # no valid pairs, so no bad arrays
                dp = [0]*size
                break
            active_diffs = [idx for idx,v in enumerate(dp) if v]
            new_dp = [0]*size
            for d in active_diffs:
                base = dp[d]
                for delta, cnt in freq_dict.items():
                    nd = d + delta
                    if nd<0 or nd>max_diff: continue
                    new_dp[nd] = (new_dp[nd] + base*cnt)%P
            dp = new_dp
        # last row handling idx = half-1
        if half==1:
            bad = 0
            # dp currently is still initial state?? For half ==1 we didn't process loops.
        row_a = mat[half-1]
        row_b = mat[n-1]
        freq_last = [0]*(2*max_val+1)
        for i in range(n):
            if row_a[i]=='1':
                val_a=i+1
                for j in range(n):
                    if row_b[j]=='1':
                        delta = val_a - (j+1)
                        freq_last[delta+shift]+=1
        bad = 0
        for d in range(size):
            if dp[d]==0: continue
            base=dp[d]
            # need delta such that d+delta ==0
            delta_needed = -d
            idx_shifted = delta_needed + shift
            if 0<=idx_shifted<2*max_val+1:
                cnt = freq_last[idx_shifted]
                if cnt:
                    bad = (bad + base*cnt)%P
        res.append(str((total - bad)%P))
    print('\n'.join(res))

if __name__ == "__main__":
    solve() 