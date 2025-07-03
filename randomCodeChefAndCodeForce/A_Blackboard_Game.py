def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        
        # Calculate counts of numbers in each modulo group (0-3)
        counts = [0, 0, 0, 0]
        for i in range(n):
            counts[i % 4] += 1
            
        # Alice wins if either:
        # 1. count[0] > count[3] (more 0s than 3s), or
        # 2. counts[1] > counts[2] (more 1s than 2s)
        if counts[0] > counts[3] or counts[1] > counts[2]:
            print("Alice")
        else:
            print("Bob")

if __name__ == "__main__":
    solve()
