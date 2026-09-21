import json,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import glob
for f in glob.glob('/usr/share/fonts/**/DejaVuSans*.ttf',recursive=True): fm.fontManager.addfont(f)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#8a8f80','axes.labelcolor':'#18200f','xtick.color':'#555b4a','ytick.color':'#555b4a','axes.grid':True,'grid.color':'#e4e6df','grid.linewidth':0.8})
O=json.load(open('fig2_out.json')); Ns=sorted(int(k) for k in O)
def arr(k,key): return np.array([[r[key] for r in O[str(n)]] for n in Ns],float)
Mg,H,Sp=arr(0,'Mg'),arr(0,'H'),arr(0,'Simp')
mean=lambda a:a.mean(1); lo=lambda a:np.percentile(a,2.5,axis=1); hi=lambda a:np.percentile(a,97.5,axis=1)
G='#3d6b1c'; OR='#d9531e'; BL='#2a78d6'
fig,ax=plt.subplots(1,2,figsize=(11,4.3),dpi=300)
a=ax[0]
a.fill_between(Ns,lo(Mg),hi(Mg),color=G,alpha=.18,lw=0)
a.plot(Ns,mean(Mg),color=G,lw=2,marker='o',ms=6,mfc='white',mew=1.8)
a.set_xscale('log'); a.set_xticks(Ns); a.set_xticklabels([f'{n:,}'.replace(',','.') for n in Ns],rotation=0,fontsize=9)
a.minorticks_off(); a.set_xlabel('Tamaño de la muestra (N, individuos)'); a.set_ylabel('Margalef  (S − 1) / ln N')
a.text(0.02,0.96,'a',transform=a.transAxes,fontsize=16,fontweight='bold',va='top')
a.set_ylim(0,None)
b=ax[1]
rel=lambda A:A/A[-1].mean()
for A,c,ls,mk,lab in [(Sp,BL,'-','s','Simpson (1 − D)'),(H,OR,'--','^','Shannon (H′)'),(Mg,G,':','o','Margalef')]:
    R=rel(A); b.fill_between(Ns,np.percentile(R,2.5,axis=1),np.percentile(R,97.5,axis=1),color=c,alpha=.12,lw=0)
    b.plot(Ns,R.mean(1),color=c,lw=2,ls=ls,marker=mk,ms=6,mfc='white',mew=1.6,label=lab)
b.axhline(1,color='#8a8f80',lw=1,ls=(0,(1,3)))
b.set_xscale('log'); b.set_xticks(Ns); b.set_xticklabels([f'{n:,}'.replace(',','.') for n in Ns],fontsize=9); b.minorticks_off()
b.set_xlabel('Tamaño de la muestra (N, individuos)'); b.set_ylabel('Valor relativo al obtenido con N = 5.000')
b.set_ylim(0,1.3)
b.legend(frameon=False,loc='lower right',fontsize=10)
b.text(0.02,0.96,'b',transform=b.transAxes,fontsize=16,fontweight='bold',va='top')
plt.tight_layout(); plt.savefig('figura2.png',dpi=300,facecolor='white')
print('Mg mean',np.round(mean(Mg),2)); print('rel Sp',np.round(rel(Sp).mean(1),3)); print('rel H',np.round(rel(H).mean(1),3)); print('rel Mg',np.round(rel(Mg).mean(1),3))
