import subprocess
import sys
import random
import time

MOD = 998244353

def run_prog(prog, inp):
    p = subprocess.Popen(["pypy3.10", prog], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate(inp)
    return p.returncode, out.strip(), err

def run_case(n, k, a):
    t = 1
    s = str(t) + "\n" + f"{n} {k}\n" + " ".join(map(str,a)) + "\n"
    rc1, out1, err1 = run_prog("replace-by_coeff.py", s)
    rc2, out2, err2 = run_prog("brute_replace_by_coeff.py", s)
    return out1, out2, err1, err2

def from_sample():
    inp = """5
2 2
0 1
2 3
2 2
4 5
0 0 0 0
3 6
2 4 3
8 1000
1 1 1 1 1 1 1 1
"""
    rc1, out1, err1 = run_prog("replace-by_coeff.py", inp)
    print("Your output on samples:\n" + out1)
    print()
    # sanity: brute
    rc2, out2, err2 = run_prog("brute_replace_by_coeff.py", inp)
    print("Brute output on samples:\n" + out2)

def random_stress(rounds=200):
    for it in range(1, rounds+1):
        n = random.randint(2, 6)
        k = random.randint(2, 8)
        a = [random.randint(0, k-1) for _ in range(n)]
        o1, o2, e1, e2 = run_case(n,k,a)
        if o1 != o2:
            print("Mismatch found at iteration", it)
            print("n,k=", n, k)
            print("a=", a)
            print("your=", o1)
            print("brut=", o2)
            # rerun once to show both programs' stdout clearly
            t = 1
            s = str(t) + "\n" + f"{n} {k}\n" + " ".join(map(str,a)) + "\n"
            print("\n--- Your full output ---")
            print(run_prog("replace-by_coeff.py", s)[1])
            print("--- Brute full output ---")
            print(run_prog("brute_replace_by_coeff.py", s)[1])
            return False
        if it % 20 == 0:
            print(it, "ok")
    print("All random tests passed")
    return True

if __name__ == "__main__":
    from_sample()
    ok = random_stress(200)
    print("Overall:", "PASSED" if ok else "FAILED")


