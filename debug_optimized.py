def debug_optimized():
    # Test case 2: A = [1, 2], expected output = 2
    a = [1, 2]
    n = len(a)
    
    # Compute initial XOR of all elements
    total_xor = 0
    for x in a:
        total_xor ^= x
    
    print(f"Initial array: {a}")
    print(f"Initial XOR: {total_xor}")
    
    best_score = -1
    
    # Try all possible Alice moves
    for i in range(n):
        for j in range(n):
            print(f"\nAlice move: i={i}, j={j}")
            
            # After Alice's move (i,j), array becomes:
            # B[i] = a[i] ^ a[j], B[k] = a[k] for k != i
            # XOR(B) = total_xor ^ a[j]
            
            xor_after_alice = total_xor ^ a[j]
            print(f"XOR after Alice (optimized): {xor_after_alice}")
            
            # Verify this is correct
            b = a[:]
            b[i] = a[i] ^ a[j]
            actual_xor = 0
            for x in b:
                actual_xor ^= x
            print(f"XOR after Alice (actual): {actual_xor}")
            
            # Bob's optimal score is min over all Bob's moves
            bob_best = float('inf')
            
            # Case 1: Bob modifies position i
            bob_score_i = total_xor ^ a[i]
            print(f"  Bob modifies pos {i}: score = {total_xor} ^ {a[i]} = {bob_score_i}")
            bob_best = min(bob_best, bob_score_i)
            
            # Case 2: Bob modifies position p != i
            for q in range(n):
                bob_score = xor_after_alice ^ a[q]
                print(f"  Bob modifies other pos with a[{q}]: score = {xor_after_alice} ^ {a[q]} = {bob_score}")
                bob_best = min(bob_best, bob_score)
            
            print(f"  Bob's best score: {bob_best}")
            best_score = max(best_score, bob_best)
    
    print(f"\nFinal answer: {best_score}")

debug_optimized()
