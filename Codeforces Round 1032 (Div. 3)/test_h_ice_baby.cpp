#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
using namespace std;

int main() {
    // Create test input file
    ofstream testFile("test_input.txt");
    testFile << "6\n";
    testFile << "1\n1 1\n";
    testFile << "2\n3 4\n1 2\n";
    testFile << "4\n4 5\n3 4\n1 3\n3 3\n";
    testFile << "8\n6 8\n4 6\n3 5\n5 5\n3 4\n1 3\n2 4\n3 3\n";
    testFile << "5\n1 2\n6 8\n4 5\n2 3\n3 3\n";
    testFile << "11\n35 120\n66 229\n41 266\n98 164\n55 153\n125 174\n139 237\n30 72\n196 212\n109 123\n174 196\n";
    testFile.close();
    
    // Expected outputs
    vector<string> expected = {
        "1",
        "1 1",
        "1 2 2 3",
        "1 2 2 3 3 3 4 5",
        "1 2 2 2 3",
        "1 2 3 4 5 6 7 7 8 8 9"
    };
    
    // Run the solution and capture output
    system("g++ -o h_ice_baby h_ice_baby.cpp");
    system("./h_ice_baby < test_input.txt > test_output.txt");
    
    // Read the output
    ifstream outputFile("test_output.txt");
    string line;
    int testCase = 0;
    
    cout << "Test Results:\n";
    cout << "=============\n";
    
    while (getline(outputFile, line)) {
        cout << "Test case " << (testCase + 1) << ":\n";
        cout << "Expected: " << expected[testCase] << "\n";
        cout << "Got:      " << line << "\n";
        
        if (line == expected[testCase]) {
            cout << "✓ PASSED\n";
        } else {
            cout << "✗ FAILED\n";
        }
        cout << "\n";
        testCase++;
    }
    
    outputFile.close();
    
    // Clean up
    system("rm test_input.txt test_output.txt h_ice_baby");
    
    return 0;
} 