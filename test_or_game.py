import subprocess

sample_input = """4
3
3 4 6
3
7 7 7
3
9 3 5
10
1 9 1 3 7 9 10 9 7 3
"""

expected_output = """Alice
Bob
Bob
Alice
"""

proc = subprocess.Popen([
    "python3", "or_game.py"
], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

out, err = proc.communicate(sample_input)
print(out)
assert out == expected_output, f"Mismatch:\n{out}\n!=\n{expected_output}"



