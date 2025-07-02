import random, subprocess, os, sys, sysconfig, textwrap, importlib.util, importlib.machinery, importlib

# Import the main solution as module
spec = importlib.util.spec_from_file_location("sol", os.path.join(os.path.dirname(__file__), "f.py"))
sol = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sol)

# Brute force reference implementation for small n

def brute(arr, s, x):
    n = len(arr)
    res = 0
    for l in range(n):
        summ = 0
        mx = -10**18
        for r in range(l, n):
            summ += arr[r]
            if arr[r] > mx:
                mx = arr[r]
            if summ == s and mx == x:
                res += 1
    return res


def run_case(arr, s, x):
    inp = f"1\n{len(arr)} {s} {x}\n" + " ".join(map(str, arr)) + "\n"
    result = subprocess.run([sys.executable, "f.py"], input=inp.encode(), stdout=subprocess.PIPE).stdout.decode().strip()
    return int(result)


def test_random():
    random.seed(0)
    for n in range(1, 15):
        for _ in range(200):
            arr = [random.randint(-5, 5) for _ in range(n)]
            x = random.randint(-5, 5)
            s = random.randint(-20, 20)
            expected = brute(arr, s, x)
            got = run_case(arr, s, x)
            assert got == expected, (arr, s, x, expected, got)

if __name__ == "__main__":
    test_random()
    print("All stress tests passed.") 