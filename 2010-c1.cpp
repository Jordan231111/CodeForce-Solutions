#include <iostream>
#include <string>

using namespace std;

int main() {
    string t;
    cin >> t;
    int length_t = t.length();
    bool found = false;

    for (int len_s = 1; len_s < length_t; ++len_s) {
        string s = t.substr(0, len_s);
        int len_s_local = s.length();
        for (int k = 1; k < len_s_local; ++k) {
            string s_prefix = s.substr(0, k);
            string s_suffix = s.substr(len_s_local - k, k);
            if (s_prefix == s_suffix) {
                string expected_t = s + s.substr(k);
                if (expected_t == t) {
                    cout << "YES" << endl;
                    cout << s << endl;
                    found = true;
                    break;
                }
            }
        }
        if (found)
            break;
    }
    if (!found)
        cout << "NO" << endl;
    return 0;
}