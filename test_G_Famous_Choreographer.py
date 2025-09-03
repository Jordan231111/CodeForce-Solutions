import subprocess
import sys
import time

def run_test_case(inp: str, expected: str):
    p = subprocess.Popen(["pypy3.10", "G_Famous_Choreographer.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate(inp)
    ok = out.strip() == expected.strip()
    return ok, out.strip(), expected.strip(), err

def run_all_tests():
    sample_inp = """6
2 3
hey
hey
3 3
abc
def
ghi
3 2
af
fa
te
1 1
x
3 3
uoe
vbe
mbu
2 3
hyh
kop
"""
    sample_out = """4
16
2
0
11
3"""
    ok, out, exp, err = run_test_case(sample_inp, sample_out)
    print(f"Sample: {'✓' if ok else '✗'}")
    if not ok:
        print("Got:\n" + out)
        print("Expected:\n" + exp)
        print("Stderr:\n" + err)

if __name__ == "__main__":
    run_all_tests()


