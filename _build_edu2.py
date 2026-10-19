# -*- coding: utf-8 -*-
"""آپدیت دوره‌های Ausbildung: کامل (نامحدود)، فاین‌لاین (۱۲هفته/۲جلسه)، آپدیت (جدید)"""
import io, re, glob

COURSES = [
    dict(n=1, slug="komplett-ausbildung", img="3",
        de=dict(h1="Komplett-Ausbildung", tag="Kurs", dur="Unbegrenzt",
            p1="Vom 0 auf 100: Materials, sterile Arbeitsweise, Kundenkommunikation, Maschinen- & Nadelführung und sauberes Arbeiten – plus praktisches Tätowieren und anschließend Kundenakquise & Business-Aufbau. Die Dauer ist unbegrenzt: wir trainieren, bis du wirklich studio-ready bist.",
            incl=["Einführung in alle Materialien", "Sterile Arbeitsweise von Tag 1", "Kundenkommunikation & Beratung", "Maschinen- & Nadelführung", "Sauberkeit & Hygiene-Workflow", "Praktisches Tätowieren an echten Modellen", "Kundenakquise & Business-Aufbau"],
            voraus=["Mindestalter 18 Jahre", "Keine Vorerfahrung nötig – Motivation zählt", "Kurzes Motivationsgespräch vor Start", "Zeit: verlässliche Teilnahme bis zum Ziel"]),
        en=dict(h1="Full Training", tag="Course", dur="Unlimited",
            p1="From 0 to 100: materials, sterile working, client communication, machine & needle handling and clean working – plus hands-on tattooing and then client acquisition & business building. Duration is unlimited: we train until you are truly studio-ready.",
            incl=["Introduction to all materials", "Sterile working from day 1", "Client communication & consultation", "Machine & needle handling", "Cleanliness & hygiene workflow", "Hands-on tattooing on real models", "Client acquisition & business building"],
            voraus=["Minimum age 18", "No experience needed – motivation counts", "Short motivation talk before start", "Time: reliable attendance until the goal"]),
        fa=dict(h1="دوره کامل تتو", tag="دوره", dur="نامحدود",
            p1="از صفر تا صد: آشنایی با متریال، روش استریل کار کردن، ارتباط با مشتری، آشنایی با دستگاه و سوزن‌ها و تمیز کار کردن — به‌علاوه کار عملی تتو و سپس روش کسب مشتری و چرخاندن بیزینس. مدت دوره نامحدود است: آموزش تا جایی ادامه دارد که واقعاً آماده‌ی کار در استودیو بشی.",
            incl=["آشنایی با همه متریال‌ها", "روش استریل کار کردن از روز اول", "ارتباط با مشتری و مشاوره", "آشنایی با دستگاه و سوزن‌ها", "تمیز کار کردن و ورک‌فلو بهداشتی", "کار عملی تتو روی مدل واقعی", "کسب مشتری و چرخاندن بیزینس"],
            voraus=["حداقل سن ۱۸ سال", "بدون نیاز به سابقه — انگیزه کافی است", "یک گفتگوی کوتاه انگیزشی قبل از شروع", "وقت: حضور منظم تا رسیدن به هدف"]),
    ),
    dict(n=2, slug="fineline-workshop", img="6",
        de=dict(h1="Workshop: Fineline", tag="Workshop", dur="12 Wochen · 2 Sessions/Woche",
            p1="Zwölf Wochen mit zwei Sessions pro Woche: Du lernst Maschinen- & Nadelführung und die sterile Arbeitsweise – aber der Fokus liegt zu 100 % auf Fineline. Feinste Linien, Punkarbeit und zarte Shadings, sauber und stabil.",
            incl=["12 Wochen · 2 Sessions pro Woche", "Einführung Maschine & Nadeln", "Sterile Arbeitsweise", "Fokus 100 % Fineline: feine Linien & Punkarbeit", "Hautspannung & Linienstabilität", "Praxis an künstlicher Haut und echten Modellen", "Teilnahme-Zertifikat"],
            voraus=["Mindestalter 18 Jahre", "Keine Vorerfahrung nötig", "Kurzes Motivationsgespräch vor Start", "Verlässliche Teilnahme: 2 Sessions pro Woche"]),
        en=dict(h1="Workshop: Fineline", tag="Workshop", dur="12 weeks · 2 sessions/week",
            p1="Twelve weeks with two sessions per week: you learn machine & needle handling and sterile working – but the focus is 100 % fineline. Finest lines, dotwork and delicate shadings, clean and stable.",
            incl=["12 weeks · 2 sessions per week", "Machine & needle introduction", "Sterile working method", "100 % fineline focus: fine lines & dotwork", "Skin tension & line stability", "Practice on artificial skin and real models", "Participation certificate"],
            voraus=["Minimum age 18", "No experience needed", "Short motivation talk before start", "Reliable attendance: 2 sessions per week"]),
        fa=dict(h1="دوره فاین‌لاین", tag="ورک‌شاپ", dur="۱۲ هفته · هفته‌ای ۲ جلسه",
            p1="دوازده هفته با هفته‌ای دو جلسه: آشنایی با دستگاه و سوزن‌ها و روش استریل کار کردن را یاد می‌گیری — ولی تمرکز ۱۰۰٪ روی فاین‌لاین است. ظریف‌ترین خط‌ها، نقطه‌کاری و سایه‌های لطیف، تمیز و پایدار.",
            incl=["۱۲ هفته · هفته‌ای ۲ جلسه", "آشنایی با دستگاه و سوزن‌ها", "روش استریل کار کردن", "تمرکز ۱۰۰٪ فاین‌لاین: خط ظریف و نقطه‌کاری", "کشش پوست و ثبات خط", "تمرین روی پوست مصنوعی و مدل واقعی", "گواهینامه پایان دوره"],
            voraus=["حداقل سن ۱۸ سال", "بدون نیاز به سابقه", "یک گفتگوی کوتاه انگیزشی قبل از شروع", "حضور منظم: هفته‌ای ۲ جلسه"]),
    ),
    dict(n=3, slug="update-kurs", img="7",
        de=dict(h1="Update-Kurs", tag="Update", dur="ab 1 Session",
            p1="Für Artists mit Vorkenntnissen, die ihr Level anheben wollen: Du zeigst uns deine Arbeiten – wir finden gemeinsam deine Schwachstellen und arbeiten gezielt an genau dem einen Bereich, der dich aktuell bremst. Kein Standardprogramm, sondern Korrektur und Upgrade ganz nach deinem Bedarf. Dauer: ab 1 Session, so viele Sessions wie du brauchst.",
            incl=["Analyse deiner bisherigen Arbeiten", "Gezielte Korrektur deiner Schwachstellen", "Fokus nur auf dein bestimmtes Themenfeld", "Hands-on an echten Modellen", "Ab 1 Session – flexibel nach deinem Bedarf", "Teilnahme-Zertifikat"],
            voraus=["Mindestalter 18 Jahre", "Du tätowierst bereits (Vorkenntnisse)", "Deine bisherigen Arbeiten für die Analyse mitbringen", "Offenheit für ehrliches Feedback"]),
        en=dict(h1="Update Course", tag="Update", dur="from 1 session",
            p1="For artists with existing knowledge who want to level up: show us your work – together we find your weak spots and work specifically on exactly the one area that is holding you back right now. No standard program, but correction and upgrade entirely according to your needs. Duration: from 1 session, as many as you need.",
            incl=["Analysis of your previous work", "Targeted correction of your weak spots", "Focus only on your specific topic area", "Hands-on on real models", "From 1 session – flexible as needed", "Participation certificate"],
            voraus=["Minimum age 18", "You already tattoo (basic knowledge)", "Bring your previous work for analysis", "Openness to honest feedback"]),
        fa=dict(h1="دوره آپدیت", tag="آپدیت", dur="از ۱ جلسه",
            p1="برای آرتیست‌هایی که شناخت تتو دارند و می‌خواهند سطحشان را ارتقا بدهند: کارهات را نشون ما می‌دی — با هم اشکالاتت را پیدا می‌کنیم و دقیقاً روی همان موضوع خاصی که گیر کرده کار می‌کنیم تا ارتقا بگیری. برنامه استاندارد نیست؛ صرفاً اصلاح و ارتقای همان نقطه‌ضعف. مدت: از ۱ جلسه، به تعداد نیازت.",
            incl=["آنالیز کارهای قبلی‌ات", "رفع هدفمند اشکالاتت", "تمرکز فقط روی همان موضوع خاص", "کار عملی روی مدل واقعی", "از ۱ جلسه — منعطف طبق نیازت", "گواهینامه شرکت"],
            voraus=["حداقل سن ۱۸ سال", "قبلاً تتو می‌زنی (شناخت اولیه)", "کارهای قبلی‌ات را برای آنالیز بیار", "پذیرش فیدبک صادقانه"]),
    ),
]

