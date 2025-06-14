import subprocess, textwrap, os, sys

SAMPLE_INPUT = textwrap.dedent(
    """\
    7
    2
    1 2
    8
    1 2
    2 3
    3 8
    2 4
    4 5
    5 6
    6 7
    10
    1 2
    2 3
    3 4
    4 5
    5 6
    4 7
    7 8
    4 9
    9 10
    7
    1 4
    4 2
    3 2
    3 5
    2 6
    6 7
    7
    1 2
    2 3
    3 4
    3 5
    4 6
    6 7
    7
    5 7
    4 6
    1 6
    1 3
    2 6
    6 7
    5
    3 4
    1 2
    1 3
    2 5
    """
)

EXPECTED_OUTPUT = textwrap.dedent(
    """\
    4
    24
    0
    16
    48
    0
    4
    """
)


def run_case(input_data: str) -> str:
    """Run F_Wildflower.py via PyPy3 inside a subprocess and capture stdout."""
    proc = subprocess.run(
        [sys.executable, "F_Wildflower.py"],
        input=input_data.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return proc.stdout.decode().strip()


def main():
    out = run_case(SAMPLE_INPUT).strip()
    exp = EXPECTED_OUTPUT.strip()
    print("Sample status:", "✓" if out == exp else "✗")
    if out != exp:
        print("--- expected --\n" + exp + "\n--- got --\n" + out)
        sys.exit(1)
    # quick custom sanity cases
    edge1 = "1\n1\n"  # single node
    assert run_case(edge1).strip() == "2"
    edge2_n = 5
    # path 1-2-3-4-5 (root at 1)
    path_input = "1\n" + str(edge2_n) + "\n" + "\n".join(f"{i} {i+1}" for i in range(1, edge2_n)) + "\n"
    expected = pow(2, edge2_n, 1_000_000_007)
    assert int(run_case(path_input).strip()) == expected
    print("Edge cases ✓")


if __name__ == "__main__":
    main() 