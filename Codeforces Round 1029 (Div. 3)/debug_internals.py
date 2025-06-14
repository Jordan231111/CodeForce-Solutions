from e_lost_soul import solve_case, MaskTable, BIT_MAP, GOOD_TABLE

a=[2,1,5,3,6,4]
b=[3,2,4,5,1,6]
print('ans',solve_case(len(a),a,b))

n=len(a)

# replicate internals

good_orig=[0]*n
suf_tog=[0]*(n+2)

to=MaskTable(); tt=MaskTable(); toggcnt=0
for idx in range(n-1,-1,-1):
    par_even=(idx%2==1)
    parity_bit=0 if par_even else 1
    t_parity=parity_bit^1
    to.add_bit(a[idx], BIT_MAP[0][parity_bit])
    tt.add_bit(a[idx], BIT_MAP[0][t_parity])
    to.add_bit(b[idx], BIT_MAP[1][parity_bit])
    tt.add_bit(b[idx], BIT_MAP[1][t_parity])
    parity_idx=0 if par_even else 1
    good_orig[idx]=1 if to.good(parity_idx) else 0
    if tt.good(parity_idx^1):
        toggcnt+=1
    suf_tog[idx]=toggcnt
print('good_orig',good_orig)
print('suf_tog',suf_tog[:-1])

pref=[0]*(n+1)
for i in range(n):
    pref[i+1]=pref[i]+good_orig[i]
print('pref',pref)
for k in range(n+1):
    cand=pref[k]+suf_tog[k] if k<n else pref[k]
    print('k',k,'cand',cand) 