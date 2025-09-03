import sys
input = sys.stdin.readline
II = lambda : int(input())

def solve():
    x = II()
    n = II()
    total = 0
    for _ in range(n):
        p = II()
        total += p
    print(x*(n+1) - total)

if __name__ == "__main__":
    solve()


