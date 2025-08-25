import subprocess, textwrap

SAMPLE = textwrap.dedent("""
5
1 1000
1
2 2
1 2
2 2
1 1
5 4
1 1 3 3 3
7 6
1 2 1 2 2 3 4
""")
EXPECTED = textwrap.dedent("""
1000
3
1
0
4518
""").strip()

proc = subprocess.Popen(["pypy3.10","Lexicographic_Matching.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = proc.communicate(SAMPLE)
print(out.strip())
