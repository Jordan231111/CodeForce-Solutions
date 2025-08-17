import itertools, subprocess, sys, random

def brute(n, x, s):
    inp = f"1\n{n} {x}\n{s}\n"
    proc = subprocess.Popen([
        "python3", "brute_B_Hamiiid_Haaamid_Hamid.py"
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = proc.communicate(inp)
    if proc.returncode != 0:
        raise RuntimeError(f"Brute failed: {err}")
    return int(out.strip())

def formula(n, x, s):
    if '#' not in s:
        return 1
    return min(x, n - x + 1)

def sweep(max_n=9):
    for n in range(2, max_n+1):
        for x in range(1, n+1):
            for bits in range(1<<n):
                s = ''.join('#' if (bits>>i)&1 else '.' for i in range(n))
                if s[x-1] == '#':
                    continue
                if s.count('.') < 2:
                    continue
                b = brute(n, x, s)
                f = formula(n, x, s)
                if b != f:
                    print("Mismatch:", n, x, s, "brute=", b, "formula=", f)
                    return False
    return True

if __name__ == "__main__":
    ok = sweep(7)
    print("All match" if ok else "Mismatch found")


