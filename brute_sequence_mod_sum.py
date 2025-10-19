import sys


def solve_case(n, k, max_cap=50):
    seq = [0] * n

    def search(cap):
        def dfs(idx, prev, cur_sum):
            if idx == n:
                if cur_sum == k:
                    return seq.copy()
                return None
            for v in range(prev, cap + 1):
                rem = v % prev
                if cur_sum + rem > k:
                    continue
                seq[idx] = v
                res = dfs(idx + 1, v, cur_sum + rem)
                if res is not None:
                    return res
            return None

        for first in range(1, cap + 1):
            seq[0] = first
            res = dfs(1, first, 0)
            if res is not None:
                return res
        return None

    for cap in range(1, max_cap + 1):
        res = search(cap)
        if res is not None:
            return res
    raise RuntimeError("No solution within search limit")


def main():
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return
    t = data[0]
    idx = 1
    out_lines = []
    for _ in range(t):
        n = data[idx]
        k = data[idx + 1]
        idx += 2
        ans = solve_case(n, k)
        out_lines.append(" ".join(map(str, ans)))
    sys.stdout.write("\n".join(out_lines))


if __name__ == "__main__":
    main()