# ---------- ۱) i18n: حذف کلیدهای au قدیمی و درج جدید ----------
p = "assets/js/i18n.js"; s = io.open(p, encoding="utf-8").read()
s = re.sub(r'au1_h1:".*?au_note:"[^"]*",', '', s, flags=re.S)
blocks = {
"de": " ".join(
    (f'au{d["n"]}_h1:"{d["de"]["h1"]}", au{d["n"]}_tag:"{d["de"]["tag"]}", au{d["n"]}_dur:"{d["de"]["dur"]}", au{d["n"]}_preis:"Auf Anfrage / mit Anruf", au{d["n"]}_p1:"{d["de"]["p1"]}", '
     f'au{d["n"]}_incl_h:"Im Kurs enthalten", au{d["n"]}_incl:"' + " | ".join(d["de"]["incl"]) + f'", au{d["n"]}_vor_h:"Voraussetzungen", au{d["n"]}_vor:"' + " | ".join(d["de"]["voraus"]) + '",')
    for d in COURSES) + ' au_h1:"Werde Tattoo-Artist – bei SAAD", au_p:"Professionelle Ausbildungs-Pakete: vom kompletten Kurs bis zum gezielten Update. Kleine Gruppen, echte Modelle, gültiges Zertifikat – direkt im Studio in Wiesbaden.", au_cert:"Nach Abschluss des Kurses erhältst du ein gültiges Zertifikat.", au_details:"Kursdetails", au_incl_h:"Enthalten", au_vor_h:"Voraussetzungen", au_anmelden:"Platz anfragen", au_note:"Kostenloses Erstgespräch – ohne Verpflichtung.",',
"en": " ".join(
    (f'au{d["n"]}_h1:"{d["en"]["h1"]}", au{d["n"]}_tag:"{d["en"]["tag"]}", au{d["n"]}_dur:"{d["en"]["dur"]}", au{d["n"]}_preis:"On request / call us", au{d["n"]}_p1:"{d["en"]["p1"]}", '
     f'au{d["n"]}_incl_h:"Included in the course", au{d["n"]}_incl:"' + " | ".join(d["en"]["incl"]) + f'", au{d["n"]}_vor_h:"Requirements", au{d["n"]}_vor:"' + " | ".join(d["en"]["voraus"]) + '",')
    for d in COURSES) + ' au_h1:"Become a Tattoo Artist – at SAAD", au_p:"Professional training packages: from the full course to a targeted update. Small groups, real models, valid certificate – right here in our Wiesbaden studio.", au_cert:"After completing the course you receive a valid certificate.", au_details:"Course details", au_incl_h:"Included", au_vor_h:"Requirements", au_anmelden:"Request a spot", au_note:"Free first consultation – no obligation.",',
"fa": " ".join(
    (f'au{d["n"]}_h1:"{d["fa"]["h1"]}", au{d["n"]}_tag:"{d["fa"]["tag"]}", au{d["n"]}_dur:"{d["fa"]["dur"]}", au{d["n"]}_preis:"با تماس", au{d["n"]}_p1:"{d["fa"]["p1"]}", '
     f'au{d["n"]}_incl_h:"شامل دوره", au{d["n"]}_incl:"' + " | ".join(d["fa"]["incl"]) + f'", au{d["n"]}_vor_h:"شرایط ثبت‌نام", au{d["n"]}_vor:"' + " | ".join(d["fa"]["voraus"]) + '",')
    for d in COURSES) + ' au_h1:"تتوآرتیست شو — در SAAD", au_p:"پکیج‌های حرفه‌ای آموزش: از دوره کامل تا آپدیت هدفمند. گروه کوچک، مدل واقعی، گواهینامه معتبر — مستقیم در استودیو ویسبادن.", au_cert:"بعد از اتمام هر دوره، گواهینامه معتبر دریافت می‌کنی.", au_details:"جزئیات دوره", au_incl_h:"شامل", au_vor_h:"شرایط", au_anmelden:"درخواست جایگاه", au_note:"مشاوره اول رایگان — بدون هیچ تعهدی.",',
}
for lang, keys in blocks.items():
    a2 = {"de":'bk_h1:"Wähle Datum & Uhrzeit"','en':'bk_h1:"Choose date & time"','fa':'bk_h1:"تاریخ و ساعت را انتخاب کن"'}[lang]
    idx = s.index(a2); s = s[:idx] + keys + s[idx:]
