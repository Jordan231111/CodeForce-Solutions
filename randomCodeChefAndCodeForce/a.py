from sys import stdin
import sys

# It is not recommended to use this unless you are certain that the problem requires a deep recursion
#sys.setrecursionlimit(10**6)

def solve():
    it = iter(stdin.buffer.read().split())
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        m = int(next(it))
        
        edges = []
        total_w = 0
        for _ in range(m):
            u, v, w = map(int, (next(it), next(it), next(it)))
            u -= 1
            v -= 1
            edges.append((u, v, w))
            total_w += w

        adj_1_mask = [0] * n
        adj_0_mask = [0] * n
        for u, v, w in edges:
            if w == 1:
                adj_1_mask[u] |= (1 << v)
                adj_1_mask[v] |= (1 << u)
            else:
                adj_0_mask[u] |= (1 << v)
                adj_0_mask[v] |= (1 << u)

        is_tree = [False] * (1 << n)
        cost = [0] * (1 << n)
        
        internal_1 = [0] * (1 << n)
        internal_0 = [0] * (1 << n)
        num_v_bits = [0] * (1 << n)

        for i in range(1, 1 << n):
            num_v_bits[i] = num_v_bits[i >> 1] + (i & 1)

        all_adj_mask = [(adj_0_mask[i] | adj_1_mask[i]) for i in range(n)]

        for mask in range(1, 1 << n):
            p = (mask & -mask).bit_length() - 1
            prev_mask = mask ^ (1 << p)
            internal_1[mask] = internal_1[prev_mask] + bin(adj_1_mask[p] & prev_mask).count('1')
            internal_0[mask] = internal_0[prev_mask] + bin(adj_0_mask[p] & prev_mask).count('1')

            num_e = internal_1[mask] + internal_0[mask]
            
            if num_e != num_v_bits[mask] - 1:
                continue

            if num_v_bits[mask] <= 1:
                is_tree[mask] = True
                cost[mask] = 0
                continue
            
            start_node = (mask & -mask).bit_length() - 1
            
            q = [start_node]
            visited_bfs = 1 << start_node
            
            head = 0
            while head < len(q):
                u = q[head]
                head += 1
                
                neighbors = all_adj_mask[u] & mask
                while neighbors > 0:
                    v_bit = neighbors & -neighbors
                    v = v_bit.bit_length() - 1
                    if not (visited_bfs & v_bit):
                        visited_bfs |= v_bit
                        q.append(v)
                    neighbors &= neighbors - 1
            
            if visited_bfs == mask:
                is_tree[mask] = True
                cost[mask] = internal_1[mask] - internal_0[mask]
        
        dp = [float('inf')] * (1 << n)
        dp[0] = 0
        
        full_mask = (1 << n) - 1
        for mask in range(1, full_mask + 1):
            p_mask = mask & -mask
            sub = mask
            while sub > 0:
                if (sub & p_mask) and is_tree[sub]:
                    dp[mask] = min(dp[mask], dp[mask ^ sub] + cost[sub])
                sub = (sub - 1) & mask

        min_score = dp[full_mask]
        ans = m - total_w + min_score
        out.append(str(ans))

    print('\n'.join(out))

if __name__ == "__main__":
    solve()
