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

class SegTree:
    __slots__ = ("n","k","size","data")
    def __init__(self,a,b,k):
        self.n=len(a)
        self.k=k
        self.size=1
        while self.size<self.n:
            self.size<<=1
        self.data=[(0,0,0,0)]*(self.size*2)
        for i in range(self.n):
            self.data[self.size+i]=self._leaf(a[i],b[i])
        for i in range(self.size-1,0,-1):
            self.data[i]=self._merge(self.data[i<<1],self.data[i<<1|1])
    def _leaf(self,ai,bi):
        if ai+self.k<bi:
            s0=bi;f0=1
        else:
            s0=ai;f0=0
        if bi+self.k<ai:
            s1=ai;f1=0
        else:
            s1=bi;f1=1
        return (s0,f0,s1,f1)
    @staticmethod
    def _merge(l,r):
        s0l,f0l,s1l,f1l=l
        s0r,f0r,s1r,f1r=r
        if f0l==0:
            sc0=s0l+s0r;fo0=f0r
        else:
            sc0=s0l+s1r;fo0=f1r
        if f1l==0:
            sc1=s1l+s0r;fo1=f0r
        else:
            sc1=s1l+s1r;fo1=f1r
        return (sc0,fo0,sc1,fo1)
    def update(self,idx,ai,bi):
        p=self.size+idx
        self.data[p]=self._leaf(ai,bi)
        p>>=1
        while p:
            self.data[p]=self._merge(self.data[p<<1],self.data[p<<1|1])
            p>>=1
    def query(self):
        return self.data[1][0]

def solve():
    t=II()
    res=[]
    for _ in range(t):
        n,k=MI()
        A=LI()
        B=LI()
        st=SegTree(A,B,k)
        q=II()
        for _ in range(q):
            typ,p,x=MI()
            p-=1
            if typ==1:
                A[p]=x
            else:
                B[p]=x
            st.update(p,A[p],B[p])
            res.append(str(st.query()))
    sys.stdout.write("\n".join(res))

if __name__=="__main__":
    solve() 