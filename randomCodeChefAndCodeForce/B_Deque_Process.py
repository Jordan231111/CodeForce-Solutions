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


def update_state(last:int|None, run_dir:int, run_len:int, val:int):
    if last is None:
        return (val, 0, 1)
    new_dir = 1 if val > last else -1
    if run_dir == 0:
        new_run_len = 2
    elif new_dir == run_dir:
        new_run_len = run_len + 1
    else:
        new_run_len = 2
    if new_run_len >= 5:
        return None
    return (val, new_dir, new_run_len)


def can_move(arr, l:int, r:int, last:int|None, run_dir:int, run_len:int):
    if l>r:
        return True
    if update_state(last, run_dir, run_len, arr[l]) is not None:
        return True
    if update_state(last, run_dir, run_len, arr[r]) is not None:
        return True
    return False


def solve_single(arr:list[int]):
    l = 0
    r = len(arr)-1
    last = None
    run_dir = 0
    run_len = 0
    res_chars = []
    while l <= r:
        choices = []
        
        st_left = update_state(last, run_dir, run_len, arr[l])
        if st_left is not None:
            l2 = l+1
            r2 = r
            if can_move(arr, l2, r2, *st_left):
                choices.append(('L', st_left, l2, r2))
        
        st_right = update_state(last, run_dir, run_len, arr[r])
        if st_right is not None:
            l2 = l
            r2 = r-1
            if can_move(arr, l2, r2, *st_right):
                choices.append(('R', st_right, l2, r2))
        
        if not choices:
            
            choices.append(('L', update_state(last, run_dir, run_len, arr[l]), l+1, r))
        
        best = choices[0]
        for c in choices[1:]:
            _, st, _, _ = c
            _, new_dir, new_len = st
            _, best_dir, best_len = best[1]
            
            if new_len < best_len:
                best = c
            elif new_len == best_len and (run_dir!=0 and new_dir != run_dir):
                
                best = c
        side, new_state, l, r = best
        res_chars.append(side)
        last, run_dir, run_len = new_state
    return ''.join(res_chars)


def main():
    t = II()
    out_lines = []
    for _ in range(t):
        n = II()
        arr = LI()
        out_lines.append(solve_single(arr))
    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    main() 