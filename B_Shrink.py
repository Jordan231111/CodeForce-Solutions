import sys

def solve():
    """
    Solves a single test case for the B. Shrink problem.
    """
    try:
        n_str = sys.stdin.readline()
        if not n_str:
            return
        n = int(n_str)

        # The goal is to construct a permutation of length n that maximizes the
        # number of "shrink" operations. A shrink operation removes an element
        # if it's a "peak" (greater than both its neighbors).

        # The maximum number of operations possible is n-2, as the two
        # elements at the ends of the array can never be removed. We can achieve
        # this maximum score by constructing a permutation that allows for a
        # sequential removal of n-2 elements.

        # A simple construction is to create a single "hill". We place two small
        # numbers at the ends (e.g., 1 and 2) and arrange the rest of the
        # numbers in descending order in between.
        # The permutation looks like: [1, n, n-1, n-2, ..., 3, 2].

        # Let's trace this for n=5: p = [1, 5, 4, 3, 2]
        # 1. Remove 5 (peak between 1 and 4) -> [1, 4, 3, 2]
        # 2. Remove 4 (peak between 1 and 3) -> [1, 3, 2]
        # 3. Remove 3 (peak between 1 and 2) -> [1, 2]
        # Total operations: 3 (which is n-2). This is maximal.

        # This pattern works for all n >= 3, which is guaranteed by the constraints.
        
        # Construct the permutation
        result = [1] + [i for i in range(n, 2, -1)] + [2]
        
        # Print the result
        print(*result)

    except (IOError, ValueError):
        # Handle potential empty lines or malformed input.
        return

def main():
    """
    Main function to read the number of test cases and process each.
    """
    try:
        t_str = sys.stdin.readline()
        if not t_str or not t_str.strip():
            return
        t = int(t_str)
        for _ in range(t):
            solve()
    except (IOError, ValueError):
        return

if __name__ == "__main__":
    main()
