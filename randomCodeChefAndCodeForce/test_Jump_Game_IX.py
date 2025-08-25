import subprocess
import sys
import time
import random

def brute(a):
    n = len(a)
    g = [[] for _ in range(n)]
    for i in range(n):
        ai = a[i]
        for j in range(i+1, n):
            if ai > a[j]:
                g[i].append(j)
                g[j].append(i)
    seen = [False]*n
    ans = [0]*n
    for i in range(n):
        if not seen[i]:
            st=[i]; seen[i]=True; comp=[]; mx=a[i]
            while st:
                u=st.pop()
                comp.append(u)
                vu=a[u]
                if vu>mx:
                    mx=vu
                for v in g[u]:
                    if not seen[v]:
                        seen[v]=True
                        st.append(v)
            for v in comp:
                ans[v]=mx
    return ans

def run_case(a):
    t_in = "1\n{}\n{}\n".format(len(a), " ".join(map(str,a)))
    proc = subprocess.Popen(
        ["pypy3.10", "Jump_Game_IX.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    out, err = proc.communicate(t_in)
    if proc.returncode != 0:
        return False, f"Runtime error: {err}"
    fast = list(map(int, out.strip().split()))
    brute_ans = brute(a)
    ok = fast == brute_ans
    if not ok:
        return False, f"Mismatch\nnums={a}\nfast={fast}\nbrut={brute_ans}"
    return True, "ok"

def run_all_tests():
    samples = [
        [2,1,3],
        [2,3,1],
        [1,1,1,1],
        [5,4,3,2,1],
        [1,2,3,4,5],
    ]
    results = []
    start = time.time()
    for a in samples:
        results.append(run_case(a))
    for _ in range(200):
        n=random.randint(1,50)
        a=[random.randint(0,20) for _ in range(n)]
        results.append(run_case(a))
    end = time.time()
    all_passed = all(ok for ok,_ in results)
    print("Test Results:")
    for ok,msg in results:
        print(("\u2713" if ok else "\u2717"), msg)
    print(f"\nExecution time: {end-start:.4f} seconds")
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")

if __name__ == "__main__":
    run_all_tests()


