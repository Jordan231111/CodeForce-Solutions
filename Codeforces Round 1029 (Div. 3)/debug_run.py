import textwrap, e_lost_soul
exp=[3,3,0,4,3,5,6,4,5,2]
raw='''10
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
3 2 1 5 4'''
data=list(map(int, raw.strip().split()))
it=iter(data)
next(it)
for idx, expv in enumerate(exp):
    n=next(it)
    a=[next(it) for _ in range(n)]
    b=[next(it) for _ in range(n)]
    res=e_lost_soul.solve_case(n,a,b)
    print(idx, res, expv) 