io.open(p, "w", encoding="utf-8").write(s)
print("i18n updated")

# ---------- ۲) کارت‌های landing و index: دیتا جدید (کلیدها همین‌ها هستند) ----------
# ausbildung.html: کارت B&G → Update
s = io.open("ausbildung.html", encoding="utf-8").read()
s = s.replace('href="ausbildung-black-grey-workshop.html"', 'href="ausbildung-update-kurs.html"')
s = s.replace('src="assets/img/7.webp" alt="Black and Grey Workshop – SAAD Tattoo Wiesbaden"', 'src="assets/img/7.webp" alt="Update Kurs – SAAD Tattoo Wiesbaden"')
# گواهینامه در کارت‌ها اضافه شود: بعد از هر foot یک خط cert
s = s.replace('</a>\n    </div>\n  </div>\n</section>', '''</a>
    </div>
    <p style="margin-top:24px;color:var(--grey);font-size:14px;text-align:center" data-i18n="au_cert">Nach Abschluss des Kurses erhältst du ein gültiges Zertifikat.</p>
  </div>
</section>''')
io.open("ausbildung.html","w",encoding="utf-8").write(s)
print("ausbildung.html updated")

# index.html: کارت سوم (B&G workshop) → Update
s = io.open("index.html", encoding="utf-8").read()
s = s.replace('<a class="card edu-card" href="ausbildung-black-grey-workshop.html">', '<a class="card edu-card" href="ausbildung-update-kurs.html">')
io.open("index.html","w",encoding="utf-8").write(s)
print("index updated")

