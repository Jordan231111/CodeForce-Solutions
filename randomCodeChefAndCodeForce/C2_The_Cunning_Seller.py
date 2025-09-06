# input
import sys
input = sys.stdin.readline
II = lambda : int(input())
MI = lambda : map(int, input().split())
LI = lambda : [int(a) for a in input().split()]
SI = lambda : input().rstrip()
LLI = lambda n : [[int(a) for a in input().split()] for _ in range(n)]
LSI = lambda n : [input().rstrip() for _ in range(n)]
MI_1 = lambda : map(lambda x:int(x)-1, input().split())
LI_1 = lambda : [int(a)-1 for a in input().split()]

mod = 998244353
inf = 1001001001001001001
ordalp = lambda s : ord(s)-65 if s.isupper() else ord(s)-97
ordallalp = lambda s : ord(s)-39 if s.isupper() else ord(s)-97
yes = lambda : print("Yes")
no = lambda : print("No")
yn = lambda flag : print("Yes" if flag else "No")
def acc(a:list[int]):
    sa = [0]*(len(a)+1)
    for i in range(len(a)):
        sa[i+1] = a[i] + sa[i]
    return sa

prinf = lambda ans : print(ans if ans < 1000001001001001001 else -1)
alplow = "abcdefghijklmnopqrstuvwxyz"
alpup = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alpall = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
URDL = {'U':(-1,0), 'R':(0,1), 'D':(1,0), 'L':(0,-1)}
DIR_4 = [[-1,0],[0,1],[1,0],[0,-1]]
DIR_8 = [[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]]
DIR_BISHOP = [[-1,1],[1,1],[1,-1],[-1,-1]]
prime60 = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59]
sys.set_int_max_str_digits(0)

from collections import defaultdict,deque
from heapq import heappop,heappush
from bisect import bisect_left,bisect_right
DD = defaultdict
BSL = bisect_left
BSR = bisect_right

def solve():
    n, k = MI()

    if n == 0:
        return 0

    # If we can use all deal 0, that's optimal
    if n <= k:
        return n * 3

    # We need to save n - k deals by using larger deals instead of groups of deal 0
    deals_to_save = n - k

    # Precompute deal information
    pow3 = [1]  # 3^x
    costs = [3]  # cost for deal x
    extra_cost_per_replacement = []  # extra cost when replacing 3^x deal 0 with 1 deal x
    deals_saved_per_replacement = []  # deals saved per replacement

    x = 1
    while True:
        next_pow = pow3[-1] * 3
        if next_pow > n:
            break
        pow3.append(next_pow)
        cost = (9 + x) * pow3[x - 1]
        costs.append(cost)

        # Extra cost per replacement: cost_x - 3*3^x
        extra_cost = cost - 3 * next_pow
        extra_cost_per_replacement.append(extra_cost)

        # Deals saved per replacement: 3^x - 1
        deals_saved = next_pow - 1
        deals_saved_per_replacement.append(deals_saved)

        x += 1

    # Start with all deal 0: cost = 3*n, deals_used = n
    total_cost = 3 * n
    deals_used = n

    if deals_used <= k:
        return total_cost

    # We need to save deals_used - k deals
    deals_to_save = deals_used - k

    # Use greedy replacement: choose the most efficient replacement (lowest extra cost per deal saved)

    while deals_to_save > 0 and n > 0 and any(x < float('inf') for x in extra_cost_per_replacement):
        best_i = -1
        best_efficiency = float('inf')

        for i in range(len(extra_cost_per_replacement)):
            if deals_saved_per_replacement[i] > 0:
                efficiency = extra_cost_per_replacement[i] / deals_saved_per_replacement[i]
                if efficiency < best_efficiency:
                    best_efficiency = efficiency
                    best_i = i

        if best_i == -1:
            return -1

        # How many such replacements can we do?
        watermelons_per_replacement = pow3[best_i + 1]
        max_replacements = n // watermelons_per_replacement

        if max_replacements == 0:
            return -1

        # Calculate the minimum number of replacements needed to make deals_used <= k
        deals_saved_per_rep = deals_saved_per_replacement[best_i]
        watermelons_per_rep = pow3[best_i + 1]

        # We need: n - r * (watermelons_per_rep - 1) <= k
        # So r >= ceil((n - k) / (watermelons_per_rep - 1))
        if watermelons_per_rep - 1 == 0:
            replacements = 0
        else:
            replacements = (n - k + watermelons_per_rep - 2) // (watermelons_per_rep - 1)

        replacements = max(replacements, 0)
        replacements = min(replacements, max_replacements)

        # Check if this replacement will make deals_used <= k
        final_deals_used = n - replacements * (watermelons_per_rep - 1)
        if final_deals_used > k:
            # This replacement doesn't work, skip to next best
            extra_cost_per_replacement[best_i] = float('inf')  # Mark as used
            continue

        if replacements == 0:
            # This replacement doesn't help, skip to next best
            extra_cost_per_replacement[best_i] = float('inf')  # Mark as used
            continue

        # Apply the replacements
        extra_cost = replacements * extra_cost_per_replacement[best_i]
        total_cost += extra_cost

        deals_saved = replacements * deals_saved_per_rep
        deals_used = final_deals_used
        deals_to_save = 0  # We have exactly the right number of deals

        # Update n
        watermelons_replaced = replacements * watermelons_per_rep
        n -= watermelons_replaced

        # Since we have the optimal, break
        break

    if deals_used <= k:
        return total_cost
    else:
        return -1

def main():
    t = II()
    for _ in range(t):
        result = solve()
        print(result)

if __name__ == "__main__":
    main()
