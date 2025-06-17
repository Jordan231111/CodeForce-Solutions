import sys

def main() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    idx = 1
    out_lines = []
    for _ in range(t):
        n = data[idx]; k = data[idx + 1]
        idx += 2
        # Construction: a contiguous block of 1s followed by 0s has
        # zero occurrences of both 101 and 010 as subsequences.
        bitstring = '1' * k + '0' * (n - k)
        out_lines.append(bitstring)
    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    main()
