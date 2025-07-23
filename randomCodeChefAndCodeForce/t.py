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

def is_good(s):
    n = len(s)
    if n <= 2:
        return False
    
    for k in range(2, n):
        if n % k == 0:
            rows = n // k
            cols = k
            
            all_cols_valid = True
            for c in range(cols):
                has_zero = False
                has_one = False
                for r in range(rows):
                    idx = r * cols + c
                    if s[idx] == '0':
                        has_zero = True
                    else:
                        has_one = True
                
                if not (has_zero and has_one):
                    all_cols_valid = False
                    break
            
            if all_cols_valid:
                return True
    
    return False

def is_beautiful(s):
    n = len(s)
    if n <= 2:
        return False
    
    if is_good(s):
        return True
    
    zeros = s.count('0')
    ones = s.count('1')
    
    for target_len in range(4, n + 1):
        for k in range(2, target_len):
            if target_len % k == 0:
                if zeros >= k and ones >= k:
                    z_positions = [i for i, c in enumerate(s) if c == '0']
                    o_positions = [i for i, c in enumerate(s) if c == '1']
                    
                    if len(z_positions) >= k and len(o_positions) >= k:
                        total_needed = target_len
                        if zeros >= total_needed - k and ones >= k:
                            return True
                        if ones >= total_needed - k and zeros >= k:
                            return True
    
    return False

def solve():
    n = II()
    s = SI()
    
    max_len = 0
    
    for i in range(n):
        for j in range(i, n):
            substr = s[i:j+1]
            if not is_beautiful(substr):
                max_len = max(max_len, len(substr))
    
    return max_len

t = II()
for _ in range(t):
    print(solve()) 