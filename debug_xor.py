def debug_case():
    # Test case 2: A = [1, 2], expected output = 2
    a = [1, 2]
    n = len(a)
    
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
            print(f"Alice changes a[{i}] = {a[i]} to {a[i]} ^ {a[j]} = {a[i] ^ a[j]}")
            
            # Create the array after Alice's move
            b = a[:]
            b[i] = a[i] ^ a[j]
            print(f"Array after Alice: {b}")
            
            xor_after_alice = 0
            for x in b:
                xor_after_alice ^= x
            print(f"XOR after Alice: {xor_after_alice}")
            
            # Bob's optimal score
            bob_best = float('inf')
            
            # Try all Bob's moves
            for p in range(n):
                for q in range(n):
                    c = b[:]
                    c[p] = b[p] ^ b[q]
                    score = 0
                    for x in c:
                        score ^= x
                    print(f"  Bob move p={p}, q={q}: array becomes {c}, score = {score}")
                    bob_best = min(bob_best, score)
            
            print(f"  Bob's best score: {bob_best}")
            best_score = max(best_score, bob_best)
    
    print(f"\nFinal answer: {best_score}")

debug_case()
