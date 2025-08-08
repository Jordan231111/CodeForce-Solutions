import subprocess, sys

def brute(n, x, s):
    inp = f"1\n{n} {x}\n{s}\n"
    proc = subprocess.Popen([
        "python3", "brute_B_Hamiiid_Haaamid_Hamid.py"
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = proc.communicate(inp)
    if proc.returncode != 0:
        raise RuntimeError(err)
    return int(out.strip())

def features(n, x, s):
    left = s[:x-1]
    right = s[x:]
    hasL = ('#' in left)
    hasR = ('#' in right)
    # distance to nearest wall; big if none
    dL = 10**9
    for i in range(x-2, -1, -1):
        if s[i] == '#':
            dL = (x-1) - i
            break
    dR = 10**9
    for i in range(x, n):
        if s[i] == '#':
            dR = i - (x-1)
            break
    # clear to border flags
    clearL = (dL == 10**9)
    clearR = (dR == 10**9)
    immL = (x-2 >= 0 and s[x-2] == '#')
    immR = (x < n and s[x] == '#')
    return {
        'hasL': hasL,
        'hasR': hasR,
        'dL': dL if dL != 10**9 else -1,
        'dR': dR if dR != 10**9 else -1,
        'clearL': clearL,
        'clearR': clearR,
        'immL': immL,
        'immR': immR,
    }

def main():
    max_n = 7
    stats = {}
    for n in range(2, max_n+1):
        for x in range(1, n+1):
            for bits in range(1<<n):
                s = ''.join('#' if (bits>>i)&1 else '.' for i in range(n))
                if s[x-1] == '#':
                    continue
                if s.count('.') < 2:
                    continue
                b = brute(n, x, s)
                ft = features(n, x, s)
                key = (b, ft['hasL'], ft['hasR'], ft['dL'], ft['dR'], ft['clearL'], ft['clearR'], ft['immL'], ft['immR'])
                stats[key] = stats.get(key, 0) + 1
    # Print patterns for b=2 and b=3
    print("Patterns for b=2:")
    for key, cnt in stats.items():
        if key[0] == 2:
            print(key, cnt)
    print("\nPatterns for b=3:")
    for key, cnt in stats.items():
        if key[0] == 3:
            print(key, cnt)

if __name__ == '__main__':
    main()


