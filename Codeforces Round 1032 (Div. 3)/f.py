from sys import stdin, stdout

def count_subarrays_with_sum(arr, target):
    pref = 0
    cnt = {0: 1}
    ans = 0
    for v in arr:
        pref += v
        ans += cnt.get(pref - target, 0)
        cnt[pref] = cnt.get(pref, 0) + 1
    return ans


def solve():
    it = map(int, stdin.buffer.read().split())
    t = next(it)
    out_lines = []
    for _ in range(t):
        n = next(it); s = next(it); x = next(it)
        a = [next(it) for _ in range(n)]
        res = 0
        i = 0
        while i < n:
            if a[i] > x:
                i += 1
                continue
            j = i
            while j < n and a[j] <= x:
                j += 1
            segment = a[i:j]
            total = count_subarrays_with_sum(segment, s)
            minus = 0
            start = 0
            for idx, val in enumerate(segment):
                if val == x:
                    if start < idx:
                        minus += count_subarrays_with_sum(segment[start:idx], s)
                    start = idx + 1
            if start < len(segment):
                minus += count_subarrays_with_sum(segment[start:], s)
            res += total - minus
            i = j
        out_lines.append(str(res))
    stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    solve()
