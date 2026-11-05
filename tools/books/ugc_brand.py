# Adds OnMind branding to creator clips: eyebrow pill + headline sticker at top, logo + CTA near the bottom, end card.
# Usage: python3 brand.py
import base64, pathlib, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / 'books'))
from playwright.sync_api import sync_playwright

KIT = pathlib.Path('/home/claude/onmind-ad-kit'); HERE = KIT / 'ugc2645'
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
FONTS = '\n'.join(f"@font-face{{font-family:'Onest';font-weight:100 900;src:url(data:font/woff2;base64,{b64(KIT/'fonts'/f'onest-{s}.woff2')}) format('woff2')}}" for s in ['cyr','cyr-ext','latin'])
LOGO = 'data:image/png;base64,' + b64(KIT/'logo@4x.png')
CSS = f"""{FONTS}
*{{box-sizing:border-box;margin:0;padding:0}} html,body{{background:transparent;width:1080px;height:1920px;overflow:hidden}}
.ov{{position:relative;width:1080px;height:1920px;font-family:'Onest',sans-serif;letter-spacing:-0.02em}}
.top{{position:absolute;left:0;right:0;top:var(--top,250px);display:flex;flex-direction:column;align-items:center;gap:22px}}
.eyebrow{{display:inline-flex;align-items:center;gap:14px;height:62px;padding:0 28px;border-radius:100px;background:#00C945;color:#fff;font-weight:700;font-size:23px;letter-spacing:.08em;text-transform:uppercase;box-shadow:0 6px 20px rgba(0,0,0,.35)}}
.eyebrow i{{width:30px;height:30px;border-radius:50%;background:#fff;display:inline-block;position:relative}}
.eyebrow i::after{{content:'';position:absolute;left:10px;top:6px;width:8px;height:14px;border:solid #00C945;border-width:0 3.5px 3.5px 0;transform:rotate(45deg)}}
.head{{display:flex;flex-direction:column;align-items:center;transform:rotate(-2deg)}}
.line{{display:block;background:#fff;color:#000;font-weight:800;font-size:var(--hs,80px);line-height:1.04;padding:4px 26px 14px;border-radius:16px;margin-top:-4px;white-space:nowrap;box-shadow:0 6px 20px rgba(0,0,0,.3)}}
.line.hi{{background:#000;color:#fff}}
.foot{{position:absolute;left:0;right:0;top:var(--foot,1300px);display:flex;justify-content:center;align-items:center;gap:18px}}
.logo{{height:60px;background:#fff;border-radius:100px;padding:9px 20px;box-sizing:content-box;box-shadow:0 6px 20px rgba(0,0,0,.35)}}
.cta{{display:inline-flex;align-items:center;height:92px;padding:0 46px;border-radius:100px;background:#fff;color:#000;font-weight:700;font-size:35px;box-shadow:0 6px 20px rgba(0,0,0,.35)}}
.foot.sm .logo{{height:48px;padding:7px 16px}} .foot.sm .cta{{height:74px;font-size:29px;padding:0 36px}} .foot.sm .cta::after{{width:13px;height:13px;border-width:3.5px 3.5px 0 0}}
.cta::after{{content:'';width:16px;height:16px;border:solid #000;border-width:4px 4px 0 0;transform:rotate(45deg);margin-left:18px}}
/* end card */
.end{{width:1080px;height:1920px;background:#0F1B14;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:40px;font-family:'Onest',sans-serif;letter-spacing:-0.02em}}
.end .logo{{height:110px;padding:16px 36px}}
.end .big{{color:#fff;font-weight:800;font-size:92px;line-height:1.05;text-align:center;max-width:960px}}
.end .big b{{color:#00C945;font-weight:800}}
.end .site{{color:rgba(255,255,255,.7);font-size:32px;font-weight:600;margin-top:10px}}
"""

def overlay(eyebrow, lines, hi, top=250, foot=1300, hs=80):
    head = ''.join(f'<span class="line{" hi" if i==hi else ""}">{l}</span>' for i,l in enumerate(lines)) if lines else ''
    topblock = f'<div class="top" style="--top:{top}px"><div class="eyebrow"><i></i>{eyebrow}</div>{"<div class=head>"+head+"</div>" if head else ""}</div>' if eyebrow else ''
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="ov" style="--hs:{hs}px">{topblock}<div class="foot{" sm" if foot<1400 else ""}" style="--foot:{foot}px"><img class="logo" src="{LOGO}"><div class="cta">Скласти мій план</div></div></div></body></html>'

END = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="end"><img class="logo" src="{LOGO}"><div class="big">Англійська у фоні<br>твого дня. <b>Почни сьогодні.</b></div><div class="cta">Скласти мій план</div><div class="site">onmind.coach</div></div></body></html>'

JOBS = [
 # id, source, eyebrow, headline lines, highlighted line, top, foot
 ('OMD_UGC_Grammar15_B1_2645', 'OMD_UGC_Grammar15_V1_2645.mp4', 'Навчання для зайнятих людей', ['10 хвилин', 'англійської в день'], 1, 250, 1392),
 ('OMD_UGC_Demo15_B1_2645',    'OMD_UGC_Demo15_V1_2645.mp4',    'Так виглядає урок', ['Фрази, які', 'скажеш уже сьогодні'], 1, 250, 1480),
 ('OMD_UGC_Grammar_B1_2645',   'OMD_UGC_Grammar_V1_2645.mp4',   '', [], None, 250, 1392),
 ('OMD_UGC_Demo_B1_2645',      'OMD_UGC_Demo_V1_2645.mp4',      '', [], None, 250, 1480),
]

with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={'width':1080,'height':1920})
    pg.set_content(END); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(200)
    pg.screenshot(path=str(HERE/'endcard.png'))
    for jid, src, eb, lines, hi, top, foot in JOBS:
        pg.set_content(overlay(eb, lines, hi, top, foot)); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(200)
        pg.screenshot(path=str(HERE/f'{jid}.overlay.png'), omit_background=True)
    b.close()

for jid, src, *_ in JOBS:
    out = HERE/f'{jid}.mp4'
    cmd = ['ffmpeg','-loglevel','error','-y','-i',str(HERE/src),'-i',str(HERE/f'{jid}.overlay.png'),'-loop','1','-t','2.5','-i',str(HERE/'endcard.png'),
           '-f','lavfi','-t','2.5','-i','anullsrc=r=48000:cl=stereo',
           '-filter_complex','[0:v][1:v]overlay=0:0:format=auto[v0];[2:v]scale=1080:1920,fps=30,format=yuv420p[v1];[v0][0:a][v1][3:a]concat=n=2:v=1:a=1[v][a]',
           '-map','[v]','-map','[a]','-c:v','libx264','-crf','20','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(out)]
    subprocess.run(cmd, check=True)
    subprocess.run(['ffmpeg','-loglevel','error','-y','-ss','1.5','-i',str(out),'-frames:v','1',str(HERE/f'{jid}_thumb.png')], check=True)
    print('done', jid)
