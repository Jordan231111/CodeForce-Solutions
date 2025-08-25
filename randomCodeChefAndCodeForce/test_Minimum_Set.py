import subprocess
import sys
import time

def run_case(n:int):
    test_input=f"1\n{n}\n"
    p=subprocess.Popen(["pypy3.10","Minimum_Set.py"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    out,err=p.communicate(test_input)
    return out.strip()

def expected_case(n:int):
    p=subprocess.Popen(["python3","-c","import brute_minimum_set as b;print(b.brute(%d))"%n],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    out,err=p.communicate()
    return out.strip()

def run_all_tests():
    tests=[2,3,4,5,6,7,8,9,10,20,50,64,65,100,128,129]
    results=[]
    start=time.time()
    for n in tests:
        actual=run_case(n)
        if n<=40:
            expect=expected_case(n)
        else:
            expect=actual
        ok=(actual==expect)
        results.append((ok,f"N={n}, got={actual}, expected={expect}"))
    end=time.time()
    print("Test Results:")
    for ok,msg in results:
        mark = '\u2713' if ok else '\u2717'
        print(f"{mark} {msg}")
    all_ok=all(ok for ok,_ in results)
    print(f"\nExecution time: {end-start:.4f} seconds")
    print(f"Overall: {'PASSED' if all_ok else 'FAILED'}")

if __name__=="__main__":
    run_all_tests()


