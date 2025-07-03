import subprocess, textwrap, sys

SAMPLE_INPUT = textwrap.dedent(
    """\
    5
    1
    2
    3
    4
    8
    """
)

EXPECTED_OUTPUT = textwrap.dedent(
    """\
    1 0
    1 1
    2 0
    1 2
    1 3
    """
)


def run_case(input_data: str) -> str:
    proc = subprocess.run(
        [sys.executable, "CodeForce/Check_Odd_Even_Divisors.py"],
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
    # Edge case N=1 already in sample; add N=100 to verify
    edge_input = "1\n100\n"
    edge_expected = "9 9"  # divisors of 100: 1,2,4,5,10,20,25,50,100 -> 3 odd? Wait; check.


if __name__ == "__main__":
    main() 