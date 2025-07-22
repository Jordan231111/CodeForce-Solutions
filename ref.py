
import sys
from collections import defaultdict
from random import getrandbits

def solve():
    input=sys.stdin.readline
    r=getrandbits(32)
    n,q=map(int,input().split())
    color=list(map(int,input().split()))
    graph=[[] for _ in range(n)]
    for _ in range(n-1):
        a,b,c=map(int,input().split());a-=1;b-=1
        graph[a].append((b,c));graph[b].append((a,c))
    parent=[-1]*n
    soncolor=[defaultdict(int) for _ in range(n)]
    cost=[0]*n
    stack=[0]
    parent[0]=-1
    while stack:
        node=stack.pop()
        for neighbor,c in graph[node]:
            if neighbor!=parent[node]:
                parent[neighbor]=node
                cost[neighbor]=c
                stack.append(neighbor)
    ans=0
    for i in range(1,n):
        if color[i]!=color[parent[i]]:
            ans+=cost[i]
        soncolor[parent[i]][color[i]^r]+=cost[i]
    for _ in range(q):
        node,newc=map(int,input().split());node-=1
        curc=color[node]
        ans+=soncolor[node].get(curc^r,0)
        color[node]=newc
        ans-=soncolor[node].get(newc^r,0)
        if parent[node]!=-1:
            p=parent[node]
            soncolor[p][newc^r]+=cost[node]
            soncolor[p][curc^r]-=cost[node]
            if soncolor[p][curc^r]==0:
                del soncolor[p][curc^r]
            if color[p]==curc:
                ans+=cost[node]
            if color[p]==newc:
                ans-=cost[node]
        print(ans)

for _ in range(int(sys.stdin.readline())):
    solve()
