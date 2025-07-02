def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    operations = []
    
    def is_valid():
        for i in range(n-1):
            if a[i] >= a[i+1] or b[i] >= b[i+1]:
                return False
        for i in range(n):
            if a[i] >= b[i]:
                return False
        return True
    
    if is_valid():
        print(0)
        return
    
    changed = True
    while changed:
        changed = False
        
        for i in range(n-1):
            if a[i] > a[i+1]:
                operations.append((1, i + 1))
                a[i], a[i+1] = a[i+1], a[i]
                changed = True
        
        for i in range(n-1):
            if b[i] > b[i+1]:
                operations.append((2, i + 1))
                b[i], b[i+1] = b[i+1], b[i]
                changed = True
        
        for i in range(n):
            if a[i] >= b[i]:
                operations.append((3, i + 1))
                a[i], b[i] = b[i], a[i]
                changed = True
    
    print(len(operations))
    for op in operations:
        print(op[0], op[1])

t = int(input())
for _ in range(t):
    solve()