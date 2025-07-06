import subprocess
import sys
import time
import os

SCRIPT = "Skating_Rink.py"
PYTHON = "pypy3.10"
N = 40

def build_input(grid):
    M = sum(row.count('#') for row in grid)
    return f"{N} {M}\n" + "\n".join(grid) + "\n"

def validate_output(grid, output):
    M = sum(row.count('#') for row in grid)
    total_free = N * N - M
    lines = [ln.strip() for ln in output.strip().split("\n") if ln.strip()]
    if len(lines) != total_free:
        return False, f"Expected {total_free} points, got {len(lines)}"
    seen = set()
    for ln in lines:
        parts = ln.split()
        if len(parts) != 2 or not all(p.isdigit() for p in parts):
            return False, f"Invalid line format: '{ln}'"
        x, y = map(int, parts)
        if not (0 <= x < N and 0 <= y < N):
            return False, f"Coordinate out of bounds: {x} {y}"
        if grid[x][y] == '#':
            return False, f"Rock at coordinate: {x} {y}"
        if (x, y) in seen:
            return False, f"Duplicate coordinate: {x} {y}"
        seen.add((x, y))
    return True, "OK"

def run_test_case(name, grid):
    test_input = build_input(grid)
    proc = subprocess.Popen([
        PYTHON, SCRIPT
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = proc.communicate(test_input)
    if stderr:
        return False, f"{name}: Runtime error\n{stderr}"
    ok, msg = validate_output(grid, stdout)
    return ok, f"{name}: {msg}"

def generate_grid(M):
    grid = [['.' for _ in range(N)] for _ in range(N)]
    cnt = 0
    for i in range(N):
        for j in range(N):
            if cnt < M:
                grid[i][j] = '#'
                cnt += 1
    return [''.join(row) for row in grid]

# Sample grid from prompt (truncated here for brevity)
SAMPLE_GRID = [
    ".#......#..#.#..........................",
    "............#..............#..##...#..#.",
    "......#........##..#...##......#.#......",
    ".##..#...#......#.#.#....#....##.#....#.",
    "............#..............#.......#.#..",
    "..#.....#.....#...##......#............#",
    "......#.....#......#.#.....##..#.##..#..",
    "#.#.#.....#.#.#....#.#..........#.......",
    "#...##.......#...#...#.......#....#.....",
    "#..#...#...#....#...#........#...#.#....",
    "....#..........#.......#..#.............",
    "...##.......#.#..........#.#..........#.",
    "..#.......#.....#.#..#.........#..##....",
    "..##..##....#.............#.........#...",
    "............................#...........",
    "...#...#....#..####.#...........#.......",
    ".##..........#.#.#..................#...",
    "#...#.##............#......##..#........",
    "............#.#...#...#.#..#..#....#....",
    "......#.#........................#.###.#",
    "....##......#..............#.#..........",
    "#....#...#......#.#....#....#.......##..",
    "..#......#......#.#............##..#....",
    "....#.............#..#.#............#..#",
    ".....#......#..##.....#....###.....#.#..",
    "#...#...#.#.....#.....................#.",
    "#........#.......#..........#.....###...",
    "....#..#........#.......#...#.##.##..#..",
    "#..........##.#.#.#....#......#.#..##...",
    ".....##.....#....#..#.................#.",
    "...#...#...#......##.....#..........#..#",
    ".....#..#.................##............",
    "..#.............##...#.......##.........",
    "...#.#.........#.......................#",
    "..#...#..#...................#...#......",
    ".........#.....................#..#.....",
    "#...##..#...............#.#....##.#.##..",
    "#..#.........#...............##...#....#",
    "#................#.......#.......#..#.#.",
    "...#...#....#........#.........###....##"
]

TEST_CASES = [
    ("Sample", SAMPLE_GRID),
    ("Min_Rocks", generate_grid(N * N // 10)),
    ("Max_Rocks", generate_grid(N * N // 4)),
]

def run_all_tests():
    results = []
    start_time = time.time()
    for name, grid in TEST_CASES:
        ok, msg = run_test_case(name, grid)
        results.append((ok, msg))
    end_time = time.time()
    print("Test Results:")
    for ok, msg in results:
        print(f"{'✓' if ok else '✗'} {msg}")
    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    print(f"Overall: {'PASSED' if all(ok for ok, _ in results) else 'FAILED'}")

if __name__ == "__main__":
    run_all_tests() 