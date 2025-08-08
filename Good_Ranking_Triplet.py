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
from itertools import permutations

def get_partitions(curr:list[int]):
    curr.sort()
    nn=len(curr)
    if nn<2:
        if nn==0:
            return []
        res=[]
        for k in (1,2,0):
            g=[[],[],[]]
            g[k]=curr[:]
            res.append(g)
        return res
    if nn==2:
        a,b=curr
        return [[[a],[b],[]],[[b],[a],[]],[[a],[],[b]],[[b],[],[a]],[[],[a],[b]],[[],[b],[a]]]
    if nn==3:
        res=[]
        a,b,c=curr
        for p in permutations(range(3)):
            g=[[],[],[]]
            g[p[0]]=[a]
            g[p[1]]=[b]
            g[p[2]]=[c]
            res.append(g)
        return res
    s=nn//3
    r=nn%3
    len0=s+(1 if r>=1 else 0)
    len1=s+(1 if r>=2 else 0)
    sub0=curr[:len0]
    sub1=curr[len0:len0+len1]
    sub2=curr[len0+len1:]
    sp0=get_partitions(sub0)
    sp1=get_partitions(sub1)
    sp2=get_partitions(sub2)
    m_sub=max(len(sp0),len(sp1),len(sp2))
    ext=[]
    for j in range(m_sub):
        p0=sp0[j%len(sp0)]
        p1=sp1[j%len(sp1)]
        p2=sp2[j%len(sp2)]
        ext.append([p0[0]+p1[0]+p2[0],p0[1]+p1[1]+p2[1],p0[2]+p1[2]+p2[2]])
    subs=[sub0,sub1,sub2]
    top=[]
    for p in permutations(range(3)):
        g=[[],[],[]]
        for i in range(3):
            g[p[i]]=subs[i][:]
        top.append(g)
    return ext+top

def main():
    n=II()
    parts=get_partitions(list(range(1,n+1)))
    m=len(parts)
    out=[str(m)]
    for g in parts:
        perm=g[0]+g[1]+g[2]
        out.append(' '.join(map(str,perm)))
    sys.stdout.write('\n'.join(out))

if __name__=='__main__':
    main()
