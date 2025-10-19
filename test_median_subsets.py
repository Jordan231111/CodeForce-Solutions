import subprocess
import sys
import time
import os
import random

CPP_SOURCE = "median_subsets.cpp"
BIN_NAME = "median_subsets"

def compile_sources():
    subprocess.run([
        "g++-14", "-std=gnu++20", "-O2", "-pipe", CPP_SOURCE, "-o", BIN_NAME
    ], check=True)

def run_io(input_str: str) -> str:
    proc = subprocess.Popen(
        [f"./{BIN_NAME}"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    out, err = proc.communicate(input_str)
    return out

def expected_prefix_counts(p):
    # brute on small only
    def meds(arr):
        n = len(arr)
        s = set()
        for L in range(n):
            for R in range(L+1, n):
                b = sorted(arr[L:R+1])
                k = (len(b)+1)//2 - 1
                s.add(b[k])
        return s
    res = []
    for i in range(1, len(p)+1):
        res.append(len(meds(p[:i])))
    return res

def run_sample_tests():
    inp = []
    inp.append("4")
    # case1
    inp.append("2")
    inp.append("1 2")
    # case2
    inp.append("3")
    inp.append("2 1 3")
    # case3
    inp.append("5")
    inp.append("5 2 3 1 4")
    # case4
    inp.append("6")
    inp.append("4 2 3 1 6 5")
    out = run_io("\n".join(inp)+"\n")
    lines = [ln.strip() for ln in out.strip().splitlines() if ln.strip()]
    assert lines[0] == "0 1", lines[0]
    assert lines[1] == "0 1 2", lines[1]
    assert lines[2] == "0 1 2 3 3", lines[2]
    assert lines[3] == "0 1 2 3 3 4", lines[3]

def run_random_small():
    for n in range(2, 10):
        for _ in range(100):
            p = list(range(1, n+1))
            random.shuffle(p)
            inp = "1\n{}\n{}\n".format(n, " ".join(map(str,p)))
            out = run_io(inp).strip().split()
            got = list(map(int, out))
            want = expected_prefix_counts(p)
            assert got == want, (p, got, want)

def run_all_tests():
    compile_sources()
    run_sample_tests()
    run_random_small()
    print("All tests passed")

if __name__ == "__main__":
    run_all_tests()


