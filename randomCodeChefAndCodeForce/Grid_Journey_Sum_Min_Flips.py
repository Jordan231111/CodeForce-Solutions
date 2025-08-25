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

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        a = next(it).decode()
        b = next(it).decode()

        oa = [0]*(n+1)
        for i in range(1, n+1):
            oa[i] = oa[i-1] + (1 if a[i-1] == '1' else 0)

        ob = [0]*(n+1)
        for j in range(1, n+1):
            ob[j] = ob[j-1] + (1 if b[j-1] == '1' else 0)

        pairs = []
        sum_ob_tot = 0
        sum_y_tot = n*(n+1)//2
        for y in range(1, n+1):
            oy = ob[y]
            d = (oy << 1) - y
            pairs.append((d, oy, y))
            sum_ob_tot += oy

        pairs.sort(key=lambda x: x[0])
        keys = [p[0] for p in pairs]
        pre_ob = [0]*n
        pre_y = [0]*n
        s1 = 0
        s2 = 0
        for i, (_, oy, yy) in enumerate(pairs):
            s1 += oy
            s2 += yy
            pre_ob[i] = s1
            pre_y[i] = s2

        ans = 0
        for x in range(1, n+1):
            s = oa[x]
            K = x - (s << 1)
            idx = bisect_right(keys, K)
            if idx:
                cnt0 = idx
                sum_ob0 = pre_ob[idx-1]
                sum_y0 = pre_y[idx-1]
            else:
                cnt0 = 0
                sum_ob0 = 0
                sum_y0 = 0
            cnt1 = n - cnt0
            sum_ob1 = sum_ob_tot - sum_ob0
            sum_y1 = sum_y_tot - sum_y0
            ans += cnt0 * s + sum_ob0 + cnt1 * (x - s) + (sum_y1 - sum_ob1)

        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()


