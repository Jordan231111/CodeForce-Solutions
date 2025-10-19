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

    int n; if(!(cin >> n)) return 0;
    vector<long long> a(n+1);
    for(int i=1;i<=n;i++) cin >> a[i];
    int q; cin >> q;
    while(q--){
        int l,r; long long k; cin >> l >> r >> k;
        long long ans=0;
        for(int i=l;i<=r;i++){
            long long buy = min(a[i], k);
            a[i]-=buy;
            ans+=buy;
        }
        cout << ans << '\n';
    }
}
