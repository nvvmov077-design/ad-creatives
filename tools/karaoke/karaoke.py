# OnMind "read along" videos: a book page where words light up one by one, a finger follows, a word card pops up.
# 9:16, 30 fps, silent (voice to be added from the app's narration). Usage: python3 karaoke.py [out]
import base64, json, pathlib, shutil, subprocess, sys
from playwright.sync_api import sync_playwright

KIT = pathlib.Path('/home/claude/onmind-ad-kit'); HERE = KIT / 'karaoke'; A = HERE / 'assets'
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else HERE / 'out'); OUT.mkdir(parents=True, exist_ok=True)
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
FONTS = '\n'.join(f"@font-face{{font-family:'Onest';font-weight:100 900;src:url(data:font/woff2;base64,{b64(KIT/'fonts'/f'onest-{s}.woff2')}) format('woff2')}}" for s in ['cyr','cyr-ext','latin'])
LOGO = 'data:image/png;base64,' + b64(KIT/'logo@4x.png')
HAND = 'data:image/webp;base64,' + b64(A/'hand.webp')
cover = lambda n: 'data:image/webp;base64,' + b64(A/f'{n}.webp')
FPS = 30; WPS = 2.4  # words per second, a calm reading pace

CSS = f"""{FONTS}
*{{box-sizing:border-box;margin:0;padding:0}} html,body{{background:#0F1B14;width:1080px;height:1920px;overflow:hidden}}
.om{{position:relative;width:1080px;height:1920px;font-family:'Onest',sans-serif;letter-spacing:-0.02em;color:#000;background:#0F1B14}}
.bg{{position:absolute;inset:-40px;background-size:cover;background-position:50% 30%;filter:blur(28px) saturate(.8) brightness(.45)}}
.frame{{position:absolute;inset:0;padding:250px 48px 0;display:flex;flex-direction:column;align-items:center}}
.eyebrow{{display:inline-flex;align-items:center;gap:14px;height:62px;padding:0 28px;border-radius:100px;background:#00C945;color:#fff;font-weight:700;font-size:23px;letter-spacing:.08em;text-transform:uppercase;flex:none}}
.eyebrow i{{width:30px;height:30px;border-radius:50%;background:#fff;display:inline-block;position:relative}}
.eyebrow i::after{{content:'';position:absolute;left:10px;top:6px;width:8px;height:14px;border:solid #00C945;border-width:0 3.5px 3.5px 0;transform:rotate(45deg)}}
.head{{display:flex;flex-direction:column;align-items:center;transform:rotate(-2deg);margin:26px 0 34px;flex:none}}
.line{{display:block;background:#fff;font-weight:800;font-size:var(--hs,84px);line-height:1.04;padding:4px 26px 14px;border-radius:16px;margin-top:-4px;white-space:nowrap;box-shadow:0 6px 20px rgba(0,0,0,.3)}}
.line.hi{{background:#000;color:#fff}}
.coverc{{width:984px;height:300px;border-radius:28px;overflow:hidden;position:relative;flex:none;box-shadow:0 18px 50px rgba(0,0,0,.4)}}
.coverc img{{width:100%;height:100%;object-fit:cover}}
.coverc .t{{position:absolute;left:0;right:0;bottom:0;padding:70px 34px 26px;background:linear-gradient(to top,rgba(0,0,0,.78),rgba(0,0,0,0));color:#fff}}
.coverc .t small{{display:block;font-size:24px;font-weight:500;opacity:.85;margin-bottom:4px}}
.coverc .t b{{display:block;font-size:48px;font-weight:800;line-height:1.05}}
.card{{position:relative;width:984px;background:#fff;border-radius:30px;box-shadow:0 20px 60px rgba(0,0,0,.4);padding:34px 40px 36px;margin-top:22px;flex:none}}
.s{{margin-bottom:22px}}
.s .en{{font-size:44px;font-weight:600;line-height:1.3;letter-spacing:-0.015em}}
.s .ua{{font-size:29px;color:#5E6B63;line-height:1.3;margin-top:6px;font-weight:500}}
.w{{border-radius:8px;padding:0 6px;margin:0 -6px;transition:none}}
.w.on{{background:#00C945;color:#fff}}
.w.done{{color:#0A8C39}}
.pop{{position:absolute;width:560px;background:#fff;border-radius:24px;box-shadow:0 18px 50px rgba(0,0,0,.3);padding:22px 28px 0;border:1.5px solid #EEE;opacity:0;z-index:8}}
.pop .top{{display:flex;align-items:baseline;gap:14px}}
.pop .top b{{font-size:40px}}
.pop .top span{{font-size:28px;color:#8E8E93}}
.pop .tr{{font-size:36px;font-weight:600;margin:6px 0 18px;color:#00A83A}}
.pop .acts{{display:flex;border-top:1.5px solid #EEE;margin:0 -28px}}
.pop .acts div{{flex:1;text-align:center;padding:14px 0 16px;font-size:22px;font-weight:500;color:#222}}
.hand{{position:absolute;width:250px;z-index:6;transform-origin:50% 100%;filter:drop-shadow(0 10px 20px rgba(0,0,0,.35))}}
.foot{{position:absolute;left:0;right:0;top:1640px;display:flex;flex-direction:column;align-items:center}}
.foot .row{{display:flex;align-items:center;gap:18px}}
.logo{{height:60px;background:#fff;border-radius:100px;padding:9px 20px;box-sizing:content-box}}
.cta{{display:inline-flex;align-items:center;height:92px;padding:0 46px;border-radius:100px;background:#fff;color:#000;font-weight:700;font-size:35px}}
.cta::after{{content:'';width:16px;height:16px;border:solid #000;border-width:4px 4px 0 0;transform:rotate(45deg);margin-left:18px}}
.site{{margin-top:12px;color:rgba(255,255,255,.8);font-weight:600;font-size:24px}}
"""

