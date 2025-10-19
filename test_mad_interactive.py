import subprocess
import sys
import random
import shutil
import time
import select
import argparse


def unique_mode(values):
    freq = {}
    maxc = 0
    for v in values:
        c = freq.get(v, 0) + 1
        freq[v] = c
        if c > maxc:
            maxc = c
    winners = [v for v, c in freq.items() if c == maxc]
    return winners[0] if len(winners) == 1 else 0


def run_session(arrays, solver_cmd=None, timeout=5.0, verbose=False):
    t = len(arrays)
    if solver_cmd is None:
        runner = shutil.which("pypy3.10") or sys.executable
        solver_cmd = [runner, "-u", "mad_interactive_solver.py"]

    proc = subprocess.Popen(
        solver_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    start = time.time()
    proc.stdin.write(str(t) + "\n")
    # Send only the first n; subsequent n's are sent after each '!' is processed
    proc.stdin.write(str(len(arrays[0])) + "\n")
    proc.stdin.flush()

    cur = 0
    next_to_send = 1
    step = 0
    while True:
        if time.time() - start > timeout:
            proc.kill()
            return False, f"Timeout after {timeout}s at case {cur+1}, step {step}"

        rlist, _, _ = select.select([proc.stdout, proc.stderr], [], [], 0.05)
        if not rlist:
            continue
        if proc.stderr in rlist:
            err_line = proc.stderr.readline()
            if err_line:
                print("stderr:", err_line.strip())
        if proc.stdout not in rlist:
            continue
        line = proc.stdout.readline()
        if not line:
            break
        line = line.strip()
        if not line:
            continue
        step += 1
        if verbose:
            print("solver:", line)
        if line.startswith("?"):
            parts = line.split()
            k = int(parts[1])
            idxs = list(map(int, parts[2:]))
            if len(idxs) != k:
                proc.stdin.write("-1\n")
                proc.stdin.flush()
                return False, f"Malformed query at case {cur+1}"
            arr = arrays[cur]
            vals = [arr[i-1] for i in idxs]
            ans = unique_mode(vals)
            if verbose:
                print("judge:", ans)
            proc.stdin.write(str(ans) + "\n")
            proc.stdin.flush()
        elif line.startswith("!"):
            guess = list(map(int, line.split()[1:]))
            expected = arrays[cur]
            if guess != expected:
                proc.kill()
                return False, (
                    f"Wrong answer at case {cur+1}: expected {expected}, got {guess}"
                )
            cur += 1
            if cur == t:
                try:
                    proc.stdin.close()
                except Exception:
                    pass
                try:
                    proc.wait(timeout=0.2)
                except subprocess.TimeoutExpired:
                    proc.kill()
                return True, "OK"
            # Send the next n for the next test case
            proc.stdin.write(str(len(arrays[next_to_send])) + "\n")
            proc.stdin.flush()
            next_to_send += 1
        else:
            # ignore other outputs
            continue

    try:
        err = proc.stderr.read()
    except Exception:
        err = ""
    return False, f"Solver exited unexpectedly. stderr=\n{err}"


def run_transcript(tokens, solver_cmd=None, timeout=5.0, verbose=False):
    runner = shutil.which("pypy3.10") or sys.executable
    solver_cmd = solver_cmd or [runner, "-u", "mad_interactive_solver.py"]

    proc = subprocess.Popen(
        solver_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    def pop_int():
        if not tokens:
            return None
        return tokens.pop(0)

    t = pop_int()
    if t is None:
        proc.kill()
        return False, "Transcript missing t"
    proc.stdin.write(str(t) + "\n")
    first_n = pop_int()
    if first_n is None:
        proc.kill()
        return False, "Transcript missing first n"
    proc.stdin.write(str(first_n) + "\n")
    proc.stdin.flush()

    cur = 1
    start = time.time()
    while True:
        if time.time() - start > timeout:
            proc.kill()
            return False, f"Timeout after {timeout}s at case {cur}, waiting for solver"
        rlist, _, _ = select.select([proc.stdout, proc.stderr], [], [], 0.05)
        if not rlist:
            continue
        if proc.stderr in rlist:
            _ = proc.stderr.readline()
        if proc.stdout not in rlist:
            continue
        line = proc.stdout.readline()
        if not line:
            break
        s = line.strip()
        if not s:
            continue
        if verbose:
            print("solver:", s)
        if s.startswith("?"):
            ans = pop_int()
            if ans is None:
                proc.kill()
                return False, f"Transcript exhausted answering a query in case {cur}"
            if verbose:
                print("judge:", ans)
            proc.stdin.write(str(ans) + "\n")
            proc.stdin.flush()
        elif s.startswith("!"):
            next_token = pop_int()
            if next_token is None:
                # No ack/n provided; let solver finish
                continue
            if next_token in (-1, 0, 1):
                # Send ack
                proc.stdin.write(str(next_token) + "\n")
                proc.stdin.flush()
                cur += 1
                if cur <= t:
                    n_token = pop_int()
                    if n_token is None:
                        proc.kill()
                        return False, f"Transcript missing n for case {cur}"
                    proc.stdin.write(str(n_token) + "\n")
                    proc.stdin.flush()
            else:
                # No ack; this is next n
                cur += 1
                if cur-1 < t:  # we just finished previous; if not last, forward n
                    proc.stdin.write(str(next_token) + "\n")
                    proc.stdin.flush()
        else:
            continue

    try:
        err = proc.stderr.read()
    except Exception:
        err = ""
    return True, "OK" if proc.returncode == 0 else f"Exited with code {proc.returncode}. stderr=\n{err}"


def random_arrays(num_cases=100, n_min=3, n_max=40):
    cases = []
    for _ in range(num_cases):
        n = random.randint(n_min, n_max)
        arr = [random.choice([1, 2]) for _ in range(n)]
        cases.append(arr)
    return cases


def parse_manual_cases_from_stdin():
    data = sys.stdin.read().split()
    if not data:
        return None
    it = iter(data)
    try:
        t = int(next(it))
    except StopIteration:
        return None
    cases = []
    for _ in range(t):
        n = int(next(it))
        arr = [int(next(it)) for _ in range(n)]
        cases.append(arr)
    return cases


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manual", action="store_true", help="Read cases from stdin: t, then for each case: n and n values")
    parser.add_argument("--transcript", action="store_true", help="Read integer transcript for t, n, query answers, optional acks, and next n values")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()

    if args.transcript:
        toks = [int(x) for x in sys.stdin.read().split()]
        ok, msg = run_transcript(toks, timeout=args.timeout, verbose=args.verbose)
        print("Result:", "PASSED" if ok else "FAILED")
        print(msg)
        return
    elif args.manual:
        cases = parse_manual_cases_from_stdin()
        if not cases:
            print("No manual cases provided on stdin.")
            return
    else:
        cases = random_arrays(num_cases=120, n_min=3, n_max=60)

    ok, msg = run_session(cases, timeout=args.timeout, verbose=args.verbose)
    print("Result:", "PASSED" if ok else "FAILED")
    print(msg)


if __name__ == "__main__":
    main()


