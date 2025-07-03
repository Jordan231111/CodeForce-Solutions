import sys, random

def build_diffs(k: int):
    diffs = [0] if k % 2 else []
    d = 1
    while len(diffs) < k:
        diffs.extend((d, -d))
        d += 1
    return diffs


def generate(n: int, k: int):
    # Fast paths for trivial cases
    if k == 1:
        return list(range(1, n + 1))
    if k == 2:
        # Cyclic left-shift by 1 always gives exactly two distinct differences
        return list(range(2, n + 1)) + [1]

    diffs = build_diffs(k)

    # Attempt stochastic construction – guaranteed to succeed quickly for n ≤ 100
    attempts = 5000
    while attempts:
        attempts -= 1
        perm = [0] * (n + 1)  # 1-based storage; 0 means unassigned
        used = [False] * (n + 1)

        # Randomise processing order for indices and diff choices to avoid dead-ends
        idx_order = list(range(1, n + 1))
        random.shuffle(idx_order)

        ok = True
        for i in idx_order:
            random.shuffle(diffs)
            placed = False
            for d in diffs:
                j = i + d
                if 1 <= j <= n and not used[j]:
                    perm[i] = j
                    used[j] = True
                    placed = True
                    break
            if not placed:
                ok = False
                break

        if not ok:
            continue  # restart

        # Validate distinct difference count
        if len({perm[i] - i for i in range(1, n + 1)}) == k:
            return perm[1:]

    # The constraints (n ≤ 100) guarantee we should never get here.
    raise RuntimeError("Construction failed; increase attempt limit")


def main():
    raw = sys.stdin.buffer.read() if hasattr(sys.stdin, "buffer") else sys.stdin.read().encode()
    data = list(map(int, raw.split()))
    t = data[0]
    idx = 1
    out_lines = []
    for _ in range(t):
        n = data[idx]
        k = data[idx + 1]
        idx += 2
        result = generate(n, k)
        out_lines.append(" ".join(map(str, result)))
    sys.stdout.write("\n".join(out_lines))


def solve():
    main()


if __name__ == "__main__":
    main()
