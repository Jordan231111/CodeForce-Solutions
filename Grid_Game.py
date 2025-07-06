import sys
from collections import deque

def solve():
    try:
        h_str, w_str, k_str = sys.stdin.readline().split()
        h, w, k = int(h_str), int(w_str), int(k_str)
    except (IOError, ValueError):
        # Handle empty input at the end of all test cases
        return

    # Using a set of tuples for obstacle coordinates is much faster
    # than creating large integers, as tuple hashing is highly optimized.
    obstacles = {tuple(map(int, sys.stdin.readline().split())) for _ in range(k)}

    # Trivial case: a 1D grid is blocked by any obstacle.
    if h == 1 or w == 1:
        print("No" if k > 0 else "Yes")
        return

    # The queue for the BFS will store obstacle coordinates as tuples.
    q = deque()
    # The 'seen' set also stores tuples to keep track of visited obstacles.
    seen = set()

    # The BFS starts from "source" obstacles: those adjacent to the top (r=1)
    # or right (c=w) boundaries of the grid.
    for r, c in obstacles:
        if r == 1 or c == w:
            if (r, c) not in seen:
                seen.add((r, c))
                q.append((r, c))

    # The 8 directions for checking adjacent obstacles (including diagonals).
    di = [-1, -1, -1, 0, 0, 1, 1, 1]
    dj = [1, 0, -1, 1, -1, 1, 0, -1]

    while q:
        r, c = q.popleft()

        for i in range(8):
            rr, cc = r + di[i], c + dj[i]
            neighbor = (rr, cc)
            
            # If an adjacent cell is an obstacle and hasn't been visited yet...
            if neighbor in obstacles and neighbor not in seen:
                seen.add(neighbor)
                q.append(neighbor)
                
                # A blocking path is found if the chain of obstacles reaches
                # a "sink" boundary: the bottom row (rr=h) or left column (cc=1).
                if rr == h or cc == 1:
                    print("No")
                    return
    
    # If the BFS completes without reaching a sink boundary, no blocking path exists.
    print("Yes")

if __name__ == "__main__":
    solve() 