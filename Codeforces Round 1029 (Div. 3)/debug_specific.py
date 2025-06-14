#!/usr/bin/env pypy3
from e_lost_soul import solve_case, MaskTable, BIT_MAP, GOOD_TABLE

# Test case #1 that's failing
a = [2, 1, 5, 3, 6, 4]
b = [3, 2, 4, 5, 1, 6]
n = len(a)
expected = 3

print(f"Debugging test case #1: n={n}")
print(f"a = {a}")
print(f"b = {b}")

# Initialize structures for our implementation
good_orig_flag = [False] * n
suf_tog_cnt = [0] * (n + 1)

# Initialize mask tables
table_orig = MaskTable()
table_tog = MaskTable()

print("\nStep by step debug:")
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
    good_orig = table_orig.good(parity_idx)
    good_orig_flag[idx] = good_orig
    
    # Check toggled world
    toggled_good = table_tog.good(parity_idx ^ 1)
    if toggled_good:
        toggled_running_cnt += 1
        
    suf_tog_cnt[idx] = toggled_running_cnt
    
    print(f"  good_orig_flag[{idx}]={good_orig_flag[idx]}")
    print(f"  toggled_good={toggled_good}, toggled_running_cnt={toggled_running_cnt}")
    print(f"  table_orig masks: {table_orig.masks}")
    print(f"  table_tog masks: {table_tog.masks}")
    
    # Debug: Check if the mask table has correct good counts
    print(f"  table_orig.good_even={table_orig.good_even}, table_orig.good_odd={table_orig.good_odd}")
    print(f"  table_tog.good_even={table_tog.good_even}, table_tog.good_odd={table_tog.good_odd}")
    
    # Check the bit patterns more in depth
    print("  Original table mask analysis:")
    for val, mask in table_orig.masks.items():
        print(f"    Value {val}: mask={bin(mask)}, good for even={GOOD_TABLE[0][mask]}, good for odd={GOOD_TABLE[1][mask]}")
    
    print("  Toggled table mask analysis:")
    for val, mask in table_tog.masks.items():
        print(f"    Value {val}: mask={bin(mask)}, good for even={GOOD_TABLE[0][mask]}, good for odd={GOOD_TABLE[1][mask]}")

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

# Run the simpler implementation for comparison
def debug_solve_case(n, a, b):
    # 1. No-deletion case
    best_no_del = 0
    for i in range(n):
        if a[i] == b[i]:
            best_no_del = max(best_no_del, i + 1)
    for i in range(n - 1):
        if a[i] == a[i + 1] or b[i] == b[i + 1]:
            best_no_del = max(best_no_del, i + 1)

    # 2. Single-deletion case
    seen_a = set()
    seen_b = set()
    best_with_del = 0

    for j in range(n - 2, -1, -1):
        if (a[j] in seen_a) or (a[j] in seen_b) or (b[j] in seen_a) or (b[j] in seen_b):
            best_with_del = max(best_with_del, j + 1)

        seen_a.add(a[j + 1])
        seen_b.add(b[j + 1])

    print("\nSimple implementation details:")
    print(f"best_no_del = {best_no_del}")
    print(f"best_with_del = {best_with_del}")
    return max(best_no_del, best_with_del)

simple_result = debug_solve_case(n, a, b)
print(f"Simple implementation answer: {simple_result}") 