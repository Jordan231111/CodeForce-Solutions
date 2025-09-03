import subprocess
import sys
import random

def simulate_display(article, W):
    if max(article) > W:
        return 0
    l = 1
    s = 0
    for a in article:
        if s + a <= W:
            s += a
        else:
            l += 1
            s = a
    return l

def run_single_case(W, solver_path="F1_From_the_Unknown_interactive.py", verbose=False):
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

    queries = 0
    while True:
        line = read()
        if not line:
            break
        sline = line.strip()
        if verbose:
            print("solver:", sline)
        if sline.startswith("?"):
            parts = sline.split()
            if len(parts) < 3:
                send(str(-1))
                break
            try:
                n = int(parts[1])
                a = list(map(int, parts[2:2+n]))
            except:
                send(str(-1))
                break
            if len(a) != n or n < 1 or n > 100000:
                send(str(-1))
                break
            if any(x < 1 or x > 100000 for x in a):
                send(str(-1))
                break
            queries += 1
            if queries > 2:
                send(str(-1))
                break
            send(str(simulate_display(a, W)))
        elif sline.startswith("!"):
            parts = sline.split()
            if len(parts) != 2:
                break
            try:
                ansW = int(parts[1])
            except:
                break
            ok = (ansW == W)
            out, err = proc.communicate(timeout=2)
            return ok, out, err
        else:
            continue

    out, err = proc.communicate(timeout=2)
    return False, out, err

def run_tests():
    fixed = [1, 2, 3, 20, 100000]
    passed = 0
    for i, W in enumerate(fixed, 1):
        ok, out, err = run_single_case(W, verbose=False)
        print(f"Case {i}: W={W} -> {'OK' if ok else 'FAIL'}")
        if ok:
            passed += 1
    print(f"Passed {passed}/{len(fixed)}")

if __name__ == "__main__":
    run_tests()


