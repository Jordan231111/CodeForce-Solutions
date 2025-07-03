import sys
input = sys.stdin.readline

P = input().rstrip()
L = int(input())

if len(P) >= L:
    print("Yes")
else:
    print("No") 