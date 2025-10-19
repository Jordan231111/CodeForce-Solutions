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
    
    int n;
    if(!(cin >> n)) return 0;
    vector<long long> a(n+1);
    for(int i=1;i<=n;i++) cin >> a[i];
    using i128 = __int128_t;
    const long long INF = (long long)4e18;
    int sz = 4*n + 5;
    vector<i128> sum(sz);
    vector<long long> mn1(sz), mn2(sz), add(sz);
    vector<int> cnt(sz);
    auto apply_add = [&](int p, int len, long long v){
        sum[p] += (i128)v * len;
        mn1[p] += v;
        if(mn2[p] < INF) mn2[p] += v;
        add[p] += v;
    };
    auto apply_chmax = [&](int p, long long x){
        if(x <= mn1[p]) return;
        sum[p] += (i128)(x - mn1[p]) * cnt[p];
        mn1[p] = x;
    };
    function<void(int,int,int)> build = [&](int p, int l, int r){
        if(l==r){
            sum[p] = a[l];
            mn1[p] = a[l];
            mn2[p] = INF;
            cnt[p] = 1;
            add[p] = 0;
            return;
        }
        int m=(l+r)>>1;
        build(p<<1,l,m);
        build(p<<1|1,m+1,r);
        sum[p] = sum[p<<1] + sum[p<<1|1];
        if(mn1[p<<1] < mn1[p<<1|1]){
            mn1[p] = mn1[p<<1];
            cnt[p] = cnt[p<<1];
            mn2[p] = min(mn2[p<<1], mn1[p<<1|1]);
        }else if(mn1[p<<1] > mn1[p<<1|1]){
            mn1[p] = mn1[p<<1|1];
            cnt[p] = cnt[p<<1|1];
            mn2[p] = min(mn2[p<<1|1], mn1[p<<1]);
        }else{
            mn1[p] = mn1[p<<1];
            cnt[p] = cnt[p<<1] + cnt[p<<1|1];
            mn2[p] = min(mn2[p<<1], mn2[p<<1|1]);
        }
        add[p]=0;
    };
    auto pull = [&](int p){
        sum[p] = sum[p<<1] + sum[p<<1|1];
        if(mn1[p<<1] < mn1[p<<1|1]){
            mn1[p] = mn1[p<<1];
            cnt[p] = cnt[p<<1];
            mn2[p] = min(mn2[p<<1], mn1[p<<1|1]);
        }else if(mn1[p<<1] > mn1[p<<1|1]){
            mn1[p] = mn1[p<<1|1];
            cnt[p] = cnt[p<<1|1];
            mn2[p] = min(mn2[p<<1|1], mn1[p<<1]);
        }else{
            mn1[p] = mn1[p<<1];
            cnt[p] = cnt[p<<1] + cnt[p<<1|1];
            mn2[p] = min(mn2[p<<1], mn2[p<<1|1]);
        }
    };
    function<void(int,int,int)> push = [&](int p, int l, int r){
        if(l==r) return;
        int m=(l+r)>>1;
        if(add[p]!=0){
            apply_add(p<<1, m-l+1, add[p]);
            apply_add(p<<1|1, r-m, add[p]);
            add[p]=0;
        }
        // Ensure children have mn1 >= this mn1 if needed for chmax propagation
        if(mn1[p<<1] < mn1[p]) apply_chmax(p<<1, mn1[p]);
        if(mn1[p<<1|1] < mn1[p]) apply_chmax(p<<1|1, mn1[p]);
    };
    function<void(int,int,int,int,int,long long)> range_add = [&](int p,int l,int r,int ql,int qr,long long v){
        if(qr<l||r<ql) return;
        if(ql<=l && r<=qr){ apply_add(p, r-l+1, v); return; }
        push(p,l,r);
        int m=(l+r)>>1;
        range_add(p<<1,l,m,ql,qr,v);
        range_add(p<<1|1,m+1,r,ql,qr,v);
        pull(p);
    };
    function<void(int,int,int,int,int,long long)> range_chmax = [&](int p,int l,int r,int ql,int qr,long long x){
        if(qr<l||r<ql || x<=mn1[p]) return;
        if(ql<=l && r<=qr && x < mn2[p]){ apply_chmax(p,x); return; }
        if(l==r){ apply_chmax(p,x); return; }
        push(p,l,r);
        int m=(l+r)>>1;
        range_chmax(p<<1,l,m,ql,qr,x);
        range_chmax(p<<1|1,m+1,r,ql,qr,x);
        pull(p);
    };
    function<i128(int,int,int,int,int)> range_sum = [&](int p,int l,int r,int ql,int qr)->i128{
        if(qr<l||r<ql) return 0;
        if(ql<=l && r<=qr) return sum[p];
        push(p,l,r);
        int m=(l+r)>>1;
        return range_sum(p<<1,l,m,ql,qr) + range_sum(p<<1|1,m+1,r,ql,qr);
    };
    build(1,1,n);
    int q; cin >> q;
    while(q--){
        int l,r; long long k; cin >> l >> r >> k;
        i128 before = range_sum(1,1,n,l,r);
        range_add(1,1,n,l,r,-k);
        range_chmax(1,1,n,l,r,0);
        i128 after = range_sum(1,1,n,l,r);
        long long ans = (long long)(before - after);
        cout << ans << '\n';
    }
}

