import subprocess
import sys
import os

def run_solution(input_str):
    proc = subprocess.Popen([
        'pypy3.10', 'C_Smilo_and_Minecraft.py'
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate(input=input_str.encode())
    return out.decode().strip(), err.decode().strip()

def test_sample_cases():
    cases = [
        # Official samples from the statement
        ("3\n2 3 1\n#.#\ng.g\n2 3 2\n#.#\ng.g\n3 4 2\n.gg.\ng..#\ng##.\n", "2\n0\n4"),
    ]
    for idx, (inp, expected) in enumerate(cases):
        out, err = run_solution(inp)
        print(f"Sample Test {idx+1}:", "✓" if out == expected else f"✗ (got {out!r})")
        assert out == expected

def test_edge_cases():
    # All gold on the boundary can be collected in a single explosion
    inp = "1\n3 3 1\nggg\ng.g\nggg\n"
    expected = "8"
    out, err = run_solution(inp)
    print("Edge Test 1 (all gold on boundary):", "✓" if out == expected else f"✗ (got {out!r})")
    assert out == expected
    # k very large — no gold can be on the boundary of any explosion
    inp = "1\n5 5 10\n.....\n.ggg.\n.ggg.\n.ggg.\n.....\n"
    expected = "0"
    out, err = run_solution(inp)
    print("Edge Test 2 (large k, all gold inside):", "✓" if out == expected else f"✗ (got {out!r})")
    assert out == expected

def test_stress():
    # Large random grid, just check it runs
    n, m, k = 100, 100, 10
    grid = ["."*m for _ in range(n)]
    inp = f"1\n{n} {m} {k}\n" + "\n".join(grid) + "\n"
    out, err = run_solution(inp)
    print("Stress Test (empty grid):", "✓" if out.isdigit() else f"✗ (got {out!r})")

def main():
    test_sample_cases()
    test_edge_cases()
    test_stress()
    print("All tests completed.")

if __name__ == "__main__":
    main() 