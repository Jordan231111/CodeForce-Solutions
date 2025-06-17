import sys

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        # Read dimensions and tile size
        w = int(next(it))
        h = int(next(it))
        a = int(next(it))
        b = int(next(it))
        # Read pre-placed tile coordinates
        x1 = int(next(it))
        y1 = int(next(it))
        x2 = int(next(it))
        y2 = int(next(it))
        # Compute remainders and stripe indices
        rx1, rx2 = x1 % a, x2 % a
        ry1, ry2 = y1 % b, y2 % b
        kx1, kx2 = x1 // a, x2 // a
        ky1, ky2 = y1 // b, y2 // b
        # Vertical stripe tiling: stripes of width a independent in y
        can_vert = (rx1 == rx2) and (kx1 != kx2 or ry1 == ry2)
        # Horizontal stripe tiling: stripes of height b independent in x
        can_horiz = (ry1 == ry2) and (ky1 != ky2 or rx1 == rx2)
        if can_vert or can_horiz:
            out.append("Yes")
        else:
            out.append("No")
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
