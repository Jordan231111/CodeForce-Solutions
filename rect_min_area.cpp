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
        int n,m; cin>>n>>m;
        vector<string> g(n);
        for(int i=0;i<n;++i) cin>>g[i];

        bool trans=false;
        if(n>m){
            vector<string> tg(m, string(n,'0'));
            for(int i=0;i<n;++i) for(int j=0;j<m;++j) tg[j][i]=g[i][j];
            g.swap(tg); swap(n,m); trans=true;
        }

        vector<vector<int>> ones(n);
        for(int i=0;i<n;++i){
            ones[i].reserve(m);
            for(int j=0;j<m;++j) if(g[i][j]=='1') ones[i].push_back(j);
        }

        struct DSURow{ int m; vector<int> p; DSURow(){} DSURow(int m):m(m),p(m+1){ iota(p.begin(),p.end(),0);} 
            inline int find(int x){ while(p[x]!=x){ p[x]=p[p[x]]; x=p[x]; } return x; }
        };

        vector<vector<int>> ans(n, vector<int>(m,0));
        vector<DSURow> dsu(n);
        for(int i=0;i<n;++i) dsu[i]=DSURow(m);

        auto paint_row = [&](int i, int L, int R, int area){
            int x = dsu[i].find(L);
            while(x<=R){ ans[i][x]=area; dsu[i].p[x]=dsu[i].find(x+1); x=dsu[i].p[x]; }
        };

        const int B = 32; // width window size
        struct HeightWin{
            int h, ws, we; // current width window [ws..we]
            vector<vector<pair<int,int>>> buckets; // per width in window: (u, L)
            int nextw; // next width in [ws..we] that has items, else m+1
            HeightWin(){}
            HeightWin(int h_, int ws_, int m_):h(h_),ws(ws_),we(min(m_, ws_+B-1)),buckets(we-ws+1),nextw(m_+1){}
        };

        auto build_window = [&](HeightWin& hw){
            fill(hw.buckets.begin(), hw.buckets.end(), vector<pair<int,int>>());
            hw.nextw = m+1;
            for(int u=0; u+hw.h-1<n; ++u){
                int d=u+hw.h-1; const auto& A=ones[u]; const auto& Bv=ones[d];
                size_t i=0,j=0; int last=-1;
                while(i<A.size() && j<Bv.size()){
                    if(A[i]==Bv[j]){
                        int x=A[i];
                        if(last!=-1){ int w=x-last+1; if(w>=hw.ws && w<=hw.we){ hw.buckets[w-hw.ws].push_back({u,last}); if(w<hw.nextw) hw.nextw=w; } }
                        last=x; ++i; ++j;
                    }else if(A[i]<Bv[j]) ++i; else ++j;
                }
            }
        };

        struct GE{ long long area; int h; bool operator<(const GE& o) const { return area>o.area; } };
        vector<HeightWin> HW(n+1);
        priority_queue<GE> gpq;
        for(int h=2; h<=n; ++h){
            HW[h]=HeightWin(h,2,m);
            build_window(HW[h]);
            if(HW[h].nextw<=m) gpq.push({1LL*h*HW[h].nextw, h});
        }

        while(!gpq.empty()){
            auto [area,h]=gpq.top(); gpq.pop();
            auto& hw = HW[h]; int w = hw.nextw;
            auto& vec = hw.buckets[w-hw.ws];
            for(auto &p: vec){ int u=p.first, L=p.second; int d=u+h-1; int R=L+w-1; for(int r=u;r<=d;++r) paint_row(r,L,R,(int)area);} 
            vec.clear();
            int nw = w+1; while(nw<=hw.we && hw.buckets[nw-hw.ws].empty()) ++nw;
            if(nw<=hw.we){ hw.nextw=nw; gpq.push({1LL*h*hw.nextw, h}); }
            else{
                if(hw.we==m) continue; // finished height
                hw.ws = hw.we + 1; hw.we = min(m, hw.ws + B - 1); hw.buckets.assign(hw.we - hw.ws + 1, {}); hw.nextw=m+1;
                build_window(hw);
                if(hw.nextw<=m) gpq.push({1LL*h*hw.nextw, h});
            }
        }

        if(!trans){
            for(int i=0;i<n;++i){
                for(int j=0;j<m;++j){ if(j) cout<<' '; cout<<ans[i][j]; } cout<<'\n';
            }
        }else{
            for(int i=0;i<m;++i){
                for(int j=0;j<n;++j){ if(j) cout<<' '; cout<<ans[j][i]; } cout<<'\n';
            }
        }
        if(T) cout<<"\n";
    }
    return 0;
}


