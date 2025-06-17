import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
SOLVER = ROOT_DIR / "F_Shifts_and_Swaps.py"
PYTHON_EXEC = sys.executable  # assumes tests run with same interpreter (PyPy3.10 in contest env)

def run_case(inp: str) -> str:
    """Run the solver as a subprocess, return stdout."""
    proc = subprocess.run(
        [PYTHON_EXEC, str(SOLVER)],
        input=inp.encode(),
        stdout=subprocess.PIPE,
        check=True,
    )
    return proc.stdout.decode().strip()


# ---------------------------------------------------------------------------
# Custom test cases (edge / boundary examples)
# ---------------------------------------------------------------------------


def test_custom_edges() -> None:
    """Run three hand-crafted edge/boundary cases."""

    # Test-1: Simple rotation should be possible.
    case1 = """1\n4 2\n1 2 1 2\n2 1 2 1\n"""
    assert run_case(case1) == "YES"

    # Test-2: Order constraint forbids rearrangement (difference = 1 cannot cross)
    case2 = """1\n4 2\n1 2 1 2\n1 1 2 2\n"""
    assert run_case(case2) == "NO"

    # Test-3: Mismatched counts immediately impossible.
    case3 = """1\n2 2\n1 2\n1 1\n"""
    assert run_case(case3) == "NO"


if __name__ == "__main__":
    test_custom_edges()
    print("All custom edge tests passed.") 