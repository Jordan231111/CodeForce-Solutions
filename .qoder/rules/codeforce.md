---
trigger: always_on
alwaysApply: true
---
For **every problem**, follow these instructions

## 1. Problem-Solving Methodology (CRITICAL FIRST STEP)
- **Pattern Recognition:** Identify which standard technique/algorithm this problem requires
- **Solution Path:** Build logical steps from problem statement to solution approach
- **Edge Case Analysis:** Consider boundary conditions before coding
- **Complexity Estimation:** Estimate time/space complexity before implementation

## 2. Environment & Automation Setup
- All Codeforces solutions must be written in Python using the **`pypy3.10`** executable and must leverage the predefined snippet templates [python.json](mdc:python.json) to scaffold algorithms quickly.
- All files must reside directly inside the top-level directory which you must always assume we are already in (do not create ANY subfolders or duplicate directories).
- Every solution file must begin with the 67-line template snippet defined in `template.py` (lines 1–67); include it verbatim before your problem-specific code.
- **AUTOMATION REQUIRED:** Use Competitive Companion + parsing scripts for automatic test case download
- Solutions must be optimized for PyPy's JIT compiler
- **Never use web search unless the user explicitly requests it in their message.**
- **Use `sys.setrecursionlimit` sparingly.** If recursion is unavoidable (e.g., DFS on trees), set a moderate limit such as `sys.setrecursionlimit(10**6)` rather than extremely large values that risk memory limit exceeded on Codeforces.

## 3. Code Quality Standards
- Use concise, human-like variable names (e.g., n, m, a, b, res, ans, etc.) for speed, as is common in competitive programming
- Optimize critical sections (inner loops, repeated operations)
- Follow template-driven approach for faster implementation
- Prefer **single-pass scans with early exit** whenever possible
- Minimise temporary Python objects (e.g. stream integers from `stdin.buffer.read().split()` directly; avoid building throw-away lists)
- **Do not include any comments in the solution code. Solution files must be completely free of comments.**

## 3a. PyPy-specific Performance Hints
- Each additional pass over an `n = 2·10⁵` array costs ≈40–60 ms in PyPy's interpreter **before** JIT kicks in.  If the algorithm can succeed in one backwards/forwards scan, do so.
- Hash-table probes dominate: two `set.__contains__` per element is fine; eight per element risks TLE.  Merge look-ups when possible.
- The JIT warms up per function.  A tight loop in a helper that's called once per test case will never be JIT-compiled if the case is small. Keep the hot loop in the main function for large-`n` problems.

## 3b. PyPy Micro-optimisation Mandates (ALWAYS apply unless the task is I/O-bound)

1. I/O
   • Read the entire stdin buffer once using `input = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline` to avoid per-line overhead.
   • When total tokens ≳ 1e4, prefer `data = io.BytesIO(os.read(0, os.fstat(0).st_size)).read().split()` and index into `data`.

2. Data Structures for Grids & Graphs
   • **Dense Grids:** For problems where most cells are processed (e.g., a full maze), represent the grid as ONE flat list/array of length R·C (`idx = r*W + c`). Add a sentinel border to eliminate boundary checks in hot loops.
   • **Sparse Grids/Graphs:** For problems with a few points/edges in a large space, use a `set` or `dict` for O(1) lookups of the relevant features. This is far more memory- and time-efficient than a large, empty array.

3. State encoding
   • Use ONE integer per cell: `INF = 1 << 30` (unseen), `INF2 = 1 << 31` (one good neighbour), any smaller value = final distance.

4. Neighbour processing
   • Unroll the four directions explicitly; avoid `for dr,dc in DIR_4` tuple loops.
   • Use simple ±1 / ±rowStride arithmetic; avoid div/mod unless essential.

5. Queue discipline
   • Maintain a pre-allocated plain Python list as a FIFO (`q = [0]*(R*C)`); track `head`, `tail` indices manually.  No `deque`/`defaultdict`.

6. Memory / object hygiene
   • Do NOT create tuples/lists/sets inside the inner loop.
   • Pull frequently-used globals into local variables at the top of `solve()`.

7. Hot-loop footprint check
   • Aim for ≤3 memory accesses and ≤2 branches per neighbour visit.

8. Quick smoke-test before submission
   • On a synthetic worst-case (R=W=3000) ensure local run-time < 0.6 s on a standard laptop.

9. Key design
   • Store 2-D coordinates as `(r, c)` tuples or a 64-bit bit-pack (`r<<20 | c`); never `r*M+c` with large M.
   • Large-integer hashes balloon constant factors and can single-handedly cause TLE.
   • Rule of thumb: if `r*M+c` might exceed 2^30 (≈1e9), switch to tuple/bit-pack; beyond 2^64 the slowdown is severe.

