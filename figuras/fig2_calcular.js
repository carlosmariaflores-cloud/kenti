const fs=require('fs');
const src=fs.readFileSync(__dirname+'/../verificacion/kenti_core.js','utf8');
const pcaVarDefs=()=>[];
eval(src+';globalThis.K={alpha}');
const I=JSON.parse(fs.readFileSync(__dirname+'/fig2_in.json','utf8'));
const out={};
for(const n of I.Ns){out[n]=I.samples[n].map(v=>{const a=K.alpha(v);return {S:a.S,N:a.N,H:a.H,Simp:a.Simp,Mg:a.Mg,J:a.J};});}
fs.writeFileSync(__dirname+'/fig2_out.json',JSON.stringify(out));
