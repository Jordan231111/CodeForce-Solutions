from functools import lru_cache


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
    # terminal: no legal move => current player wins immediately
    for _ in legal_moves(a, alice):
        break
    else:
        return True
    # otherwise, can current player force win?
    for L,R in legal_moves(a, alice):
        b=a[:L]+a[R+1:]
        if not win_state(tuple(b), not alice):
            return True
    return False


def winning_first_moves(a):
    res=[]
    for L,R in legal_moves(a, True):
        b=a[:L]+a[R+1:]
        if not win_state(tuple(b), False):
            res.append((L,R))
    return res


def count_winning_first_moves(a):
    return len(winning_first_moves(a))

if __name__=='__main__':
    cases=[
        [1,-1,1,-1],
        [1,1,1],
        [-1,1,1,-1,1],
        [-1,1,-1],
        [1],
        [1,-1,-1,-1],
        [1,-1]
    ]
    for c in cases:
        w=winning_first_moves(c)
        print(c, len(w), w)
