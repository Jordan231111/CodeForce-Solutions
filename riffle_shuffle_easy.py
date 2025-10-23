# input
import sys
input = sys.stdin.readline
II = lambda : int(input())
MI = lambda : map(int, input().split())
LI = lambda : [int(a) for a in input().split()]
SI = lambda : input().rstrip()
LLI = lambda n : [[int(a) for a in input().split()] for _ in range(n)]
LSI = lambda n : [input().rstrip() for _ in range(n)]
MI_1 = lambda : map(lambda x:int(x)-1, input().split())
LI_1 = lambda : [int(a)-1 for a in input().split()]

mod = 998244353
inf = 1001001001001001001
ordalp = lambda s : ord(s)-65 if s.isupper() else ord(s)-97
ordallalp = lambda s : ord(s)-39 if s.isupper() else ord(s)-97
yes = lambda : print("Yes")
no = lambda : print("No")
yn = lambda flag : print("Yes" if flag else "No")

def acc(a:list[int]):
    sa = [0]*(len(a)+1)
    for i in range(len(a)):
        sa[i+1] = a[i] + sa[i]
    return sa

prinf = lambda ans : print(ans if ans < 1000001001001001001 else -1)
alplow = "abcdefghijklmnopqrstuvwxyz"
alpup = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alpall = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
URDL = {'U':(-1,0), 'R':(0,1), 'D':(1,0), 'L':(0,-1)}
DIR_4 = [[-1,0],[0,1],[1,0],[0,-1]]
DIR_8 = [[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]]
DIR_BISHOP = [[-1,1],[1,1],[1,-1],[-1,-1]]
prime60 = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59]
sys.set_int_max_str_digits(0)

# Precompute factorials up to 3005 (n <= 3000)
MAXN = 3005
fac = [1]*MAXN
ifac = [1]*MAXN
for i in range(1, MAXN):
    fac[i] = fac[i-1]*i % mod
# Fermat inverse factorials
ifac[-1] = pow(fac[-1], mod-2, mod)
for i in range(MAXN-2, -1, -1):
    ifac[i] = ifac[i+1]*(i+1) % mod

def nCr(n:int, r:int) -> int:
    if r < 0 or r > n or n < 0:
        return 0
    return fac[n]*ifac[r] % mod * ifac[n-r] % mod

def count_for_k(n:int, p:list[int], k:int, enforce_k_anchor:bool) -> int:
    res = 1
    prev_i = 0
    prev_a = 0
    seg_forcedA = 0
    seg_forcedB = 0
    # process positions 1..n, triggering anchors at known positions
    for i in range(1, n+1):
        v = p[i-1]
        if v != -1:
            if v <= k:
                seg_forcedA += 1
                a = v
            else:
                seg_forcedB += 1
                a = i - (v - k)
            if a < 0 or a > i:
                return 0
            di = i - prev_i
            da = a - prev_a
            if da < 0 or da > di:
                return 0
            free = di - seg_forcedA - seg_forcedB
            need = da - seg_forcedA
            if need < 0 or need > free:
                return 0
            res = (res * nCr(free, need)) % mod
            prev_i = i
            prev_a = a
            seg_forcedA = 0
            seg_forcedB = 0
        # optional anchor at i == k
        if enforce_k_anchor and i == k:
            # enforce anchor (k, k)
            di = i - prev_i
            da = k - prev_a
            if da < 0 or da > di:
                return 0
            free = di - seg_forcedA - seg_forcedB
            need = da - seg_forcedA
            if need < 0 or need > free:
                return 0
            res = (res * nCr(free, need)) % mod
            prev_i = i
            prev_a = k
            seg_forcedA = 0
            seg_forcedB = 0
    # final anchor at (n, k)
    di = n - prev_i
    da = k - prev_a
    if da < 0 or da > di:
        return 0
    free = di - seg_forcedA - seg_forcedB
    need = da - seg_forcedA
    if need < 0 or need > free:
        return 0
    res = (res * nCr(free, need)) % mod
    return res

def solve():
    t = II()
    out_lines = []
    for _ in range(t):
        n = II()
        p = LI()
        ok_id = 1
        for i in range(n):
            if p[i] != -1 and p[i] != i+1:
                ok_id = 0
                break
        ans = 0
        for k in range(1, n):
            f = count_for_k(n, p, k, False)
            g = count_for_k(n, p, k, True)
            ans += f - g
            if ans >= mod:
                ans -= mod
            if ans < 0:
                ans += mod
        if ok_id:
            ans += 1
            if ans >= mod:
                ans -= mod
        out_lines.append(str(ans % mod))
    print("\n".join(out_lines))

if __name__ == "__main__":
    solve()
