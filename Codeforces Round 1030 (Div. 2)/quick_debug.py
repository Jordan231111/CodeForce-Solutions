from collections import defaultdict

def build(arr,m):
    n=len(arr)
    pos=[[] for _ in range(m+1)]
    for idx,val in enumerate(arr):
        pos[val].append(idx)
    node_hash=[0]*n
    child_map=defaultdict(list)
    next_id=2
    cache={}
    for idx in pos[1]:
        node_hash[idx]=1
    for val in range(2,m+1):
        parents=pos[val]
        children=pos[val-1]
        ext=children+[p+n for p in children]
        ptr=0
        for i,st in enumerate(parents):
            ed=parents[(i+1)%len(parents)]
            if i==len(parents)-1:
                ed+=n
            ch=[]
            while ptr<len(ext) and ext[ptr]<ed:
                if ext[ptr]>st:
                    h=node_hash[ext[ptr]%n]
                    ch.append(h)
                ptr+=1
            child_map[st]=ch
            key=tuple(ch)
            if key not in cache:
                cache[key]=next_id
                next_id+=1
            node_hash[st]=cache[key]
    return node_hash,child_map

a=[1,1,2,1,2,3]
h_a,cm_a=build(a,3)
print('node hashes',h_a)
print('child map',cm_a)

b=[2,1,1,2,3,1]
h_b,cm_b=build(b,3)
print('node hashes',h_b)
print('child map',cm_b)

# additional debug 