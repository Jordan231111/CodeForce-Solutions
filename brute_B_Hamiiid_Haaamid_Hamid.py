import sys
sys.setrecursionlimit(10**6)

def solve():
    it = iter(sys.stdin.read().strip().split())
    t = int(next(it))
    out_lines = []
    for _ in range(t):
        n = int(next(it)); x = int(next(it))
        s = list(next(it).strip())

        walls_init = 0
        for i,ch in enumerate(s, start=1):
            if ch == '#':
                walls_init |= 1 << (i-1)

        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dp(pos, mask):
            if pos == 1 or pos == n:
                return 1

            empties_mask = ((1<<n) - 1) ^ mask
            # Mani cannot build at Hamid's position
            empties_mask &= ~ (1 << (pos-1))

            # If there is no empty cell at all (shouldn't happen with constraints), Hamid chooses a direction
            if empties_mask == 0:
                # Hamid moves optimally given there are only walls
                # Left
                resL = float('inf')
                left_mask = mask
                j = pos-1
                while j >= 1 and ((left_mask >> (j-1)) & 1) == 0:
                    j -= 1
                if j < 1:
                    resL = 1
                else:
                    left_mask &= ~(1 << (j-1))
                    resL = 1 + dp(j, left_mask)
                # Right
                resR = float('inf')
                right_mask = mask
                k = pos+1
                while k <= n and ((right_mask >> (k-1)) & 1) == 0:
                    k += 1
                if k > n:
                    resR = 1
                else:
                    right_mask &= ~(1 << (k-1))
                    resR = 1 + dp(k, right_mask)
                return min(resL, resR)

            best_for_mani = 0
            build_positions = []
            m = empties_mask
            while m:
                lb = m & -m
                idx0 = (lb.bit_length() - 1)  # 0-based
                build_positions.append(idx0 + 1)
                m ^= lb

            for build_pos in build_positions:
                new_mask = mask | (1 << (build_pos-1))

                # Hamid chooses direction
                # Left
                resL = float('inf')
                maskL = new_mask
                j = pos-1
                while j >= 1 and ((maskL >> (j-1)) & 1) == 0:
                    j -= 1
                if j < 1:
                    resL = 1
                else:
                    maskL &= ~(1 << (j-1))
                    resL = 1 + dp(j, maskL)

                # Right
                resR = float('inf')
                maskR = new_mask
                k = pos+1
                while k <= n and ((maskR >> (k-1)) & 1) == 0:
                    k += 1
                if k > n:
                    resR = 1
                else:
                    maskR &= ~(1 << (k-1))
                    resR = 1 + dp(k, maskR)

                best_for_mani = max(best_for_mani, min(resL, resR))

            return best_for_mani

        out_lines.append(str(dp(x, walls_init)))

    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()


