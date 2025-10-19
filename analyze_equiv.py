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
    if not any(True for _ in legal_moves(a, alice)):
        return True
    for L,R in legal_moves(a, alice):
        b=a[:L]+a[R+1:]
        if not win_state(tuple(b), not alice):
            return True
    return False


def equiv(max_n=8):
    for n in range(1,max_n+1):
        ok=0
        tot=0
        bad=[]
        for arr in product([-1,1], repeat=n):
            if 1 not in arr:
                continue
            blose = not win_state(tuple(arr), False)
            rule = (arr[0]==-1 and arr[-1]==-1)
            if blose==rule:
                ok+=1
            else:
                bad.append((arr,blose,rule))
            tot+=1
        print('n=',n,'ok',ok,'/' ,tot)
        if bad:
            print('counterexamples:', bad[:3])
            break

if __name__=='__main__':
    equiv(9)
