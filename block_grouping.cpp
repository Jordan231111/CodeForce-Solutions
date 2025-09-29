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
        int n;
        string s;
        cin >> n >> s;
        
        vector<int> pa, pb;
        pa.reserve(n);
        pb.reserve(n);
        for(int i = 0; i < n; i++) {
            if(s[i] == 'a') pa.push_back(i);
            else pb.push_back(i);
        }
        
        if(pa.empty() || pb.empty()) {
            cout << 0 << '\n';
            continue;
        }
        
        auto calc = [](const vector<int>& p){
            int k = (int)p.size();
            if(k <= 1) return 0LL;
            vector<long long> x(k);
            for(int i = 0; i < k; i++) x[i] = (long long)p[i] - i;
            long long med = x[k/2];
            long long res = 0;
            for(int i = 0; i < k; i++) res += llabs(x[i] - med);
            return res;
        };
        
        long long ans = min(calc(pa), calc(pb));
        cout << ans << '\n';
    }
    
    return 0;
}