import subprocess, sys, os, textwrap, pathlib, shutil


def run_solution(input_data: str) -> str:
    # Prefer PyPy for performance, fall back to current interpreter if unavailable.
    interpreter = shutil.which("pypy3.10") or sys.executable
    proc = subprocess.run(
        [interpreter, os.fspath(pathlib.Path(__file__).with_name("E_From_Kazan_with_Love.py"))],
        input=input_data.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"Solution exited with code {proc.returncode}. Stderr: {proc.stderr.decode()}")
    return proc.stdout.decode().strip()


def test_sample():
    sample_input = textwrap.dedent(
        """\
        5
        4 1 1 4
        1 2
        2 3
        3 4
        4 1
        5 1 1 5
        1 2
        2 3
        3 4
        4 5
        5 1
        9 2 1 9
        1 2
        2 3
        3 4
        3 5
        5 6
        6 7
        6 8
        8 9
        9 1
        7 1
        9 2 7 2
        1 4
        2 5
        3 6
        4 5
        5 6
        4 7
        5 8
        6 9
        2 8
        3 7
        3 2 1 3
        1 2
        2 3
        2 1
        3 1
        """.strip()
    )
    expected_output = textwrap.dedent(
        """\
        4
        6
        10
        5
        -1"""
    ).strip()
    actual_output = run_solution(sample_input)
    # Compare token-wise to ignore harmless trailing spaces/newlines.
    assert actual_output.split() == expected_output.split(), (
        f"Mismatch:\nExpected -> {expected_output!r}\nGot      -> {actual_output!r}"
    )


if __name__ == "__main__":
    test_sample()
    print("Sample test passed!") 