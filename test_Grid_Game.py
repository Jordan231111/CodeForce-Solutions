import subprocess
import time

SOLUTION = "Grid_Game.py"

TEST_CASES = [
    ("""4 5 5\n1 4\n2 3\n3 2\n3 4\n4 2\n""", "No"),
    ("""2 7 3\n1 2\n2 4\n1 6\n""", "Yes"),
    ("""1 1 0\n""", "Yes"),
]

def run_test_case(input_data, expected):
    proc = subprocess.Popen(["pypy3.10", SOLUTION], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = proc.communicate(input_data)
    output = out.strip()
    return output == expected, output, err

def run_all():
    start = time.time()
    all_passed = True
    for idx, (inp, exp) in enumerate(TEST_CASES, 1):
        ok, out, err = run_test_case(inp, exp)
        if ok:
            print(f"✓ Case {idx} passed")
        else:
            print(f"✗ Case {idx} failed: expected {exp}, got {out}")
            if err:
                print(err)
            all_passed = False
    print(f"Time: {time.time()-start:.3f}s")
    if all_passed:
        print("All sample cases passed.")

if __name__ == "__main__":
    run_all() 