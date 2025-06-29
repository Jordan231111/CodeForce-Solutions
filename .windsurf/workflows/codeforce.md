---
description: For **every Codeforces problem**, follow these instructions
---

## 1. Problem-Solving Methodology (CRITICAL FIRST STEP)
- **Pattern Recognition:** Identify which standard technique/algorithm this problem requires
- **Solution Path:** Build logical steps from problem statement to solution approach
- **Edge Case Analysis:** Consider boundary conditions before coding
- **Complexity Estimation:** Estimate time/space complexity before implementation

## 2. Environment & Automation Setup
- All Codeforces solutions should be written in **PyPy**, using the **`pypy3.10`** executable
- The working directory is always assumed to be the [CodeForce](cci:7://file:///Users/jordan/Documents/CodeForce:0:0-0:0) directory
- **AUTOMATION REQUIRED:** Use Competitive Companion + parsing scripts for automatic test case download
- Solutions must be optimized for PyPy's JIT compiler

## 3. Code Quality Standards
- Use descriptive variable names (no single letters except loop counters)
- Optimize critical sections (inner loops, repeated operations)
- Follow template-driven approach for faster implementation

## 4. Algorithm Documentation
- Briefly explain the algorithm and prove its correctness in ≤ 5 sentences
- **Must include:** Why this approach works and why alternatives won't

## 5. Complexity Analysis & Validation
- **Time Complexity:** O(?) with brief justification
- **Space Complexity:** O(?) with brief justification  
- **Constraint Check:** Verify solution works within time limits (typically 1-2 seconds)
- **Mathematical Proof:** Ensure the solution handles maximum constraints

## 6. Comprehensive Testing Protocol
- **Automated Sample Testing:** Use parsing tools to test against official samples automatically
- **Edge Case Testing:** Include ≥ 2 custom edge/boundary cases with documentation
- **Stress Testing:** Generate random test cases and compare with brute force solution when applicable
- **Execution:** Run all tests using `pypy3.10` immediately in the same response
- **Validation:** Show comprehensive test results table (✓/✗)

## 7. Post-Solution Analysis
- **Alternative Approaches:** Briefly mention other possible solutions
- **Optimization Opportunities:** Identify potential improvements
- **Learning Notes:** Document new techniques or insights gained