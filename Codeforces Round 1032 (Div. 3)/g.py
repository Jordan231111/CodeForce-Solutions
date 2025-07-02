import sys

def solve():
    it = iter(sys.stdin.buffer.read().split())
    t = int(next(it))
    out_lines = []
    for _ in range(t):
        n = int(next(it))
        s = next(it).decode()
        pref = 0
        arr = [0]
        for ch in s:
            pref += 1 if ch == '0' else -1
            arr.append(pref)
        arr.sort()
        m = n + 1
        prefix_sum = 0
        sum_abs = 0
        for i, val in enumerate(arr):
            sum_abs += val * i - prefix_sum
            prefix_sum += val
        sum_len = n * (n + 1) * (n + 2) // 6
        ans = (sum_len + sum_abs) // 2
        out_lines.append(str(ans))
    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    solve()
