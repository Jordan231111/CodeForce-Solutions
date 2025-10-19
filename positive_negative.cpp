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

    int T; if(!(cin>>T)) return 0;
    while(T--){
        int n; cin>>n; vector<int>a(n); for(int i=0;i<n;i++) cin>>a[i];
        vector<int> pref(n+1,0);
        for(int i=0;i<n;i++) pref[i+1]=pref[i]+a[i];
        long long ans=0;
        auto middleCount = [&](){
            if(n<=2) return 0LL;
            if(!(a[0]==-1 && a[n-1]==-1)) return 0LL;
            int size = 2*n + 5, off = n + 2;
            vector<long long> bit(size+1,0);
            auto add=[&](int v,long long delta){ for(int i=v+1;i<=size;i+=i&-i) bit[i]+=delta; };
            auto sum=[&](int v){ long long r=0; for(int i=v+1;i>0;i-=i&-i) r+=bit[i]; return r; };
            long long res=0;
            int addL=1;
            for(int R=0; R<=n-2; ++R){
                while(addL<=R){ add(pref[addL]+off,1); ++addL; }
                res += sum(pref[R+1]+off);
            }
            return res;
        }();
        ans += middleCount;
        if(a[n-1]==-1){
            for(int R=0; R<=n-2; ++R){
                if(a[R+1]==-1 && pref[R+1]>=0) ans++;
            }
        }
        if(a[0]==-1){
            for(int L=1; L<=n-1; ++L){
                if(a[L-1]==-1 && pref[L]<=pref[n]) ans++;
            }
        }
        cout<<ans<<"\n";
    }
    return 0;
}
