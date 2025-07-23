import subprocess
import sys
import time
from collections import Counter

def is_valid(original: str, rearranged: str) -> bool:
    if Counter(original) != Counter(rearranged):
        return False
    if 'FTF' in rearranged or 'NTN' in rearranged:
        return False
    return True

def run_test_case(strings: list[str]):
    t = len(strings)
    test_input = f"{t}\n" + "\n".join(strings) + "\n"
    process = subprocess.Popen(
        ["pypy3.10", "A_Difficult_Contest.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(test_input)
    if stderr:
        return False, f"Runtime error: {stderr}"
    outs = stdout.strip().split("\n")
    if len(outs) != t:
        return False, "Output line count mismatch"
    for s, res in zip(strings, outs):
        if not is_valid(s, res):
            return False, f"Invalid rearrangement for {s}: got {res}"
    return True, "PASSED"

def run_all_tests():
    test_sets = [
        ["FFT", "ABFBANTTA", "FTTNTT", "FFFTTFFTNTNNNT", "AFTBTFNTTTTTZ"],
        ["FTF"],
        ["NTN"],
        ["F"],
        ["T"],
        ["".join(["T"*1000 + "F"*1000 + "N"*1000])],
    ]
    results = []
    start = time.time()
    for case in test_sets:
        success, message = run_test_case(case)
        results.append((success, message))
    end = time.time()
    print("Test Results:")
    for success, message in results:
        print(f"{'✓' if success else '✗'} {message}")
    all_passed = all(s for s, _ in results)
    print(f"\nExecution time: {end - start:.4f} seconds")
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")

if __name__ == "__main__":
    run_all_tests() 