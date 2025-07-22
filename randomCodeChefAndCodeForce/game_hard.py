
import sys
import os
import io

input = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline

II = lambda : int(input())
MI = lambda : map(int, input().split())
LI = lambda : [int(a) for a in input().split()]

T = II()
for _ in range(T):
    N = II()
    A = LI()
    B = sorted(A, reverse=True)
    prefix = [0] * (N + 1)
    for i in range(1, N + 1):
        prefix[i] = prefix[i - 1] + B[i - 1]
    full_s = [0] * (N + 1)
    for m in range(1, N + 1):
        full_s[m] = prefix[m] + m * (m - 1) // 2

    ans_list = []
    for K in range(1, 2 * N + 1):
        max1 = full_s[min(K // 2, N)]
        low = K // 2 + 1
        high = min(K, N)
        max2 = 0
        if low <= high:
            l = low
            r = high - 1
            res = -1
            while l <= r:
                mid = (l + r) // 2
                delt = B[mid] + 2 * K - 3 * mid - 1
                if delt >= 0:
                    res = mid
                    l = mid + 1
                else:
                    r = mid - 1
            if res != -1:
                peak = res + 1
            else:
                peak = low
            t = K - peak
            extra = t * (2 * peak - t - 1) // 2
            max2 = prefix[peak] + extra
        current_ans = max(max1, max2)
        ans_list.append(current_ans)
    print(' '.join(map(str, ans_list))) 