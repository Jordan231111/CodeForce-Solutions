import sys

def leaf_peeling_labels(n, adj):
    degree=[len(adj[v]) for v in range(n)]
    from collections import deque
    q=deque([v for v in range(n) if degree[v]==1])
    label=[-1]*n
    cur=0
    while q:
        v=q.popleft()
        if label[v]!=-1:
            continue
        label[v]=cur
        cur+=1
        for nei in adj[v]:
            degree[nei]-=1
            if degree[nei]==1:
                q.append(nei)
    for v in range(n):
        if label[v]==-1:
            label[v]=cur
            cur+=1
    return label

def build_lca(n, parent):
    LOG=n.bit_length()
    up=[[0]*n for _ in range(LOG)]
    for v in range(n):
        up[0][v]=parent[v] if parent[v]!=-1 else v
    for k in range(1,LOG):
        row_prev=up[k-1]
        row_cur=up[k]
        for v in range(n):
            row_cur[v]=row_prev[row_prev[v]]
    return up

def lca(u,v,depth,up):
    if depth[u]<depth[v]:
        u,v=v,u
    diff=depth[u]-depth[v]
    bit=0
    while diff:
        if diff&1:
            u=up[bit][u]
        diff>>=1
        bit+=1
    if u==v:
        return u
    for k in range(len(up)-1,-1,-1):
        if up[k][u]!=up[k][v]:
            u=up[k][u]
            v=up[k][v]
    return up[0][u]

def solve_case(n, edges):
    adj=[[] for _ in range(n)]
    for a,b in edges:
        a-=1
        b-=1
        adj[a].append(b)
        adj[b].append(a)
    labels=leaf_peeling_labels(n, adj)
    root=0
    parent=[-1]*n
    depth=[0]*n
    stack=[root]
    order=[root]
    while stack:
        v=stack.pop()
        for nei in adj[v]:
            if nei==parent[v]:
                continue
            parent[nei]=v
            depth[nei]=depth[v]+1
            stack.append(nei)
            order.append(nei)
    up=build_lca(n,parent)
    path_bits=[0]*n
    for v in order:
        p=parent[v]
        if p==-1:
            path_bits[v]=1<<labels[v]
        else:
            path_bits[v]=path_bits[p]|(1<<labels[v])
    mask=(1<<n)-1
    total=0
    for u in range(n):
        for v in range(u,n):
            w=lca(u,v,depth,up)
            union=path_bits[u]^path_bits[v]^(1<<labels[w])
            missing=(~union)&mask
            if missing==0:
                mex=n
            else:
                mex=(missing&-missing).bit_length()-1
            total+=mex
    return str(total)

def main():
    data=list(map(int,sys.stdin.buffer.read().split()))
    it=iter(data)
    t=next(it)
    out=[]
    for _ in range(t):
        n=next(it)
        edges=[(next(it),next(it)) for _ in range(n-1)]
        out.append(solve_case(n,edges))
    sys.stdout.write('\n'.join(out)+'\n')

if __name__=='__main__':
    main()
