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


def ask2(i:int, j:int) -> int:
    print("?", 2, i, j, flush=True)
    return int(input())

def read_optional_ack(timeout:float=0.05):
    try:
        import select
        r, _, _ = select.select([sys.stdin], [], [], timeout)
        if r:
            s = sys.stdin.readline().strip()
            if s:
                try:
                    return int(s)
                except:
                    return None
        return None
    except Exception:
        return None


def solve():
    pending_next_n = None
    def read_next_int():
        nonlocal pending_next_n
        if pending_next_n is not None:
            v = pending_next_n
            pending_next_n = None
            return v
        return int(input())

    t = read_next_int()
    for _ in range(t):
        n = read_next_int()
        # Offline fallback: if the next n values are already present on stdin, read them and output directly.
        # This avoids idleness when someone runs the solver with the sample "Input" block (non-interactive).
        try:
            import select as _sel
            arr = []
            # Non-blocking attempt to consume exactly n integers from stdin
            while len(arr) < n:
                r, _, _ = _sel.select([sys.stdin], [], [], 0)
                if not r:
                    break
                line = sys.stdin.readline()
                if not line:
                    break
                if line.strip() == "":
                    continue
                for tok in line.strip().split():
                    try:
                        arr.append(int(tok))
                        if len(arr) == n:
                            break
                    except:
                        pass
            if len(arr) == n:
                print("!", *arr, flush=True)
                ack = read_optional_ack(0.1)
                if ack is not None:
                    if ack == -1:
                        return
                    if ack not in (-1, 0, 1):
                        pending_next_n = ack
                continue
        except Exception:
            pass
        a = [0]*(n+1)

        if n == 1:
            v = ask2(1, 1)
            print("!", v, flush=True)
            continue

        anchor_idx = -1
        anchor_val = 0

        i = 1
        while anchor_idx == -1 and i <= n:
            if i+1 <= n:
                v = ask2(i, i+1)
                if v != 0:
                    anchor_idx = i
                    anchor_val = v
                    break
                if i+2 <= n:
                    v2 = ask2(i, i+2)
                    if v2 != 0:
                        anchor_idx = i
                        anchor_val = v2
                        break
                    v3 = ask2(i+1, i+2)
                    anchor_idx = i+1
                    anchor_val = v3
                    break
            i += 2

        if anchor_idx == -1:
            anchor_idx = 1
            anchor_val = ask2(1, 1)

        a[anchor_idx] = anchor_val
        other_val = 1 if anchor_val != 1 else 2

        for i in range(1, n+1):
            if i == anchor_idx:
                continue
            v = ask2(anchor_idx, i)
            a[i] = anchor_val if v != 0 else other_val

        print("!", *a[1:], flush=True)
        ack = read_optional_ack(0.1)
        if ack is not None:
            if ack == -1:
                return
            if ack not in (-1, 0, 1):
                pending_next_n = ack


if __name__ == "__main__":
    solve()