# ---------- ۳) صفحات جزئیات: بازسازی ۳ صفحه (حذف B&G قدیمی) ----------
import os
if os.path.exists("ausbildung-black-grey-workshop.html"): os.remove("ausbildung-black-grey-workshop.html")
base = io.open("buchen.html", encoding="utf-8").read()
NAV = base.split("<section")[0].split("<body>\n")[1]
FOOT = re.search(r"<footer>[\s\S]*?</div>\n</body>", base).group(0)
HEAD = '''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__T__ | SAAD Tattoo Wiesbaden</title>
<meta name="description" content="__D__">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css">
<link rel="stylesheet" href="assets/css/style.css?v=9">
<script src="assets/js/i18n.js?v=5" defer></script>
</head>
<body>
'''
def page(fname, title, desc, body):
    io.open(fname, "w", encoding="utf-8").write(HEAD.replace("__T__", title).replace("__D__", desc) + NAV + "\n" + body + "\n" + FOOT + "\n</body>\n</html>\n")
    print(fname, "built")

DETAIL = '''<section class="page-head" style="padding-bottom:0;text-align:start">
  <div class="wrap">
    <p class="eyebrow"><span class="num">03</span><span data-i18n="edu_eye">Ausbildung</span></p>
    <h1 data-i18n="au{n}_h1">{h1}</h1>
    <p class="lead" style="margin-top:16px" data-i18n="au{n}_p1">{p1}</p>
  </div>
</section>

<section style="padding-top:var(--sp-5)">
  <div class="wrap">
    <div class="split" style="align-items:start">
      <div class="ph zoom"><img class="mono" src="assets/img/{img}.webp" alt="{h1} – SAAD Tattoo Wiesbaden"></div>
      <div>
        <p class="eyebrow"><span class="num">i</span><span data-i18n="au_details">Kursdetails</span></p>
        <div class="steps" style="grid-template-columns:1fr;margin-top:0">
          <div class="step"><b data-i18n="sv_dauer">Dauer</b><p style="font-family:var(--font-head);color:var(--white);font-size:16px" data-i18n="au{n}_dur">{dur}</p></div>
          <div class="step"><b data-i18n="sv_preis">Preis</b><p style="font-family:var(--font-head);color:var(--white);font-size:16px" data-i18n="au{n}_preis">Auf Anfrage / mit Anruf</p></div>
          <div class="step"><b data-i18n="au_cert_h">Zertifikat</b><p data-i18n="au_cert">Nach Abschluss erhältst du ein gültiges Zertifikat.</p></div>
        </div>
        <div class="btn-row" style="margin-top:var(--sp-5)"><a class="btn btn-solid" href="kontakt.html?course={title}" data-i18n="au_anmelden">Platz anfragen</a>
        <a class="btn btn-ghost" href="tel:+4917622067475">0176 22067475</a></div>
      </div>
    </div>
  </div>
</section>

<div class="marquee" aria-hidden="true"><div class="track" data-i18n="mq_words">TATTOO · <i>WIESBADEN</i> · CUSTOM DESIGNS · <i>BERATUNG KOSTENLOS</i> · TATTOO · <i>WIESBADEN</i> · CUSTOM DESIGNS · <i>BERATUNG KOSTENLOS</i> · </div></div>

<section class="section" style="background:var(--ink)">
  <div class="wrap">
    <p class="eyebrow"><span class="num">✓</span><span data-i18n="au{n}_incl_h">Im Kurs enthalten</span></p>
    <h2 data-i18n="au{n}_incl_h">Im Kurs enthalten</h2>
    <div class="steps">
{incl_items}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <p class="eyebrow"><span class="num">§</span><span data-i18n="au{n}_vor_h">Voraussetzungen</span></p>
    <h2 data-i18n="au{n}_vor_h">Voraussetzungen</h2>
    <div class="faq" style="margin-top:48px">
{vor_items}
    </div>
  </div>
</section>'''

