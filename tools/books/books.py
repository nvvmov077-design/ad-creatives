# OnMind feature ads: books. Same tokens as kit.mjs, plus a reader card rebuilt from the real reader UI.
# Usage: python3 books.py out
import base64, sys, pathlib
from playwright.sync_api import sync_playwright

KIT = pathlib.Path(__file__).resolve().parent.parent
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 and __name__=='__main__' else 'out'); OUT.mkdir(parents=True, exist_ok=True)
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()
FONTS = '\n'.join(f"@font-face{{font-family:'Onest';font-weight:100 900;src:url(data:font/woff2;base64,{b64(KIT/'fonts'/f'onest-{s}.woff2')}) format('woff2')}}" for s in ['cyr', 'cyr-ext', 'latin'])
LOGO = 'data:image/png;base64,' + b64(KIT/'logo@4x.png')
photo = lambda n: 'data:image/webp;base64,' + b64(KIT/'photos'/f'{n}.webp')

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#000}
.om{position:relative;overflow:hidden;width:1080px;height:1350px;font-family:'Onest',sans-serif;letter-spacing:-0.02em;color:#000;background:#151A18}
.bg{position:absolute;inset:-20px;background-size:cover;background-position:var(--focus,50% 50%);filter:blur(3px) saturate(.9) brightness(.62)}
.frame{position:absolute;inset:0;padding:52px 56px 44px;display:flex;flex-direction:column;align-items:center;gap:0}
.eyebrow{display:inline-flex;align-items:center;gap:12px;height:54px;padding:0 24px;border-radius:100px;background:#00C945;color:#fff;font-weight:600;font-size:19px;letter-spacing:.1em;text-transform:uppercase;flex:none}
.eyebrow i{width:26px;height:26px;border-radius:50%;background:#fff;display:inline-block;position:relative}
.eyebrow i::after{content:'';position:absolute;left:8px;top:5px;width:7px;height:12px;border:solid #00C945;border-width:0 3px 3px 0;transform:rotate(45deg)}
.head{display:flex;flex-direction:column;align-items:center;transform:rotate(-2.5deg);margin:34px 0 34px;flex:none}
.line{display:block;background:#fff;font-weight:700;font-size:var(--hs,84px);line-height:1.04;padding:4px 24px 12px;border-radius:14px;margin-top:-4px;white-space:nowrap;box-shadow:0 4px 15px rgba(0,0,0,.12)}
.line.hi{background:#000;color:#fff}
.card{position:relative;width:940px;background:#fff;border-radius:30px;box-shadow:0 20px 60px rgba(0,0,0,.35);padding:30px 38px 34px;flex:none}
.mid{flex:1 1 auto;display:flex;align-items:center;justify-content:center;width:100%}
.foot{flex:none;display:flex;flex-direction:column;align-items:center}
.foot .row{display:flex;align-items:center;gap:18px}
.logo{height:56px;background:#fff;border-radius:100px;padding:8px 18px;box-sizing:content-box}
.cta{display:inline-flex;align-items:center;height:88px;padding:0 42px;border-radius:100px;background:#000;color:#fff;font-weight:600;font-size:33px}
.site{margin-top:14px;color:#fff;font-weight:600;font-size:25px;text-shadow:0 1px 8px rgba(0,0,0,.5)}
/* reader */
.book{display:flex;align-items:center;gap:14px;font-size:21px;color:#6E6E73;font-weight:500;padding-bottom:16px;margin-bottom:8px;border-bottom:1px solid #EEE}
.book b{color:#000;font-weight:700}
.book .dot{width:8px;height:8px;border-radius:50%;background:#00C945}
.s{display:flex;gap:18px;padding:14px 16px;border-radius:16px;margin:0 -16px}
.s .tri{flex:none;width:0;height:0;border-left:15px solid #C7C7CC;border-top:9px solid transparent;border-bottom:9px solid transparent;margin-top:12px}
.s .en{font-size:33px;font-weight:500;line-height:1.22;letter-spacing:-0.01em}
.s .ua{font-size:23px;color:#6E6E73;line-height:1.3;margin-top:5px;font-weight:450}
.s.now{background:#EAF8EE}
.s.now .tri{border-left-color:#00C945}
.w{background:#EDEDF0;border-radius:7px;padding:0 5px}
.g{color:#2DB84C}
.pop{position:absolute;width:520px;background:#fff;border-radius:22px;box-shadow:0 14px 44px rgba(0,0,0,.22);padding:22px 26px 0}
.pop .top{display:flex;align-items:baseline;gap:12px}
.pop .top b{font-size:30px}
.pop .top span{font-size:24px;color:#8E8E93}
.pop .top .spk{margin-left:auto}
.pop .tr{font-size:28px;margin:8px 0 18px;color:#333}
.pop .acts{display:flex;border-top:1px solid #EEE;margin:0 -26px}
.pop .acts div{flex:1;text-align:center;padding:14px 0 16px;font-size:19px;color:#333;display:flex;flex-direction:column;align-items:center;gap:6px}
.tap{position:absolute;width:74px;height:74px;border-radius:50%;background:rgba(0,201,69,.25);border:3px solid rgba(0,201,69,.8)}
.player{display:flex;align-items:center;gap:22px;margin-top:22px;padding:20px 24px;border-radius:22px;background:#F5F5F7}
.player .pl{width:58px;height:58px;border-radius:50%;background:#000;display:flex;align-items:center;justify-content:center;flex:none}
.player .meta{flex:1}
.player .t{display:flex;justify-content:space-between;font-size:21px;font-weight:600}
.player .t span{color:#6E6E73;font-weight:500;font-variant-numeric:tabular-nums}
.bar{position:relative;height:8px;border-radius:4px;background:#DCDCE0;margin-top:14px}
.bar i{position:absolute;left:0;top:0;bottom:0;width:42%;background:#00C945;border-radius:4px}
.bar b{position:absolute;left:42%;top:50%;width:24px;height:24px;margin:-12px 0 0 -12px;border-radius:50%;background:#00C945;border:4px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,.2)}
.tabs{display:flex;gap:30px;font-size:22px;color:#8E8E93;font-weight:500;margin:4px 0 6px;border-bottom:1px solid #EEE}
.tabs span{padding-bottom:12px}
.tabs .on{color:#000;border-bottom:3px solid #00C945}
.d{display:flex;align-items:center;gap:16px;padding:14px 0;border-bottom:1px solid #F0F0F2}
.d:last-child{border-bottom:none}
.d .wd{flex:1}
.d .wd b{font-size:31px;font-weight:700}
.d .wd b em{font-style:normal;font-weight:450;color:#333}
.d .wd div{font-size:21px;color:#8E8E93;margin-top:3px}
"""

SPK = '<svg width="26" height="26" viewBox="0 0 24 24"><path d="M4 9h4l5-4v14l-5-4H4z" fill="#000"/><path d="M16 8.5a5 5 0 0 1 0 7M18.5 6a8.5 8.5 0 0 1 0 12" fill="none" stroke="#000" stroke-width="1.8" stroke-linecap="round"/></svg>'
PLAY = '<svg width="24" height="24" viewBox="0 0 24 24"><path d="M7 5l12 7-12 7z" fill="#000"/></svg>'
SAVE = '<svg width="24" height="24" viewBox="0 0 24 24"><path d="M6 3h12v18l-6-4-6 4z" fill="#000"/></svg>'
SAVE_G = '<svg width="22" height="22" viewBox="0 0 24 24"><path d="M6 3h12v18l-6-4-6 4z" fill="#F08A24"/></svg>'
SAVE_O = '<svg width="22" height="22" viewBox="0 0 24 24"><path d="M6 3h12v18l-6-4-6 4z" fill="#3A3A3C"/></svg>'

def s(en, ua, now=False):
    return f'<div class="s{" now" if now else ""}"><i class="tri"></i><div><div class="en">{en}</div><div class="ua">{ua}</div></div></div>'

BOOK = '<div class="book"><i class="dot"></i><b>The Iliad</b> · Гомер · розділ 4</div>'

CARDS = {
 'read': BOOK + s('Achilles’ closest friend was <span class="w">Patroclus</span>.', 'Найближчим другом Ахілла був Патрокл.')
        + s('He could not watch the Greeks suffer any longer.', 'Він більше не міг дивитися, як страждають греки.', now=True)
        + s('He went to <span class="g">Achilles</span> and begged him to help.', 'Він пішов до Ахілла і благав його допомогти.'),
 'tap': BOOK + s('He went to <span class="g">Achilles</span> and begged him to help.', 'Він пішов до Ахілла і благав його допомогти.', now=True)
        + '<div style="height:250px"></div>'
        + s('The plan worked.', 'План спрацював.')
        + f'<div class="pop" style="left:120px;top:222px"><div class="top"><b>Achilles</b><span>/əˈkɪliːz/</span><span class="spk">{SPK}</span></div><div class="tr">Ахілл</div><div class="acts"><div>{PLAY}Відтворити</div><div>{SAVE}Обране</div></div></div>'
        + '<div class="tap" style="left:258px;top:104px"></div>',
 'listen': BOOK + s('Then Hector came to meet him.', 'Тоді йому назустріч вийшов Гектор.')
        + s('But Patroclus was already in danger.', 'Але Патрокл уже був у небезпеці.', now=True)
        + f'<div class="player"><div class="pl"><svg width="26" height="26" viewBox="0 0 24 24"><path d="M7 5l12 7-12 7z" fill="#fff"/></svg></div><div class="meta"><div class="t">The Iliad <span>0:05:35 / 0:13:12</span></div><div class="bar"><i></i><b></b></div></div></div>',
 'dict': '<div class="book" style="border:none;margin:0;padding-bottom:10px"><i class="dot"></i><b>The Iliad</b> · Гомер</div>'
        + '<div class="tabs"><span>Коротко</span><span>Тести</span><span>Граматика</span><span class="on">Словник</span></div>'
        + ''.join(f'<div class="d"><div class="wd"><b>{w} <em>· {t}</em></b><div>{ph}</div></div>{SPK}{SAVE_G if i in (1,3) else SAVE_O}</div>'
                  for i,(w,t,ph) in enumerate([('armor','обладунки','/ˈɑːrmər/'),('enemy','ворог','/ˈenəmi/'),('warning','застереження','/ˈwɔːrnɪŋ/'),('grief','горе','/ɡriːf/'),('defend','захищати','/dɪˈfend/')])),
}

ADS = [
 dict(id='OMD_Books_Read_V1_2645', head=['Читай книжки', 'англійською'], hi=1, card='read', photo='sofa'),
 dict(id='OMD_Books_Tap_V1_2645', head=['Слово англійською?', 'Натисни на нього'], hi=0, card='tap', photo='lamp', hs=76),
 dict(id='OMD_Books_Listen_V1_2645', head=['Слухай книжки', 'англійською в дорозі'], hi=1, card='listen', photo='tram', hs=78),
 dict(id='OMD_Books_Dict_V1_2645', head=['Книжка англійською', 'і словник до неї'], hi=0, card='dict', photo='nightstand', hs=78),
]

def page(ad):
    lines = ''.join(f'<span class="line{" hi" if ad.get("hi")==i else ""}">{l}</span>' for i,l in enumerate(ad['head']))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}{CSS}</style></head><body>
<div class="om" style="--hs:{ad.get('hs',84)}px"><div class="bg" style="background-image:url({photo(ad['photo'])})"></div>
<div class="frame"><div class="eyebrow"><i></i>Створено для зайнятих людей</div>
<div class="head">{lines}</div>
<div class="mid"><div class="card">{CARDS[ad['card']]}</div></div>
<div class="foot"><div class="row"><img class="logo" src="{LOGO}"><div class="cta">Почати квіз</div></div><div class="site">onmind.coach</div></div></div></div></body></html>"""

CHECK = """() => { const om=document.querySelector('.om'), W=om.clientWidth, p=[];
 for (const l of document.querySelectorAll('.line')) if (l.getBoundingClientRect().width > W-80) p.push('headline too wide: '+l.textContent);
 const c=document.querySelector('.card').getBoundingClientRect(), h=document.querySelector('.head').getBoundingClientRect(), f=document.querySelector('.foot').getBoundingClientRect();
 if (c.top < h.bottom+8) p.push('card hits headline'); if (c.bottom > f.top-12) p.push('card hits footer '+Math.round(c.bottom)+' '+Math.round(f.top));
 for (const e of document.querySelectorAll('.card *')) { const r=e.getBoundingClientRect(); if (r.right > c.right+1) { p.push('overflow: '+e.className); break; } }
 return p; }"""

def main():
  with sync_playwright() as pw:
      b = pw.chromium.launch(); pg = b.new_page(viewport={'width':1080,'height':1350})
      bad = 0
      for ad in ADS:
          pg.set_content(page(ad)); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(200)
          probs = pg.evaluate(CHECK)
          f = OUT/f"{ad['id']}.png"; pg.screenshot(path=str(f), clip=dict(x=0,y=0,width=1080,height=1350))
          print('PROBLEM' if probs else 'OK     ', ad['id'], probs or ''); bad += bool(probs)
      b.close()
  sys.exit(1 if bad else 0)


if __name__=='__main__': main()
