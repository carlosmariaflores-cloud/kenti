from playwright.sync_api import sync_playwright
import json
st=json.load(open('sim_state.json'))['state']
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':1400,'height':1000},device_scale_factor=3)
    ctx.add_init_script("localStorage.setItem('kenti-libre-v1', %s)"%json.dumps(json.dumps(st)))
    pg=ctx.new_page()
    pg.goto('file://'+__import__('os').path.abspath('../web/Kenti-Libre-0.3.html')+''); pg.wait_for_timeout(800)
    pg.add_style_tag(content="body,.card,.panel,svg{background:#fff !important}")
    pg.click('#tab-pca'); pg.wait_for_timeout(400)
    r=pg.evaluate("(()=>{const s=document.querySelectorAll('#p-pca svg')[3];s.scrollIntoView({block:'center'});const r=s.getBoundingClientRect();return [r.x,r.y,r.width,r.height, s.getAttribute('viewBox')]})()")
    print(r)
    pg.wait_for_timeout(200)
    r=pg.evaluate("(()=>{const r=document.querySelectorAll('#p-pca svg')[3].getBoundingClientRect();return [r.x,r.y,r.width,r.height]})()")
    pg.screenshot(path='f_vr2.png',clip={'x':r[0]-10,'y':r[1]-6,'width':r[2]+60,'height':r[3]+12})
    b.close()
