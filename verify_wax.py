import sys

def parse_case(inp:str):
    it = iter(inp.strip().splitlines())
    N,M,K = map(int, next(it).split())
    robots = [tuple(map(int, next(it).split())) for _ in range(M)]
    v = [next(it).strip() for _ in range(N)]
    h = [next(it).strip() for _ in range(N-1)]
    return N,M,K,robots,v,h

def run_solver(case:str):
    import subprocess
    p = subprocess.Popen(
        ["pypy3.10","Waxing_Robots.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    out, err = p.communicate(case)
    return out

def simulate(N,M,K,robots,v,h,assignment_lines,presses):
    grid_vis = [[False]*N for _ in range(N)]
    pos = [list(r) for r in robots]
    for r,c in pos:
        grid_vis[r][c] = True
    dr = [-1,1,0,0]
    dc = [0,0,-1,1]
    for a in presses:
        a = int(a)
        if not (0 <= a < K):
            raise ValueError("invalid button")
        for m in range(M):
            cmd = assignment_lines[a][m]
            if cmd == 'S':
                continue
            d = {'U':0,'D':1,'L':2,'R':3}[cmd]
            r,c = pos[m]
            nr, nc = r + dr[d], c + dc[d]
            if nr < 0 or nr >= N or nc < 0 or nc >= N:
                nr, nc = r, c
            else:
                if d == 0 and h[r-1][c] == '1':
                    nr, nc = r, c
                elif d == 1 and h[r][c] == '1':
                    nr, nc = r, c
                elif d == 2 and v[r][c-1] == '1':
                    nr, nc = r, c
                elif d == 3 and v[r][c] == '1':
                    nr, nc = r, c
            pos[m] = [nr, nc]
            grid_vis[nr][nc] = True
    R = sum(not x for row in grid_vis for x in row)
    return R

if __name__ == "__main__":
    with open("case_wax.txt","r") as f:
        case = f.read()
    N,M,K,robots,v,h = parse_case(case)
    out = run_solver(case)
    lines = out.strip().splitlines()
    assign = lines[:K]
    presses = lines[K:]
    R = simulate(N,M,K,robots,v,h,assign,presses)
    print("R=", R, "T=", len(presses))