## 4. Algorithm Documentation
- Briefly explain the algorithm and prove its correctness in ≤ 5 sentences
- **Must include:** Why this approach works and why alternatives won't

## 4a. Fast-Fail Checklist (add to every solution write-up)
  1. Is there any pass over the input that can be fused with another?
  2. Can membership tests be merged into one `set` instead of two?
  3. Is there an early return once the answer is known?
  4. Does the I/O layer avoid building large intermediate lists?
  5. Are any hot-loop operations using big-integers, strings, or other heavyweight objects?
  6. Have you benchmarked under **PyPy3.10** on a worst-case input? CPython timings are not representative.

## 5. Complexity Analysis & Validation
- **Time Complexity:** O(?) with brief justification
- **Space Complexity:** O(?) with brief justification  
- **Constraint Check:** Verify solution works within time limits (typically 1-2 seconds)
- **Mathematical Proof:** Ensure the solution handles maximum constraints

## 6. Comprehensive Testing Protocol
- **Automated Sample Testing:** Use parsing tools to test against official samples automatically
- **Edge Case Testing:** Include ≥ 2 custom edge/boundary cases with documentation
- **Stress Testing:** Generate random test cases and also ALWAYS compare with brute force solution
- **Execution:** Run all tests using `pypy3.10` immediately in the same response
- **Validation:** Show comprehensive test results table (✓/✗)
- **Separate Test File:** Store all testing logic in its own Python source (e.g., `test_<problem_id>.py`) placed alongside the solution; do not embed tests inside the main solution script.

