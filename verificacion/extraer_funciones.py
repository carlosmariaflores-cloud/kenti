"""Extrae, sin modificarlas, las funciones de cálculo de Kenti Libre 0.3 (archivo HTML) a kenti_core.js."""
import re,sys
src=sys.argv[1] if len(sys.argv)>1 else '../web/Kenti-Libre-0.3.html'
h=open(src,encoding='utf-8').read()
def func(name):
    m=re.search(r'^function '+name+r'\s*\(',h,re.M); i=m.start(); j=h.index('{',i); d=0
    for k in range(j,len(h)):
        if h[k]=='{': d+=1
        elif h[k]=='}':
            d-=1
            if d==0: return h[i:k+1]
def line(prefix): return re.search(r'^'+re.escape(prefix)+r'.*$',h,re.M).group(0)
parts=[func(n) for n in ['alpha','jaccard','morisitaHorn','brayCurtis','pearson','upgma','lgamma','betacf','ibeta','regression','jacobiEigen','pcaCompute']]
parts+=[line('const tPValue'),line('function tCrit'),line('const okNum')]
open('kenti_core.js','w').write('\n'.join(parts)); print('ok',len('\n'.join(parts)))
