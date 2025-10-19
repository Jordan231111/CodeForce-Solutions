#include <bits/stdc++.h>
using namespace std;
#ifdef LOCAL
#include "algo/debug.h"
#else
#define debug(...) 42
#endif

struct DSU {
    int n;
    vector<int> p, sz;
    DSU() : n(0) {}
    DSU(int n_){init(n_);}    
    void init(int n_){ n=n_; p.resize(n); sz.assign(n,1); iota(p.begin(),p.end(),0);}    
    int find(int a){ while(a!=p[a]){ p[a]=p[p[a]]; a=p[a]; } return a; }
    bool unite(int a,int b){ a=find(a); b=find(b); if(a==b) return false; if(sz[a]<sz[b]) swap(a,b); p[b]=a; sz[a]+=sz[b]; return true; }
};

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T; if(!(cin>>T)) return 0;
    while(T--){
        int n,k,s,q; cin>>n>>k>>s>>q;
        vector<vector<int>> g(n+1);
        for(int i=0;i<n-1;i++){int u,v;cin>>u>>v; g[u].push_back(v); g[v].push_back(u);}        
        vector<int> par(n+1,0), depth(n+1,0);
        {
            deque<int> dq; dq.push_back(1); par[1]=0; depth[1]=0;
            while(!dq.empty()){
                int u=dq.front(); dq.pop_front();
                for(int v:g[u]) if(v!=par[u]){ par[v]=u; depth[v]=depth[u]+1; dq.push_back(v);}            
            }
        }

        vector<vector<int>> nodeColors(n+1);
        nodeColors.shrink_to_fit();
        for(int i=0;i<s;i++){int v,x;cin>>v>>x; nodeColors[v].push_back(x);}        
        int m=0;
        vector<vector<pair<int,int>>> nodePairs(n+1);
        nodePairs.shrink_to_fit();
        for(int u=1;u<=n;u++){
            auto &vc = nodeColors[u];
            sort(vc.begin(), vc.end());
            vc.erase(unique(vc.begin(), vc.end()), vc.end());
            nodePairs[u].reserve(vc.size());
            for(int x:vc){ nodePairs[u].push_back({x, m++}); }
        }
        DSU dsu(m);
        auto find_mem = [&](const vector<pair<int,int>>& a, int x)->int{
            int l=0,r=(int)a.size();
            while(l<r){ int mid=(l+r)>>1; if(a[mid].first<x) l=mid+1; else r=mid; }
            if(l<(int)a.size() && a[l].first==x) return a[l].second; return -1;
        };
        for(int u=1;u<=n;u++){
            int p=par[u]; if(p==0) continue;
            const auto &au = nodePairs[u];
            const auto &ap = nodePairs[p];
            for(auto [x,idu]: au){ int idp = find_mem(ap, x); if(idp!=-1) dsu.unite(idu, idp); }
        }

        vector<int> U(q), V(q);
        for(int i=0;i<q;i++){ int u,v;cin>>u>>v; U[i]=u; V[i]=v; }

        vector<vector<int>> queriesAt(n+1);
        queriesAt.shrink_to_fit();
        for(int i=0;i<q;i++){ queriesAt[U[i]].push_back(i); queriesAt[V[i]].push_back(i); }

        unordered_map<int,int> rootToIdx;
        rootToIdx.reserve((size_t) (m*1.3)+1);
        vector<vector<int>> compNodes;
        compNodes.reserve(m);
        vector<int> memNode(m,0);
        for(int u=1;u<=n;u++) for(auto &pr:nodePairs[u]) memNode[pr.second]=u;
        for(int id=0;id<m;id++){
            int r = dsu.find(id);
            auto it = rootToIdx.find(r);
            if(it==rootToIdx.end()){
                int idx = (int)compNodes.size();
                rootToIdx.emplace(r, idx);
                compNodes.push_back(vector<int>());
                compNodes.back().push_back(memNode[id]);
            }else{
                compNodes[it->second].push_back(memNode[id]);
            }
        }

        int B = max(1, (int) sqrt(max(1, m)));
        vector<char> mark(n+1, 0);
        vector<int> ans(q,0);

        vector<int> compIdxBig; compIdxBig.reserve(compNodes.size());
        for(int i=0;i<(int)compNodes.size();i++) if((int)compNodes[i].size() >= B) compIdxBig.push_back(i);

        for(int idx: compIdxBig){
            auto &vec = compNodes[idx];
            for(int u:vec) mark[u]=1;
            for(int i=0;i<q;i++) ans[i] += (mark[U[i]] & mark[V[i]]);
            for(int u:vec) mark[u]=0;
        }

        vector<int> degQ(n+1,0);
        for(int u=1;u<=n;u++) degQ[u] = (int)queriesAt[u].size();

        unordered_map<unsigned long long, vector<int>> byPair;
        byPair.reserve((size_t)(q*1.3)+1);
        for(int i=0;i<q;i++){
            int a=U[i], b=V[i]; if(a>b) swap(a,b);
            unsigned long long key = ( (unsigned long long)a << 32 ) | (unsigned long long)b;
            byPair[key].push_back(i);
        }

        for(int i=0;i<(int)compNodes.size();i++){
            if((int)compNodes[i].size() >= B) continue;
            auto &vec = compNodes[i];
            long long sumDeg = 0; for(int u:vec) sumDeg += degQ[u];
            int t = (int)vec.size();
            if(sumDeg <= 1LL*t*t){
                for(int u:vec) mark[u]=1;
                for(int u:vec){
                    const auto &qs = queriesAt[u];
                    for(int id: qs){ int a=U[id], b=V[id]; int w = a ^ b ^ u; if(mark[w]) ans[id]++; }
                }
                for(int u:vec) mark[u]=0;
            }else{
                for(int ii=0;ii<t;ii++){
                    int a = vec[ii];
                    for(int jj=ii;jj<t;jj++){
                        int b = vec[jj];
                        int x=a, y=b; if(x>y) swap(x,y);
                        unsigned long long key = ( (unsigned long long)x << 32 ) | (unsigned long long)y;
                        auto it = byPair.find(key);
                        if(it!=byPair.end()){
                            auto &vlist = it->second;
                            for(int id: vlist) ans[id]++;
                        }
                    }
                }
            }
        }

        for(int i=0;i<q;i++){
            cout<<ans[i]<<" ";
        }
        cout<<'\n';
    }
}


