#!/usr/bin/env python3
from e_lost_soul import solve_case, MaskTable, BIT_MAP

a=[2,1,5,3,6,4]
b=[3,2,4,5,1,6]
n=len(a)
print('solve', solve_case(n,a,b))

good_orig_flag=[0]*n
suf_tog_cnt=[0]*(n+2)

table_orig=MaskTable(); table_tog=MaskTable(); toggled_running_cnt=0
for idx in range(n-1,-1,-1):
    par_even=(idx%2==1)
    parity_bit=0 if par_even else 1
    toggled_parity_bit=parity_bit^1
    table_orig.add_bit(a[idx], BIT_MAP[0][parity_bit])
    table_tog.add_bit(a[idx], BIT_MAP[0][toggled_parity_bit])
    table_orig.add_bit(b[idx], BIT_MAP[1][parity_bit])
    table_tog.add_bit(b[idx], BIT_MAP[1][toggled_parity_bit])
    parity_idx=0 if par_even else 1
    good_orig_flag[idx]=1 if table_orig.good(parity_idx) else 0
    if table_tog.good(parity_idx^1):
        toggled_running_cnt+=1
    suf_tog_cnt[idx]=toggled_running_cnt

print('good_orig_flag', good_orig_flag)
prefix=[0]
for i in range(n):
    prefix.append(prefix[-1]+good_orig_flag[i])
print('prefix', prefix)
print('suf_tog_cnt', suf_tog_cnt)

# Print table_tog.good values at each idx for debug
table_orig=MaskTable(); table_tog=MaskTable();
print('toggle_good_idx_based:')
toggled_good=[None]*n
for idx in range(n-1,-1,-1):
    par_even=(idx%2==1)
    parity_bit=0 if par_even else 1
    toggled_parity_bit=parity_bit^1
    table_tog.add_bit(a[idx], BIT_MAP[0][toggled_parity_bit])
    table_tog.add_bit(b[idx], BIT_MAP[1][toggled_parity_bit])
    parity_idx=0 if par_even else 1
    toggled_good[idx]=table_tog.good(parity_idx^1)
print('toggled_good', toggled_good) 