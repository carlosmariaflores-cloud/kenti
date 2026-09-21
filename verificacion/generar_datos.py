import numpy as np, json
rng=np.random.default_rng(20260921)
N=1000
def counts(S):
    kind=rng.integers(0,3)
    if kind==0: v=rng.poisson(rng.uniform(0.3,30),S)
    elif kind==1: v=rng.negative_binomial(0.5,rng.uniform(0.01,0.3),S)
    else: v=np.floor(rng.lognormal(1,1.5,S)*(rng.random(S)<rng.uniform(.2,.9))).astype(int)
    return v.astype(int)
alpha=[]
while len(alpha)<N:
    v=counts(int(rng.integers(2,80)))
    if v.sum()>0: alpha.append(v.tolist())
beta=[]
while len(beta)<N:
    S=int(rng.integers(3,80)); a=counts(S); b=counts(S)
    if a.sum()>0 and b.sum()>0 and ((a>0)|(b>0)).any(): beta.append([a.tolist(),b.tolist()])
upg=[]
def bc(a,b): return 2*np.minimum(a,b).sum()/(a+b).sum()
while len(upg)<N:
    n=int(rng.integers(3,13)); S=int(rng.integers(5,60))
    base=counts(S)+1
    V=[np.maximum(0,(base*rng.lognormal(0,rng.uniform(.2,1.2),S)*(rng.random(S)<.8)).round()).astype(int)+ (rng.random(S)<.02) for _ in range(n)]
    if any(v.sum()==0 for v in V): continue
    M=[[1.0 if i==j else bc(V[i],V[j]) for j in range(n)] for i in range(n)]
    upg.append({'M':M})
pca=[]
while len(pca)<N:
    n=int(rng.integers(4,31)); p=int(rng.integers(2,9))
    L=rng.normal(size=(p,int(rng.integers(1,p+1))))
    X=rng.normal(size=(n,L.shape[1]))@L.T+rng.normal(scale=rng.uniform(.1,1.5),size=(n,p))
    X=X*rng.uniform(.1,1000,size=p)+rng.uniform(-50,50,size=p)
    pca.append({'X':X.tolist()})
reg=[]
while len(reg)<N:
    n=int(rng.integers(3,41)); x=rng.normal(rng.uniform(-50,50),rng.uniform(.1,30),n)
    y=rng.uniform(-5,5)*x+rng.normal(size=n)*rng.uniform(.1,40)+rng.uniform(-100,100)
    reg.append({'x':x.tolist(),'y':y.tolist()})
t=[[float(rng.uniform(0,15)),int(rng.integers(1,60))] for _ in range(N)]
tcrit=[int(rng.integers(1,120)) for _ in range(N)]
json.dump({'alpha':alpha,'beta':beta,'upgma':upg,'pca':pca,'reg':reg,'t':t,'tcrit':tcrit},open('in.json','w'))
