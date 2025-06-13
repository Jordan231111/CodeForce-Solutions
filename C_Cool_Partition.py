#!/usr/bin/env pypy3.10
"""
Codeforces 1980C - Cool Partition
METHOD: Forward Greedy Strategy

ALGORITHM:
The problem requires partitioning an array `a` into contiguous subarrays
`b_1, b_2, ..., b_k` such that for any `j`, `set(b_j)` is a subset
of `set(b_{j+1})`. We want to maximize `k`.

A greedy approach from left-to-right is effective. To maximize the
number of segments, each segment should be as short as possible.

1. Initialize segment count to 0. The `required_elements` for the
   first segment is an empty set, as it has no predecessor.
2. Loop through the array, starting a new segment at each step.
   - Increment segment count.
   - The goal is to find the shortest possible current segment that
     fulfills the subset condition.
   - We iterate from the start of the current segment, adding elements
     to `current_set` until `required_elements.issubset(current_set)`.
   - Once the condition is met, we have found the shortest valid
     segment. We break the inner loop.
   - If we reach the end of the array and the condition is never met,
     the last segment is invalid. We must merge it with the previous
     one, which means the last increment to `count` was erroneous.
   - The `current_set` becomes the `required_elements` for the next
     iteration.

This process correctly finds the maximum number of segments.
"""
import sys

def solve_case(n, arr):
    """Solves a single test case using the forward greedy strategy."""
    if n == 0:
        return 0
    
    segments = 0
    current_pos = 0
    required_elements = set()

    while current_pos < n:
        segments += 1
        
        # Find the end of the current, valid segment
        end_of_segment = current_pos
        current_set = set()
        found_valid_segment = False
        
        while end_of_segment < n:
            current_set.add(arr[end_of_segment])
            if required_elements.issubset(current_set):
                # This is the shortest possible valid segment
                found_valid_segment = True
                break
            end_of_segment += 1
            
        if not found_valid_segment:
            # Reached the end of the array without satisfying the condition.
            # The last segment is not valid, so it must be merged with
            # the previous one. The last increment to segments was incorrect.
            segments -= 1
            break
            
        # Prepare for the next segment
        required_elements = current_set
        current_pos = end_of_segment + 1
        
    return segments

def main():
    """Driver for all test cases."""
    try:
        data = sys.stdin.read().split()
        if not data:
            return
            
        test_cases = int(data[0])
        current_idx = 1
        
        output_lines = []
        for _ in range(test_cases):
            if current_idx >= len(data): break
            n = int(data[current_idx])
            current_idx += 1
            if current_idx + n > len(data): break
            arr = [int(x) for x in data[current_idx:current_idx + n]]
            current_idx += n
            
            result = solve_case(n, arr)
            output_lines.append(str(result))
            
        print("\n".join(output_lines))
    except (IOError, IndexError, ValueError):
        # Handles empty or malformed input.
        return

if __name__ == "__main__":
    main() 