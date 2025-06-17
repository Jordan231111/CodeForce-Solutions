import runpy, pathlib, os, sys

dir_path = pathlib.Path(__file__).parent / "Codeforces Round 1030 (Div. 2)"
module_path = dir_path / "F_Shifts_and_Swaps.py"
if not module_path.exists():
    sys.stderr.write(f"[stub] Target script not found: {module_path}\n")
    sys.exit(1)
runpy.run_path(os.fspath(module_path), run_name="__main__") 