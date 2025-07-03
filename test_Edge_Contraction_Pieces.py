import subprocess, textwrap, sys, os, pathlib

def run_io(input_str: str) -> str:
    proc = subprocess.Popen(
        [sys.executable, pathlib.Path(__file__).with_name("Edge_Contraction_Pieces.py")],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    out, err = proc.communicate(input_str)
    if err:
        raise RuntimeError(err)
    return out.strip()

def test_sample():
    sample_input = textwrap.dedent(
        """\
        7 7
        1 2
        1 3
        2 3
        1 4
        1 5
        2 5
        6 7
        5
        1 2 3 1 5
        """
    )
    expected = textwrap.dedent(
        """\
        4
        3
        3
        3
        2
        """
    ).strip()
    assert run_io(sample_input) == expected

if __name__ == "__main__":
    test_sample()
    print("Passed") 