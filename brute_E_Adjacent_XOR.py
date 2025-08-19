import sys
from collections import deque

def possible(a, b):
    n = len(a)
    start = tuple(a)
    target = tuple(b)
    if start == target:
        return True
    q = deque()
    q.append((start, 0))
    seen = { (start,0) }
    while q:
        arr, mask = q.popleft()
        if arr == target:
            return True
        if mask == (1<<(n-1)) - 1:
            continue
        for i in range(n-1):
            if not (mask >> i) & 1:
                arr2 = list(arr)
                arr2[i] ^= arr2[i+1]
                state = (tuple(arr2), mask | (1<<i))
                if state not in seen:
                    seen.add(state)
                    q.append(state)
    return False

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    p = 1
    out = []
    for _ in range(t):
        n = data[p]; p += 1
        a = data[p:p+n]; p += n
        b = data[p:p+n]; p += n
        out.append("YES" if possible(a, b) else "NO")
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()


