import subprocess, textwrap, os, sys

def run_solution(inp: str) -> str:
    """Helper: run the user's solution using pypy3 and return stdout text."""
    # Assumes this test is in the project root and PyPy is available as `pypy3`
    proc = subprocess.run(
        ["python3", "E_Grid_Coloring.py"],
        input=inp.encode(),
        stdout=subprocess.PIPE,
        check=True,
    )
    return proc.stdout.decode().strip()

def test_sample_cases():
    sample_input = textwrap.dedent(
        """\
        3
        3 3
        1 1
        1 5
        """
    )
    # The sample contains three test cases: 3×3, 1×1 and 1×5 grids.
    # We do **not** require the program to reproduce the statement's example
    # order verbatim – many valid colourings exist – but we DO verify that the
    # produced order is valid for the problem constraints:
    #   1. Exactly n·m coordinates per test case, all distinct & within bounds
    #   2. While colouring in the given order no already coloured cell ever has
    #      more than three coloured 4-neighbours.
    out = run_solution(sample_input)

    # Helper to walk through one test case and validate constraints
    def verify_case(n: int, m: int, coords):
        assert len(coords) == n * m, "wrong number of coordinates"
        seen = set()
        coloured = set()

        dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))  # 4-neighbour directions

        for r, c in coords:
            # Check invariant **before** colouring the next cell
            for pr, pc in coloured:
                cnt = sum(((pr + dr, pc + dc) in coloured) for dr, dc in dirs)
                assert cnt <= 3, "A cell exceeded 3 coloured neighbours"

            # bounds & uniqueness of upcoming cell
            assert 1 <= r <= n and 1 <= c <= m, "coordinate out of bounds"
            assert (r, c) not in seen, "duplicate coordinate"

            seen.add((r, c))
            coloured.add((r, c))

    parts = list(map(int, out.strip().split()))
    ptr = 0

    # -- first test: 3×3 --
    n, m = 3, 3
    coords = [(parts[ptr + 2 * i], parts[ptr + 2 * i + 1]) for i in range(n * m)]
    verify_case(n, m, coords)
    ptr += 2 * n * m

    # Empty line separator may or may not be present – skip all zero-length
    # tokens (produced by splitlines on blank lines)

    # -- second test: 1×1 --
    n, m = 1, 1
    coords = [(parts[ptr], parts[ptr + 1])]
    verify_case(n, m, coords)
    ptr += 2

    # -- third test: 1×5 --
    n, m = 1, 5
    coords = [(parts[ptr + 2 * i], parts[ptr + 2 * i + 1]) for i in range(n * m)]
    verify_case(n, m, coords)

if __name__ == "__main__":
    test_sample_cases()
    print("All sample-case checks passed.") 