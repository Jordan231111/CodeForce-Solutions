import sys
import io
import os

mod = 998244353
MAX_X = 2 * 10**5 + 5

fact = [1] * (MAX_X + 1)
inv_fact = [1] * (MAX_X + 1)
for i in range(1, MAX_X + 1):
    fact[i] = (fact[i - 1] * i) % mod
inv_fact[MAX_X] = pow(fact[MAX_X], mod - 2, mod)
for i in range(MAX_X - 1, -1, -1):
    inv_fact[i] = (inv_fact[i + 1] * (i + 1)) % mod

def nCr_mod(n, r):
    if r < 0 or r > n:
        return 0
    num = fact[n]
    den = (inv_fact[r] * inv_fact[n - r]) % mod
    return (num * den) % mod

# Using Mobius inversion / inclusion-exclusion for the core counting
mu = [0] * (MAX_X)
is_prime = [True] * (MAX_X)
primes = []
mu[1] = 1
is_prime[0] = is_prime[1] = False

for i in range(2, MAX_X):
    if is_prime[i]:
        primes.append(i)
        mu[i] = -1
    for p in primes:
        if i * p >= MAX_X:
            break
        is_prime[i * p] = False
        if i % p == 0:
            mu[i * p] = 0
            break
        else:
            mu[i * p] = -mu[i]

def solve():
    """
    This function encapsulates the entire logic for reading input,
    and solving all test cases using the correct combinatorial insight.
    """
    input_buffer = io.BytesIO(os.read(0, os.fstat(0).st_size))
    input = input_buffer.readline
    
    t = int(input())
    queries = []
    for _ in range(t):
        n, x = map(int, input().split())
        queries.append((n, x))

    results = []
    for n, x in queries:
        if n == 1:
            results.append(str(x))
            continue
        
        # Total number of sets where all elements are divisible by d
        # is sum_{r=1..d} C(floor((x-r)/d)+1, n).
        # By inclusion-exclusion, the answer is sum_{d=2..x} -mu[d] * count(d)
        
        ans = 0
        for d in range(1, x // (n - 1) + 2 if n > 1 else x + 1):
            if d > x: break
            if mu[d] == 0:
                continue

            num_multiples = x // d
            term = nCr_mod(num_multiples, n)
            
            if mu[d] == 1:
                ans = (ans + term) % mod
            else: # mu[d] == -1
                ans = (ans - term + mod) % mod
        
        # The inclusion-exclusion counts sets where elements have a common divisor d>1.
        # This is equivalent to Q = {d*a_1, d*a_2, ...}.
        # The problem is about v_i = r (mod d). The logic needs to account for the remainder.
        
        ans = 0
        for d in range(2, x + 1):
            if mu[d] == 0: continue
            
            # Count sets where all elements are congruent mod d.
            # This is sum over r=1..d of C(count(v=r mod d), n)
            # count(v=r mod d) is floor((x-r)/d) + 1
            # Let k = floor(x/d). There are x%d remainders with k+1 multiples,
            # and d-(x%d) remainders with k multiples.
            
            k = x // d
            r_count = x % d
            
            term = (r_count * nCr_mod(k + 1, n)) % mod
            term = (term + (d - r_count) * nCr_mod(k, n)) % mod

            if mu[d] == 1: # This should be -mu[d] in the formula
                ans = (ans - term + mod) % mod
            else: # mu[d] == -1
                ans = (ans + term) % mod

        results.append(str(ans))

    sys.stdout.write('\n'.join(results) + '\n')

solve()