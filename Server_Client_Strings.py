import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())

    pcs = [None] * (n + 1)  # Each entry is (chunk_str, prev_node)
    server = None  # Head of server linked list

    for _ in range(q):
        parts = input().split()
        t = int(parts[0])
        p = int(parts[1])

        if t == 1:
            pcs[p] = server  # Share chain (immutable)
        elif t == 2:
            s = parts[2]
            pcs[p] = (s, pcs[p])  # Prepend new chunk
        else:  # t == 3
            server = pcs[p]

    # Collect chunks from server chain (stored in reverse order)
    chunks = []
    cur = server
    while cur is not None:
        chunk, cur = cur  # Unpack tuple (chunk, prev)
        chunks.append(chunk)

    print("".join(reversed(chunks)))

solve() 