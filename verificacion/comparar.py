import json,numpy as np
from scipy import stats
from scipy.spatial.distance import jaccard as sj, braycurtis as sbc, squareform
from scipy.cluster.hierarchy import linkage, cophenet
import scipy, numpy
I=json.load(open('in.json')); O=json.load(open('out.json'))
R={}
def rec(name,n,absd,reld,extra=''):
    R[name]=(n,absd,reld,extra)
def mx(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    d=np.abs(a-b); rel=d/np.maximum(np.abs(b),1e-300)
    return d.max(), rel[np.abs(b)>1e-12].max() if (np.abs(b)>1e-12).any() else 0.0
# alpha
for key,fn in [('S',lambda v,N,S:S),('N',lambda v,N,S:N),
  ('H',lambda v,N,S:stats.entropy(v[v>0]/N)),
  ('D',lambda v,N,S:np.sum((v/N)**2)),
  ('Simp',lambda v,N,S:1-np.sum((v/N)**2)),
  ('Mg',lambda v,N,S:(S-1)/np.log(N) if N>1 else None),
  ('Mn',lambda v,N,S:S/np.sqrt(N)),
  ('J',lambda v,N,S:stats.entropy(v[v>0]/N)/np.log(S) if S>1 else None)]:
    a=[];b=[];skip=0
    for v,o in zip(I['alpha'],O['alpha']):
        v=np.array(v,float);N=v.sum();S=int((v>0).sum()); r=fn(v,N,S)
        if r is None:
            assert o[key] is None; skip+=1; continue
        a.append(o[key]);b.append(r)
    rec('alpha_'+key,len(a),*mx(a,b),f'nulos {skip}')
# beta
ja=[];jb=[];ma=[];mb=[];ba=[];bb=[]
for (a,b),o in zip(I['beta'],O['beta']):
    a=np.array(a,float);b=np.array(b,float)
    ja.append(o['jac']);jb.append(1-sj(a>0,b>0))
    pa=a/a.sum();pb=b/b.sum()
    ma.append(o['mh']);mb.append(2*np.sum(pa*pb)/(np.sum(pa**2)+np.sum(pb**2)))
    ba.append(o['bc']);bb.append(1-sbc(a,b))
rec('jaccard',len(ja),*mx(ja,jb));rec('morisita_horn',len(ma),*mx(ma,mb));rec('bray_curtis',len(ba),*mx(ba,bb))
# upgma
ca=[];cb=[];Ma=[];Mb=[];bad=0
for u,o in zip(I['upgma'],O['upgma']):
    M=np.array(u['M']);D=1-M;np.fill_diagonal(D,0)
    Z=linkage(squareform(D,checks=False),'average')
    c,cd=cophenet(Z,squareform(D,checks=False))
    ca.append(o['ccc']);cb.append(c)
    Ck=1-np.array(o['C']);np.fill_diagonal(Ck,0)
    Ma.append(Ck);Mb.append(squareform(cd))
d=[np.abs(x-y).max() for x,y in zip(Ma,Mb)]
rec('upgma_cophenetic_matrix',len(d),max(d),max(d))
rec('upgma_cophenetic_r',len(ca),*mx(ca,cb))
# pca
la=[];lb=[];ea=[];eb=[];sa=[];sb=[];skip=0
for p,o in zip(I['pca'],O['pca']):
    if 'error' in o: skip+=1; continue
    X=np.array(p['X']);C=np.corrcoef(X,rowvar=False)
    w,V=np.linalg.eigh(C);idx=np.argsort(w)[::-1];w=w[idx];V=V[:,idx]
    k=len(o['lam'])
    w=np.maximum(w[:k],0)
    la+=list(o['lam']);lb+=list(w)
    Z=(X-X.mean(0))/X.std(0,ddof=1)
    for j in range(k):
        # ignore near-zero eigenvalue axes (sign/direction undefined)
        if w[j]<1e-8: continue
        v=V[:,j]*np.sqrt(w[j]); l=np.array(o['load'][j]); 
        if np.dot(v,l)<0: v=-v
        ea+=list(l);eb+=list(v)
        s=Z@V[:,j]; sk=np.array(o['scores'][j])
        if np.dot(s,sk)<0: s=-s
        sa+=list(sk);sb+=list(s)
rec('pca_eigenvalues',len(la),*mx(la,lb),f'omitidos {skip}')
rec('pca_loadings',len(ea),*mx(ea,eb));rec('pca_scores',len(sa),*mx(sa,sb))
# regression
keys=['b1','b0','r','p','s','tc']
A={k:[] for k in keys};B={k:[] for k in keys};cia=[];cib=[];sk=0
for g,o in zip(I['reg'],O['reg']):
    if 'error' in o: sk+=1;continue
    x=np.array(g['x']);y=np.array(g['y']);L=stats.linregress(x,y);n=len(x);df=n-2
    resid=y-(L.intercept+L.slope*x);s=np.sqrt((resid**2).sum()/df)
    tc=stats.t.ppf(.975,df)
    ref={'b1':L.slope,'b0':L.intercept,'r':L.rvalue,'p':L.pvalue,'s':s,'tc':tc}
    for k in keys:A[k].append(o[k]);B[k].append(ref[k])
    cia.append(o['ci0']);cib.append(tc*s*np.sqrt(1/n+(0-x.mean())**2/((x-x.mean())**2).sum()))
for k in keys:
    a=np.array(A[k]);b=np.array(B[k]);d=np.abs(a-b)
    rec('reg_'+k,len(a),d.max(),(d/np.maximum(np.abs(b),1e-300))[np.abs(b)>1e-12].max())
rec('reg_ci95_halfwidth',len(cia),*mx(cia,cib))
# t
a=[o['p'] for o in O['t']];b=[2*stats.t.sf(t,df) for t,df in I['t']]
rec('t_pvalue',len(a),*mx(a,b))
a=O['tcrit'];b=[stats.t.ppf(.975,df) for df in I['tcrit']]
rec('t_critical_0.05',len(a),*mx(a,b))
print('numpy',numpy.__version__,'scipy',scipy.__version__)
for k,v in R.items(): print(f'{k:26s} n={v[0]:6d} max_abs={v[1]:.3e} max_rel={v[2]:.3e} {v[3]}')
json.dump({k:list(v) for k,v in R.items()},open('res.json','w'))
