import subprocess
import sys
import time

SOLUTION = "Swap_Equal_Sum_Subarrays.py"

def run_case(n, a, b):
    test_input = "1\n" + str(n) + "\n" + " ".join(map(str,a)) + "\n" + " ".join(map(str,b)) + "\n"
    process = subprocess.Popen(
        ["pypy3.10", SOLUTION],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = process.communicate(test_input)
    return stdout.strip()

def run_all_tests():
    cases = []
    cases.append((6,[1,1,1,0,0,1],[0,1,1,0,1,1],"Yes"))
    cases.append((2,[0,0],[1,0],"No"))
    cases.append((3,[1,1,1],[1,1,1],"Yes"))
    cases.append((2,[1,0],[0,1],"No"))
    cases.append((4,[0,1,0,0],[1,0,0,0],"No"))
    cases.append((4,[0,1,0,0],[0,0,1,0],"Yes"))
    cases.append((5,[1,0,1,0,1],[0,1,0,1,1],"Yes"))

    results=[]
    start=time.time()
    for n,a,b,expected in cases:
        out=run_case(n,a,b)
        results.append((out==expected,f"n={n} -> {out} expected {expected}"))
    end=time.time()
    print("Test Results:")
    for ok,msg in results:
        print(f"{'✓' if ok else '✗'} {msg}")
    print(f"\nExecution time: {end-start:.4f} seconds")
    print("Overall:","PASSED" if all(ok for ok,_ in results) else "FAILED")

if __name__ == "__main__":
    run_all_tests()


