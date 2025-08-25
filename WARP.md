# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository Overview

This is a **competitive programming** repository focused on **Codeforces** solutions written in Python. The codebase follows a highly optimized, template-driven approach designed for speed and efficiency in contest environments.

### Core Architecture

**Template-Based Development**: All solution files begin with a standardized 67-line template (`template.py`) containing:
- Fast I/O macros (II, MI, LI, SI, etc.)
- Graph construction utilities (`graph()`, `graph_w()`)
- Common constants (mod, inf, direction arrays)
- Utility functions (acc, yn, ordalp)
- Standard imports optimized for competitive programming

**Dual Solution Pattern**: Most problems implement a **main solution + brute force** approach:
- Main solution: Optimized algorithm in `Problem_Name.py`
- Reference solution: Brute force implementation in `brute_Problem_Name.py` 
- Test harness: Comprehensive testing in `test_Problem_Name.py`

**Contest Organization**: Problems are organized both by individual files and contest directories (e.g., `Codeforces Round 1029 (Div. 3)/`).

## Essential Commands

### Running Solutions
```bash
# Execute a solution (primary method)
pypy3.10 Problem_Name.py < input_file

# Run with sample input from 's' file
pypy3.10 Problem_Name.py < s

# Quick test with echo input
echo "test_input" | pypy3.10 Problem_Name.py
```

### Testing and Validation
```bash
# Run comprehensive test suite for a problem
pypy3.10 test_Problem_Name.py

# Run brute force reference solution
pypy3.10 brute_Problem_Name.py < input_file

# Stress test (compare optimized vs brute force)
pypy3.10 test_Problem_Name.py  # includes automated stress testing
```

### Development Workflow
```bash
# Create new problem from template
cp template.py New_Problem_Name.py

# Set up test file structure
cp test_Jump_Game_IX.py test_New_Problem_Name.py
# Edit test file to match new problem

# Run solution during development
pypy3.10 New_Problem_Name.py < s
```

## Performance Requirements

**Runtime Environment**: All solutions must run under `pypy3.10` for optimal JIT compilation. The codebase is specifically tuned for PyPy's performance characteristics.

**Optimization Philosophy**:
- **Single-pass algorithms**: Prefer one scan over multiple passes through data
- **Minimize object creation**: Avoid temporary lists/tuples in hot loops  
- **Template-driven speed**: Use pre-optimized I/O macros and utility functions
- **Early termination**: Exit loops/functions as soon as answer is determined

**Memory Management**: 
- Use flat arrays instead of nested structures where possible
- Implement rolling arrays for DP to reduce space complexity
- Stream-process large inputs rather than storing intermediate results

## Code Standards

### Competitive Programming Conventions
- **Concise variable names**: Use `n, m, a, b, res, ans` style naming
- **No comments in solution files**: Solutions must be comment-free for submission
- **Template inclusion**: Every solution starts with the exact 67-line template
- **PyPy optimizations**: Follow micro-optimization patterns for hot loops

### I/O Patterns
Standard input macros are used throughout:
- `II()` - single integer
- `MI()` - map integers 
- `LI()` - list of integers
- `SI()` - string input
- `LI_1()` - list of integers decremented by 1 (for 0-indexing)

### Algorithm Implementation
- **Graph problems**: Use `graph(n, m)` or `graph_w(n, m)` template functions
- **Mathematical operations**: Leverage `mod = 998244353`, `inf = 1001001001001001001`
- **Direction handling**: Use predefined `DIR_4`, `DIR_8`, `DIR_BISHOP` arrays
- **Common utilities**: `acc()` for prefix sums, `yn()` for yes/no output

## Testing Architecture

### Three-Layer Testing System
1. **Unit Testing**: Sample cases from problem statements
2. **Edge Case Testing**: Boundary conditions and corner cases  
3. **Stress Testing**: Random test generation comparing optimized vs brute force

### Test File Structure
Each `test_Problem_Name.py` follows a standardized pattern:
- Subprocess execution of both solutions
- Automated comparison of outputs
- Performance timing and reporting
- Both deterministic and randomized test cases

### Validation Process
- All solutions must pass comprehensive test suites before submission
- Brute force implementations serve as correctness references
- Stress testing generates random inputs to catch edge cases
- Performance validation ensures solutions run within contest time limits

## Problem-Solving Methodology

### Algorithmic Approach
1. **Pattern Recognition**: Identify standard algorithms/techniques required
2. **Complexity Analysis**: Estimate time/space complexity before coding
3. **Template Selection**: Choose appropriate template functions and utilities
4. **Optimization Focus**: Apply PyPy-specific performance optimizations
5. **Validation**: Implement brute force reference and comprehensive testing

### Performance Optimization Priority
- Algorithmic efficiency takes precedence over micro-optimizations
- Single-pass solutions preferred over multiple iterations
- Memory access patterns optimized for cache efficiency  
- Early exit conditions implemented wherever possible
- JIT-friendly code structures (avoid excessive function calls in hot loops)

## Development Environment

### VS Code Configuration
The `.vscode/settings.json` configures Code Runner to use `pypy3.10` with input redirection from file `s`, enabling rapid testing during development.

### Competitive Companion Integration
- `.cph/` directory contains problem metadata from Competitive Companion browser extension
- Automatic test case download and parsing
- Integration with contest platforms for seamless workflow

### File Organization
- **Root level**: Individual problem solutions and their associated test/brute files
- **Contest directories**: Organized by specific contest (e.g., "Codeforces Round 1029 (Div. 3)")
- **Template files**: `template.py` and `python.json` (VS Code snippets)
- **Utility files**: Debug scripts, profiling tools, and development helpers
