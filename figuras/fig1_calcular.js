// Calcula con las funciones de Kenti (extraídas sin modificar) los resultados de la Figura 1.
const fs=require('fs');
const src=fs.readFileSync(__dirname+'/../verificacion/kenti_core.js','utf8');
globalThis.pcaVarDefs=()=>[{k:'S'},{k:'N'},{k:'J'},{k:'H'}];
globalThis.okNum=x=>x!=null&&isFinite(x);
eval(src+';globalThis.K={alpha,brayCurtis,upgma,pcaCompute}');
const S0=JSON.parse(fs.readFileSync(__dirname+'/sim_state.json','utf8'));
const I={sites:S0.state.sites.map(x=>x.code),names:S0.state.sites.map(x=>x.name),counts:S0.counts};
const n=I.counts.length;
const M=I.counts.map((a,i)=>I.counts.map((b,j)=>i===j?1:K.brayCurtis(a,b)));
const U=K.upgma(M);
const clean=t=>t.leaf?{leaf:true,members:t.members}:{h:t.h,members:t.members,left:clean(t.left),right:clean(t.right)};
const rows=I.counts.map(v=>{const a=K.alpha(v);return {S:a.S,N:a.N,J:a.J,H:a.H};});
const P=K.pcaCompute(rows,['S','N','J','H']);
const out={sites:I.sites,names:I.names,bc:M,ccc:U.ccc,tree:clean(U.root),
 vars:P.vars.map(v=>v.k),pct:P.comps.map(c=>c.pct),loadings:P.comps.map(c=>c.loadings),scores:P.comps.map(c=>c.scores)};
fs.writeFileSync(__dirname+'/fig1_out.json',JSON.stringify(out));
console.log('ccc',U.ccc.toFixed(3),'pct',P.comps.map(c=>c.pct.toFixed(1)).join(' '));
console.log(M.map(r=>r.map(x=>x.toFixed(2)).join(' ')).join('\n'));
