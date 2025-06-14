#!/usr/bin/env pypy3
"""
Codeforces 1980C - Cool Partition
METHOD: Ultra-Optimized Forward Greedy

ALGORITHM:
Same greedy approach but with minimal overhead and optimized data structures.
Uses integer sets represented as presence arrays for very fast lookups.
"""

def solve_case(n, arr):
    """Optimized greedy solution using reusable presence arrays with lazy clearing."""
    if n == 0:
        return 0

    # Determine the compact range of values for array-based indexing
    min_val = min(arr)
    max_val = max(arr)
    range_size = max_val - min_val + 1

    # If the value range is too large, switch to the set-based fallback
    if range_size > 200_000:
        return solve_case_with_sets(n, arr)

    segments = 0
    current_pos = 0

    # Boolean presence arrays (offset by min_val) — allocated once and reused
    required = [False] * range_size          # values required in next segment
    required_list = []                       # list of indices currently marked in `required`
    required_count = 0                       # len(required_list)

    in_current = [False] * range_size        # values seen in the current segment (lazy cleared)
    found = [False] * range_size             # values from `required` already satisfied (lazy cleared)

    while current_pos < n:
        segments += 1

        remaining = required_count           # how many required values still to satisfy
        found_indices = []                   # indices set in `found` — to clear afterwards
        current_indices = []                 # indices appearing in this segment — becomes new `required`
        valid_segment = False

        for i in range(current_pos, n):
            val_offset = arr[i] - min_val

            # Register value in current segment (avoid duplicates)
            if not in_current[val_offset]:
                in_current[val_offset] = True
                current_indices.append(val_offset)

            # Does it satisfy a pending requirement?
            if required[val_offset] and not found[val_offset]:
                found[val_offset] = True
                found_indices.append(val_offset)
                remaining -= 1

            # All requirements satisfied — segment ends here
            if remaining == 0:
                valid_segment = True
                current_pos = i + 1
                break

        if not valid_segment:
            # Ran out of elements before fulfilling requirements — discard last increment
            segments -= 1
            break

        # ---------- House-keeping for next iteration ----------

        # 1) Clear `found` flags that were set this segment
        for idx in found_indices:
            found[idx] = False

        # 2) Unmark previous `required` flags
        for idx in required_list:
            required[idx] = False

        # 3) Promote current segment's set to the new `required`
        for idx in current_indices:
            required[idx] = True      # mark as required for next segment
            in_current[idx] = False   # clear `in_current` for reuse

        required_list = current_indices
        required_count = len(required_list)

    return segments


def solve_case_with_sets(n, arr):
    """Fallback for when value range is too large."""
    if n == 0:
        return 0
    
    segments = 0
    current_pos = 0
    required_set = set()
    
    while current_pos < n:
        segments += 1
        
        # Make a copy of required elements
        needed = required_set.copy()
        current_set = set()
        valid_segment = False
        
        for i in range(current_pos, n):
            current_set.add(arr[i])
            needed.discard(arr[i])
            
            if not needed:
                valid_segment = True
                current_pos = i + 1
                break
        
        if not valid_segment:
            segments -= 1
            break
        
        required_set = current_set
    
    return segments


def main():
    """Optimized input reading and processing."""
    import sys
    
    # Read all input at once
    input_data = sys.stdin.read().strip()
    tokens = input_data.split()
    
    test_cases = int(tokens[0])
    pos = 1
    
    results = []
    
    for _ in range(test_cases):
        n = int(tokens[pos])
        pos += 1
        
        if n == 0:
            results.append(0)
            continue
        
        # Read array directly without intermediate list
        arr = []
        for i in range(n):
            arr.append(int(tokens[pos + i]))
        pos += n
        
        result = solve_case(n, arr)
        results.append(result)
    
    # Output all results at once
    print('\n'.join(map(str, results)))


if __name__ == "__main__":
    main()