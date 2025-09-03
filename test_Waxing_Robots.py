import subprocess
import sys
import time

def run_case(inp:str):
    p = subprocess.Popen(
        ["pypy3.10","Waxing_Robots.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    out, err = p.communicate(inp)
    return p.returncode, out, err

def make_empty_case(N=30, M=10, K=10):
    robots = [(i*3%N, (i*7+5)%N) for i in range(M)]
    lines = [f"{N} {M} {K}"]
    lines += [f"{r} {c}" for r,c in robots]
    v = ["0"*(N-1) for _ in range(N)]
    h = ["0"*N for _ in range(N-1)]
    lines += v
    lines += h
    return "\n".join(lines)+"\n"

def make_simple_walls(N=30, M=10, K=10):
    robots = [(0,0)] + [(i+1, i+2) for i in range(M-1)]
    lines = [f"{N} {M} {K}"]
    lines += [f"{r} {c}" for r,c in robots]
    v = [list("0"*(N-1)) for _ in range(N)]
    h = [list("0"*N) for _ in range(N-1)]
    for j in range(5,25):
        h[10][j] = '1'
    for i in range(5,25):
        v[i][15] = '1'
    v = ["".join(row) for row in v]
    h = ["".join(row) for row in h]
    lines += v
    lines += h
    return "\n".join(lines)+"\n"

def run_all_tests():
    tests = [make_empty_case(), make_simple_walls()]
    start = time.time()
    for idx, t in enumerate(tests, 1):
        rc, out, err = run_case(t)
        ok = rc == 0 and len(out.strip())>0
        print(f"{idx}: {'✓' if ok else '✗'} rc={rc} out_lines={len(out.splitlines())}")
        if not ok:
            print(err)
    end = time.time()
    print(f"Execution time: {end-start:.3f}s")

if __name__ == "__main__":
    run_all_tests()


