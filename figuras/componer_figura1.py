from PIL import Image, ImageDraw, ImageFont
import glob
fb=[f for f in glob.glob('/usr/share/fonts/**/DejaVuSans-Bold.ttf',recursive=True)][0]
fr=fb.replace('-Bold','')
F=lambda s,b=False:ImageFont.truetype(fb if b else fr,s)
hm=Image.open('f_hm.png').convert('RGB'); dn=Image.open('f_dn.png').convert('RGB')
bp=Image.open('f_bp.png').convert('RGB'); vr=Image.open('f_vr2.png').convert('RGB').crop((0,0,1400,636))
W=3900; M=70; gap=90
dn2=dn.resize((int(dn.width*0.74),int(dn.height*0.74)),Image.LANCZOS)
hdr=110
row1h=max(hm.height,dn2.height)+hdr
row2h=max(bp.height,vr.height)+hdr
H=M+row1h+gap+row2h+M
im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im)
def label(x,y,letter,txt):
    d.text((x,y),letter,font=F(64,True),fill=(20,20,20)); d.text((x+70,y+12),txt,font=F(44),fill=(60,60,60))
y1=M
label(M,y1,'a','Similitud de Bray-Curtis')
im.paste(hm,(M,y1+hdr))
x2=M+hm.width+gap
label(x2,y1,'b','Agrupamiento UPGMA · correlación cofenética 0,993')
im.paste(dn2,(x2,y1+hdr+(hm.height-dn2.height)//2))
y2=M+row1h+gap
label(M,y2,'c','Análisis de componentes principales (PCA)')
im.paste(bp,(M,y2+hdr))
x3=M+bp.width+gap+120
label(x3,y2,'d','Varianza explicada por eje')
im.paste(vr,(x3,y2+hdr+300))
im.save('figura1.png',dpi=(300,300)); print(im.size)
