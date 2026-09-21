import numpy as np, json
rng=np.random.default_rng(20260921)
S=120; p=rng.lognormal(0,1.2,S); p/=p.sum()
Ns=[25,50,100,200,500,1000,2000,5000]; R=500
data={'Ns':Ns,'R':R,'samples':{str(n):[rng.multinomial(n,p).tolist() for _ in range(R)] for n in Ns}}
json.dump(data,open('fig2_in.json','w')); print(p.max(),p.min())
