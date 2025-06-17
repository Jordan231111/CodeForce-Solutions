import sys

def max_portions(k, a, b, x, y):
    # Try both greedy orders: type-1 first, then type-2; and type-2 first, then type-1
    res = 0
    # Special handling for small k: try both first moves if both are possible
    candidates = []
    if k >= a:
        temp = k - x
        cnt1 = 1
        cnt2 = 0
        if temp >= b:
            cnt2 = (temp - b) // y + 1
        candidates.append(cnt1 + cnt2)
    if k >= b:
        temp = k - y
        cnt2 = 1
        cnt1 = 0
        if temp >= a:
            cnt1 = (temp - a) // x + 1
        candidates.append(cnt1 + cnt2)
    # Also try the original greedy bulk approach
    # Order 1: type-1 first
    temp = k
    cnt1 = 0
    if temp >= a:
        cnt1 = (temp - a) // x + 1
        temp -= cnt1 * x
    cnt2 = 0
    if temp >= b:
        cnt2 = (temp - b) // y + 1
    candidates.append(cnt1 + cnt2)
    # Order 2: type-2 first
    temp = k
    cnt2 = 0
    if temp >= b:
        cnt2 = (temp - b) // y + 1
        temp -= cnt2 * y
    cnt1 = 0
    if temp >= a:
        cnt1 = (temp - a) // x + 1
    candidates.append(cnt1 + cnt2)
    return max(candidates) if candidates else 0

def main():
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        k, a, b, x, y = map(int, input().split())
        print(max_portions(k, a, b, x, y))

if __name__ == "__main__":
    main()
