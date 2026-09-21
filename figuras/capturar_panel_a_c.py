from playwright.sync_api import sync_playwright
import json
st=json.load(open('sim_state.json'))['state']
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':1400,'height':1000},device_scale_factor=3)
    ctx.add_init_script("localStorage.setItem('kenti-libre-v1', %s)"%json.dumps(json.dumps(st)))
    pg=ctx.new_page()
    pg.goto('file://'+__import__('os').path.abspath('../web/Kenti-Libre-0.3.html')+''); pg.wait_for_timeout(800)
    pg.add_style_tag(content="body,.card,.panel,svg{background:#fff !important}")
    pg.click('#tab-beta'); pg.wait_for_timeout(300)
    pg.click('#cl-bc'); pg.wait_for_timeout(400)
    sv=pg.locator('#p-beta svg')
    sv.nth(2).screenshot(path='f_hm.png'); sv.nth(3).screenshot(path='f_dn.png')
    print(pg.evaluate("[...document.querySelectorAll('#p-beta *')].filter(e=>/cofen/i.test(e.textContent)&&e.children.length==0).map(e=>e.textContent)"))
    pg.click('#tab-pca'); pg.wait_for_timeout(400)
    n=pg.evaluate("document.querySelectorAll('#p-pca svg').length")
    for i in range(n):
        r=pg.evaluate(f"(()=>{{const r=document.querySelectorAll('#p-pca svg')[{i}].getBoundingClientRect();return [r.width,r.height]}})()"); print(i,r)
    sv=pg.locator('#p-pca svg')
    sv.nth(2).screenshot(path='f_bp.png'); sv.nth(3).screenshot(path='f_vr.png')
    print(pg.evaluate("document.querySelector('#p-pca').innerText.slice(0,300)"))
    b.close()
