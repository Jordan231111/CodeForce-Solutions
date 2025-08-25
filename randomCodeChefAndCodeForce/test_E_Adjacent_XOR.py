import subprocess
import sys
import time

def run_case(a, b):
    n = len(a)
    t_input = "1\n{}\n{}\n{}\n".format(
        n,
        " ".join(map(str, a)),
        " ".join(map(str, b)),
    )
    p = subprocess.Popen(
        ["pypy3.10", "E_Adjacent_XOR.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    out, err = p.communicate(t_input)
    return out.strip()

def brute_case(a, b):
    n = len(a)
    t_input = "1\n{}\n{}\n{}\n".format(
        n,
        " ".join(map(str, a)),
        " ".join(map(str, b)),
    )
    p = subprocess.Popen(
        ["pypy3.10", "brute_E_Adjacent_XOR.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    out, err = p.communicate(t_input)
    return out.strip()

def run_all_tests():
    samples = [
        ([1,2,3,4,5],[3,2,7,1,5],"YES"),
        ([0,0,1],[1,0,1],"NO"),
        ([0,0,1],[0,0,0],"NO"),
        ([0,0,1,2],[1,3,3,2],"NO"),
        ([1,1,4,5,1,4],[0,5,4,5,5,4],"YES"),
        ([0,1,2],[2,3,2],"NO"),
        ([10,10],[11,10],"NO"),
    ]
    results = []
    for a,b,exp in samples:
        got = run_case(a,b)
        results.append((got==exp, f"sample a={a} b={b} expected={exp} got={got}"))
    print("Sample Results:")
    for ok,msg in results:
        print(f"{'✓' if ok else '✗'} {msg}")
    all_ok = all(ok for ok,_ in results)
    return all_ok

def stress(num=80):
    import random
    random.seed(0)
    for _ in range(num):
        n = random.randint(2,7)
        a = [random.randint(0,7) for _ in range(n)]
        b = [random.randint(0,7) for _ in range(n)]
        got = run_case(a,b)
        exp = brute_case(a,b)
        if got != exp:
            print("Mismatch:")
            print("a:", a)
            print("b:", b)
            print("got:", got, "exp:", exp)
            return False
    print("Stress OK")
    return True

if __name__ == "__main__":
    ok1 = run_all_tests()
    ok2 = stress(200)
    print("Overall:", "PASSED" if ok1 and ok2 else "FAILED")


