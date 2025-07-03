import sys
input=sys.stdin.buffer.readline
n,m=map(int,input().split())
edges=[]
adj=[set() for _ in range(n)]
for _ in range(m):
    u,v=map(int,input().split())
    u-=1
    v-=1
    edges.append((u,v))
    adj[u].add(v)
    adj[v].add(u)
q=int(input())
xs=[]
while len(xs)<q:
    xs.extend(map(int,input().split()))
xs=[x-1 for x in xs]
parent=list(range(n))
size=[1]*n

def find(x:int)->int:
    while parent[x]!=x:
        parent[x]=parent[parent[x]]
        x=parent[x]
    return x
edge_cnt=m
out=[]
for idx in xs:
    u,v=edges[idx]
    ru=find(u)
    rv=find(v)
    if ru==rv:
        out.append(str(edge_cnt))
        continue
    adj[ru].remove(rv)
    adj[rv].remove(ru)
    edge_cnt-=1
    if len(adj[ru])<len(adj[rv]):
        ru,rv=rv,ru
    parent[rv]=ru
    size[ru]+=size[rv]
    for nb in list(adj[rv]):
        adj[nb].remove(rv)
        if nb==ru:
            continue
        if nb in adj[ru]:
            edge_cnt-=1
        else:
            adj[ru].add(nb)
            adj[nb].add(ru)
    adj[rv].clear()
    out.append(str(edge_cnt))
print("\n".join(out)) 