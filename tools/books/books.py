# OnMind feature ads: books, V2. Reader card rebuilt from the real reader UI; type sized for a phone at arm's length.
# Each ad carries one persuasion idea (see ADS). Usage: python3 books.py out
import base64, sys, pathlib
from playwright.sync_api import sync_playwright

KIT = pathlib.Path(__file__).resolve().parent.parent
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 and __name__ == '__main__' else 'out'); OUT.mkdir(parents=True, exist_ok=True)
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
FONTS = '\n'.join(f"@font-face{{font-family:'Onest';font-weight:100 900;src:url(data:font/woff2;base64,{b64(KIT/'fonts'/f'onest-{s}.woff2')}) format('woff2')}}" for s in ['cyr', 'cyr-ext', 'latin'])
LOGO = 'data:image/png;base64,' + b64(KIT/'logo@4x.png')
photo = lambda n: 'data:image/webp;base64,' + b64(KIT/'photos'/f'{n}.webp')
CTA = 'Скласти мій план'

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#000}
.om{position:relative;overflow:hidden;width:1080px;height:1350px;font-family:'Onest',sans-serif;letter-spacing:-0.02em;color:#000;background:#0F1B14}
.bg{position:absolute;inset:-30px;background-size:cover;background-position:var(--focus,50% 50%);filter:blur(6px) saturate(.85) brightness(.42)}
.frame{position:absolute;inset:0;padding:54px 48px 46px;display:flex;flex-direction:column;align-items:center}
.eyebrow{display:inline-flex;align-items:center;gap:14px;height:62px;padding:0 28px;border-radius:100px;background:#00C945;color:#fff;font-weight:700;font-size:23px;letter-spacing:.08em;text-transform:uppercase;flex:none}
.eyebrow i{width:30px;height:30px;border-radius:50%;background:#fff;display:inline-block;position:relative}
.eyebrow i::after{content:'';position:absolute;left:10px;top:6px;width:8px;height:14px;border:solid #00C945;border-width:0 3.5px 3.5px 0;transform:rotate(45deg)}
.head{display:flex;flex-direction:column;align-items:center;transform:rotate(-2deg);margin:30px 0 30px;flex:none}
.line{display:block;background:#fff;font-weight:800;font-size:var(--hs,92px);line-height:1.04;padding:4px 26px 14px;border-radius:16px;margin-top:-4px;white-space:nowrap;box-shadow:0 6px 20px rgba(0,0,0,.25)}
.line.hi{background:#000;color:#fff}
.card{position:relative;width:984px;background:#fff;border-radius:32px;box-shadow:0 24px 70px rgba(0,0,0,.45);padding:30px 40px 34px;flex:none}
.mid{flex:1 1 auto;display:flex;align-items:center;justify-content:center;width:100%}
.foot{flex:none;display:flex;flex-direction:column;align-items:center}
.foot .row{display:flex;align-items:center;gap:18px}
.logo{height:60px;background:#fff;border-radius:100px;padding:9px 20px;box-sizing:content-box}
.cta{display:inline-flex;align-items:center;height:92px;padding:0 46px;border-radius:100px;background:#fff;color:#000;font-weight:700;font-size:35px}
.cta::after{content:'';width:16px;height:16px;border:solid #000;border-width:4px 4px 0 0;transform:rotate(45deg);margin-left:18px}
.site{margin-top:14px;color:rgba(255,255,255,.85);font-weight:600;font-size:24px}
/* reader */
.book{display:flex;align-items:center;gap:14px;font-size:26px;color:#6E6E73;font-weight:500;padding-bottom:16px;margin-bottom:10px;border-bottom:1.5px solid #EEE}
.book b{color:#000;font-weight:700}
.book .dot{width:12px;height:12px;border-radius:50%;background:#00C945}
.s{display:flex;gap:20px;padding:16px 18px;border-radius:18px;margin:0 -18px}
.s .tri{flex:none;width:0;height:0;border-left:18px solid #C7C7CC;border-top:11px solid transparent;border-bottom:11px solid transparent;margin-top:15px}
.s .en{font-size:45px;font-weight:600;line-height:1.18;letter-spacing:-0.015em}
.s .ua{font-size:31px;color:#5E6B63;line-height:1.28;margin-top:6px;font-weight:500}
.s.now{background:#E7FAEE}
.s.now .tri{border-left-color:#00C945}
.w{background:#E4E4E8;border-radius:8px;padding:0 6px}
.g{color:#00A83A}
.pop{position:absolute;width:640px;background:#fff;border-radius:26px;box-shadow:0 18px 50px rgba(0,0,0,.28);padding:26px 32px 0;border:1.5px solid #EEE}
.pop .top{display:flex;align-items:baseline;gap:14px}
.pop .top b{font-size:44px}
.pop .top span{font-size:32px;color:#8E8E93}
.pop .top .spk{margin-left:auto}
.pop .tr{font-size:40px;font-weight:600;margin:8px 0 22px;color:#00A83A}
.pop .acts{display:flex;border-top:1.5px solid #EEE;margin:0 -32px}
.pop .acts div{flex:1;text-align:center;padding:16px 0 18px;font-size:25px;font-weight:500;color:#222;display:flex;flex-direction:column;align-items:center;gap:6px}
.tap{position:absolute;width:96px;height:96px;border-radius:50%;background:rgba(0,201,69,.22);border:4px solid #00C945}
.player{display:flex;align-items:center;gap:24px;margin-top:22px;padding:22px 26px;border-radius:24px;background:#F2F3F2}
.player .pl{width:72px;height:72px;border-radius:50%;background:#000;display:flex;align-items:center;justify-content:center;flex:none}
.player .meta{flex:1}
.player .t{display:flex;justify-content:space-between;font-size:27px;font-weight:700}
.player .t span{color:#5E6B63;font-weight:600;font-variant-numeric:tabular-nums}
.bar{position:relative;height:10px;border-radius:5px;background:#D5D8D6;margin-top:16px}
.bar i{position:absolute;left:0;top:0;bottom:0;width:42%;background:#00C945;border-radius:5px}
.bar b{position:absolute;left:42%;top:50%;width:28px;height:28px;margin:-14px 0 0 -14px;border-radius:50%;background:#00C945;border:5px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,.25)}
.tabs{display:flex;gap:34px;font-size:27px;color:#8E8E93;font-weight:600;margin:2px 0 4px;border-bottom:1.5px solid #EEE}
.tabs span{padding-bottom:14px}
.tabs .on{color:#000;border-bottom:4px solid #00C945}
.d{display:flex;align-items:center;gap:22px;padding:18px 0;border-bottom:1.5px solid #F0F0F2}
.d:last-child{border-bottom:none}
.d .wd{flex:1}
.d .wd b{font-size:42px;font-weight:700}
.d .wd b em{font-style:normal;font-weight:500;color:#333}
.d .wd div{font-size:27px;color:#8E8E93;margin-top:4px}
"""

SPK = '<svg width="34" height="34" viewBox="0 0 24 24"><path d="M4 9h4l5-4v14l-5-4H4z" fill="#000"/><path d="M16 8.5a5 5 0 0 1 0 7M18.5 6a8.5 8.5 0 0 1 0 12" fill="none" stroke="#000" stroke-width="1.8" stroke-linecap="round"/></svg>'
PLAY = '<svg width="30" height="30" viewBox="0 0 24 24"><path d="M7 5l12 7-12 7z" fill="#000"/></svg>'
SAVE = '<svg width="30" height="30" viewBox="0 0 24 24"><path d="M6 3h12v18l-6-4-6 4z" fill="#000"/></svg>'
mark = lambda on: f'<svg width="30" height="30" viewBox="0 0 24 24"><path d="M6 3h12v18l-6-4-6 4z" fill="{"#00C945" if on else "#C7C7CC"}"/></svg>'

def s(en, ua, now=False, i=None):
    return f'<div class="s{" now" if now else ""}"{f" id=s{i}" if i is not None else ""}><i class="tri"></i><div><div class="en">{en}</div><div class="ua">{ua}</div></div></div>'

ILIAD = '<div class="book"><i class="dot"></i><b>The Iliad</b> · Гомер</div>'
DORIAN = '<div class="book"><i class="dot"></i><b>The Picture of Dorian Gray</b> · Оскар Вайлд</div>'

CARDS = {
 'read': ILIAD + s('Achilles’ closest friend was Patroclus.', 'Найближчим другом Ахілла був Патрокл.', now=True)
        + s('The plan worked.', 'План спрацював.'),
 'known': DORIAN + s('Basil Hallward lives and works in London.', 'Безіл Голворд живе і працює в Лондоні.', now=True)
        + s('He enjoys painting portraits of people.', 'Він любить малювати портрети людей.'),
 'tap': ILIAD + s('He went to <span class="g">Achilles</span> and begged him to help.', 'Він пішов до Ахілла і благав його допомогти.', now=True)
        + '<div style="height:300px"></div>'
        + f'<div class="pop" style="left:150px;top:268px"><div class="top"><b>Achilles</b><span>/əˈkɪliːz/</span><span class="spk">{SPK}</span></div><div class="tr">Ахілл</div><div class="acts"><div>{PLAY}Відтворити</div><div>{SAVE}Обране</div></div></div>'
        + '<div class="tap" style="left:352px;top:80px"></div>',
 'listen': ILIAD + s('But Patroclus was already in danger.', 'Але Патрокл уже був у небезпеці.', now=True)
        + '<div class="player"><div class="pl"><svg width="32" height="32" viewBox="0 0 24 24"><path d="M6 5h4v14H6zM14 5h4v14h-4z" fill="#fff"/></svg></div><div class="meta"><div class="t">The Iliad <span>0:05:35 / 0:13:12</span></div><div class="bar"><i></i><b></b></div></div></div>',
 'dict': '<div class="tabs"><span>Коротко</span><span>Тести</span><span>Граматика</span><span class="on">Словник</span></div>'
        + ''.join(f'<div class="d"><div class="wd"><b>{w} <em>· {t}</em></b><div>{ph}</div></div>{SPK}{mark(on)}</div>'
                  for w, t, ph, on in [('friend', 'друг', '/frend/', True), ('armor', 'обладунки', '/ˈɑːrmər/', True), ('enemy', 'ворог', '/ˈenəmi/', True), ('defend', 'захищати', '/dɪˈfend/', False)]),
}

# Each ad: one psychological lever, said once.
ADS = [
 # Identity and milestone: a first book is a visible step that says "I can"; goal gradient starts the moment it's named.
 dict(id='OMD_Books_First_V2_2645', eyebrow='Англійська через книжки', head=['Твоя перша книжка', 'англійською'], hi=1, card='read', photo='sofa',
      body='Сторінка за сторінкою, з перекладом під кожним рядком. Почни з першого розділу сьогодні ввечері.', title='Твоя перша книжка англійською'),
 # Processing fluency: a story you already know feels easier, so the first step looks small; curiosity to see it in English.
 dict(id='OMD_Books_Known_V1_2645', eyebrow='Англійська через книжки', head=['Цю історію ти знаєш.', 'Тепер англійською'], hi=1, card='known', photo='lamp',
      body='Знайомий сюжет читається легше. Простий англійський текст, переклад під кожним рядком, вимова поруч.', title='Знайома історія англійською'),
 # Friction removal: names the moment people quit (an unknown word) and shows it costs one tap.
 dict(id='OMD_Books_Tap_V2_2645', eyebrow='Англійська без словника', head=['Не знаєш слово?', 'Просто торкнись'], hi=1, card='tap', photo='nightstand',
      body='Торкнись слова в книжці англійською: переклад і вимова одразу. Не треба зупинятись і шукати.', title='Торкнись слова, почуй вимову'),
 # Habit stacking and time reframe: attaches English to a trip that already happens, no new time needed.
 dict(id='OMD_Books_Commute_V2_2645', eyebrow='Навчання для зайнятих людей', head=['Дорога додому', 'з книжкою англійською'], hi=1, card='listen', photo='tram', hs=84,
      body='Книжку англійською можна слухати, поки їдеш. Текст і переклад відкриються, коли захочеш подивитись.', title='Книжка англійською в дорозі'),
 # Endowment and visible progress: words become "yours", a collection that grows and is worth coming back to.
 dict(id='OMD_Books_Words_V2_2645', eyebrow='Словник з кожної книжки', head=['Слова з книжки', 'стають твоїми'], hi=1, card='dict', photo='balcony',
      body='Слова з книжки англійською зберігаються у твоєму словнику разом з вимовою. Повторюй їх, коли зручно.', title='Слова з книжки стають твоїми'),
]

def page(ad):
    lines = ''.join(f'<span class="line{" hi" if ad.get("hi") == i else ""}">{l}</span>' for i, l in enumerate(ad['head']))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}{CSS}</style></head><body>
<div class="om" style="--hs:{ad.get('hs', 92)}px"><div class="bg" style="background-image:url({photo(ad['photo'])})"></div>
<div class="frame"><div class="eyebrow"><i></i>{ad['eyebrow']}</div>
<div class="head">{lines}</div>
<div class="mid"><div class="card">{CARDS[ad['card']]}</div></div>
<div class="foot"><div class="row"><img class="logo" src="{LOGO}"><div class="cta">{CTA}</div></div><div class="site">onmind.coach</div></div></div></div></body></html>"""

# Shrink the headline until both lines fit, then check nothing collides or overflows.
CHECK = """() => { const om=document.querySelector('.om'), W=om.clientWidth, p=[];
 let hs=parseFloat(getComputedStyle(om).getPropertyValue('--hs'));
 const wide=()=>[...document.querySelectorAll('.line')].some(l=>l.getBoundingClientRect().width>W-70);
 while (hs>70 && wide()) { hs-=2; om.style.setProperty('--hs', hs+'px'); }
 if (wide()) p.push('headline too wide');
 const c=document.querySelector('.card').getBoundingClientRect(), h=document.querySelector('.head').getBoundingClientRect(), f=document.querySelector('.foot').getBoundingClientRect();
 if (c.top < h.bottom+8) p.push('card hits headline'); if (c.bottom > f.top-14) p.push('card hits footer '+Math.round(c.bottom)+' '+Math.round(f.top));
 for (const e of document.querySelectorAll('.card *')) { const r=e.getBoundingClientRect(); if (r.right > c.right+1) { p.push('overflow: '+e.className+' '+e.textContent.slice(0,30)); break; } }
 return {p, hs}; }"""

def main():
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1350})
        bad = 0
        for ad in ADS:
            pg.set_content(page(ad)); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(200)
            r = pg.evaluate(CHECK)
            pg.screenshot(path=str(OUT / f"{ad['id']}.png"), clip=dict(x=0, y=0, width=1080, height=1350))
            print('PROBLEM' if r['p'] else 'OK     ', ad['id'], 'headline', r['hs'], r['p'] or ''); bad += bool(r['p'])
        b.close()
    sys.exit(1 if bad else 0)

if __name__ == '__main__': main()
