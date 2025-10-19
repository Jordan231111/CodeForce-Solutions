import itertools

def medians_of_all_subarrays(arr):
    n = len(arr)
    meds = set()
    for L in range(n):
        for R in range(L+1, n):  # length > 1
            b = sorted(arr[L:R+1])
            k = (len(b)+1)//2 - 1
            meds.add(b[k])
    return meds

def medians_of_pairs_triples(arr):
    n = len(arr)
    meds = set()
    for i in range(n-1):
        a,b = arr[i], arr[i+1]
        meds.add(min(a,b))
    for i in range(n-2):
        a,b,c = arr[i], arr[i+1], arr[i+2]
        s = sorted((a,b,c))
        meds.add(s[1])
    return meds

def feasible_values_by_center(arr):
    n = len(arr)
    pos = {v:i for i,v in enumerate(arr)}
    res = set()
    for v,c in pos.items():
        L = c-1
        R = c+1
        less = 0
        greater = 0
        # expand outward and track diff; stop if bounds exceeded
        # pick side greedily by nearer index
        while L >= 0 or R < n:
            # check current window if length>1
            if (less+greater) > 0:
                if greater - less in (0,1):
                    res.add(v)
                    break
            # choose closer side
            dl = abs(c-L) if L>=0 else 10**9
            dr = abs(R-c) if R<n else 10**9
            if dl <= dr:
                if arr[L] < v:
                    less += 1
                else:
                    greater += 1
                L -= 1
            else:
                if arr[R] < v:
                    less += 1
                else:
                    greater += 1
                R += 1
    return res

def brute_prefix_counts(p):
    n = len(p)
    out = []
    for i in range(1, n+1):
        meds = medians_of_all_subarrays(p[:i])
        out.append(len(meds))
    return out

def test_small(n=6, limit=2000):
    import random
    cnt = 0
    while cnt < limit:
        arr = list(range(1, n+1))
        random.shuffle(arr)
        # compare feasible via simple local rules vs brute
        brute = medians_of_all_subarrays(arr)
        # nearest-greater distance <=1 rule
        local2 = set()
        pos = {v:i for i,v in enumerate(arr)}
        n = len(arr)
        for v in range(1, n+1):
            i = pos[v]
            # nearest greater to left distance
            dl = None
            for j in range(i-1, -1, -1):
                if arr[j] > v:
                    dl = i - j - 1
                    break
            dr = None
            for j in range(i+1, n):
                if arr[j] > v:
                    dr = j - i - 1
                    break
            ok = False
            if dl is not None and dl <= 1:
                ok = True
            if dr is not None and dr <= 1:
                ok = True
            if ok:
                local2.add(v)
        if local2 != brute:
            print("Counterexample to d<=1 rule:", arr)
            print("Brute:", sorted(brute))
            print("Rule:", sorted(local2))
            return False
        cnt += 1
    print("No counterexample found in", limit, "random cases of n=", n)
    return True

if __name__ == "__main__":
    # Check one-sided sufficiency for medians
    def one_sided_possible(arr, v):
        n = len(arr)
        p = {val:i for i,val in enumerate(arr)}[v]
        # right side
        s = 0
        seen = set([0])
        for j in range(p+1, n):
            s += 1 if arr[j] > v else -1
            if s in (0,1):
                return True
        # left side
        s = 0
        for j in range(p-1, -1, -1):
            s += 1 if arr[j] > v else -1
            if s in (0,1):
                return True
        return False
    import random
    for n in range(2,11):
        for _ in range(2000):
            arr = list(range(1, n+1))
            random.shuffle(arr)
            meds = medians_of_all_subarrays(arr)
            for v in meds:
                if not one_sided_possible(arr, v):
                    print("Found median requiring two-sided only:", arr, v)
                    raise SystemExit
    print("All medians were achievable by one-sided extension in tested cases up to n=10")
    # Test small-K rule: median implies a greater neighbor within distance <= K
    def ok_with_K(arr, K):
        n=len(arr)
        pos={v:i for i,v in enumerate(arr)}
        meds=medians_of_all_subarrays(arr)
        for v in meds:
            i=pos[v]
            good=False
            # check left
            for d in range(1, K+1):
                j=i-d
                if j<0: break
                if arr[j]>v:
                    good=True
                    break
            if not good:
                # check right
                for d in range(1, K+1):
                    j=i+d
                    if j>=n: break
                    if arr[j]>v:
                        good=True
                        break
            if not good:
                return False
        return True
    bestK=None
    for K in range(1,8):
        ok=True
        for n in range(2,11):
            for _ in range(500):
                arr=list(range(1,n+1))
                random.shuffle(arr)
                if not ok_with_K(arr, K):
                    ok=False
                    break
            if not ok:
                break
        if ok:
            bestK=K
            break
    print("Small-K characterization holds with K=", bestK)

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
    if not any(True for _ in legal_moves(a, alice)):
        return True
    for L,R in legal_moves(a, alice):
        b=a[:L]+a[R+1:]
        if not win_state(tuple(b), not alice):
            return True
    return False


def features(a):
    S=sum(a)
    pref=0
    mn=0
    mx=0
    zero_sub=False
    seen={0}
    for x in a:
        pref+=x
        mn=min(mn,pref)
        mx=max(mx,pref)
        if pref in seen:
            zero_sub=True
        seen.add(pref)
    return dict(S=S, mn_pref=mn, mx_pref=mx, zero_sub=zero_sub, start=a[0] if a else None, end=a[-1] if a else None, n=len(a), c1=a.count(1), cm=a.count(-1))

cases=[
    [-1,1,-1],
    [-1,-1],
    [-1],
    [-1,1,1,-1],
    [1,-1],
    [-1,1,-1,1],
]

for a in cases:
    f=features(a)
    wb=win_state(tuple(a), False)
    print(a, 'BobWins' if wb else 'BobLoses', f)
