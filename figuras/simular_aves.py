import numpy as np, json
rng=np.random.default_rng(20260921)
S=30; sites=[('B1','Bosque 1'),('B2','Bosque 2'),('B3','Bosque 3'),('P1','Pastizal 1'),('P2','Pastizal 2'),('P3','Pastizal 3')]
# regional pool: log-series-like abundances; bosque favors first 18 spp, pastizal spp 10-30
base=np.array([max(0.3,40*np.exp(-0.16*i)) for i in range(S)])
w_b=np.array([1.0 if i<18 else 0.05 for i in range(S)]); w_p=np.array([0.05 if i<10 else 1.0 for i in range(S)])
rng.shuffle(base)
counts=[]
for k in range(6):
    w=w_b if k<3 else w_p
    mu=base*w*rng.uniform(0.7,1.4)
    counts.append(rng.poisson(mu))
counts=np.array(counts)
# esfuerzo: mismo esfuerzo (mismo n de puntos); mantener totales similares
species=[]
for i in range(S):
    species.append({'name':f'Especie {i+1:02d}','family':'','counts':{f's{k}':int(counts[k,i]) for k in range(6) if counts[k,i]>0}})
keep=[sp for sp in species if sp['counts']]
state={'sites':[{'id':f's{k}','code':c,'name':n,'estado':'relevado'} for k,(c,n) in enumerate(sites)],'species':keep,'unit':'individuos','example':False,'formato':2}
json.dump({'state':state,'counts':counts.tolist()},open('sim_state.json','w'))
print(counts.sum(1), (counts>0).sum(1), len(keep))
