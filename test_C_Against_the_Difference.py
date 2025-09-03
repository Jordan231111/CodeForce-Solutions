import subprocess
import sys
import time

def run_case(inp:str):
    p = subprocess.Popen(["pypy3.10","/Users/jordan/Documents/CodeForce/C_Against_the_Difference.py"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    out, err = p.communicate(inp)
    return out.strip()

def run_brutecase(a):
    n = len(a)
    p = subprocess.Popen(["pypy3.10","/Users/jordan/Documents/CodeForce/brute_c_against_diff.py"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    out, err = p.communicate(f"{n}\n"+" ".join(map(int.__str__,a))+"\n")
    return out.strip()

def main():
    sample_input = """6
1
1
2
2 2
4
2 2 1 1
6
1 2 3 3 3 1
8
8 8 8 8 8 8 8 7
10
2 3 3 1 2 3 5 1 1 7
"""
    sample_output = """1
2
4
5
0
5""".strip()
    got = run_case(sample_input)
    print("Samples:", "OK" if got==sample_output else "FAIL")
    import random
    random.seed(0)
    ok = True
    for _ in range(100):
        n = random.randint(1,12)
        a = [random.randint(1,6) for _ in range(n)]
        t = 1
        inp = str(t)+"\n"+str(n)+"\n"+" ".join(map(str,a))+"\n"
        sol = run_case(inp)
        brute = run_brutecase(a)
        if sol != brute:
            print("Mismatch", a, sol, brute)
            ok = False
            break
    print("Stress:", "OK" if ok else "FAIL")

if __name__ == "__main__":
    main()


