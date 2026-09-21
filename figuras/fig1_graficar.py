# Figura 1: dibuja con matplotlib los resultados calculados por fig1_calcular.js (funciones de Kenti).
import json,numpy as np,matplotlib,glob
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
for f in glob.glob('/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyrepagella-*.otf'): fm.fontManager.addfont(f)
plt.rcParams.update({'font.family':'TeX Gyre Pagella','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':0.8,'mathtext.fontset':'stix'})
O=json.load(open('fig1_out.json'))
sites=O['sites']; n=len(sites); BC=np.array(O['bc'])
fig=plt.figure(figsize=(7.2,6.6),dpi=300)
gs=fig.add_gridspec(2,2,height_ratios=[1,1.15],hspace=0.38,wspace=0.32,left=0.08,right=0.98,top=0.92,bottom=0.08)
def tag(ax,l): ax.text(-0.02,1.06,l,transform=ax.transAxes,fontsize=13,fontweight='bold',va='bottom',ha='right')
# a) matriz de Bray-Curtis
a=fig.add_subplot(gs[0,0]); tag(a,'a')
Mm=np.ma.masked_where(np.eye(n,dtype=bool),BC)
im=a.imshow(Mm,cmap='Greens',vmin=0.3,vmax=1,aspect='equal')
for i in range(n):
    for j in range(n):
        if i!=j:
            a.text(j,i,f'{BC[i,j]:.2f}',ha='center',va='center',fontsize=7.5,color='white' if BC[i,j]>0.6 else 'black')
a.set_xticks(range(n)); a.set_yticks(range(n)); a.set_xticklabels(sites); a.set_yticklabels(sites)
a.xaxis.tick_top(); a.tick_params(length=0)
for s in a.spines.values(): s.set_visible(False)
# b) dendrograma UPGMA
b=fig.add_subplot(gs[0,1]); tag(b,'b')
order=[]
def leaves(t):
    if 'left' not in t: order.append(t['members'][0]); return
    leaves(t['left']); leaves(t['right'])
leaves(O['tree']); ypos={m:i for i,m in enumerate(order)}
def draw(t):
    if 'left' not in t: return ypos[t['members'][0]],1.0
    yl,hl=draw(t['left']); yr,hr=draw(t['right']); h=t['h']
    b.plot([hl,h,h,hr],[yl,yl,yr,yr],color='black',lw=1)
    return (yl+yr)/2,h
draw(O['tree'])
b.set_xlim(1,0); b.set_ylim(n-0.5,-0.5); b.set_yticks(range(n)); b.set_yticklabels([sites[m] for m in order])
b.set_xlabel('Similitud de Bray-Curtis'); b.spines['left'].set_visible(False); b.tick_params(axis='y',length=0)
b.text(0.98,0.08,f"Correlación cofenética = {O['ccc']:.3f}",transform=b.transAxes,ha='right',fontsize=8)
# c) biplot PCA
c=fig.add_subplot(gs[1,0]); tag(c,'c')
sc1,sc2=np.array(O['scores'][0]),np.array(O['scores'][1]); L=np.array([O['loadings'][0],O['loadings'][1]]).T
k=0.85*max(abs(sc1).max(),abs(sc2).max())/np.abs(L).max()
c.axhline(0,color='#999999',lw=0.6,ls='--'); c.axvline(0,color='#999999',lw=0.6,ls='--')
for i,s in enumerate(sites):
    c.plot(sc1[i],sc2[i],'o',color='black',ms=5); c.annotate(s,(sc1[i],sc2[i]),xytext=(4,4),textcoords='offset points',fontsize=8)
lab={'S':'S','N':'N','J':'J′','H':'H′'}
for v,(lx,ly) in zip(O['vars'],L):
    c.annotate('',xy=(lx*k,ly*k),xytext=(0,0),arrowprops=dict(arrowstyle='-|>',color='#d9531e',lw=1.4))
    c.text(lx*k*1.1,ly*k*1.1,lab[v],color='#d9531e',fontsize=9,ha='center',va='center',fontweight='bold')
c.set_xlabel(f"CP 1 ({O['pct'][0]:.1f}%)"); c.set_ylabel(f"CP 2 ({O['pct'][1]:.1f}%)")
lim=max(abs(sc1).max(),abs(sc2).max(),np.abs(L).max()*k)*1.25; c.set_xlim(-lim,lim); c.set_ylim(-lim,lim); c.set_aspect('equal')
# d) varianza explicada
d=fig.add_subplot(gs[1,1]); tag(d,'d')
p=O['pct']; d.bar(range(len(p)),p,color='#2a78d6',width=0.6)
for i,v in enumerate(p): d.text(i,v+1.5,f'{v:.1f}%',ha='center',fontsize=8)
d.set_xticks(range(len(p))); d.set_xticklabels([f'CP {i+1}' for i in range(len(p))]); d.set_ylim(0,100)
d.set_ylabel('Varianza explicada (%)'); d.set_xlabel('Eje')
fig.savefig('figura1.png',dpi=300,facecolor='white'); print('ok')
