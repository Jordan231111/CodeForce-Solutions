from functools import lru_cache
from itertools import product

def legal_moves(a, alice=True):
    n=len(a)
    for L in range(n):
        s=0
        for R in range(L,n):
            s+=a[R]
            if (alice and s>=0) or ((not alice) and s<=0):
                yield (L,R)

@lru_cache(maxsize=None)
def win_state(tup, alice):
    a=list(tup)
    # terminal: no legal move -> current player wins
    has=False
    for _ in legal_moves(a, alice):
        has=True
        break
    if not has:
        return True
    # if any move leads opponent to lose, current wins
    for L,R in legal_moves(a, alice):
        b=a[:L]+a[R+1:]
        if not win_state(tuple(b), not alice):
            return True
    return False


def check_depends_on_counts(max_n=8):
    for n in range(1, max_n+1):
        stat={}
        for arr in product([-1,1], repeat=n):
            if 1 not in arr:
                continue
            key=(arr.count(1), n - arr.count(1))
            wb = win_state(tuple(arr), False)
            if key not in stat:
                stat[key]=[0,0]
            stat[key][0]+=1
            stat[key][1]+=1 if wb else 0
        print('n =', n)
        depends_only=True
        for key in sorted(stat):
            tot,win=stat[key]
            print('counts', key, 'bob_wins', f"{win}/{tot}")
            if win!=0 and win!=tot:
                depends_only=False
        print('depends_only_on_counts =', depends_only)
        print()

if __name__=='__main__':
    check_depends_on_counts(8)
