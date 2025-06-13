import random
import time
from C_Cool_Partition import solve_case


def random_case(n: int, max_val: int):
    """Generate a random test case of length n with values in [1, max_val]."""
    rng = random.Random(42)  # fixed seed for reproducibility
    return [rng.randint(1, max_val) for _ in range(n)]


def run_benchmark():
    """Run a single large benchmark to gauge performance within 2-second limit."""
    n = 200_000
    arr = random_case(n, n)

    start = time.perf_counter()
    _ = solve_case(n, arr)
    elapsed = time.perf_counter() - start

    print(f"Benchmark: n={n}, elapsed={elapsed * 1000:.2f} ms")


if __name__ == "__main__":
    run_benchmark() 