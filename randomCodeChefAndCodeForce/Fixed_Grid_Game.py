import sys
from collections import deque


def solve():
    try:
        h_str, w_str, k_str = sys.stdin.readline().split()
        h, w, k = int(h_str), int(w_str), int(k_str)
    except (IOError, ValueError):
        return

    obstacles = {tuple(map(int, sys.stdin.readline().split())) for _ in range(k)}

    if h == 1 or w == 1:
        print("No" if k > 0 else "Yes")
        return

    q = deque()
    seen = set()

    for r, c in obstacles:
        if r == 1 or c == w:
            seen.add((r, c))
            q.append((r, c))

    di = [-1, -1, -1, 0, 0, 1, 1, 1]
    dj = [1, 0, -1, 1, -1, 1, 0, -1]

    while q:
        r, c = q.popleft()
        for i in range(8):
            rr, cc = r + di[i], c + dj[i]
            if (rr, cc) in obstacles and (rr, cc) not in seen:
                if rr == h or cc == 1:
                    print("No")
                    return
                seen.add((rr, cc))
                q.append((rr, cc))

    print("Yes")


if __name__ == "__main__":
    solve() 