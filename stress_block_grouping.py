import subprocess
import random
import sys
import time

CPP_SOURCE = "block_grouping.cpp"
BIN_NAME = "block_grouping"


def compile_solution():
    res = subprocess.run([
        "g++-14", "-std=gnu++20", "-O2", "-pipe", CPP_SOURCE, "-o", BIN_NAME
    ], capture_output=True, text=True)
    if res.returncode != 0:
        print("Compilation failed:\n" + res.stderr)
        sys.exit(1)


def brute_force(s: str) -> int:
    n = len(s)
    a = s.count('a')
    b = n - a
    if a == 0 or b == 0:
        return 0

    def cost_to_group(ch: str, k: int) -> int:
        pos = [i for i, c in enumerate(s) if c == ch]
        best = 10 ** 9
        for start in range(0, n - k + 1):
            cost = 0
            for i in range(k):
                cost += abs(pos[i] - (start + i))
            best = min(best, cost)
        return best

    return min(cost_to_group('a', a), cost_to_group('b', b))


def run_correctness_stress(num_cases: int = 300, max_n: int = 18):
    compile_solution()
    print(f"Running correctness stress: {num_cases} cases, n <= {max_n}")
    random.seed(0)
    for t in range(1, num_cases + 1):
        n = random.randint(1, max_n)
        s = ''.join(random.choice('ab') for _ in range(n))
        expected = brute_force(s)
        test_input = f"1\n{n}\n{s}\n"
        proc = subprocess.Popen([
            f"./{BIN_NAME}"
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out, _ = proc.communicate(test_input)
        got = int(out.strip())
        if got != expected:
            print("Mismatch detected!\nInput:\n" + test_input)
            print(f"Expected: {expected}, Got: {got}")
            return False
        if t % 50 == 0:
            print(f"  {t}/{num_cases} ok", flush=True)
    print("Correctness stress passed.")
    return True


def run_performance(max_n: int = 200000, trials: int = 5):
    compile_solution()
    print(f"Running performance test: {trials} trials up to n={max_n}")
    worst = 0.0
    for _ in range(trials):
        n = max_n
        s = ''.join(random.choice('ab') for _ in range(n))
        test_input = f"1\n{n}\n{s}\n"
        start = time.time()
        proc = subprocess.Popen([
            f"./{BIN_NAME}"
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out, _ = proc.communicate(test_input)
        elapsed = time.time() - start
        worst = max(worst, elapsed)
    print(f"Performance OK. Worst time: {worst:.3f}s")
    return True


if __name__ == "__main__":
    ok = run_correctness_stress() and run_performance()
    sys.exit(0 if ok else 1)


