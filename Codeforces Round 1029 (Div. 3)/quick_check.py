def solve_pref(a,b):
    n=len(a)
    ans_no=0
    for i in range(n):
        if a[i]==b[i]:
            ans_no=max(ans_no,i+1)  # results 1-indexed length
    for i in range(n-1):
        if a[i]==a[i+1] or b[i]==b[i+1]:
            ans_no=max(ans_no, i+1)
    seenA=set(); seenB=set(); ans_rem=0
    for j in range(n-2,-1,-1):
        if a[j] in seenA or a[j] in seenB or b[j] in seenA or b[j] in seenB:
            ans_rem=max(ans_rem, j+1)
        seenA.add(a[j+1]); seenB.add(b[j+1])
    return max(ans_no, ans_rem)

t_raw="""10
4
1 3 1 4
4 3 2 2
6
2 1 5 3 6 4
3 2 4 5 1 6
2
1 2
2 1
6
2 5 1 3 6 4
3 5 2 3 4 6
4
1 3 2 2
2 1 3 4
8
3 1 4 6 2 2 5 7
4 2 3 7 1 1 6 5
10
5 1 2 7 3 9 4 10 6 8
6 2 3 6 4 10 5 1 7 9
5
3 2 4 1 5
2 4 5 1 3
7
2 2 6 4 1 3 5
3 1 6 5 1 4 2
5
4 1 3 2 5
3 2 1 5 4"""
exp=[3,3,0,4,3,5,6,4,5,2]

data=list(map(int,t_raw.strip().split()))
itr=iter(data)
next(itr)
results=[]
for e in exp:
    n=next(itr)
    a=[next(itr) for _ in range(n)]
    b=[next(itr) for _ in range(n)]
    results.append(solve_pref(a,b))
print(results)
print('ok', results==exp) 