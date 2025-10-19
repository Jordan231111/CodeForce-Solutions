#include <bits/stdc++.h>
using namespace std;
#ifdef LOCAL
#include "algo/debug.h"
#else
#define debug(...) 42
#endif


int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int t;
    cin >> t;
    
    while(t--) {
        int n, k;
        cin >> n >> k;
        
        if(k == 0) {
            for(int i = 1; i <= n; i++) {
                cout << i << (i == n ? '\n' : ' ');
            }
        }
        else if(k == 1) {
            if(n < 3) {
                cout << "-1\n";
            }
            else {
                cout << "1 3 2";
                for(int i = 4; i <= n; i++) {
                    cout << " " << i;
                }
                cout << '\n';
            }
        }
        else if(k == 2) {
            if(n < 3) {
                cout << "-1\n";
            }
            else {
                cout << "3 1 2";
                for(int i = 4; i <= n; i++) {
                    cout << " " << i;
                }
                cout << '\n';
            }
        }
        else if(k == 3) {
            if(n < 2) {
                cout << "-1\n";
            }
            else {
                cout << "2 1";
                for(int i = 3; i <= n; i++) {
                    cout << " " << i;
                }
                cout << '\n';
            }
        }
        else {
            if(k >= 8) {
                cout << "-1\n";
            }
            else {
                int a = -1, b = -1;
                for(int i = 1; i <= n; i++) {
                    int j = i ^ k;
                    if(i < j && j <= n) {
                        a = i;
                        b = j;
                        break;
                    }
                }
                
                if(a == -1) {
                    cout << "-1\n";
                }
                else {
                    vector<int> arr;
                    for(int i = 1; i <= n; i++) {
                        if(i != a && i != b) {
                            arr.push_back(i);
                        }
                    }
                    arr.insert(arr.begin() + 2, a);
                    arr.insert(arr.begin() + 2, b);
                    
                    for(int i = 0; i < n; i++) {
                        cout << arr[i] << (i == n-1 ? '\n' : ' ');
                    }
                }
            }
        }
    }
}

