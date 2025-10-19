import subprocess, textwrap

CPP_SOURCE = "rect_min_area.cpp"
BIN = "rect_min_area"

sample_input = textwrap.dedent(
    """
    3
    3 5
    10101
    10100
    00101
    4 6
    011101
    010001
    100010
    101110
    5 5
    11100
    10110
    11111
    01101
    00111
    """
).strip()+"\n"

expected_output = textwrap.dedent(
    """
    6 6 6 9 9
    6 6 6 9 9
    0 0 9 9 9

    0 10 8 8 10 10
    0 10 8 8 10 10
    10 10 8 8 10 0
    10 10 8 8 10 0

    6 6 6 0 0
    6 6 4 4 0
    6 4 4 4 6
    0 4 4 6 6
    0 0 6 6 6
    """
).strip()

def compile():
    subprocess.run(["g++-14","-std=gnu++20","-O2","-pipe",CPP_SOURCE,"-o",BIN], check=True)

def run():
    proc = subprocess.Popen([f"./{BIN}"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    out,_ = proc.communicate(sample_input)
    print(out.strip())
    print("\nExpected:\n"+expected_output)

if __name__ == "__main__":
    compile()
    run()