### 6a. Test File Template
Always use this structure for test files:
```python
import subprocess
import sys
import time

def run_test_case(params...):
    # Calculate expected output
    # Logic to determine expected result based on test parameters
    
    # Prepare input
    test_input = f"1\n{param1} {param2} ... \n"
    
    # Run the solution
    process = subprocess.Popen(
        ["pypy3.10", "solution_file.py"], 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate(test_input)
    
    # Check output
    actual = stdout.strip()  # Adjust parsing as needed
    
    if actual == expected:
        return True, f"PASSED: params..., output={actual}"
    else:
        return False, f"FAILED: params..., expected={expected}, got={actual}"

def run_all_tests():
    test_cases = [
        # Sample test cases from problem statement
        (param1, param2, ...),
        
        # Edge cases
        # Add minimum 2 edge cases with documentation
    ]
    
    results = []
    start_time = time.time()
    
    for params... in test_cases:
        success, message = run_test_case(params...)
        results.append((success, message))
    
    end_time = time.time()
    
    # Print results
    all_passed = all(success for success, _ in results)
    
    print("Test Results:")
    for success, message in results:
        print(f"{'✓' if success else '✗'} {message}")
    
    print(f"\nExecution time: {end_time - start_time:.4f} seconds")
    print(f"Overall: {'PASSED' if all_passed else 'FAILED'}")

# ---- New helper for randomised stress testing ----
def stress_test(max_n=10**5, num_tests=100, verbose=False):
    """Generate random test cases and compare solution with reference."""
    import random, subprocess, os, time, sys

    passed = 0
    start = time.time()
    for _ in range(num_tests):
        # ---------------------------------------------------------------
        # TODO: Replace with problem-specific random case generator
        # Example below assumes a single integer input; adjust as needed.
        n = random.randint(1, max_n)
        test_input = f"1\n{n}\n"
        # ---------------------------------------------------------------

        # Run the contestant solution
        proc_sol = subprocess.Popen(
            ["pypy3.10", "solution_file.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out_sol, err_sol = proc_sol.communicate(test_input)

        # Run the reference (brute-force) solution if available
        proc_ref = subprocess.Popen(
            ["pypy3.10", "brute.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out_ref, err_ref = proc_ref.communicate(test_input)

        if out_sol.strip() != out_ref.strip():
            print("\nMISMATCH FOUND:\nInput:\n", test_input, sep="")
            print("Output:", out_sol, "\nExpected:", out_ref)
            return
        passed += 1
        if verbose and passed % 10 == 0:
            print(f"{passed}/{num_tests} ok", end="\r", flush=True)
    end = time.time()
    print(f"\nStress testing completed: {passed}/{num_tests} cases passed in {end - start:.2f}s")

if __name__ == "__main__":
    run_all_tests()

## 7. Post-Solution Analysis
- **Alternative Approaches:** Briefly mention other possible solutions
- **Optimization Opportunities:** Identify potential improvements
- **Learning Notes:** Document new techniques or insights gained

## 8. Additional Notes
- When using coordinate compression, ensure the compressed grid remains O(K) in size; avoid BFS/DP over an O(K²) grid of compressed cells.

## 9. Advanced Algorithmic Optimization Patterns

### 9a. Constraint Preprocessing Techniques
- **Backwards DP for Constraint Propagation:** When dealing with multiple constraints on future states, use backwards DP to precompute "earliest violation position" for each possible action.
  ```python
  # Example: precompute when value v becomes forbidden if we start at position p
  constraint[p][v] = min_forbidden_position
  for p in range(n-1, -1, -1):
      for v in range(n):
          constraint[p][v] = min(constraint[p][v], constraint[p+1][v+1])
  ```
- **Constraint Batching:** Group similar constraints together to reduce check overhead from O(m·operations) to O(operations).
- **Early Constraint Violation Detection:** Store constraints in formats that allow O(1) violation checks instead of O(constraint_size).

### 9b. Range Operation Optimization Techniques
- **Difference Arrays for Batch Updates:** Use difference arrays to convert range updates from O(range_size) to O(1).
  ```python
  # Range update [l, r] with value v
  diff[l] += v
  diff[r+1] -= v
  # Reconstruct: prefix_sum(diff) gives actual values
  ```
- **Segment Trees with Lazy Propagation:** For complex range queries + updates, implement lazy propagation to achieve O(log n) per operation.
- **Coordinate Compression + Range Ops:** When ranges are sparse, compress coordinates first then apply range operations on compressed space.

### 9c. DP Implementation Strategy Selection
- **Bottom-up vs Memoization Trade-offs:**
  - **Use Bottom-up when:** States can be processed in topological order, memory access patterns are predictable, avoiding recursion overhead matters
  - **Use Memoization when:** State space is sparse, transition dependency is complex, natural recursive structure exists
- **State Space Optimization:**
  - **Rolling Arrays:** When DP only depends on previous layer, use rolling arrays to reduce space from O(n·k) to O(k)
  - **State Compression:** Pack multiple boolean flags into single integers using bitmasking
  - **Canonical State Representation:** Avoid double-counting by enforcing canonical ordering (e.g., in counting problems)### 9d. Cache-Efficient Algorithm Design
- **Memory Access Patterns:**
  - **Sequential Access:** Process arrays in row-major order when possible
  - **Blocked Processing:** For 2D problems, process in cache-friendly blocks rather than full rows/columns
  - **Locality Optimization:** Keep related data structures close in memory layout
- **Loop Structure Optimization:**
  - **Loop Fusion:** Combine multiple passes over same data into single pass
  - **Loop Interchange:** Reorder nested loops to improve cache locality
  - **Loop Blocking:** For large arrays, process in cache-sized chunks

### 9e. Algorithm-Specific Optimization Patterns
- **Graph Algorithms:**
  - **Bidirectional Search:** For shortest path, search from both ends simultaneously
  - **Edge List vs Adjacency List:** Choose based on operation frequency (queries vs iteration)
  - **Union-Find Optimization:** Use path compression + union by rank for near-constant amortized operations
- **String Algorithms:**
  - **Rolling Hash with Multiple Bases:** Use 2-3 different hash bases to avoid collisions
  - **KMP vs Z-Algorithm:** Choose based on pattern vs text length ratio
- **Number Theory:**
  - **Precomputed Factorials + Inverse:** For multiple combination queries, precompute factorials and modular inverses
  - **Chinese Remainder Theorem:** For multiple modular constraints, use CRT to combine them

### 9f. Advanced Fast-Fail Optimization Checklist
  1. **Constraint Processing:** Can constraints be preprocessed to enable O(1) checks?
  2. **Range Operations:** Are there multiple updates to contiguous ranges that can be batched?
  3. **State Space:** Can DP states be processed in an order that eliminates redundant computation?
  4. **Memory Layout:** Are data structures arranged for optimal cache performance?
  5. **Algorithm Selection:** Is there a more specialized algorithm for this specific constraint pattern?
  6. **Early Termination:** Can the algorithm exit early once the answer is determined?
  7. **Amortized Analysis:** Are there expensive operations that can be spread across multiple cheap ones?

### 9g. Competition-Specific Optimization Priorities
- **When Time is Critical:**
  1. Eliminate all unnecessary memory allocations in hot loops
  2. Use flat arrays instead of nested data structures
  3. Prefer iterative over recursive solutions
  4. Minimize function call overhead
- **When Memory is Critical:**
  1. Use rolling arrays for DP
  2. Compress state representations
  3. Stream process large inputs
  4. Avoid storing intermediate results
- **When Implementation Speed Matters:**
  1. Use proven templates from snippet library
  2. Prefer standard library functions over custom implementations
  3. Write straightforward code over overly optimized code
  4. Test with maximum constraints immediately

