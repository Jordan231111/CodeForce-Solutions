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
    int N,K; if(!(cin>>N>>K)) return 0;
    int NK=N*K;
    vector<int>P(NK+1);
    for(int i=1;i<=NK;++i) cin>>P[i];
    vector<char> vis(NK+1,0);
    long long ans=0;
    vector<int> cyc;
    cyc.reserve(NK);
    for(int s=1;s<=NK;++s){
        if(vis[s]) continue;
        cyc.clear();
        int x=s;
        while(!vis[x]){ vis[x]=1; cyc.push_back(x); x=P[x]; }
        int L=cyc.size();
        if(L<=1) continue;
        vector<int> res(L);
        for(int i=0;i<L;++i) res[i]=(cyc[i]-1)%N;
        int M=2*L;
        vector<int> arr(M);
        for(int i=0;i<M;++i) arr[i]=res[i%L];
        vector<vector<int>> where(N);
        for(int i=0;i<M;++i) where[arr[i]].push_back(i);
        vector<vector<int>> dp(M);
        for(int l=0;l<M;++l){
            int maxlen=min(L, M-l);
            dp[l].assign(maxlen,0);
        }
        auto GET = [&](int l,int r)->int{ if(l>r) return 0; return dp[l][r-l]; };
        for(int len=2; len<=L; ++len){
            for(int l=0;l+len-1<M;++l){
                int r=l+len-1;
                int best = GET(l, r-1);
                const auto& v = where[arr[r]];
                auto itL = lower_bound(v.begin(), v.end(), l);
                auto itR = lower_bound(v.begin(), v.end(), r);
                for(auto it=itL; it!=itR; ++it){
                    int k=*it;
                    int cand = GET(l, k-1) + GET(k+1, r-1) + 1;
                    if(cand>best) best=cand;
                }
                dp[l][r-l]=best;
            }
        }
        int best=0;
        for(int start=0; start<L; ++start) best=max(best, GET(start, start+L-1));
        ans += best;
    }
    cout<<ans<<"\n";
    return 0;
}
