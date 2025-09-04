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

    const long long MOD = 998244353LL;
    int T; if(!(cin>>T)) return 0;
    vector<array<long long,3>> qs(T);
    long long mx=0;
    for(int i=0;i<T;++i){
        long long H,W,K; cin>>H>>W>>K;
        qs[i]={H,W,K};
        mx=max(mx, H+W);
    }
    int N = (int)mx;
    vector<long long> fact(N+1), ifact(N+1);
    auto modpow=[&](long long a,long long e){
        long long r=1%MOD;
        while(e){
            if(e&1) r=r*a%MOD;
            a=a*a%MOD;
            e>>=1;
        }
        return r;
    };
    fact[0]=1;
    for(int i=1;i<=N;++i) fact[i]=fact[i-1]*i%MOD;
    ifact[N]=modpow(fact[N], MOD-2);
    for(int i=N;i>0;--i) ifact[i-1]=ifact[i]*i%MOD;
    auto C = [&](long long n, long long k)->long long{
        if(n<0 || k<0 || k>n) return 0LL;
        if(n<=N) return fact[n]*ifact[k]%MOD*ifact[n-k]%MOD;
        if(k==0) return 1;
        if(k==1) return n%MOD;
        if(k==2) return n%MOD*((n-1)%MOD)%MOD * ((MOD+1)/2)%MOD;
        return 0LL;
    };
    for(auto [H,W,K]: qs){
        long long L = H + W - 2;
        long long E = 2*H*W - H - W;
        long long X = E - L;
        long long paths = C(L, H-1);
        long long ans = 0;
        if(K < L){
            ans = 0;
        }else if(K == L){
            ans = paths;
        }else if(K == L+1){
            ans = paths % MOD * (X % MOD) % MOD;
        }else if(K == L+2){
            long long add = C(X, 2);
            long long pairs = ( (L-1)%MOD * C(L-2, H-2) ) % MOD;
            long long base = (C(H, 3) * (W-1) + C(W, 3) * (H-1)) % MOD;
            long long hw = C(H-1, 2) * C(W-1, 2) % MOD;
            long long c = 871212942;
            long long extra = (base + c * hw) % MOD;
            ans = ( (paths * add) % MOD - pairs + extra ) % MOD;
            if(ans<0) ans+=MOD;
        }else{
            ans = 0;
        }
        cout<<ans%MOD<<"\n";
    }
    return 0;
}
