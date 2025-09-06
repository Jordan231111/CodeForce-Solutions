import sys
from itertools import combinations

def longest_neat(a):
    n = len(a)
    best = 0
    for r in range(n+1):
        for idxs in combinations(range(n), r):
            b = [a[i] for i in idxs]
            if is_neat(b):
                if r > best:
                    best = r
    return best

def is_neat(b):
    i = 0
    m = len(b)
    while i < m:
        x = b[i]
        need = x
        j = i
        while j < m and b[j] == x and j - i < need:
            j += 1
        if j - i != need:
            return False
        i = j
    return True

if __name__ == "__main__":
    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))
    print(longest_neat(a))


