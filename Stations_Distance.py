import sys
input = sys.stdin.readline

n, q = map(int, input().split())
a = list(map(int, input().split()))

is_black = [False] * (n + 2)
intervals = 0

for i in range(q):
    pos = a[i]
    
    left = is_black[pos-1]
    right = is_black[pos+1]
    current = is_black[pos]
    
    is_black[pos] = not is_black[pos]
    
    if not current:  # White to black
        if not left and not right:
            intervals += 1
        elif left and right:
            intervals -= 1
    else:  # Black to white
        if not left and not right:
            intervals -= 1
        elif left and right:
            intervals += 1
    
    print(intervals) 