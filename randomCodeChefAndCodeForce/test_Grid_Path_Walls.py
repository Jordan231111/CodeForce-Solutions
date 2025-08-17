import subprocess
import sys
import time
from itertools import combinations

MOD = 998244353

def nCr_prepare(n):
    fact = [1]*(n+1)
    for i in range(1, n+1):
        fact[i] = fact[i-1]*i % MOD
    invfact = [1]*(n+1)
    invfact[n] = pow(fact[n], MOD-2, MOD)
    for i in range(n, 0, -1):
        invfact[i-1] = invfact[i]*i % MOD
    return fact, invfact

def nCr(n,k,fact,invfact):
    if k < 0 or k > n or n < 0:
        return 0
    return fact[n]*invfact[k]%MOD*invfact[n-k]%MOD

def expected_formula(h,w,k):
    d = h + w - 2
    fact, invfact = nCr_prepare(max(1, d))
    nsp = nCr(d, h-1, fact, invfact)
    outside = 2*(h-1)*(w-1) % MOD
    if k < d:
        return 0
    if k == d:
        return nsp % MOD
    if k == d+1:
        return nsp * outside % MOD
    if k == d+2:
        c2 = outside * ((outside-1) % MOD) % MOD
        inv2 = (MOD+1)//2
        c2 = c2 * inv2 % MOD
        pairs = (d-1) % MOD * nCr(d-2, h-2, fact, invfact) % MOD
        return (nsp * c2 - pairs) % MOD
    return 0

def expected_bruteforce(h,w,k):
    H, W = h, w
    # enumerate walls: assign id to each wall; create adjacency when removed
    walls = []
    # vertical walls between (r,c) and (r+1,c)
    for r in range(H-1):
        for c in range(W):
            a = (r, c)
            b = (r+1, c)
            walls.append((a,b))
    base_v = len(walls)
    for r in range(H):
        for c in range(W-1):
            a = (r, c)
            b = (r, c+1)
            walls.append((a,b))
    m = len(walls)
    cnt = 0
    for idxs in combinations(range(m), k):
        removed = set(idxs)
        from collections import deque
        q = deque([(0,0)])
        seen = {(0,0)}
        while q:
            r,c = q.popleft()
            if (r,c) == (H-1,W-1):
                cnt += 1
                break
            if r+1 < H:
                i = r*W + c  # not used directly
                wid = r*W + c  # placeholder
                wid = r*W + c  # unused
            # up
            if r > 0:
                wall_id = (r-1)*W + c
                if wall_id in removed and (r-1,c) not in seen:
                    seen.add((r-1,c))
                    q.append((r-1,c))
            # down
            if r+1 < H:
                wall_id = r*W + c
                if wall_id in removed and (r+1,c) not in seen:
                    seen.add((r+1,c))
                    q.append((r+1,c))
            # left
            if c > 0:
                wall_id = base_v + r*(W-1) + (c-1)
                if wall_id in removed and (r,c-1) not in seen:
                    seen.add((r,c-1))
                    q.append((r,c-1))
            # right
            if c+1 < W:
                wall_id = base_v + r*(W-1) + c
                if wall_id in removed and (r,c+1) not in seen:
                    seen.add((r,c+1))
                    q.append((r,c+1))
    return cnt % MOD

def run_test_case(h, w, k, use_brute=False):
    if use_brute:
        expected = expected_bruteforce(h,w,k)
    else:
        expected = expected_formula(h,w,k)

    test_input = f"1\n{h} {w} {k}\n"
    process = subprocess.Popen(
        ["pypy3.10", "Grid_Path_Walls.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(test_input)
    actual = int(stdout.strip()) if stdout.strip() else None
    if actual == expected:
        return True, f"PASSED: H={h}, W={w}, K={k}, output={actual}"
    else:
        return False, f"FAILED: H={h}, W={w}, K={k}, expected={expected}, got={actual}, stderr={stderr.strip()}"

def run_all_tests():
    test_cases = [
        (2,2,1, False),
        (2,2,3, False),
        (2,2,2, False),
        (2,2,4, False),
        (200000,200000,400000, False),
        (2,203,203, False),
        # Edge cases with brute-force validation
        (3,3,4, True),
        (3,3,5, True),
    ]

    results = []
    start_time = time.time()
    for h,w,k,use_brute in test_cases:
        success, message = run_test_case(h,w,k,use_brute)
        results.append((success, message))
    end_time = time.time()

    all_passed = all(success for success, _ in results)
    print("Test Results:")
    for success, message in results:
        mark = 'PASS' if success else 'FAIL'
        print(f"{mark} {message}")
    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")

if __name__ == "__main__":
    run_all_tests()


