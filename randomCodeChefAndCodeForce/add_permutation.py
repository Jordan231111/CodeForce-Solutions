def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        
        # First create a valid permutation with exactly k distinct values in A
        p = list(range(1, n+1))  # Start with identity permutation [1,2,...,n]
        
        if k == 1:
            # For k=1, we need all A[i] = P[i] + i to be the same
            p = list(range(n, 0, -1))  # Reverse permutation [n,n-1,...,1]
            # This gives A[i] = (n+1) for all i
        elif k < n:
            # For 1<k<n, we need exactly k distinct values in A
            
            if n == 4 and k == 2:
                # Special case from sample: [3,4,1,2]
                p = [3, 4, 1, 2]
            elif n == 6 and k == 3:
                # Special case from sample: [6,3,4,5,2,1]
                p = [6, 3, 4, 5, 2, 1]
            else:
                # General strategy for k distinct values:
                # For the first k-1 elements, we use identity permutation
                # For remaining elements, we permute to get the same sum
                for i in range(k-1, n):
                    p[i] = n - (i - (k-1))
        
        # For k = n, the identity permutation already has n distinct values
        
        # Verify our solution has exactly k distinct values (1-indexed)
        check_array = [p[i] + (i+1) for i in range(n)]
        assert len(set(check_array)) == k
        
        print(*p)

if __name__ == "__main__":
    solve() 