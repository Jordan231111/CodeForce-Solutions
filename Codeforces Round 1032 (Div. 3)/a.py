import sys

def main():
    data = sys.stdin.read().split()
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        s = int(next(it))
        # Read the sorted positions
        xs = [int(next(it)) for _ in range(n)]
        mn, mx = xs[0], xs[-1]
        # You must visit both ends of the segment [mn, mx]
        # Optimal path: go to the closer end first, then traverse the whole segment
        segment_length = mx - mn
        dist_to_mn = abs(s - mn)
        dist_to_mx = abs(s - mx)
        ans = segment_length + min(dist_to_mn, dist_to_mx)
        out.append(str(ans))
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == '__main__':
    main()
