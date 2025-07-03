mod=998244353
inv6=pow(6,mod-2,mod)
prob=[(k*inv6)%mod for k in range(7)]
inv_prob=[0, pow(prob[1],mod-2,mod), pow(prob[2],mod-2,mod), pow(prob[3],mod-2,mod), pow(prob[4],mod-2,mod),pow(prob[5],mod-2,mod),pow(prob[6],mod-2,mod)]
print(prob)
print(inv_prob)
