import subprocess
import sys
import time
import random
import itertools

def f_brutal(arr, K):
    n = len(arr)
    if n == 0:
        return []
    best = None
    upto = min(K, n)
    for e in range(1, upto + 1):
        left = sorted(arr[:e])
        right = f_brutal(arr[e:], K)
        cand = left + right
        if best is None or cand < best:
            best = cand
    return best

def run_case(A, K, queries):
    N = len(A)
    Q = len(queries)
    lines = []
    lines.append("1")
    lines.append(f"{N} {K} {Q}")
    lines.append(" ".join(map(str, A)))
    for L,R,X in queries:
        lines.append(f"{L} {R} {X}")
    data = "\n".join(lines) + "\n"
    proc = subprocess.Popen(
        ["pypy3.10", "Split_Subarray_Sort.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd="."
    )
    out, err = proc.communicate(data)
    if proc.returncode != 0:
        return None, f"Runtime error: {err}"
    ans = list(map(int, out.strip().split()))
    return ans, None

def expected_answers(A, K, queries):
    res = []
    for L,R,X in queries:
        B = A[L-1:R]
        C = f_brutal(B, K)
        res.append(C[X-1])
    return res

def exhaustive_small():
    start = time.time()
    checked = 0
    for N in range(1, 8):
        values = list(range(1, N+1))
        for A in itertools.permutations(values):
            A = list(A)
            for K in range(1, N+1):
                qs = []
                for L in range(1, N+1):
                    for R in range(L, N+1):
                        for X in range(1, R-L+1+1):
                            qs.append((L,R,X))
                exp = expected_answers(A, K, qs)
                got, err = run_case(A, K, qs)
                if err is not None:
                    print(err)
                    return False
                if got != exp:
                    print("[EXHAUSTIVE] Mismatch!\nA=", A, "K=", K)
                    print("First cases:")
                    print("Expected=", exp[:20])
                    print("Got=     ", got[:20])
                    return False
                checked += 1
    end = time.time()
    print(f"Exhaustive small passed: {checked} cases in {end-start:.2f}s")
    return True

def adversarial_tests(rounds=200):
    random.seed(1)
    start = time.time()
    for _ in range(rounds):
        # Construct arrays with descending runs and spikes
        N = random.randint(2, 10)
        base = list(range(1, N+1))
        # Make adversarial by reversing random chunks
        i = 0
        A = base[:]
        while i < N:
            len_chunk = random.randint(1, min(4, N-i))
            A[i:i+len_chunk] = reversed(A[i:i+len_chunk])
            i += len_chunk
        random.shuffle(A)
        K = random.randint(1, N)
        qs = []
        for __ in range(random.randint(5, 20)):
            L = random.randint(1, N)
            R = random.randint(L, N)
            X = random.randint(1, R-L+1)
            qs.append((L,R,X))
        exp = expected_answers(A, K, qs)
        got, err = run_case(A, K, qs)
        if err is not None:
            print(err)
            return False
        if got != exp:
            print("[ADVERSARIAL] Mismatch!\nA=", A, "K=", K)
            print("Queries=", qs)
            print("Expected=", exp)
            print("Got=     ", got)
            return False
    end = time.time()
    print(f"Adversarial passed: {rounds} rounds in {end-start:.2f}s")
    return True

def random_bulk(rounds=200):
    random.seed(0)
    start = time.time()
    for _ in range(rounds):
        N = random.randint(1, 20)
        A = list(range(1, N+1))
        random.shuffle(A)
        K = random.randint(1, N)
        qs = []
        for __ in range(random.randint(5, 50)):
            L = random.randint(1, N)
            R = random.randint(L, N)
            X = random.randint(1, R-L+1)
            qs.append((L,R,X))
        exp = expected_answers(A, K, qs)
        got, err = run_case(A, K, qs)
        if err is not None:
            print(err)
            return False
        if got != exp:
            print("[RANDOM] Mismatch!\nA=", A, "K=", K)
            print("Queries=", qs)
            print("Expected=", exp)
            print("Got=     ", got)
            return False
    end = time.time()
    print(f"Random bulk passed: {rounds} rounds in {end-start:.2f}s")
    return True

def run_all_tests():
    ok1 = exhaustive_small()
    if not ok1:
        return
    ok2 = adversarial_tests(200)
    if not ok2:
        return
    ok3 = random_bulk(300)
    if not ok3:
        return
    print("All enhanced tests passed.")

if __name__ == "__main__":
    run_all_tests()


