#!/usr/bin/env pypy3
import sys
data = sys.stdin.buffer.read().split()
t = int(data[0])
ptr = 1
out = []
for _ in range(t):
    # read n, s
    n = int(data[ptr]); ptr += 1
    s = data[ptr].decode(); ptr += 1
    # count frequencies
    cnt = [0]*26
    for ch in s:
        cnt[ord(ch)-97] += 1

    ok = False
    # we only need to scan 1..n-2 (0-based)
    for i in range(1, n-1):
        if cnt[ord(s[i]) - 97] > 1:
            ok = True
            break
    out.append("Yes" if ok else "No")
sys.stdout.write("\n".join(out))
