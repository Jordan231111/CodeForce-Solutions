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

n = II()

def get_partitions(curr):

    curr = sorted(curr)

    nn = len(curr)

    if nn < 2:

        if nn == 0:

            return []

        else:

            res = []

            for k in [1,2,0]:

                g = [[], [], []]

                g[k] = curr

                res.append(g)

            return res

    if nn == 2:

        res = []

        res.append([[curr[0]], [curr[1]], []])

        res.append([[curr[1]], [curr[0]], []])

        res.append([[curr[0]], [], [curr[1]]])

        res.append([[curr[1]], [], [curr[0]]])

        res.append([ [], [curr[0]], [curr[1]] ])

        res.append([ [], [curr[1]], [curr[0]] ])

        return res

    if nn == 3:

        res = []

        for p in permutations(range(3)):

            g = [[], [], []]

            g[p[0]] = [curr[0]]

            g[p[1]] = [curr[1]]

            g[p[2]] = [curr[2]]

            res.append(g)

        return res

    s = nn // 3

    r = nn % 3

    len0 = s + (1 if r >= 1 else 0)

    len1 = s + (1 if r >= 2 else 0)

    len2 = s

    sub0 = curr[0:len0]

    sub1 = curr[len0:len0+len1]

    sub2 = curr[len0+len1:]

    sub_part0 = get_partitions(sub0)

    sub_part1 = get_partitions(sub1)

    sub_part2 = get_partitions(sub2)

    m_sub = max(len(sub_part0), len(sub_part1), len(sub_part2))

    extended = []

    for j in range(m_sub):

        part0 = [lst[:] for lst in sub_part0[j % len(sub_part0)]]

        part1 = [lst[:] for lst in sub_part1[j % len(sub_part1)]]

        part2 = [lst[:] for lst in sub_part2[j % len(sub_part2)]]

        g = [[], [], []]

        for k in range(3):

            g[k] = part0[k] + part1[k] + part2[k]

        extended.append(g)

    subs = [sub0, sub1, sub2]

    top = []

    for p in permutations(range(3)):

        g = [[], [], []]

        for i in range(3):

            g[p[i]] = subs[i][:]

        top.append(g)

    return extended + top

contestants = list(range(1, n + 1))

parts = get_partitions(contestants)

m = len(parts)

print(m)

for g in parts:

    perm = sorted(g[0]) + sorted(g[1]) + sorted(g[2])

    print(' '.join(map(str, perm)))