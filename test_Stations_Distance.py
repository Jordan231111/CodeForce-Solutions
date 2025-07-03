import sys
import io
import unittest
from contextlib import redirect_stdout

class TestStationsDistance(unittest.TestCase):
    def run_with_input(self, input_text):
        # Save original stdin and redirect to our test input
        original_stdin = sys.stdin
        sys.stdin = io.StringIO(input_text)
        
        # Capture stdout
        output = io.StringIO()
        with redirect_stdout(output):
            # Create a local version of the solution
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
        
        # Restore stdin
        sys.stdin = original_stdin
        
        return output.getvalue().strip()

    def test_sample1(self):
        input_text = "5 7\n2 3 5 1 5 2 2"
        expected_output = "1\n1\n2\n2\n1\n2\n1"
        self.assertEqual(self.run_with_input(input_text), expected_output)
    
    def test_sample2(self):
        input_text = "1 2\n1 1"
        expected_output = "1\n0"
        self.assertEqual(self.run_with_input(input_text), expected_output)
        
    def test_sample3(self):
        input_text = "3 3\n1 3 2"
        expected_output = "1\n2\n1"
        self.assertEqual(self.run_with_input(input_text), expected_output)
        
    def test_edge_case1(self):
        # All positions flipped once
        input_text = "5 5\n1 2 3 4 5"
        expected_output = "1\n1\n1\n1\n1"
        self.assertEqual(self.run_with_input(input_text), expected_output)
    
    def test_edge_case2(self):
        # Alternating pattern
        input_text = "5 5\n1 3 5 2 4"
        expected_output = "1\n2\n3\n2\n1"
        self.assertEqual(self.run_with_input(input_text), expected_output)

if __name__ == "__main__":
    unittest.main()
