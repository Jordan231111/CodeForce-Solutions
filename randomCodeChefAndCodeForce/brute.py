import sys
from collections import deque
input = sys.stdin.readline
II = lambda: int(input())
MI = lambda: map(int, input().split())
LI = lambda: list(map(int, input().split()))
INF = 10**18

T = II()
for _ in range(T):
    N = II()
    S = [0] + LI()
    edge = [[] for _ in range(N+1)]
    for i in range(1, N+1):
        for j in range(1, N+1):
            if i != j and S[i] * 2 >= S[j]:
                edge[i].append(j)
    dist = [INF] * (N+1)
    dist[1] = 0
    queue = deque([1])
    while queue:
        u = queue.popleft()
        for v in edge[u]:
            if dist[v] > dist[u] + 1:
                dist[v] = dist[u] + 1
                queue.append(v)
    if dist[N] == INF:
        print(-1)
    else:
        print(dist[N] + 1) 