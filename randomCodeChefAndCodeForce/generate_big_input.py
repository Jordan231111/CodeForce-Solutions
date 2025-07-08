import sys

# Parameters for input generation
H = 1000000000
W = 1000000000
K = 200000

print(f"{H} {W} {K}")

# Generate a dense 450x445 block (~200k) starting from (1, W) downward-left
a = 450
b = 445  # 450*445 = 200,250 > 200,000
count = 0
for i in range(a):
    if count >= K:
        break
    r = 1 + i  # rows 1..450
    for j in range(b):
        if count >= K:
            break
        c = W - j  # columns from W downwards
        print(f"{r} {c}")
        count += 1 