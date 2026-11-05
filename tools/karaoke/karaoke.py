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


import wave, struct, tempfile, os
PIPER = HERE / 'piper' / 'piper' / 'piper'; VOICE = HERE / 'piper' / 'en-us-lessac-medium.onnx'
SR = 22050
def tts(text, path):
    subprocess.run([str(PIPER), '--model', str(VOICE), '--length_scale', '1.12', '--sentence_silence', '0.0', '--output_file', str(path)],
                   input=text.encode(), check=True, capture_output=True)
    with wave.open(str(path)) as w: return w.getnframes() / w.getframerate()

def build_audio(v, workdir):
    """Synthesises each sentence, measures word end times with cumulative prefixes, inserts a pause after pop words.
    Returns (word_times [(start,end)], total_seconds, wav_path)."""
    LEAD, GAP, HOLD, TAIL = 0.8, 0.35, 1.3, 1.6
    import numpy as np
    out = [np.zeros(int(LEAD * SR), dtype=np.int16)]
    t = LEAD; times = []
    for si, (en, _) in enumerate(v['text']):
        words = en.split(' ')
        full = workdir / f's{si}.wav'; dur = tts(en, full)
        # word boundaries from prefixes
        ends = []
        for i in range(1, len(words)):
            d = tts(' '.join(words[:i]), workdir / 'p.wav')
            ends.append(min(d - 0.18, dur))  # prefixes end with a trailing pause; trim it
        ends.append(dur)
        with wave.open(str(full)) as w: data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
        cursor = 0.0; start_t = t
        for i, w_ in enumerate(words):
            a, z = cursor, ends[i]
            key = ''.join(c for c in w_ if c.isalpha() or c == "'").lower()
            times.append((t + a - cursor + (0), t + (z - cursor)))  # placeholder, fixed below
            cursor = z
        # rebuild with pauses: simpler, walk again
        times = times[:-len(words)]
        cursor = 0.0
        for i, w_ in enumerate(words):
            z = ends[i]
            seg = data[int(cursor * SR):int(z * SR)]
            out.append(seg); times.append((t, t + (z - cursor))); t += (z - cursor)
            key = ''.join(c for c in w_ if c.isalpha() or c == "'").lower()
            if key in v['pops']:
                out.append(np.zeros(int(HOLD * SR), dtype=np.int16)); t += HOLD
            cursor = z
        out.append(np.zeros(int(GAP * SR), dtype=np.int16)); t += GAP
    out.append(np.zeros(int(TAIL * SR), dtype=np.int16)); t += TAIL
    audio = np.concatenate(out)
    wav = workdir / 'voice.wav'
    with wave.open(str(wav), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(audio.tobytes())
    return times, t, wav

RECTS = """() => { const card=document.getElementById('card').getBoundingClientRect();
 return [...document.querySelectorAll('.w')].map(w=>{const r=w.getBoundingClientRect(); return {x:r.left-card.left+r.width/2, y:r.top-card.top+r.height*0.95, w:r.width, cw:card.width, txt:w.textContent};}); }"""
JS = """([cur, hx, hy, rot, popIdx, pops]) => {
 const words=[...document.querySelectorAll('.w')];
 words.forEach((w,i)=>{ w.classList.toggle('on', i===cur); w.classList.toggle('done', i<cur); });
 const hand=document.getElementById('hand'), pop=document.getElementById('pop');
 if (cur<0) { hand.style.opacity=0; pop.style.opacity=0; return; }
 hand.style.opacity=1; hand.style.left=(hx-250*0.33+6)+'px'; hand.style.top=(hy-250*1.357*0.03)+'px'; hand.style.transform='rotate('+rot+'deg)';
 if (popIdx>=0) { const r=words[popIdx].getBoundingClientRect(), card=document.getElementById('card').getBoundingClientRect();
   const txt=words[popIdx].textContent.replace(/[^A-Za-z']/g,'').toLowerCase(); const p=pops[txt];
   document.getElementById('pw').textContent=txt; document.getElementById('pp').textContent=p[0]; document.getElementById('pt').textContent=p[1];
   const x=r.left-card.left+r.width/2, y=r.top-card.top+r.height*0.95;
   pop.style.opacity=1; pop.style.left=Math.max(10, Math.min(card.width-580, x-280))+'px'; pop.style.top=(y+70)+'px'; }
 else pop.style.opacity=0;
}"""
ease = lambda x: 0 if x <= 0 else 1 if x >= 1 else (3*x*x - 2*x*x*x)

def main():
  import math
  with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    for v in VIDEOS:
        work = OUT / ('work_' + v['id']); shutil.rmtree(work, ignore_errors=True); work.mkdir()
        times, total, wav = build_audio(v, work)
        fr = OUT / 'frames'; shutil.rmtree(fr, ignore_errors=True); fr.mkdir()
        pg.set_content(html(v)); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(250)
        rects = pg.evaluate(RECTS)
        keys = [''.join(c for c in r['txt'] if c.isalpha() or c == "'").lower() for r in rects]
        nf = int(total * FPS)
        for f in range(nf):
            t = f / FPS
            cur = -1
            for i, (a, z) in enumerate(times):
                if t >= a: cur = i
            if cur < 0:
                pg.evaluate(JS, [-1, 0, 0, 0, -1, v['pops']])
            else:
                a, z = times[cur]
                # glide from the previous word to this one over the first 55% of the word, eased; small vertical lift mid glide
                prev = rects[cur-1] if cur > 0 else rects[cur]
                frac = ease(min(1, (t - a) / max(0.12, (z - a) * 0.55)))
                hx = prev['x'] + (rects[cur]['x'] - prev['x']) * frac
                hy = prev['y'] + (rects[cur]['y'] - prev['y']) * frac + (-14 * math.sin(frac * math.pi))
                rot = -10 + 3 * math.sin(frac * math.pi) + 1.2 * math.sin(t * 2.1)
                # word card: shown during the hold after a pop word (from the word's end until the next word starts)
                popIdx = -1
                if keys[cur] in v['pops'] and t >= z - 0.15 and (cur + 1 >= len(times) or t < times[cur+1][0]):
                    popIdx = cur
                pg.evaluate(JS, [cur, hx, hy, rot, popIdx, v['pops']])
            pg.screenshot(path=str(fr / f'{f:04d}.jpg'), type='jpeg', quality=92, clip=dict(x=0, y=0, width=1080, height=1920))
        mp4 = OUT / f"{v['id']}.mp4"
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', str(FPS), '-i', str(fr / '%04d.jpg'), '-i', str(wav),
                        '-af', 'aresample=48000,volume=1.4', '-shortest',
                        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'medium', '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '128k', str(mp4)], check=True)
        shutil.copy(fr / f'{int(2.5*FPS):04d}.jpg', OUT / f"{v['id']}_thumb.jpg")
        shutil.rmtree(fr); shutil.rmtree(work)
        print(v['id'], round(total, 1), 's', flush=True)
    b.close()

if __name__ == '__main__': main()