VIDEOS = [
 dict(id='OMD_Read_Alice_V1_2645', cover='alice', author='Льюїс Керролл', title="Alice's Adventures in Wonderland",
      eyebrow='Англійська через книжки', head=['Цю історію ти знаєш.', 'Тепер англійською'], hs=74,
      text=[('Alice was sitting by her sister on the bank.', 'Аліса сиділа біля сестри на березі.'),
            ('She had nothing to do, and she was bored.', 'Їй не було чого робити, і їй було нудно.'),
            ('Suddenly a white rabbit with pink eyes ran past her.', 'Раптом повз неї пробіг білий кролик з рожевими очима.'),
            ('The rabbit took a watch out of its pocket and looked at it.', 'Кролик дістав з кишені годинник і подивився на нього.')],
      pops={'bank': ('/bæŋk/', 'берег'), 'bored': ('/bɔːrd/', 'знуджена'), 'pocket': ('/ˈpɒkɪt/', 'кишеня')}),
 dict(id='OMD_Read_Dorian_V1_2645', cover='dorian', author='Оскар Вайлд', title='The Picture of Dorian Gray',
      eyebrow='Англійська через книжки', head=['Читай класику', 'англійською'], hs=84,
      text=[('Basil Hallward is a talented artist who lives in London.', 'Безіл Голворд, талановитий художник, живе в Лондоні.'),
            ('He enjoys painting portraits of people.', 'Він любить малювати портрети людей.'),
            ('One afternoon Basil finishes a portrait of a young man.', 'Одного дня Безіл закінчує портрет молодого чоловіка.'),
            ('The young man is extremely beautiful.', 'Молодий чоловік надзвичайно гарний.')],
      pops={'talented': ('/ˈtæləntɪd/', 'талановитий'), 'portraits': ('/ˈpɔːrtrɪts/', 'портрети'), 'extremely': ('/ɪkˈstriːmli/', 'надзвичайно')}),
 dict(id='OMD_Read_Iliad_V1_2645', cover='iliad', author='Гомер', title='The Iliad',
      eyebrow='Англійська без словника', head=['Не знаєш слово?', 'Просто торкнись'], hs=84,
      text=[("Achilles' closest friend was Patroclus.", 'Найближчим другом Ахілла був Патрокл.'),
            ('He could not watch the Greeks suffer any longer.', 'Він більше не міг дивитися, як страждають греки.'),
            ('He went to Achilles and begged him to help.', 'Він пішов до Ахілла і благав його допомогти.'),
            ('The plan worked.', 'План спрацював.')],
      pops={'closest': ('/ˈkloʊsɪst/', 'найближчий'), 'suffer': ('/ˈsʌfər/', 'страждати'), 'begged': ('/beɡd/', 'благав')}),
 dict(id='OMD_Read_Sherlock_V1_2645', cover='sherlock', author='Артур Конан Дойл', title='The Adventures of Sherlock Holmes',
      eyebrow='Навчання для зайнятих людей', head=['10 хвилин книжки', 'англійською в день'], hs=76,
      text=[('It was a cold night in March.', 'Була холодна березнева ніч.'),
            ('Sherlock Holmes sat by the fire with his pipe.', 'Шерлок Холмс сидів біля каміна зі своєю люлькою.'),
            ('A letter lay on the table in front of him.', 'Перед ним на столі лежав лист.'),
            ('“We will have a visitor tonight,” he said.', '«Сьогодні ввечері в нас буде гість», сказав він.')],
      pops={'pipe': ('/paɪp/', 'люлька'), 'letter': ('/ˈletər/', 'лист'), 'visitor': ('/ˈvɪzɪtər/', 'гість')}),
 dict(id='OMD_Read_Crusoe_V1_2645', cover='crusoe', author='Даніель Дефо', title='Robinson Crusoe',
      eyebrow='Англійська через книжки', head=['Твоя перша книжка', 'англійською'], hs=84,
      text=[('The ship broke on the rocks in the storm.', 'Корабель розбився об скелі під час шторму.'),
            ('I swam to the shore and fell on the sand.', 'Я доплив до берега і впав на пісок.'),
            ('I was alive, but I was alone on the island.', 'Я був живий, але я був сам на острові.'),
            ('The next morning I began to build a shelter.', 'Наступного ранку я почав будувати укриття.')],
      pops={'storm': ('/stɔːrm/', 'шторм'), 'shore': ('/ʃɔːr/', 'берег'), 'shelter': ('/ˈʃeltər/', 'укриття')}),
]

