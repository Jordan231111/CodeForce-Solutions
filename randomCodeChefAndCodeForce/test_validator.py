import subprocess, random, os, sys, time, shutil

CPP_SOURCE = "solution_file.cpp"
BIN_NAME = "solution_file"
BRUTE_SOURCE = "brute.cpp"
BRUTE_BIN = "brute"

SAMPLES = [
    (3,2,[1,6,5,3,2,4], 2),
    (1,1,[1], 0),
    (4,6,[10,24,3,4,8,14,5,2,22,9,21,1,15,6,13,23,18,12,7,17,19,16,20,11],7),
]

def find_compiler():
    cand = [os.environ.get("CXX"), "g++-14", "g++-13", "g++-12", "g++-11", "g++-10", "g++"]
    for c in cand:
        if c and shutil.which(c):
            return c
    return "g++"


def compile_sources():
    cxx = find_compiler()
    subprocess.run([cxx,"-std=gnu++20","-O2","-pipe",CPP_SOURCE,"-o",BIN_NAME],check=True)
    subprocess.run([cxx,"-std=gnu++20","-O2","-pipe",BRUTE_SOURCE,"-o",BRUTE_BIN],check=True)


def run_one(n,k,p):
    s = f"{n} {k}\n"+" ".join(map(str,p))+"\n"
    out1 = subprocess.run([f"./{BIN_NAME}"],input=s,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out2 = subprocess.run([f"./{BRUTE_BIN}"],input=s,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return out1.stdout.strip(), out2.stdout.strip()


def run_samples():
    ok=True
    for n,k,p,ans in SAMPLES:
        s = f"{n} {k}\n"+" ".join(map(str,p))+"\n"
        r = subprocess.run([f"./{BIN_NAME}"],input=s,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        got = r.stdout.strip()
        exp = str(ans)
        print("Sample:", got, exp, "OK" if got==exp else "FAIL")
        ok = ok and (got==exp)
    return ok


def stress(max_n=9, trials=2000, seed=0):
    random.seed(seed)
    for _ in range(trials):
        N = random.randint(1,4)
        K = random.randint(1, max(1, max_n//max(1,N)))
        n = N*K
        n = min(n, 9)
        P = list(range(1,n+1))
        random.shuffle(P)
        s = f"{N} {K}\n"+" ".join(map(str,P))+"\n"
        a = subprocess.run([f"./{BIN_NAME}"],input=s,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        b = subprocess.run([f"./{BRUTE_BIN}"],input=s,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if a.stdout.strip()!=b.stdout.strip():
            print("Mismatch!\nInput:\n"+s)
            print("Solution:", a.stdout)
            print("Brute:", b.stdout)
            return False
    print("Stress passed", trials, "cases")
    return True

if __name__ == "__main__":
    compile_sources()
    run_samples()
    stress()
