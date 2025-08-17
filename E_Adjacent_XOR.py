import sys

def solve() -> None:
	data = list(map(int, sys.stdin.buffer.read().split()))
	it = iter(data)
	t = next(it)
	out_lines = []
	for _ in range(t):
		n = next(it)
		a = [next(it) for _ in range(n)]
		b = [next(it) for _ in range(n)]

		# Last element never changes; necessary condition
		if a[-1] != b[-1]:
			out_lines.append("NO")
			continue

		ok = True
		for i in range(n - 2, -1, -1):
			ai = a[i]
			bi = b[i]
			# At position i, the only possibilities are:
			# - no op at i: bi == ai
			# - op at i with neighbor value being either a[i+1] (if i+1 happens after i)
			#   or b[i+1] (if i+1 happens before i): bi == ai ^ a[i+1] or bi == ai ^ b[i+1]
			if bi == ai or bi == (ai ^ a[i + 1]) or bi == (ai ^ b[i + 1]):
				continue
			ok = False
			break

		out_lines.append("YES" if ok else "NO")

	sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
	solve()