def html(v):
    lines = ''.join(f'<span class="line{" hi" if i==1 else ""}">{l}</span>' for i, l in enumerate(v['head']))
    sents = ''
    wi = 0
    for en, ua in v['text']:
        words = ''
        for w in en.split(' '):
            words += f'<span class="w" data-i="{wi}">{w}</span> '
            wi += 1
        sents += f'<div class="s"><div class="en">{words}</div><div class="ua">{ua}</div></div>'
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="om" style="--hs:{v['hs']}px"><div class="bg" style="background-image:url({cover(v['cover'])})"></div>
<div class="frame"><div class="eyebrow"><i></i>{v['eyebrow']}</div><div class="head">{lines}</div>
<div class="coverc"><img src="{cover(v['cover'])}"><div class="t"><small>{v['author']}</small><b>{v['title']}</b></div></div>
<div class="card" id="card">{sents}
<div class="pop" id="pop"><div class="top"><b id="pw"></b><span id="pp"></span></div><div class="tr" id="pt"></div><div class="acts"><div>▶ Відтворити</div><div>🔖 Обране</div></div></div>
<img class="hand" id="hand" src="{HAND}"></div></div>
<div class="foot"><div class="row"><img class="logo" src="{LOGO}"><div class="cta">Скласти мій план</div></div><div class="site">onmind.coach</div></div></div></body></html>"""

JS = """([t, pops, wps]) => {
 const words=[...document.querySelectorAll('.w')]; const n=words.length;
 const lead=0.8; const k=Math.floor((t-lead)*wps); const cur=Math.min(n-1, Math.max(-1,k));
 words.forEach((w,i)=>{ w.classList.toggle('on', i===cur); w.classList.toggle('done', i<cur); });
 const card=document.getElementById('card').getBoundingClientRect();
 const hand=document.getElementById('hand'), pop=document.getElementById('pop');
 if (cur<0) { hand.style.opacity=0; pop.style.opacity=0; return; }
 const r=words[cur].getBoundingClientRect();
 // finger tip at the word's bottom centre; hand image tip is at about (33%, 2%) of the image
 const x=r.left-card.left+r.width/2, y=r.top-card.top+r.height*0.95;
 hand.style.opacity=1; hand.style.left=(x-250*0.33+6)+'px'; hand.style.top=(y-250*1.357*0.03)+'px'; hand.style.transform='rotate(-10deg)';
 // word card: hold on a pop word for 1.1 s of its 1/wps slot... we pause reading instead: handled in python by a time warp
 const txt=words[cur].textContent.replace(/[^A-Za-z']/g,'').toLowerCase();
 const p=pops[txt];
 if (p) { document.getElementById('pw').textContent=txt; document.getElementById('pp').textContent=p[0]; document.getElementById('pt').textContent=p[1];
   pop.style.opacity=1; pop.style.left=Math.max(10, Math.min(card.width-580, x-280))+'px'; pop.style.top=(y+70)+'px'; }
 else pop.style.opacity=0;
}"""

def timeline(v):
    # Reading time per word is 1/WPS, except pop words, which hold for 1.6 s so the card can be read.
    n = sum(len(en.split(' ')) for en, _ in v['text'])
    t = 0.8; times = []
    wi = 0
    for en, _ in v['text']:
        for w in en.split(' '):
            key = ''.join(c for c in w if c.isalpha() or c == "'").lower()
            dur = 1.6 if key in v['pops'] else 1 / WPS
            times.append((t, t + dur)); t += dur; wi += 1
        t += 0.25  # breath between sentences
    return times, t + 1.4  # tail hold

def main():
  with sync_playwright() as pw:
      b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
      for v in VIDEOS:
          times, total = timeline(v)
          fr = OUT / 'frames'; shutil.rmtree(fr, ignore_errors=True); fr.mkdir()
          pg.set_content(html(v)); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(250)
          nf = int(total * FPS)
          for f in range(nf):
              t = f / FPS
              cur = -1
              for i, (a, z) in enumerate(times):
                  if a <= t < z: cur = i
              if t >= times[-1][1]: cur = len(times) - 1
              # drive by index: feed a synthetic time so that floor((t-lead)*wps) == cur
              pg.evaluate(JS, [0.8 + (cur + 0.5) / WPS if cur >= 0 else 0, v['pops'], WPS])
              pg.screenshot(path=str(fr / f'{f:04d}.jpg'), type='jpeg', quality=92, clip=dict(x=0, y=0, width=1080, height=1920))
          mp4 = OUT / f"{v['id']}.mp4"
          subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', str(FPS), '-i', str(fr / '%04d.jpg'),
                          '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'medium', '-movflags', '+faststart', '-c:a', 'aac', str(mp4)], check=True)
          shutil.copy(fr / f'{int(2.5*FPS):04d}.jpg', OUT / f"{v['id']}_thumb.jpg")
          for s, nme in [(1, 'a'), (int(total*0.4), 'b'), (int(total*0.7), 'c')]:
              shutil.copy(fr / f'{min(nf-1, s*FPS):04d}.jpg', OUT / f"{v['id']}_{nme}.jpg")
          shutil.rmtree(fr)
          print(v['id'], round(total, 1), 's')
      b.close()


if __name__=='__main__': main()
