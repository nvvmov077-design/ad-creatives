# 9:16 Reels: the reader plays, the highlight moves line by line, then a tap opens the word card.
# Usage: python3 video.py out
import sys, subprocess, pathlib, shutil
from playwright.sync_api import sync_playwright
import books
from books import FONTS, CSS, LOGO, photo, SPK, PLAY, SAVE

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'out'); OUT.mkdir(exist_ok=True)
FR = OUT / 'frames'; shutil.rmtree(FR, ignore_errors=True); FR.mkdir()
FPS, SEC = 30, 11
NAME = 'OMD_Books_Reel_V2_2645'

LINES = [
 ('Achilles’ closest friend was Patroclus.', 'Найближчим другом Ахілла був Патрокл.'),
 ('He went to <span class="g" id="ach">Achilles</span> and begged him to help.', 'Він пішов до Ахілла і благав його допомогти.'),
 ('The plan worked.', 'План спрацював.'),
]
EXTRA = """
.om{height:1920px}
.frame{padding:170px 40px 400px}

.card{width:1010px}
.s{transition:none}
.pop{opacity:0}
.tap{opacity:0}
.cap{position:absolute;left:0;right:0;bottom:330px;text-align:center}
"""
rows = ''.join(f'<div class="s" id="s{i}"><i class="tri"></i><div><div class="en">{en}</div><div class="ua">{ua}</div></div></div>' for i, (en, ua) in enumerate(LINES))
HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}{CSS}{EXTRA}</style></head><body>
<div class="om" style="--hs:84px"><div class="bg" style="background-image:url({photo('sofa')})"></div>
<div class="frame"><div class="eyebrow"><i></i>Англійська через книжки</div>
<div class="head" id="head"><span class="line">Читай і слухай</span><span class="line hi">книжки англійською</span></div>
<div class="mid"><div class="card" id="card"><div class="book"><i class="dot"></i><b>The Iliad</b> · Гомер</div>{rows}
<div class="player"><div class="pl"><svg width="26" height="26" viewBox="0 0 24 24"><path d="M6 5h4v14H6zM14 5h4v14h-4z" fill="#fff"/></svg></div><div class="meta"><div class="t">The Iliad <span id="time">0:05:35 / 0:13:12</span></div><div class="bar"><i id="bi"></i><b id="bb"></b></div></div></div>
<div class="pop" id="pop"><div class="top"><b>Achilles</b><span>/əˈkɪliːz/</span><span class="spk">{SPK}</span></div><div class="tr">Ахілл</div><div class="acts"><div>{PLAY}Відтворити</div><div>{SAVE}Обране</div></div></div>
<div class="tap" id="tap"></div></div></div>
<div class="foot"><div class="row"><img class="logo" src="{LOGO}"><div class="cta">{books.CTA}</div></div><div class="site">onmind.coach</div></div></div></div></body></html>"""

JS = """(t) => {
 const ease = x => x<0?0:x>1?1:1-Math.pow(1-x,3);
 const cur = t<3.0?0 : 1;
 for (let i=0;i<3;i++) document.getElementById('s'+i).classList.toggle('now', i===cur);
 const p = 30 + Math.min(t,7.2)/7.2*14;
 document.getElementById('bi').style.width = p+'%'; document.getElementById('bb').style.left = p+'%';
 const sec = 335 + Math.floor(Math.min(t,7.2)*1.3); const mm = Math.floor(sec/60), ss = String(sec%60).padStart(2,'0');
 document.getElementById('time').textContent = `0:0${mm}:${ss} / 0:13:12`;
 const card = document.getElementById('card').getBoundingClientRect(), a = document.getElementById('ach').getBoundingClientRect();
 const tap = document.getElementById('tap'), pop = document.getElementById('pop');
 const tx = a.left - card.left + a.width/2 - 48, ty = a.top - card.top + a.height/2 - 48;
 const k = ease((t-6.0)/0.5); tap.style.left = tx+'px'; tap.style.top = ty+'px';
 tap.style.opacity = t<6 ? 0 : t<7.4 ? k : Math.max(0, 1-(t-7.4)/0.4); tap.style.transform = `scale(${0.6+0.4*k})`;
 const q = ease((t-6.6)/0.45); pop.style.opacity = q; pop.style.left = Math.max(10, tx-120)+'px';
 pop.style.top = (ty+110+20*(1-q))+'px';
 const h = ease(t/0.5); document.getElementById('head').style.opacity = h;
}"""

with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.set_content(HTML); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
    for f in range(FPS * SEC):
        pg.evaluate(JS, f / FPS)
        pg.screenshot(path=str(FR / f'{f:04d}.png'), clip=dict(x=0, y=0, width=1080, height=1920))
    b.close()
mp4 = OUT / f'{NAME}.mp4'
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', str(FPS), '-i', str(FR / '%04d.png'),
                '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'medium', '-movflags', '+faststart',
                '-c:a', 'aac', str(mp4)], check=True)
for t, n in [(1, 'a'), (3.5, 'b'), (5.5, 'c'), (8, 'd')]:
    shutil.copy(FR / f'{int(t*FPS):04d}.png', OUT / f'reel_{n}.png')
shutil.copy(FR / f'{int(8*FPS):04d}.png', OUT / f'{NAME}_thumb.png')
shutil.rmtree(FR)
print(mp4, mp4.stat().st_size)
