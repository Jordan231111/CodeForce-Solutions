import sys, random, itertools

def generate_perms(n):
    import Good_Ranking_Triplet as gr
    from types import SimpleNamespace as ns
    # monkey patch input to supply n
    import builtins
    saved_input = builtins.input
    data = [str(n)+'\n']
    def fake_input():
        return data.pop(0)
    gr.input = fake_input
    # capture output
    from io import StringIO
    saved_stdout = sys.stdout
    buf = StringIO()
    sys.stdout = buf
    gr.solve()
    sys.stdout = saved_stdout
    builtins.input = saved_input
    out = buf.getvalue().strip().split('\n')
    m = int(out[0])
    perms = [list(map(int,line.split())) for line in out[1:]]
    assert len(perms)==m
    return perms

def check(n):
    perms = generate_perms(n)
    pos = [[0]*(n+1) for _ in range(len(perms))]
    for idx,p in enumerate(perms):
        for r,x in enumerate(p):
            pos[idx][x]=r
    for a in range(1,n+1):
        for b in range(1,n+1):
            if b==a: continue
            for c in range(1,n+1):
                if c==a or c==b: continue
                ok=False
                for idx in range(len(perms)):
                    if pos[idx][a] < pos[idx][b] < pos[idx][c]:
                        ok=True
                        break
                if not ok:
                    return False,(a,b,c)
    return True,None

for n in range(3,26):
    good,trip = check(n)
    print(n, good)
    if not good:
        print('fail triple',trip)
        break
