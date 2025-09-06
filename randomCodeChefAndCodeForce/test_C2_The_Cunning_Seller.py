import subprocess
import sys
import time

def run_test_case(test_input, expected_output):
    """Run a single test case and check the result."""

    # Run the solution
    process = subprocess.Popen(
        ["pypy3.10", "C2_The_Cunning_Seller.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = process.communicate(test_input)

    if stderr:
        print(f"Error: {stderr}")
        return False, f"ERROR: {stderr}"

    actual = stdout.strip()

    if actual == str(expected_output):
        return True, f"PASSED: output={actual}"
    else:
        return False, f"FAILED: expected={expected_output}, got={actual}"

def run_all_tests():
    """Run all test cases."""
    test_cases = [
        # Sample test cases
        ("8\n1 1\n3 3\n8 3\n2 4\n10 10\n20 14\n3 2\n9 1",
         "3\n9\n-1\n6\n30\n63\n10\n33"),

        # Individual test cases
        ("1\n1 1", "3"),  # n=1, k=1
        ("1\n1 2", "3"),  # n=1, k=2 (k > n)
        ("1\n2 2", "6"),  # n=2, k=2
        ("1\n3 3", "9"),  # n=3, k=3
        ("1\n3 2", "10"), # n=3, k=2
        ("1\n4 4", "12"), # n=4, k=4
        ("1\n4 3", "13"), # n=4, k=3 (1 deal 1 + 1 deal 0)
        ("1\n5 5", "15"), # n=5, k=5
        ("1\n6 6", "18"), # n=6, k=6
        ("1\n6 4", "19"), # n=6, k=4 (1 deal 1 + 3 deal 0)
        ("1\n7 7", "21"), # n=7, k=7
        ("1\n8 8", "24"), # n=8, k=8
        ("1\n9 9", "27"), # n=9, k=9
        ("1\n9 1", "33"), # n=9, k=1 (use deal 2)
        ("1\n10 10", "30"), # n=10, k=10
        ("1\n20 14", "63"), # n=20, k=14

        # Large n with small k
        ("1\n100 1", "-1"),  # n=100, k=1 (impossible)
        ("1\n27 1", "108"), # n=27, k=1 (use deal 3)
        ("1\n28 2", "111"),  # n=28, k=2 (use deal 3 + deal 0)

        # Edge cases
        ("1\n1 100", "3"),  # k much larger than n
    ]

    results = []
    start_time = time.time()

    for test_input, expected in test_cases:
        success, message = run_test_case(test_input, expected)
        results.append((success, message))

    end_time = time.time()

    # Print results
    all_passed = all(success for success, _ in results)

    print("Test Results:")
    for success, message in results:
        print(f"{'✓' if success else '✗'} {message}")

    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")

    return all_passed

def stress_test(max_n=10**5, num_tests=100, verbose=False):
    """Generate random test cases and compare with expected results."""
    import random

    passed = 0
    start = time.time()

    for _ in range(num_tests):
        # Generate random n and k
        n = random.randint(1, min(max_n, 10**9))
        k = random.randint(1, min(n, 10**9))

        test_input = f"1\n{n} {k}\n"

        # Calculate expected result
        if n <= k:
            expected = n * 3
        else:
            # This is a simplified expected calculation
            # In a real stress test, we'd need a reference solution
            deals_to_save = n - k

            # Use greedy approach to calculate expected cost
            remaining_n = n
            remaining_k = k
            expected_cost = 0

            # Use largest possible deals
            pow3 = [1]
            while pow3[-1] * 3 <= remaining_n:
                pow3.append(pow3[-1] * 3)

            for i in range(len(pow3) - 1, -1, -1):
                if remaining_n == 0:
                    break

                watermelons_per_deal = pow3[i]
                if i == 0:
                    cost_per_deal = 3
                else:
                    cost_per_deal = (9 + i) * pow3[i - 1]

                max_deals = min(remaining_k, remaining_n // watermelons_per_deal)

                if max_deals > 0:
                    expected_cost += max_deals * cost_per_deal
                    remaining_n -= max_deals * watermelons_per_deal
                    remaining_k -= max_deals

            if remaining_n > 0:
                expected = -1
            else:
                expected = expected_cost

        success, _ = run_test_case(test_input, expected)
        if success:
            passed += 1
        elif verbose:
            print(f"Failed test: n={n}, k={k}, expected={expected}")

        if verbose and passed % 10 == 0:
            print(f"{passed}/{num_tests} ok", end="\r", flush=True)

    end = time.time()
    print(f"\nStress testing completed: {passed}/{num_tests} cases passed in {end - start:.2f}s")
    return passed == num_tests

if __name__ == "__main__":
    if not run_all_tests():
        sys.exit(1)

    print("\nRunning stress test...")
    if not stress_test(max_n=1000, num_tests=50, verbose=True):
        print("Stress test failed!")
        sys.exit(1)

    print("All tests passed!")
