#include <bits/stdc++.h>
using namespace std;

static inline int read_int() { int x; if(!(cin>>x)) exit(0); return x; }

static int solve_small(vector<int> p, int N, int K){
    int n = N*K;
    auto is_sorted = [&](const vector<int>& a){
        for(int i=1;i<n;i++) if(a[i-1]>a[i]) return 0; return 1;
    };
    auto key = [&](const vector<int>& a){ string s; s.resize(4*n); char* c=s.data(); int idx=0; for(int v: a){ c[idx++]=(char)(v>>24); c[idx++]=(char)(v>>16); c[idx++]=(char)(v>>8); c[idx++]=(char)(v); } return s; };

    queue<string> q; unordered_map<string,int> dist; unordered_map<string,int> best;
    string s0 = key(p); q.push(s0); dist[s0]=0; best[s0]=0;
    int ansDist = -1; int ansBest = 0;

    while(!q.empty()){
        string s = q.front(); q.pop();
        vector<int> a(n); for(int i=0;i<n;i++){ unsigned char b0=s[4*i+3]; unsigned char b1=s[4*i+2]; unsigned char b2=s[4*i+1]; unsigned char b3=s[4*i]; a[i]= (b3<<24)|(b2<<16)|(b1<<8)|b0; }
        int d = dist[s]; int b = best[s];
        if(is_sorted(a)){
            if(ansDist==-1 || d<ansDist || (d==ansDist && b>ansBest)){
                ansDist=d; ansBest=b;
            }
            continue;
        }
        if(ansDist!=-1 && d>=ansDist) continue;
        for(int i=0;i<n;i++) for(int j=i+1;j<n;j++){
            vector<int> bA=a; swap(bA[i], bA[j]);
            string sk = key(bA);
            int gain = ((abs(i-j)%N)==0) ? 1:0;
            int nb = b + gain;
            auto it = dist.find(sk);
            if(it==dist.end()){
                dist[sk]=d+1; best[sk]=nb; q.push(sk);
            }else if(it->second==d+1 && best[sk] < nb){
                best[sk]=nb; q.push(sk);
            }
        }
    }
    return ansBest;
}

int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int N,K; if(!(cin>>N>>K)) return 0; int n=N*K; vector<int> P(n); for(int i=0;i<n;i++) cin>>P[i];
    if(n>9){ cout<<-1<<"\n"; return 0; }
    cout<<solve_small(P,N,K)<<"\n"; return 0;
}