for d in COURSES:
    incl = "\n".join(
        f'      <div class="step"><b>0{i+1}</b><p style="color:var(--white);font-family:var(--font-body);font-size:15px;text-transform:none">{x}</p></div>'
        for i, x in enumerate(d["de"]["incl"]))
    vor = "\n".join(
        f'      <details><summary>{x}</summary></details>'
        for x in d["de"]["voraus"])
    body = DETAIL.format(n=d["n"], h1=d["de"]["h1"], p1=d["de"]["p1"], img=d["img"], dur=d["de"]["dur"], incl_items=incl, vor_items=vor, title=d["de"]["h1"])
    page(f"ausbildung-{d['slug']}.html", f"{d['de']['h1']} Wiesbaden | SAAD Tattoo", d["de"]["p1"][:150], body)

# ---------- ۴) au_cert_h کلید اضافه ----------
s = io.open("assets/js/i18n.js", encoding="utf-8").read()
extra = {"de":'au_cert_h:"Zertifikat",', "en":'au_cert_h:"Certificate",', "fa":'au_cert_h:"گواهینامه",'}
for lang, k in extra.items():
    a2 = {"de":'au_cert:"Nach jedem Kurs','en':'au_cert:"After completing','fa':'au_cert:"بعد از اتمام'}[lang]
    idx = s.index(a2); s = s[:idx] + k + s[idx:]
io.open("assets/js/i18n.js","w",encoding="utf-8").write(s)
print("cert key ok")

# ---------- ۵) cache-bust v6 ----------
for f in glob.glob("*.html"):
    t = io.open(f, encoding="utf-8").read().replace("i18n.js?v=5", "i18n.js?v=6")
    io.open(f, "w", encoding="utf-8").write(t)
print("v6")
