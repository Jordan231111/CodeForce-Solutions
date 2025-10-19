import random, subprocess, time

BIN = "rect_min_area"

def compile():
    subprocess.run(["g++-14","-std=gnu++20","-O2","-pipe","rect_min_area.cpp","-o",BIN], check=True)

def run_solver(n, m, grid):
    data = "\n".join(["1", f"{n} {m}"] + grid) + "\n"
    proc = subprocess.Popen([f"./{BIN}"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    out,_ = proc.communicate(data)
    return out

def rand_grid(n, m, p):
    return ["".join('1' if random.random() < p else '0' for _ in range(m)) for _ in range(n)]

def small_brute(n=20, m=20, tests=60, p=0.92):
    # import brute from previous script lazily
    from stress_rect_min_area import brute
    random.seed(2)
    ok = 0
    for _ in range(tests):
        grid = rand_grid(n, m, p)
        out = run_solver(n, m, grid).strip().splitlines()
        got = [list(map(int, row.split())) for row in out]
        exp = brute(n, m, grid)
        if got != exp:
            print("Mismatch (high density small):\n1\n", n, m)
            print("\n".join(grid))
            print("\nGot:")
            for r in got: print(" ".join(map(str,r)))
            print("\nExpected:")
            for r in exp: print(" ".join(map(str,r)))
            return False
        ok += 1
        if ok % 10 == 0: print(f"ok {ok}/{tests}")
    print("Small high-density tests passed")
    return True

def max_perf(n=500, m=500, p=0.98):
    print("Running max-size performance tests...")
    random.seed(3)
    # all ones
    grid = ["1"*m for _ in range(n)]
    t0=time.time(); run_solver(n, m, grid); print(f"All-ones: {time.time()-t0:.2f}s")
    # random dense
    grid = rand_grid(n, m, p)
    t0=time.time(); run_solver(n, m, grid); print(f"Random p={p:.2f}: {time.time()-t0:.2f}s")

if __name__ == "__main__":
    compile()
    small_brute()
    max_perf()


