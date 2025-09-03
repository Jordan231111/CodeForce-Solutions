import random
import subprocess
import string

def gen_case(n, m):
    rows = [''.join(random.choice(string.ascii_lowercase[:4]) for _ in range(m)) for __ in range(n)]
    s = f"1\n{n} {m}\n" + "\n".join(rows) + "\n"
    return s

def run_prog(prog, inp):
    p = subprocess.Popen(["pypy3.10", prog], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate(inp)
    return p.returncode, out.strip(), err

def main():
    tests = 300
    for it in range(1, tests+1):
        n = random.randint(1, 7)
        m = random.randint(1, 7)
        case = gen_case(n, m)
        rc1, out1, err1 = run_prog("G_Famous_Choreographer.py", case)
        rc2, out2, err2 = run_prog("brute.py", case)
        if out1 != out2:
            print("Mismatch on test", it)
            print(case)
            print("sol:", out1)
            print("brute:", out2)
            print("stderr sol:", err1)
            print("stderr brute:", err2)
            return
        if it % 50 == 0:
            print(f"{it}/{tests} ok")
    print("All tests passed")

if __name__ == "__main__":
    main()


