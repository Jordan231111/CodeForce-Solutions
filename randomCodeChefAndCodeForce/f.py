import sys
import os
import io
from collections import defaultdict

# --- Start Fast I/O Setup ---
_input_buffer = io.BytesIO(os.read(0, os.fstat(0).st_size))
input = lambda: _input_buffer.readline().decode()
# --- End Fast I/O Setup ---

# --- Template Helpers ---
II = lambda : int(input())
SI = lambda : input().rstrip()
LLI = lambda n : [[int(a) for a in input().split()] for _ in range(n)]
inf = float('inf')
DD = defaultdict
# --- End Template Helpers ---


def solve():
    """
    Main logic to solve a single test case.
    """
    try:
        s = SI()
        if not s: return
        n = II()
        attendees = LLI(n)
    except (ValueError, IndexError):
        return

    D = "docker"
    LS = len(s)
    max_k = LS // 6

    # --- Step 1: Calculate cost(k) for k up to max_k ---
    costs_for_k = {0: 0}
    if max_k > 0:
        change_costs = []
        for i in range(LS - 5):
            cost = sum(1 for j in range(6) if s[i + j] != D[j])
            change_costs.append(cost)

        dp_prev = [0] + [inf] * max_k
        for i in range(6, LS + 1):
            dp_curr = list(dp_prev)
            cost_at_i = change_costs[i - 6]
            for k in range(1, max_k + 1):
                if dp_prev[k - 1] != inf:
                    dp_curr[k] = min(dp_curr[k], dp_prev[k - 1] + cost_at_i)
            dp_prev = dp_curr
        
        # This DP formulation was incorrect. Let's use the working one.
        dp_prev_k = [0] * (LS + 1)
        for k in range(1, max_k + 1):
            dp_curr_k = [inf] * (LS + 1)
            for i in range(1, LS + 1):
                dp_curr_k[i] = dp_curr_k[i-1]
                if i >= 6 and dp_prev_k[i-6] != inf:
                    dp_curr_k[i] = min(dp_curr_k[i], dp_prev_k[i-6] + change_costs[i-6])
            costs_for_k[k] = dp_curr_k[LS]
            dp_prev_k = dp_curr_k

    # --- Step 2: Simplified sweep to find the optimum ---
    event_map = DD(int)
    for l, r in attendees:
        if l <= max_k:
            event_map[l] += 1
            event_map[min(r, max_k) + 1] -= 1

    max_attendees = 0
    min_cost = 0
    current_attendees = 0

    # Iterate through all event points k
    for k in sorted(event_map.keys()):
        if k > max_k + 1: break
        
        # The number of attendees changes at point k.
        # `current_attendees` is valid for the interval [prev_k, k-1]
        # Let's use a simpler loop from k=0 to max_k
    
    # Final corrected, simpler logic:
    attendee_counts = [0] * (max_k + 2)
    for l,r in attendees:
        if l <= max_k:
            attendee_counts[l] += 1
            attendee_counts[min(r, max_k) + 1] -= 1
    
    max_attendees = -1
    min_cost = inf
    current_attendees = 0
    for k in range(max_k + 1):
        current_attendees += attendee_counts[k]
        cost = costs_for_k.get(k, inf)
        
        if current_attendees > max_attendees:
            max_attendees = current_attendees
            min_cost = cost
        elif current_attendees == max_attendees:
            min_cost = min(min_cost, cost)
            
    print(min_cost)


def main():
    """
    Main function to handle multiple test cases.
    """
    try:
        t_str = input()
        if t_str.strip():
            for _ in range(int(t_str)):
                solve()
    except (IOError, EOFError):
        pass

if __name__ == "__main__":
    main()