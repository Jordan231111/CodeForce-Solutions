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
        int n; cin>>n;
        vector<int> a(n+1), pos(n+1);
        for(int i=1;i<=n;i++){ cin>>a[i]; pos[a[i]] = i; }
        struct BIT{
            int n; vector<int> f;
            BIT(int n=0):n(n),f(n+1,0){}
            void reset(int m){ n=m; f.assign(n+1,0); }
            void add(int i,int v){ for(; i<=n; i+= i&-i) f[i]+=v; }
            int sum(int i){ int s=0; for(; i>0; i-= i&-i) s+=f[i]; return s; }
            int total(){ return sum(n); }
            int kth(int k){ if(k<=0) return 0; int idx=0; int bit=1; while((bit<<1)<=n) bit<<=1; for(int step=bit; step>0; step>>=1){ int j=idx+step; if(j<=n && f[j]<k){ idx=j; k-=f[j]; } } return idx+1; }
            int prevIdx(int i){ int r = sum(i-1); if(r<=0) return 0; return kth(r); }
            int nextIdx(int i){ int r = sum(i) + 1; if(r>total()) return 0; return kth(r); }
        } bitG(n), bitL(n);

        // Initialize: for v = n, greater set empty; less set contains positions of 1..n-1
        bitG.reset(n); bitL.reset(n);
        for(int v=1; v<=n-1; ++v) bitL.add(pos[v], 1);

        auto has_left = [&](int pv)->bool{
            int curr = pv;
            int s = 0;
            while(true){
                int pg = bitG.prevIdx(curr);
                int pl = bitL.prevIdx(curr);
                if(pg==0 && pl==0) return false;
                int pnext = max(pg, pl);
                if(pnext==pg) s += 1; else s -= 1;
                if(s==1 || s==0) return true;
                curr = pnext;
                if(curr<=1) return false;
            }
        };

        auto right_t = [&](int pv)->int{
            int curr = pv;
            int s = 0;
            int t = 0;
            while(true){
                int pg = bitG.nextIdx(curr);
                int pl = bitL.nextIdx(curr);
                int pnext;
                if(pg==0 && pl==0) return n+1;
                if(pg==0) pnext = pl; else if(pl==0) pnext = pg; else pnext = min(pg, pl);
                t += (pnext - curr);
                if(pnext==pg) s += 1; else s -= 1;
                if(t==1 && s==1) return 1;
                if(s==0) return t;
                curr = pnext;
                if(curr>=n) return n+1;
            }
        };

        vector<int> earliest(n+1, n+1);
        for(int v=n; v>=1; --v){
            if(v<n){ bitG.add(pos[v+1], 1); }
            if(v<n) bitL.add(pos[v], -1); // remove current v from less set
            int pv = pos[v];
            if(has_left(pv)) earliest[v] = min(earliest[v], pv);
            int t = right_t(pv);
            if(t<=n) earliest[v] = min(earliest[v], pv + t);
        }

        vector<int> add(n+2, 0);
        for(int v=1; v<=n; ++v){ if(earliest[v] <= n) add[earliest[v]]++; }
        int cur=0;
        vector<int> ans(n+1,0);
        for(int i=1;i<=n;i++){
            cur += add[i];
            ans[i] = (i==1?0:cur);
        }
        for(int i=1;i<=n;i++){
            if(i>1) cout<<' ';
            cout<<ans[i];
        }
        cout<<'\n';
    }
}


