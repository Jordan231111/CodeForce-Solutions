import subprocess
import random
import sys
import time

SOLUTION = "Grid_Game.py"

TEST_CASES = [
    ("""4 5 5\n1 4\n2 3\n3 2\n3 4\n4 2\n""", "No"),
    ("""2 7 3\n1 2\n2 4\n1 6\n""", "Yes"),
    ("""1 1 0\n""", "Yes"),
    ("""10 12 20\n8 3\n1 11\n6 4\n3 7\n10 4\n5 7\n4 7\n5 5\n4 3\n6 1\n1 6\n2 7\n6 7\n1 3\n6 3\n2 12\n9 6\n7 3\n3 11\n9 7\n""", "Yes"),
]

def run_test_case(test_input: str, expected: str):
    proc = subprocess.Popen(
        ["pypy3.10", SOLUTION],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = proc.communicate(test_input)
    actual = stdout.strip()
    return actual == expected, actual, stderr

def run_all_tests():
    start_time = time.time()
    results = []
    for idx, (inp, exp) in enumerate(TEST_CASES, 1):
        success, out, err = run_test_case(inp, exp)
        msg = f"Case {idx}: {'PASSED' if success else f'FAILED (exp={exp}, got={out})'}"
        if err:
            msg += f"\nstderr: {err}"
        print(msg)
        results.append(success)
    duration = time.time() - start_time
    print(f"\nExecution time: {duration:.3f} seconds")
    print(f"Overall: {'PASSED' if all(results) else 'FAILED'}")

# ---- Randomised stress testing ----

def brute_solver(H, W, obstacles):
    from collections import deque
    grid_block = [[False]* (W+1) for _ in range(H+1)]
    for r, c in obstacles:
        grid_block[r][c] = True
    q = deque([(1,1)])
    vis = [[False]*(W+1) for _ in range(H+1)]
    vis[1][1] = True
    while q:
        r, c = q.popleft()
        if (r, c) == (H, W):
            return True
        for dr, dc in ((-1,0),(1,0),(0,-1),(0,1)):
            nr, nc = r+dr, c+dc
            if 1<=nr<=H and 1<=nc<=W and not grid_block[nr][nc] and not vis[nr][nc]:
                vis[nr][nc] = True
                q.append((nr,nc))
    return False

def stress_test(max_dim=20, num_tests=100, verbose=False):
    random.seed(0)
    for t in range(1, num_tests + 1):
        H = random.randint(1, max_dim)
        W = random.randint(1, max_dim)
        max_k_possible = H * W - 2
        if max_k_possible < 0:
            max_k_possible = 0 # Handle tiny grids like 1x1
        
        K = random.randint(0, min(max_k_possible, max_dim * 2))

        all_cells = [(r, c) for r in range(1, H + 1) for c in range(1, W + 1) if (r, c) not in [(1, 1), (H, W)]]
        
        # Ensure K is not larger than the number of available cells for obstacles
        if K > len(all_cells):
            K = len(all_cells)
            
        obstacles = random.sample(all_cells, K)
        # build input string
        inp_lines = [f"{H} {W} {K}\n"] + [f"{r} {c}\n" for r,c in obstacles]
        test_input = "".join(inp_lines)
        expected = "Yes" if brute_solver(H, W, obstacles) else "No"
        proc = subprocess.Popen(
            ["pypy3.10", SOLUTION],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        out, err = proc.communicate(test_input)
        got = out.strip()
        if got != expected:
            print("\nMISMATCH FOUND:")
            print("Input:\n" + test_input)
            print(f"Expected: {expected}, Got: {got}")
            if err:
                print("stderr:\n" + err)
            return
        if verbose and t % 10 == 0:
            print(f"{t}/{num_tests} ok", end="\r", flush=True)
    print(f"\nStress testing passed {num_tests} random cases up to {max_dim}x{max_dim}.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stress":
        stress_test()
    else:
        run_all_tests() 