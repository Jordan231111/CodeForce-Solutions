import os
import sys
from bisect import bisect_left, bisect_right
from collections import defaultdict, deque
from heapq import heappop, heappush

# Using template.py for boilerplate
input = sys.stdin.readline
II = lambda: int(input())
MI = lambda: map(int, input().split())
LI = lambda: [int(a) for a in input().split()]
SI = lambda: input().rstrip()
LLI = lambda n: [[int(a) for a in input().split()] for _ in range(n)]

def solve():
    N, C = MI()
    A = LI()
    
    friend_cookies_set = set(A)
    min_friend_cookies = min(A)
    
    # Alice's final cookie count, X, must satisfy three conditions:
    # 1. X >= C (she can only buy more)
    # 2. X > min_friend_cookies (strictly more than at least one friend)
    # 3. X is not in friend_cookies_set (no friend has an equal amount)
    
    # We can combine the first two conditions to find a starting search value.
    # X must be at least C, and also at least min_friend_cookies + 1.
    x = max(C, min_friend_cookies + 1)
    
    # Now, we find the first value from this starting point that also
    # satisfies the third condition (uniqueness).
    while x in friend_cookies_set:
        x += 1
            
    # The result is the number of extra cookies she has to buy.
    print(x - C)

def main():
    try:
        T = II()
        for _ in range(T):
            solve()
    except (IOError, ValueError):
        # Gracefully handle cases where input is not available
        # (e.g., when running tests without piping input)
        pass

if __name__ == "__main__":
    main() 