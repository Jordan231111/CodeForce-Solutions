#include <bits/stdc++.h>
using namespace std;
int main(){
    const long long MOD=998244353LL; long long H=200000,W=200000; long long L=H+W-2; long long E=2*H*W-H-W; long long X=E-L; long long N=H+W; vector<long long> fact(N+1),ifact(N+1);
    auto modpow=[&](long long a,long long e){ long long r=1%MOD; while(e){ if(e&1) r=r*a%MOD; a=a*a%MOD; e>>=1;} return r; };
    fact[0]=1; for(int i=1;i<=N;++i) fact[i]=fact[i-1]*i%MOD; ifact[N]=modpow(fact[N], MOD-2); for(int i=N;i>0;--i) ifact[i-1]=ifact[i]*i%MOD;
    auto C=[&](long long n,long long k)->long long{
        if(n<0||k<0||k>n) return 0LL; if(n<=N) return fact[n]*ifact[k]%MOD*ifact[n-k]%MOD; if(k==0) return 1; if(k==1) return n%MOD; if(k==2) return (n%MOD)*((n-1)%MOD)%MOD*((MOD+1)/2)%MOD; return 0LL; };
    long long paths=C(L, H-1);
    long long add=C(X,2);
    long long pairs=((L-1)%MOD)*C(L-2, H-2)%MOD;
    long long ans=(paths*add%MOD - pairs + MOD)%MOD;
    cout<<paths<<"\n"<<add<<"\n"<<pairs<<"\n"<<ans<<"\n";
}
