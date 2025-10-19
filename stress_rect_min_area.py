import random, subprocess

BIN = "rect_min_area"

def compile():
    subprocess.run(["g++-14","-std=gnu++20","-O2","-pipe","rect_min_area.cpp","-o",BIN], check=True)

def run_solver(n, m, grid):
    data = "\n".join(["1", f"{n} {m}"] + grid) + "\n"
    proc = subprocess.Popen([f"./{BIN}"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    out,_ = proc.communicate(data)
    rows = [list(map(int, line.split())) for line in out.strip().splitlines()]
    return rows

def brute(n, m, grid):
    ans = [[0]*m for _ in range(n)]
    for u in range(n):
        for d in range(u+1, n):
            for l in range(m-1):
                if grid[u][l] != '1' or grid[d][l] != '1':
                    continue
                for r in range(l+1, m):
                    if grid[u][r] == '1' and grid[d][r] == '1':
                        a = (d-u+1)*(r-l+1)
                        for i in range(u, d+1):
                            for j in range(l, r+1):
                                if ans[i][j] == 0 or a < ans[i][j]:
                                    ans[i][j] = a
    return ans

def rand_grid(n, m, p):
    return ["".join('1' if random.random() < p else '0' for _ in range(m)) for _ in range(n)]

def main():
    random.seed(1)
    compile()
    tests = 500
    for t in range(1, tests+1):
        n = random.randint(2, 10)
        m = random.randint(2, 10)
        p = random.uniform(0.25, 0.75)
        grid = rand_grid(n, m, p)
        got = run_solver(n, m, grid)
        exp = brute(n, m, grid)
        if got != exp:
            print("Mismatch!\nInput:")
            print(1)
            print(n, m)
            print("\n".join(grid))
            print("\nGot:")
            for row in got: print(" ".join(map(str,row)))
            print("\nExpected:")
            for row in exp: print(" ".join(map(str,row)))
            return
        if t % 50 == 0:
            print(f"ok {t}/{tests}")
    print("All simple stress tests passed")

if __name__ == "__main__":
    main()


