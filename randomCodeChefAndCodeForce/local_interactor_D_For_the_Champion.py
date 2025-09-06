import subprocess
import sys
import time
import random

def run_single_case(n, pts, X, Y, solver_path="D_For_the_Champion_interactive.py", verbose=False):
    proc = subprocess.Popen(
        ["pypy3.10", solver_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    def send(line):
        proc.stdin.write(line + "\n")
        proc.stdin.flush()

    def read():
        return proc.stdout.readline()

    send("1")
    send(str(n))
    for x,y in pts:
        send(f"{x} {y}")

    cx, cy = X, Y
    moves = 0
    ok = False
    msg = ""
    while True:
        line = read()
        if not line:
            break
        line = line.strip()
        if verbose:
            print("solver:", line)
        if line.startswith("?"):
            parts = line.split()
            if len(parts) != 3:
                msg = f"Invalid query format: {line}"
                break
            _, d, ks = parts
            try:
                k = int(ks)
            except:
                msg = f"Invalid k: {ks}"
                break
            if k < 0 or k > 10**9:
                msg = f"k out of range: {k}"
                break
            if d == 'U':
                cy += k
            elif d == 'D':
                cy -= k
            elif d == 'L':
                cx -= k
            elif d == 'R':
                cx += k
            else:
                msg = f"Invalid dir: {d}"
                break
            moves += 1
            if moves > 10:
                send(str(-1))
                msg = "Exceeded 10 moves"
                break
            s = min(abs(x - cx) + abs(y - cy) for x,y in pts)
            send(str(s))
        elif line.startswith("!"):
            parts = line.split()
            if len(parts) != 3:
                msg = f"Invalid answer format: {line}"
                break
            ax = int(parts[1]); ay = int(parts[2])
            ok = (ax == X and ay == Y)
            if not ok:
                msg = f"Wrong answer: expected {X} {Y}, got {ax} {ay}"
            break
        else:
            # Ignore stray lines
            continue

    # Allow process to exit naturally
    out, err = proc.communicate(timeout=2)
    return ok, msg, out, err

def random_pts(n, lo=-10**6, hi=10**6):
    pts = set()
    while len(pts) < n:
        x = random.randint(lo, hi)
        y = random.randint(lo, hi)
        pts.add((x,y))
    return list(pts)

def run_tests(num_cases=20, verbose=False):
    passed = 0
    for i in range(num_cases):
        n = random.randint(1, 50)
        pts = random_pts(n)
        X = random.randint(-10**9, 10**9)
        Y = random.randint(-10**9, 10**9)
        ok, msg, out, err = run_single_case(n, pts, X, Y, verbose=verbose)
        if ok:
            passed += 1
            if verbose:
                print(f"Case {i+1}: OK")
        else:
            print(f"Case {i+1}: FAIL - {msg}")
            if verbose:
                print("child stdout:\n", out)
                print("child stderr:\n", err)
            break
    print(f"Passed {passed}/{num_cases}")

if __name__ == "__main__":
    random.seed(0)
    run_tests(num_cases=20, verbose=False)


