#include <bits/stdc++.h>
using namespace std;
using int64 = long long;
const int MOD = 998244353;
inline int addmod(int a,int b){ int s=a+b; return s>=MOD? s-MOD : s; }
inline int submod(int a,int b){ int s=a-b; return s<0? s+MOD : s; }
inline int mulmod(int64 a,int64 b){ return int(a*b%MOD); }
int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N,M; if(!(cin>>N>>M)) return 0;
    vector<vector<int>> C(N, vector<int>(N));
    for(int i=0;i<M;++i){
        int u,v; cin>>u>>v; --u; --v;
        if(u==v) continue; // self-loops ignored
        C[u][v] = addmod(C[u][v],1);
        C[v][u] = addmod(C[v][u],1);
    }
    const int INV2 = (MOD+1)/2;
    int ans = 0;

    // Enumerate cycles of length >=2 using smallest vertex trick
    for(int s=N-1; s>=0; --s){
        int SZ = s; // only vertices < s may appear in mask
        if(SZ==0) continue;
        int FULL = 1<<SZ;
        vector<vector<int>> dp(SZ, vector<int>(FULL));
        // initialise one-edge paths (s -> i)
        for(int i=0;i<SZ;++i) if(C[i][s]) dp[i][1<<i] = C[i][s];
        for(int mask=1; mask<FULL; ++mask){
            vector<int> visited, unvisited;
            for(int v=0; v<SZ; ++v){
                if(mask>>v & 1) visited.push_back(v);
                else unvisited.push_back(v);
            }
            bool enoughVisited = visited.size()>=2;
            for(int x: visited){
                int ways = dp[x][mask];
                if(!ways) continue;
                if(enoughVisited && C[x][s])
                    ans = addmod(ans, mulmod(ways, C[x][s]));
                for(int z: unvisited){
                    if(!C[x][z]) continue;
                    int nextMask = mask | (1<<z);
                    int &cell = dp[z][nextMask];
                    cell = addmod(cell, mulmod(ways, C[x][z]));
                }
            }
        }
    }

    ans = submod(ans, M); // remove single edges counted as cycles of length 1 in enumeration
    ans = mulmod(ans, INV2); // undirected cycles counted twice
    cout<<ans<<"\n";
    return 0;
}

