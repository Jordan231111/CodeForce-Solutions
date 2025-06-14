#!/usr/bin/env pypy3
from e_lost_soul import solve_case, MaskTable, BIT_MAP, GOOD_TABLE

# First test case from the sample
a = [1, 3, 1, 4]
b = [4, 3, 2, 2]
n = len(a)
expected = 3

# Initialize the structures
good_orig_flag = [False] * n
suf_tog_cnt = [0] * (n + 1)

# Initialize mask tables
table_orig = MaskTable()
table_tog = MaskTable()

print("Step by step debug:")
# Scan from right to left
toggled_running_cnt = 0
for idx in range(n - 1, -1, -1):
    print(f"\nIndex {idx}:")
    # Calculate parities
    par_even = (idx % 2 == 1)
    parity_bit = 0 if par_even else 1
    toggled_parity_bit = parity_bit ^ 1
    
    print(f"  par_even={par_even}, parity_bit={parity_bit}, toggled_parity_bit={toggled_parity_bit}")
    print(f"  a[idx]={a[idx]}, b[idx]={b[idx]}")
    
    # Update both tables
    table_orig.add_bit(a[idx], BIT_MAP[0][parity_bit])
    table_orig.add_bit(b[idx], BIT_MAP[1][parity_bit])
    
    table_tog.add_bit(a[idx], BIT_MAP[0][toggled_parity_bit])
    table_tog.add_bit(b[idx], BIT_MAP[1][toggled_parity_bit])
    
    # Check original world
    parity_idx = 0 if par_even else 1
    good_orig_flag[idx] = table_orig.good(parity_idx)
    
    # Check toggled world
    if table_tog.good(parity_idx ^ 1):
        toggled_running_cnt += 1
        
    suf_tog_cnt[idx] = toggled_running_cnt
    
    print(f"  good_orig_flag[{idx}]={good_orig_flag[idx]}")
    print(f"  toggled_running_cnt={toggled_running_cnt}, suf_tog_cnt[{idx}]={suf_tog_cnt[idx]}")
    print(f"  table_orig masks: {table_orig.masks}")
    print(f"  table_tog masks: {table_tog.masks}")

# Build prefix sum
prefix_sum = [0] * (n + 1)
for i in range(n):
    prefix_sum[i + 1] = prefix_sum[i] + (1 if good_orig_flag[i] else 0)

print("\nFinal structures:")
print(f"good_orig_flag: {good_orig_flag}")
print(f"prefix_sum: {prefix_sum}")
print(f"suf_tog_cnt: {suf_tog_cnt}")

# Try all deletion positions
best_ans = prefix_sum[n]  # No deletion case
print(f"\nNo deletion case: {best_ans}")

for k in range(n):
    current_ans = prefix_sum[k] + suf_tog_cnt[k + 1]
    print(f"Delete at {k}: prefix_sum[{k}]={prefix_sum[k]} + suf_tog_cnt[{k+1}]={suf_tog_cnt[k+1]} = {current_ans}")
    best_ans = max(best_ans, current_ans)

print(f"Final answer: {best_ans}, Expected: {expected}") 