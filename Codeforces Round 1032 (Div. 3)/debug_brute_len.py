from itertools import combinations, product
intervals=[(6,8),(4,6),(3,5),(5,5),(3,4),(1,3),(2,4),(3,3)]
max_len=0
for sz in range(1,len(intervals)+1):
    for idxs in combinations(range(len(intervals)), sz):
        prev=-10**20
        ok=True
        for i in idxs:
            l,r=intervals[i]
            if prev<l:
                x=l
            else:
                x=prev
            if x>r:
                ok=False
                break
            prev=x
        if ok:
            max_len=sz
print(max_len) 