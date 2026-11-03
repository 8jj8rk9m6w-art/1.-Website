#!/usr/bin/env python3
"""Erzeugt alle Seiten der Website aus einer gemeinsamen Vorlage.

Aufruf:  python3 build.py
Inhalte ändern: Texte in den PAGES unten, Gottesdienstzeiten in SERVICES.
Die fertigen .html-Dateien liegen danach im selben Ordner (sie sind
eigenständig und funktionieren auch ohne JavaScript).
"""
import json
import pathlib
from html import escape as e

OUT = pathlib.Path(__file__).parent
STAND = "3. November 2026"
OFFICIAL = "https://www.katholisch-in-wipperfuerth.de"

# ---------------------------------------------------------------- Daten
BUERO = {
    "tel": "02267 88187-0", "tel_href": "+492267881870",
    "fax": "02267 88187-70", "notruf": "02267 88187-77", "notruf_href": "+4922678818777",
    "mail": "pastoralbuero-wipp@erzbistum-koeln.de",
    "adresse": "Kirchplatz 1, 51688 Wipperfürth",
}

CHURCHES = [
    {"id": "nik", "name": "St. Nikolaus", "place": "Wipperfürth", "addr": "Kirchplatz 3", "main": True},
    {"id": "neye", "name": "St. Michael", "place": "Neye", "addr": "Paulstraße 10"},
    {"id": "aga", "name": "St. Agatha", "place": "Agathaberg", "addr": "Agathaberg 24"},
    {"id": "kreuz", "name": "St. Johannes Ap. u. Ev.", "place": "Kreuzberg", "addr": "Westfalenstraße 36"},
    {"id": "thier", "name": "St. Anna", "place": "Thier", "addr": "Joh.-Wilh.-Roth-Straße 30a"},
    {"id": "wipf", "name": "St. Clemens", "place": "Wipperfeld", "addr": "Dorfstraße 8b"},
    {"id": "egen", "name": "Unbefleckte Empfängnis", "place": "Egen", "addr": ""},
    {"id": "haem", "name": "St. Anna", "place": "Hämmern", "addr": "Jostberg 4"},
    {"id": "nied", "name": "Herz Jesu", "place": "Niederwipper", "addr": "Niederwipper 83"},
    {"id": "omm", "name": "St. Johannes der Täufer", "place": "Ommerborn", "addr": ""},
    {"id": "franz", "name": "Franziskusheim", "place": "Seniorenzentrum", "addr": "Konrad-Martin-Weg 3", "senior": True},
    {"id": "quart", "name": "Senioren-Quartier", "place": "Seniorenzentrum", "addr": "Lüdenscheider Str. 49–51", "senior": True},
]
CH = {c["id"]: c for c in CHURCHES}
KUESTER = {
    "nik": "Markus Löhr", "neye": "Markus Löhr", "kreuz": "Andrea Agartz", "thier": "Andrea Agartz",
    "aga": "Susanne Hebbecker", "wipf": "Heidi Küster", "egen": "Heidi Küster", "haem": "Heidi Küster",
    "nied": "Heidi Küster", "omm": "Heidi Küster",
}

# d = Wochentage (0 So … 6 Sa), n = Woche im Monat (1–5 oder "last"), m = Monate, k = Art
SERVICES = [
    {"c": "nik", "d": [6], "t": "18:00", "title": "Vorabendmesse", "k": "mass"},
    {"c": "nik", "d": [0], "t": "08:00", "title": "Hl. Messe", "k": "mass"},
    {"c": "nik", "d": [0], "t": "11:00", "title": "Hochamt", "k": "mass"},
    {"c": "nik", "d": [1, 2, 5], "t": "08:00", "title": "Hl. Messe", "k": "mass"},
    {"c": "nik", "d": [3], "t": "08:00", "title": "Schulmesse", "k": "school", "note": "nicht in den Ferien"},
    {"c": "nik", "d": [3], "t": "18:00", "title": "Hl. Messe (mit Gebet für die Verstorbenen der Woche)", "k": "mass"},
    {"c": "nik", "d": [4], "t": "08:00", "title": "Hl. Messe / Schulmesse", "k": "mass", "note": "Schulmesse ggf. 08:15"},
    {"c": "nik", "d": [6], "t": "17:00", "title": "Beichtgelegenheit", "k": "prayer"},
    {"c": "neye", "d": [0], "t": "19:00", "title": "Hl. Messe", "k": "mass"},
    {"c": "neye", "d": [0], "n": [3], "t": "11:00", "title": "Familiengottesdienst", "k": "fam", "note": "Abweichungen in den Pfarrnachrichten"},
    {"c": "neye", "d": [0], "n": ["last"], "t": "10:30", "title": "Kleine-Leute-Gottesdienst", "k": "fam"},
    {"c": "aga", "d": [0], "n": [1, 3], "t": "09:30", "title": "Hl. Messe", "k": "mass"},
    {"c": "aga", "d": [2], "n": [1, 3], "m": [3, 4, 5, 6, 7, 8, 9, 10], "t": "18:30", "title": "Andacht", "k": "prayer", "note": "März bis Oktober"},
    {"c": "kreuz", "d": [0], "n": [2, 4], "t": "09:30", "title": "Hl. Messe", "k": "mass"},
    {"c": "kreuz", "d": [4], "t": "18:30", "tw": "17:30", "title": "Andacht", "k": "prayer", "note": "Oktober bis Ostern 17:30"},
    {"c": "kreuz", "d": [3], "n": [2], "t": "08:00", "title": "Schulmesse", "k": "school", "note": "nicht in den Ferien"},
    {"c": "kreuz", "d": [3], "n": [4], "t": "08:00", "title": "Schulgottesdienst", "k": "school", "note": "nicht in den Ferien"},
    {"c": "thier", "d": [0], "n": [1, 3], "t": "09:30", "title": "Hl. Messe", "k": "mass"},
    {"c": "thier", "d": [3], "t": "09:00", "title": "Hl. Messe bzw. Wortgottesdienst", "k": "mass"},
    {"c": "thier", "d": [5], "t": "08:30", "title": "Morgenlob", "k": "prayer", "note": "nicht in den Ferien"},
    {"c": "thier", "d": [3], "n": [2], "t": "19:00", "title": "Friedensgebet", "k": "prayer"},
    {"c": "wipf", "d": [0], "n": [2, 4], "t": "09:30", "title": "Hl. Messe", "k": "mass"},
    {"c": "wipf", "d": [2], "t": "08:00", "title": "Schulgottesdienst", "k": "school", "note": "nicht in den Ferien"},
    {"c": "egen", "d": [6], "n": [1], "t": "19:00", "title": "Hl. Messe", "k": "mass"},
    {"c": "haem", "d": [6], "n": [2], "t": "19:00", "title": "Hl. Messe", "k": "mass"},
    {"c": "nied", "d": [6], "n": [3], "t": "19:00", "title": "Hl. Messe", "k": "mass"},
    {"c": "omm", "d": [6], "n": [4], "t": "19:00", "title": "Hl. Messe", "k": "mass"},
    {"c": "franz", "d": [6], "t": "16:30", "title": "Hl. Messe", "k": "mass"},
    {"c": "quart", "d": [4], "n": [1], "t": "16:00", "title": "Hl. Messe", "k": "mass"},
]
EXTRA_PLAN = {
    "aga": ["Schulgottesdienste nach Absprache mit der Schule (3–4× im Jahr)"],
}

TEAM = [
    ("Lambert Schäfer", "Leitender Pfarrer · koordinierender Pfarrer der Pastoralen Einheit Oberberg-Nord", "02267 88187-13", "lambert.schaefer@erzbistum-koeln.de", "assets/pfarrer.jpg"),
    ("Stefan Ochalski", "Pfarrvikar", "02267 828302", "stefan.ochalski@erzbistum-koeln.de", None),
    ("Joseph Abitya", "Pfarrvikar · Taufbegleitung", "02267 8716124", "joseph.abitya@erzbistum-koeln.de", None),
    ("Kingsly Paniyadimai", "Kaplan", None, None, None),
    ("Markus Urbatzka", "Pastoralreferent · Erstkommunion", "02267 8889577", "markus.urbatzka@erzbistum-koeln.de", None),
    ("Peter Bühlstahl", "Gemeindereferent", "02268 800620", "peter.buehlstahl@erzbistum-koeln.de", None),
    ("Georg Kalkum", "Gemeindereferent · Krankenhausseelsorge Helios-Klinik · Schöpfungsverantwortung", "02195 684453", "georg.kalkum@erzbistum-koeln.de", None),
    ("Thomas Ufer", "Verwaltungsleitung", "02267 88187-14", "ufer@kath-wipp.de", None),
]

DAYS = ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"]
KIND = {"mass": "Hl. Messe", "fam": "Familie & Kinder", "prayer": "Andacht & Gebet", "school": "Schule"}


def tel(num):
    digits = "".join(ch for ch in num if ch.isdigit())
    return f'<a href="tel:+49{digits[1:]}">{e(num)}</a>'


def mail(m):
    return f'<a href="mailto:{m}">{e(m)}</a>'


def plan_lines(cid):
    out = []
    for s in SERVICES:
        if s["c"] != cid:
            continue
        days = ", ".join(DAYS[d] for d in s["d"])
        if s.get("n"):
            nn = " & ".join("letzter" if n == "last" else f"{n}." for n in s["n"])
            days = f"{nn} {days} im Monat"
        out.append((days, s["t"], s["title"], s.get("note", "")))
    return out


def plan_table(ids):
    rows = []
    for cid in ids:
        c = CH[cid]
        lines = plan_lines(cid)
        first = True
        for days, t, title, note in lines:
            label = f'<b>{e(c["name"])}</b><br><span class="muted small">{e(c["place"])}</span>' if first else ""
            note_html = f'<br><span class="muted small">{e(note)}</span>' if note else ""
            rows.append(f"<tr><td>{label}</td><td>{e(days)}</td><td>{t}</td><td>{e(title)}{note_html}</td></tr>")
            first = False
        for x in EXTRA_PLAN.get(cid, []):
            rows.append(f'<tr><td></td><td colspan="3" class="muted">{e(x)}</td></tr>')
    return ('<div class="tbl-wrap"><table class="tbl plan"><thead><tr><th>Kirche</th><th>Wann</th><th>Uhr</th>'
            '<th>Gottesdienst</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table></div>")


# ---------------------------------------------------------------- Vorlage
NAV = [
    ("gottesdienste.html", "Gottesdienste"),
    ("anliegen.html", "Taufe, Hochzeit &amp; Co."),
    ("kirchorte.html", "Kirchorte"),
    ("gruppen.html", "Gruppen"),
    ("aktuelles.html", "Aktuelles"),
    ("hilfe.html", "Hilfe"),
    ("kontakt.html", "Kontakt"),
]
DRAWER_EXTRA = [("team.html", "Ansprechpersonen"), ("messe-bestellen.html", "Messe bestellen")]
ANLIEGEN_PAGES = {"taufe.html", "erstkommunion.html", "firmung.html", "hochzeit.html", "beichte.html",
                  "krankensalbung.html", "trauerfall.html", "messe-bestellen.html", "anliegen.html"}

ICON = {
    "search": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
    "moon": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
    "menu": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
}

LOGO = ('<svg width="38" height="38" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="11" fill="var(--accent)"/>'
        '<path d="M20 7v26M13 14h14" stroke="var(--accent-ink)" stroke-width="3" stroke-linecap="round"/>'
        '<path d="M11 33c0-6 4-9 9-9s9 3 9 9" fill="none" stroke="var(--accent-ink)" stroke-width="2.4" stroke-linecap="round" opacity=".7"/></svg>')


def header(current):
    def cur(href):
        active = href == current or (href == "anliegen.html" and current in ANLIEGEN_PAGES)
        return ' aria-current="page"' if active else ""
    nav = "".join(f'<a href="{h}"{cur(h)}>{t}</a>' for h, t in NAV)
    drawer = "".join(f'<a href="{h}"{cur(h)}>{t}</a>' for h, t in [("index.html", "Start")] + NAV + DRAWER_EXTRA)
    return f'''<a class="skip" href="#inhalt">Zum Inhalt springen</a>
<div class="notice" role="note"><div class="wrap"><strong>Entwurf</strong><span>Neugestaltung als Schulprojekt – keine offizielle Seite der Pfarrei. Angaben von <a href="{OFFICIAL}/">katholisch-in-wipperfuerth.de</a>, Stand {STAND}.</span></div></div>
<header class="top">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Katholisch in Wipperfürth – Startseite">{LOGO}<span><b>Katholisch in Wipperfürth</b><small>Pfarrei St. Nikolaus · Website-Entwurf</small></span></a>
    <nav class="main" aria-label="Hauptmenü">{nav}</nav>
    <div class="head-actions">
      <button class="icon-btn" id="searchBtn" type="button" aria-label="Suche öffnen" aria-expanded="false" aria-controls="searchpanel">{ICON["search"]}</button>
      <button class="icon-btn" id="themeBtn" type="button" aria-label="Hell/Dunkel umschalten">{ICON["moon"]}</button>
      <button class="icon-btn" id="menuBtn" type="button" aria-label="Menü öffnen" aria-expanded="false" aria-controls="drawer">{ICON["menu"]}</button>
    </div>
  </div>
  <div class="searchpanel" id="searchpanel"><div class="wrap">{search_box("q2")}</div></div>
  <nav class="drawer" id="drawer" aria-label="Menü">{drawer}</nav>
</header>'''


def search_box(id_):
    return f'''<form class="search" role="search" action="suche.html" data-search>
  <label class="sr" for="{id_}">Was suchst du?</label>{ICON["search"]}
  <input id="{id_}" name="q" type="search" placeholder="Was suchst du? z. B. Taufe, Beichte, Messdiener" autocomplete="off">
  <div class="results" role="listbox" hidden></div>
</form>'''


FOOTER = f'''<footer>
  <div class="wrap cols">
    <div>
      <h3>Katholisch in Wipperfürth</h3>
      <p>Kath. Pfarrei St. Nikolaus · {BUERO["adresse"]}<br>Tel. {BUERO["tel"]} · <a href="mailto:{BUERO["mail"]}">{BUERO["mail"]}</a><br>Erzbistum Köln · Pastorale Einheit Oberberg-Nord</p>
      <p class="small">Diese Website ist ein Schulprojekt (Q2 Kath. Religion) und keine offizielle Seite der Pfarrei. Verbindlich sind <a href="{OFFICIAL}/">katholisch-in-wipperfuerth.de</a> und die Pfarrnachrichten.</p>
    </div>
    <div>
      <h3>Schnell gefunden</h3>
      <ul><li><a href="gottesdienste.html">Gottesdienste</a></li><li><a href="taufe.html">Taufe</a></li><li><a href="hochzeit.html">Hochzeit</a></li><li><a href="trauerfall.html">Trauerfall</a></li><li><a href="messe-bestellen.html">Messe bestellen</a></li><li><a href="team.html">Ansprechpersonen</a></li></ul>
    </div>
    <div>
      <h3>Links</h3>
      <ul><li><a href="{OFFICIAL}/">Offizielle Website</a></li><li><a href="{OFFICIAL}/aktuelles/pfarrnachichten/">Pfarrnachrichten</a></li><li><a href="https://www.erzbistum-koeln.de/">Erzbistum Köln</a></li><li><a href="{OFFICIAL}/impressum/">Impressum</a> · <a href="{OFFICIAL}/datenschutz/">Datenschutz</a></li><li><a href="konzept-entwurf-v1.html">Unser erster Konzeptentwurf</a></li></ul>
    </div>
  </div>
</footer>
<nav class="tabbar" aria-label="Schnellnavigation">
  <a href="gottesdienste.html"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 10h16M9 3v4M15 3v4"/></svg>Messen</a>
  <a href="anliegen.html"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/></svg>Anliegen</a>
  <a href="kirchorte.html"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M12 2v4M10 4h4M6 21V11l6-5 6 5v10zM10 21v-5h4v5"/></svg>Kirchen</a>
  <a href="kontakt.html"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>Kontakt</a>
</nav>
<script src="assets/data.js"></script>
<script src="assets/app.js"></script>'''


def page(filename, title, desc, body, current=None):
    full_title = "Katholisch in Wipperfürth" if filename == "index.html" else f"{title} – Katholisch in Wipperfürth"
    html = f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#7d2328">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Crect width='40' height='40' rx='11' fill='%237d2328'/%3E%3Cpath d='M20 7v26M13 14h14' stroke='white' stroke-width='3' stroke-linecap='round'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Source+Sans+3:wght@400;600;700&display=swap">
<link rel="stylesheet" href="assets/style.css">
<script>try{{var t=localStorage.getItem("theme");if(t)document.documentElement.dataset.theme=t}}catch(_){{}}</script>
</head>
<body data-page="{filename[:-5]}">
{header(current or filename)}
<main id="inhalt">
{body}
</main>
{FOOTER}
</body>
</html>
'''
    (OUT / filename).write_text(html, encoding="utf-8")


def hero(title, lead, crumbs, eyebrow=""):
    cr = '<a href="index.html">Start</a>' + "".join(
        f' › <a href="{h}">{t}</a>' if h else f" › {t}" for h, t in crumbs)
    return f'''<section class="page-hero"><div class="wrap">
  <nav class="crumbs" aria-label="Brotkrumen">{cr}</nav>
  {f'<div class="eyebrow">{eyebrow}</div>' if eyebrow else ''}<h1>{title}</h1>
  <p class="lead">{lead}</p>
</div></section>'''


def office_card(extra=""):
    return f'''<div class="side-card">
  <h3>Pastoralbüro</h3>
  <span class="status off" data-office-badge>Öffnungszeiten</span>
  <p>{BUERO["adresse"].replace(", ", "<br>")}<br>Tel. {tel(BUERO["tel"])}<br>{mail(BUERO["mail"])}</p>
  <p class="small muted" style="margin:0">Mo, Di, Do, Fr 08:30–15:30 · Mi 08:30–12:30 · Sa 10–12 nur per E-Mail</p>
  {extra}
</div>
<div class="side-card" style="background:var(--accent-soft);border-color:transparent">
  <h3>Seelsorglicher Notruf</h3>
  <p style="margin:0">Rund um die Uhr: <b>{tel(BUERO["notruf"])}</b></p>
</div>'''


def layout(main, aside=None):
    return f'<div class="wrap layout"><div class="prose">{main}</div><aside>{aside or office_card()}</aside></div>'


# ---------------------------------------------------------------- Seiten
def build_index():
    quick = [
        ("gottesdienste.html", "Gottesdienste", "Alle Zeiten in 10 Kirchen – heute, morgen, am Wochenende."),
        ("taufe.html", "Taufe", "Taufsonntage, Tauftreff und Anmeldung."),
        ("hochzeit.html", "Hochzeit", "Termine, Unterlagen und Ablauf der Trauung."),
        ("trauerfall.html", "Trauerfall", "Was jetzt zu tun ist – und wer hilft."),
        ("erstkommunion.html", "Erstkommunion", "Termine 2027 und Vorbereitung."),
        ("beichte.html", "Beichte &amp; Gespräch", "Samstags 17:00 in St. Nikolaus oder nach Absprache."),
        ("messe-bestellen.html", "Messe bestellen", "Für Verstorbene oder ein persönliches Anliegen."),
        ("gruppen.html", "Mitmachen", "Messdiener, Chöre, Pfadfinder, Ehrenamt."),
    ]
    tiles = "".join(f'<a href="{h}"><b>{t}</b><span>{d}</span><span class="go">Öffnen →</span></a>' for h, t, d in quick)
    body = f'''
<section class="hero" aria-labelledby="h1">
  <div class="wrap">
    <div>
      <div class="eyebrow">Pfarrei St. Nikolaus · 10 Kirchen · ein Ort für dich</div>
      <h1 id="h1">Willkommen in <em>Wipperfürth.</em></h1>
      <p class="lead">Gottesdienste, Taufe, Hochzeit, Abschied, Gemeinschaft und Hilfe – hier findest du schnell, was du suchst. Egal, ob du jeden Sonntag kommst oder lange nicht mehr da warst.</p>
      {search_box("q")}
      <div class="chips-hero" aria-label="Häufig gesucht">
        <a href="gottesdienste.html">Messe am Sonntag</a><a href="taufe.html">Taufe anmelden</a><a href="trauerfall.html">Trauerfall</a><a href="messe-bestellen.html">Messe bestellen</a>
      </div>
    </div>
    <div class="now" aria-live="polite">
      <div class="now-card">
        <div class="label">Nächster Gottesdienst</div>
        <div class="big" id="nextTitle">Sa 18:00 · So 08:00 &amp; 11:00</div>
        <div class="sub" id="nextSub">St. Nikolaus, Kirchplatz · <a href="gottesdienste.html">alle Zeiten</a></div>
      </div>
      <div class="now-card">
        <div class="label">Pastoralbüro</div>
        <div class="big" id="officeNow">Mo–Fr ab 08:30</div>
        <div class="sub">{tel(BUERO["tel"])} · <a href="kontakt.html">Kontakt &amp; Öffnungszeiten</a></div>
      </div>
      <div class="now-card">
        <div class="label">Seelsorglicher Notruf – rund um die Uhr</div>
        <div class="big"><a href="tel:{BUERO["notruf_href"]}" style="color:inherit;text-decoration:none">{BUERO["notruf"]}</a></div>
        <div class="sub">Für Krankensalbung, Sterbebegleitung und akute Not.</div>
      </div>
    </div>
  </div>
</section>

<section class="block" aria-labelledby="h-start">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">Ich möchte …</div><h2 id="h-start">Die häufigsten Anliegen</h2></div></div>
    <div class="tiles">{tiles}</div>
  </div>
</section>

<section class="block alt" aria-labelledby="h-week">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">Jede Woche</div><h2 id="h-week">Gottesdienste am Wochenende</h2>
    <p>Die wichtigsten Zeiten auf einen Blick. Alle Gottesdienste mit Tagesansicht und Filtern findest du auf der Gottesdienst-Seite.</p></div>
    <a class="btn primary" href="gottesdienste.html">Alle Gottesdienste</a></div>
    <div class="week">
      <div><b>Sa 17:00</b><span>Beichtgelegenheit · St. Nikolaus</span></div>
      <div><b>Sa 18:00</b><span>Vorabendmesse · St. Nikolaus</span></div>
      <div><b>Sa 19:00</b><span>Hl. Messe, wechselnd: 1. Sa Egen · 2. Sa Hämmern · 3. Sa Niederwipper · 4. Sa Ommerborn</span></div>
      <div><b>So 08:00</b><span>Hl. Messe · St. Nikolaus</span></div>
      <div><b>So 09:30</b><span>1./3. So Agathaberg &amp; Thier · 2./4. So Kreuzberg &amp; Wipperfeld</span></div>
      <div><b>So 11:00</b><span>Hochamt · St. Nikolaus <span class="muted">(3. So zusätzlich Familiengottesdienst in Neye)</span></span></div>
      <div><b>So 19:00</b><span>Hl. Messe · St. Michael, Neye</span></div>
    </div>
  </div>
</section>

<section class="block" aria-labelledby="h-news">
  <div class="wrap">
    <div class="sec-head"><div><div class="eyebrow">Aktuelles</div><h2 id="h-news">Was gerade los ist</h2></div><a class="btn ghost" href="aktuelles.html">Alle Meldungen</a></div>
    <div class="news">{news_cards(3)}</div>
  </div>
</section>

<section class="block alt" aria-labelledby="h-kirche">
  <div class="wrap feature">
    <div>
      <div class="eyebrow">Unsere Pfarrkirche</div>
      <h2 id="h-kirche">St. Nikolaus – seit 1143</h2>
      <p style="margin-top:14px">Stiftsherren von St. Aposteln in Köln begannen 1143 mit dem Bau. Entstanden ist eine dreischiffige romanische Pfeilerbasilika mit Kreuzrippengewölben aus dem 13. Jahrhundert. Das Taufbecken stammt aus den ersten Jahrzehnten des 13. Jahrhunderts – hier wird bis heute getauft.</p>
      <p class="muted">Zur Pfarrei gehören zehn Kirchen von Agathaberg bis Wipperfeld, rund 9.970 Katholik:innen leben in Wipperfürth.</p>
      <a class="btn ghost" href="kirchorte.html">Alle Kirchorte</a>
    </div>
    <div class="art" aria-hidden="true">
      <svg viewBox="0 0 200 150" width="70%" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round">
        <path d="M92 10v12M86 16h12"/><path d="M78 140V46l14-20 14 20v94"/><path d="M106 70h70v70H106M78 70H24v70h54"/>
        <path d="M24 70l27-22 27 22M106 70l35-26 35 26"/><path d="M86 140v-22a6 6 0 0 1 12 0v22"/>
        <path d="M38 96v-8a5 5 0 0 1 10 0v8zM58 96v-8a5 5 0 0 1 10 0v8zM122 96v-8a5 5 0 0 1 10 0v8zM150 96v-8a5 5 0 0 1 10 0v8z"/>
        <path d="M86 62v-6a6 6 0 0 1 12 0v6z"/><path d="M10 140h180"/>
      </svg>
    </div>
  </div>
</section>

<section class="block" aria-labelledby="h-unit">
  <div class="wrap unit">
    <div>
      <div class="eyebrow">Kirche im Wandel</div>
      <h2 id="h-unit">Pastorale Einheit Oberberg-Nord</h2>
      <p style="margin-top:14px">Seit dem 1. September 2023 bildet unsere Pfarrei mit Lindlar, Marienheide und Hückeswagen/Radevormwald eine Pastorale Einheit. Pfarrer Lambert Schäfer ist koordinierender Pfarrer. Wir teilen Ideen, Personal und Angebote – und bleiben vor Ort ansprechbar.</p>
      <a class="btn ghost" href="{OFFICIAL}/oberberg-nord/oberberg-nord-gemeinsam/">Mehr zu Oberberg-Nord</a>
    </div>
    <div class="unit-map" aria-label="Partner der Pastoralen Einheit">
      <div class="me"><b>Wipperfürth</b><span>Pfarrei St. Nikolaus · 10 Kirchen</span></div>
      <div><b>Lindlar</b><span>Seelsorgebereich · 5 Kirchorte</span></div>
      <div><b>Marienheide</b><span>Pfarrei</span></div>
      <div><b>Hückeswagen / Radevormwald</b><span>Kirchengemeindeverband</span></div>
    </div>
  </div>
</section>'''
    page("index.html", "Start", "Pfarrei St. Nikolaus Wipperfürth – Gottesdienste, Taufe, Hochzeit, Trauerfall, Kirchorte, Gruppen und Kontakt.", body)


NEWS = [
    ("Firmung · Mitte November 2026", "Firmung in St. Michael, Neye", "Die Jugendlichen des Jahrgangs 2010 werden in Neye gefirmt – in Abstimmung mit Weihbischof Ansgar Puff. Bitte betet für sie!", "firmung.html", "Zur Firmung"),
    ("Termin · Sa, 5. Dezember 2026", "Tauftreff in St. Nikolaus", "Für Eltern, die ihr Kind taufen lassen möchten: kennenlernen, Fragen klären, Taufe vorbereiten. 10:30 Uhr.", "taufe.html", "Zur Taufe"),
    ("Patrozinium · 6. Dezember", "Fest des hl. Nikolaus", "Unser Pfarrpatron steht für Großzügigkeit und den Schutz der Kinder. Die Festgottesdienste stehen in den Pfarrnachrichten.", f"{OFFICIAL}/aktuelles/pfarrnachichten/", "Pfarrnachrichten"),
    ("Erstkommunion 2027", "Feiern ab 3. April 2027", "Sechs Erstkommunionfeiern in Neye, Agathaberg, Hämmern, Kreuzberg und Wipperfeld. Kinder der 3. Klasse werden angeschrieben.", "erstkommunion.html", "Termine ansehen"),
    ("Ehrenamt gesucht", "Taufgeschenke überbringen", "Wir suchen Menschen, die neu getauften Kindern und ihren Familien ein Geschenk der Gemeinde vorbeibringen.", "kontakt.html#anliegen-Ehrenamt", "Mitmachen"),
    ("Schöpfung bewahren", "Schöpfungsbotschafter:in werden", "Mit „Klima+Kirche“ und unserem Projekt Schöpfungsverantwortung (nach „Laudato Si’“) wird die Pfarrei klimafreundlicher.", "gruppen.html#schoepfung", "Mehr erfahren"),
    ("Gemeindereise 2027", "Donauklöster und Wien", "Gemeinsam reisen, Klöster entdecken, Gemeinschaft erleben. Infos und Anmeldung über das Pastoralbüro.", "kontakt.html#anliegen-Gemeindereise", "Interesse melden"),
    ("Stellenangebot", "Leitung KiTa St. Raphael, Kreuzberg", "Gesucht zum 1. September 2026. Außerdem: Berater:in mit stellvertretender Leitung in der Beratungsstelle Herbstmühle.", f"{OFFICIAL}/aktuelles/offene-stellen/", "Alle Stellen"),
    ("Taufsonntage ab 2027", "Neue feste Tauftermine", "Ab 1. Januar 2027 in St. Nikolaus: 2. Sonntag im Monat 12:15 Uhr und 4. Sonntag 15:00 Uhr, je bis zu drei Familien.", "taufe.html", "Zur Taufe"),
]


def news_cards(n=None):
    out = []
    for kind, title, text, href, more in NEWS[:n]:
        out.append(f'<article><span class="kind">{e(kind)}</span><h3>{e(title)}</h3><p>{e(text)}</p><a class="more" href="{href}">{more} →</a></article>')
    return "".join(out)


def build_gottesdienste():
    main_ids = ["nik", "neye", "aga", "kreuz", "thier", "wipf", "egen", "haem", "nied", "omm"]
    body = hero("Gottesdienste", "Alle regelmäßigen Gottesdienste in den zehn Kirchen und den Seniorenzentren. Änderungen, Feiertage und Ferien stehen in den Pfarrnachrichten.", [(None, "Gottesdienste")], "Messen · Andachten · Beichte") + f'''
<div class="wrap layout">
<div class="prose" style="max-width:none">
  <nav class="anchor-nav" aria-label="Auf dieser Seite"><a href="#finder">Die nächsten 7 Tage</a><a href="#ordnung">Gottesdienstordnung</a><a href="#beichte">Beichte</a><a href="#senioren">Seniorenzentren</a><a href="#messe">Messe bestellen</a></nav>
  <h2 id="finder">Die nächsten 7 Tage</h2>
  <noscript><div class="empty">Die Tagesansicht braucht JavaScript. Alle Zeiten stehen unten in der Gottesdienstordnung.</div></noscript>
  <div class="days" id="days" role="group" aria-label="Tag wählen"></div>
  <div class="filters" id="kindFilters">
    <button class="chip" type="button" data-kind="all" aria-pressed="true">Alle</button>
    <button class="chip" type="button" data-kind="mass" aria-pressed="false">Hl. Messe</button>
    <button class="chip" type="button" data-kind="fam" aria-pressed="false">Familie &amp; Kinder</button>
    <button class="chip" type="button" data-kind="prayer" aria-pressed="false">Andacht, Gebet &amp; Beichte</button>
    <button class="chip" type="button" data-kind="school" aria-pressed="false">Schule</button>
    <label class="sr" for="placeSel">Ort</label>
    <select id="placeSel"><option value="">Alle Orte</option>{"".join(f'<option value="{c["id"]}">{e(c["name"])} – {e(c["place"])}</option>' for c in CHURCHES)}</select>
  </div>
  <div class="svc-list" id="svcList" aria-live="polite"></div>

  <h2 id="ordnung">Gottesdienstordnung</h2>
  <p>So sieht eine normale Woche aus.</p>
  {plan_table(main_ids)}

  <h2 id="beichte">Beichte</h2>
  <p><b>Samstags um 17:00 Uhr in St. Nikolaus.</b> Vor den großen Feiertagen gibt es zusätzliche Beichtzeiten (siehe Pfarrnachrichten). Außerdem kannst du mit jedem Priester einen persönlichen Termin vereinbaren. <a href="beichte.html">Mehr zur Beichte</a></p>

  <h2 id="senioren">Seniorenzentren &amp; Krankenhaus</h2>
  {plan_table(["franz", "quart"])}
  <ul>
    <li>DRK-Seniorenzentrum, Sonnenweg 2–4: Montag 10:30 Uhr Hl. Messe (alle 4 Wochen)</li>
    <li>Krankenhauskapelle St. Josef, Alte Kölner Str. 3: Gottesdienste nur nach vorheriger Ankündigung</li>
  </ul>

  <h2 id="messe">Messe bestellen</h2>
  <p>Du kannst eine Messe für Verstorbene oder für ein persönliches Anliegen feiern lassen. Das Messstipendium beträgt 5,00 €. Bestellen kannst du im Pastoralbüro, telefonisch, mit dem Papierformular in den Kirchen oder über unser Formular.</p>
  <p><a class="btn primary" href="messe-bestellen.html">Messe bestellen</a></p>
  <p class="muted small">Jeden Mittwoch um 18:00 Uhr betet die Gemeinde in St. Nikolaus für alle, die in der Woche zuvor beerdigt wurden.</p>
</div>
<aside>
  <div class="side-card"><h3>Für Familien</h3><p class="muted" style="margin:0"><b>3. Sonntag</b> 11:00 Familiengottesdienst und <b>letzter Sonntag</b> 10:30 Kleine-Leute-Gottesdienst – beide in St. Michael, Neye.</p></div>
  {office_card()}
</aside>
</div>'''
    page("gottesdienste.html", "Gottesdienste", "Gottesdienstzeiten aller zehn Kirchen der Pfarrei St. Nikolaus Wipperfürth.", body)


ANLIEGEN = [
    ("taufe.html", "Taufe", "Taufsonntage, Tauftreff am 5.12.2026, Anmeldung und Paten."),
    ("erstkommunion.html", "Erstkommunion", "Feiertermine 2027, Vorbereitung und Anmeldung."),
    ("firmung.html", "Firmung", "Firmkurs, Jahrgang und Firmfeier in Neye."),
    ("hochzeit.html", "Hochzeit", "Trauungstermine, Unterlagen, Musik und Ablauf."),
    ("beichte.html", "Beichte &amp; Gespräch", "Samstags 17:00 oder nach Vereinbarung."),
    ("krankensalbung.html", "Krankensalbung", "Kein Abschiedssakrament – Stärkung in schwerer Zeit."),
    ("trauerfall.html", "Trauerfall", "Beerdigung, Friedhöfe, Trauerbegleitung und Hospiz."),
    ("messe-bestellen.html", "Messe bestellen", "Für Verstorbene oder ein Anliegen – 5 € Stipendium."),
]


def build_anliegen():
    tiles = "".join(f'<a href="{h}"><b>{t}</b><span>{d}</span><span class="go">Öffnen →</span></a>' for h, t, d in ANLIEGEN)
    body = hero("Wir begleiten dich", "An den wichtigen Tagen deines Lebens – von der Taufe bis zum Abschied. Wähle dein Anliegen: Du findest jeweils Termine, Ablauf und Ansprechpersonen.", [(None, "Anliegen")], "Sakramente &amp; Lebenswege") + f'''
<section class="block"><div class="wrap"><div class="tiles">{tiles}</div>
<div class="info" style="margin-top:28px"><b>Zurückkommen?</b>Du bist ausgetreten und denkst über einen Wiedereintritt nach – oder möchtest als Erwachsene:r getauft werden? Ein unverbindliches Gespräch ist der erste Schritt. Deine Taufe bleibt gültig. <a href="kontakt.html#anliegen-Wiedereintritt">Gespräch anfragen</a></div>
</div></section>'''
    page("anliegen.html", "Anliegen", "Taufe, Erstkommunion, Firmung, Hochzeit, Beichte, Krankensalbung und Trauerfall in Wipperfürth.", body)


def build_taufe():
    main = f'''
<div class="info"><b>Nächster Tauftreff</b>Samstag, 5. Dezember 2026, 10:30 Uhr in St. Nikolaus. Die Einladungen liegen am Schriftenstand aus.</div>
<h2>So meldest du eine Taufe an</h2>
<ol class="steps">
  <li><b>Pastoralbüro kontaktieren</b> – telefonisch unter {tel(BUERO["tel"])} oder per E-Mail. Der Tauftermin wird individuell mit dir abgestimmt.</li>
  <li><b>Tauftreff besuchen</b> – die offenen Treffen finden in unregelmäßigen Abständen statt; dort lernst du andere Familien kennen und bereitest die Feier vor.</li>
  <li><b>Taufe feiern</b> – gespendet von einem Priester oder Diakon.</li>
</ol>
<h2>Tauftermine</h2>
<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Wann</th><th>Wo</th><th>Hinweis</th></tr></thead><tbody>
<tr><td>2. Sonntag im Monat, 12:15 Uhr</td><td>St. Nikolaus</td><td>ab 1. Januar 2027, bis zu 3 Familien</td></tr>
<tr><td>4. Sonntag im Monat, 15:00 Uhr</td><td>St. Nikolaus</td><td>ab 1. Januar 2027, bis zu 3 Familien</td></tr>
<tr><td>in einer Sonntagsmesse</td><td>nach Absprache</td><td>auch in anderen Kirchorten, z. B. Thier oder Wipperfeld</td></tr>
<tr><td>Familiengottesdienst, Kleine-Leute-Gottesdienst zu Ostern, Firmfeier</td><td>nach Absprache</td><td>nach vorheriger Klärung</td></tr>
</tbody></table></div>
<h2>Was bedeutet die Taufe?</h2>
<p>Mit der Taufe wird ein Mensch Christ und Teil der Kirche. Eltern und Paten bekennen ihren Glauben und versprechen, das Kind im katholischen Glauben zu begleiten und zu erziehen.</p>
<h3>Patinnen und Paten</h3>
<p>Nach dem Kirchenrecht sollte mindestens eine Patin oder ein Pate katholisch und gefirmt sein und das 16. Lebensjahr vollendet haben. Bei Fragen hilft das Pastoralbüro.</p>
<h3>Erwachsene und ältere Kinder</h3>
<p>Auch als Jugendliche:r oder Erwachsene:r kannst du getauft werden. Ein Gespräch mit dem Seelsorgeteam ist der erste Schritt.</p>
<p><a class="btn primary" href="kontakt.html#anliegen-Taufe">Taufe anfragen</a></p>'''
    aside = f'''<div class="side-card"><h3>Taufbegleitung</h3><p><b>Joseph Abitya</b>, Pfarrvikar<br>Tel. {tel("02267 8716124")}<br>{mail("joseph.abitya@erzbistum-koeln.de")}</p></div>{office_card()}'''
    page("taufe.html", "Taufe", "Taufe in der Pfarrei St. Nikolaus Wipperfürth: Termine, Tauftreff, Anmeldung.",
         hero("Taufe", "Willkommen in der Gemeinschaft! Hier erfährst du, wie du dein Kind (oder dich selbst) taufen lassen kannst.", [("anliegen.html", "Anliegen"), (None, "Taufe")], "Sakrament") + layout(main, aside))


def build_erstkommunion():
    rows = [("Sa, 03.04.2027", "12:00", "St. Michael, Neye"), ("Sa, 03.04.2027", "14:30", "St. Michael, Neye"),
            ("So, 04.04.2027", "10:00", "St. Agatha, Agathaberg"), ("Sa, 10.04.2027", "14:00", "St. Anna, Hämmern"),
            ("So, 11.04.2027", "10:00", "St. Joh. Ap. u. Ev., Kreuzberg"), ("So, 25.04.2027", "11:00", "St. Clemens, Wipperfeld")]
    trs = "".join(f"<tr><td>{a}</td><td>{b} Uhr</td><td>{c}</td></tr>" for a, b, c in rows)
    main = f'''
<h2>Termine der Erstkommunion 2027</h2>
<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Datum</th><th>Uhrzeit</th><th>Kirche</th></tr></thead><tbody>{trs}</tbody></table></div>
<div class="info"><b>Wichtig</b>Eine Feier findet nur dort statt, wo mindestens 7 Kinder angemeldet sind.</div>
<h2>Anmeldung</h2>
<p>Katholische Kinder im 3. Schuljahr werden in der Regel im Juni angeschrieben. Dein Kind möchte teilnehmen, hat aber keinen Brief bekommen? Dann melde dich bei Pastoralreferent Markus Urbatzka, Tel. {tel("02267 8889577")}.</p>
<h2>So läuft die Vorbereitung</h2>
<p>Die Vorbereitung dauert mehrere Monate und hat vier Bausteine:</p>
<ol class="steps">
  <li><b>Gottesdienste feiern</b> – Weggottesdienste für die Kinder und Werktagsmessen mit einer Begleitperson; die Familien besuchen die Sonntagsmesse oder die Familienmesse.</li>
  <li><b>Feier der Versöhnung</b> – zwei Nachmittage im Pfarrheim oder in der Kirche.</li>
  <li><b>Österliches Triduum</b> – Gründonnerstag, Karfreitag und Osternacht werden gemeinsam gefeiert.</li>
  <li><b>Ich bin dabei!</b> – Eltern tragen Verantwortung mit: Hilfe bei Projekten, Eucharistie- und Beichtkatechese oder der Familienmesse ist willkommen (mit Präventionsschulung).</li>
</ol>
<h3>Begleiterin oder Begleiter</h3>
<p>Jedes Kommunionkind wählt einen erwachsenen Menschen als Begleitung – Eltern, Paten, Großeltern oder eine andere vertraute Person. Sie besucht die Gottesdienste gemeinsam mit dem Kind.</p>'''
    aside = f'''<div class="side-card"><h3>Ansprechpartner</h3><p><b>Markus Urbatzka</b>, Pastoralreferent<br>Tel. {tel("02267 8889577")}<br>{mail("markus.urbatzka@erzbistum-koeln.de")}</p></div>{office_card()}'''
    page("erstkommunion.html", "Erstkommunion", "Erstkommunion 2027 in Wipperfürth: Termine, Anmeldung, Vorbereitung.",
         hero("Erstkommunion", "Das erste Mal am Tisch des Herrn – Termine, Anmeldung und Vorbereitung für 2027.", [("anliegen.html", "Anliegen"), (None, "Erstkommunion")], "Sakrament") + layout(main, aside))


def build_firmung():
    main = f'''
<div class="info"><b>Firmung 2026</b>Mitte November 2026 in St. Michael, Neye – in Abstimmung mit Weihbischof Ansgar Puff.</div>
<h2>Wer wird eingeladen?</h2>
<p>Zum Firmkurs 2026 wurden alle Jugendlichen des Geburtsjahrgangs 2010 (1. Januar bis 31. Dezember 2010) schriftlich eingeladen. Die Anmeldung lief über einen QR-Code in der Einladung.</p>
<h2>So läuft die Vorbereitung</h2>
<ol class="steps">
  <li><b>Einladung und Anmeldung</b> – per Brief bzw. QR-Code.</li>
  <li><b>Kompakte Einheiten an mehreren Samstagvormittagen</b> – inhaltliche Auseinandersetzung mit den Themen der Firmung.</li>
  <li><b>Glauben gemeinsam leben</b> – zusammen Gottesdienst feiern und aktiv werden.</li>
  <li><b>Firmfeier</b> – mit dem Weihbischof bzw. seinem Beauftragten.</li>
</ol>
<h2>Keine Einladung bekommen oder älter?</h2>
<p>Auch wenn du zu einem anderen Jahrgang gehörst, später dazukommen möchtest oder als Erwachsene:r gefirmt werden willst: Melde dich im Pastoralbüro – wir finden einen Weg.</p>
<p><a class="btn primary" href="kontakt.html#anliegen-Firmung">Frage zur Firmung</a></p>'''
    page("firmung.html", "Firmung", "Firmung in Wipperfürth: Firmkurs, Jahrgang und Firmfeier.",
         hero("Firmung", "Ja sagen – selbst entscheiden. Infos zum Firmkurs und zur Firmfeier.", [("anliegen.html", "Anliegen"), (None, "Firmung")], "Sakrament") + layout(main))


def build_hochzeit():
    main = f'''
<h2>Trauungstermine</h2>
<div class="tbl-wrap"><table class="tbl"><thead><tr><th>Tag</th><th>Uhrzeiten</th></tr></thead><tbody>
<tr><td>Freitag</td><td>14:30 und 16:00 Uhr</td></tr><tr><td>Samstag</td><td>14:30 Uhr</td></tr>
<tr><td>Fr/Sa vormittags</td><td>bis 12:00 Uhr nach Absprache frei</td></tr></tbody></table></div>
<h2>So meldet ihr eure Trauung an</h2>
<ol class="steps">
  <li><b>Im Pastoralbüro melden</b> – so früh wie möglich, aber <b>mindestens einen Monat vorher</b>. Nennt eure Wünsche zu Termin, Kirche und Zelebrant; die feste Zusage folgt nach interner Bearbeitung.</li>
  <li><b>Ehevorbereitung</b> – Traugespräch mit dem trauenden Geistlichen. Ein eigener Geistlicher darf mitgebracht werden. Wohnt ihr nicht in Wipperfürth, ist zunächst der Pfarrer am Wohnort des katholischen Partners zuständig.</li>
  <li><b>Gottesdienst gestalten</b> – Wortgottesdienst oder Heilige Messe; Musik, Blumen, Liedhefte und Kerzen absprechen.</li>
  <li><b>Nach der Trauung</b> – Stammbuch bzw. Trauurkunde nach etwa 2 Wochen im Pfarrbüro abholen. Bei einer Trauung mit Messe 5,00 € Messstipendium im Pfarrbüro zahlen.</li>
</ol>
<h2>Diese Unterlagen braucht ihr</h2>
<ul>
  <li>Für beide Partner einen <b>aktuellen Taufbuchauszug</b> vom Taufpfarramt – am Trauungstag höchstens 6 Monate alt.</li>
  <li>Falls schon standesamtlich geheiratet: die <b>Bescheinigung über die zivile Eheschließung</b>.</li>
  <li><b>Stammbuch bzw. Trauurkunde</b> im Pfarrbüro abgeben oder spätestens am Trauungstag in der Sakristei.</li>
  <li>Frühere kirchliche oder standesamtliche Ehen bitte bei der Anmeldung angeben.</li>
</ul>
<h2>Vorbereitung als Paar</h2>
<p>Wir empfehlen einen Ehevorbereitungskurs – Termine beim <a href="hilfe.html#familie">Haus der Familie</a>, Tel. {tel("02267 871420")}. Zweimal im Jahr gibt es außerdem eine <b>Trauwerkstatt</b> in der Kirche.</p>
<h2>Musik und Schmuck</h2>
<ul>
  <li>Musikwünsche rechtzeitig mit Seelsorgebereichsmusiker <b>Stefan Barde</b> abstimmen ({tel("02267 8818718")}); es gelten die Regeln der Deutschen Bischofskonferenz.</li>
  <li>Blumenschmuck, Liedhefte und Kerzen mit dem Küsterdienst absprechen (Kontakt über das Pastoralbüro).</li>
  <li>Bitte in den Kirchen keine Blumen streuen und möglichst keinen Reis werfen.</li>
</ul>
<p><a class="btn primary" href="kontakt.html#anliegen-Hochzeit">Trauung anfragen</a></p>'''
    page("hochzeit.html", "Hochzeit", "Kirchlich heiraten in Wipperfürth: Termine, Unterlagen, Ablauf.",
         hero("Hochzeit", "Den Bund fürs Leben schließen – in einer unserer zehn Kirchen. Alles zu Terminen, Unterlagen und Ablauf.", [("anliegen.html", "Anliegen"), (None, "Hochzeit")], "Sakrament") + layout(main))


def build_beichte():
    main = f'''
<div class="info"><b>Regelmäßige Beichtgelegenheit</b>Samstags um 17:00 Uhr in St. Nikolaus, Kirchplatz.</div>
<h2>Wann und wo?</h2>
<ul>
  <li><b>Jeden Samstag, 17:00 Uhr</b> in St. Nikolaus – direkt vor der Vorabendmesse.</li>
  <li><b>Vor den großen Feiertagen</b> zusätzliche Beichtzeiten – siehe <a href="{OFFICIAL}/aktuelles/pfarrnachichten/">Pfarrnachrichten</a>.</li>
  <li><b>Persönlicher Termin</b> – bei jedem Priester der Pfarrei nach Vereinbarung, auch als Beichtgespräch.</li>
</ul>
<h2>Etwas loswerden dürfen</h2>
<p>In der Beichte darfst du aussprechen, was dich belastet, und Gottes Vergebung zugesprochen bekommen. Alles, was du sagst, unterliegt dem Beichtgeheimnis. Du warst lange nicht mehr? Sag es einfach – der Priester hilft dir durch das Gespräch.</p>
<h2>Lieber erst einmal reden?</h2>
<p>Unser ganzes <a href="team.html">Seelsorgeteam</a> ist für vertrauliche Gespräche da – Priester, Pastoral- und Gemeindereferenten.</p>'''
    page("beichte.html", "Beichte & Gespräch", "Beichte in Wipperfürth: samstags 17 Uhr in St. Nikolaus oder nach Vereinbarung.",
         hero("Beichte &amp; Gespräch", "Versöhnung feiern oder einfach reden – vertraulich und ohne Druck.", [("anliegen.html", "Anliegen"), (None, "Beichte")], "Sakrament der Versöhnung") + layout(main))


def build_krankensalbung():
    main = f'''
<div class="info red"><b>Krankensalbung erbitten – rund um die Uhr</b>Tel. {tel(BUERO["notruf"])}. Bitte sag dazu, ob die kranke Person auch die Kommunion empfangen und/oder beichten möchte.</div>
<h2>Kein Abschiedssakrament</h2>
<p>Die Krankensalbung ist eines der sieben Sakramente – und nicht nur für die Sterbestunde gedacht. Sie stärkt in schwerer Zeit, zum Beispiel:</p>
<ul>
  <li>vor einer größeren oder schweren Operation,</li>
  <li>bei einer Krankheit, die mehrere Wochen dauert,</li>
  <li>bei einer schweren seelischen Erkrankung wie einer Depression,</li>
  <li>bei einer unheilbaren Krankheit – um sie besser tragen zu können.</li>
</ul>
<p>Auch Angehörige dürfen den Wunsch äußern, wenn die kranke Person selbst noch nicht danach gefragt hat.</p>
<h2>Wie läuft sie ab?</h2>
<ol class="steps">
  <li><b>Gebet</b> von Priester und Angehörigen.</li>
  <li><b>Handauflegung</b> durch den Priester.</li>
  <li><b>Salbung</b> von Stirn und Handinnenflächen mit geweihtem Öl.</li>
</ol>
<h2>Wo?</h2>
<p>Zu Hause, in einem Wipperfürther Seniorenheim oder in der Helios-Klinik. Angehörige sind ausdrücklich willkommen. Für zu Hause hilft ein weiß gedeckter Tisch nahe am Bett mit brennenden Kerzen und einem Kreuz – das Salböl bringt der Priester mit.</p>'''
    page("krankensalbung.html", "Krankensalbung", "Krankensalbung in Wipperfürth – zu Hause, im Heim oder im Krankenhaus.",
         hero("Krankensalbung", "Stärkung in schwerer Krankheit – zu Hause, im Heim oder im Krankenhaus.", [("anliegen.html", "Anliegen"), (None, "Krankensalbung")], "Sakrament") + layout(main))


def build_trauerfall():
    main = f'''
<div class="info red"><b>Sterbebegleitung und Gebet am Sterbebett</b>Seelsorglicher Notruf rund um die Uhr: {tel(BUERO["notruf"])}</div>
<h2>Was jetzt zu tun ist</h2>
<ol class="steps">
  <li><b>Bestattungsinstitut beauftragen.</b> Es klärt mit euch Erd- oder Feuerbestattung und ob eine Totenmesse (Exequien) gefeiert wird – und meldet sich beim Pastoralbüro.</li>
  <li><b>Termin abstimmen.</b> Beerdigungen sind Mo, Mi und Fr um 14:30 Uhr sowie Di um 10:00 Uhr. Wunsch nach einer bestimmten Person bitte über das Pastoralbüro – die Dienstpläne stehen fest.</li>
  <li><b>Trauergespräch</b> mit der Person, die die Beerdigung hält.</li>
  <li><b>Abschied feiern.</b> Exequien auf Wunsch in der Kirche, danach Trauerfeier und Beisetzung – oft direkt am Grab. Wipperfürth und Wipperfeld haben eigene Trauerhallen.</li>
  <li><b>Sechswochenamt.</b> Auf Wunsch – das Bestattungsinstitut teilt uns das Datum mit, meist in einer Sonntagsmesse.</li>
</ol>
<p>Beerdigungen halten Pfarrer Schäfer, Pfarrvikar Stefan Ochalski, Kaplan Kingsly Paniyadimai sowie die ehrenamtlichen Beerdigungsbeauftragten Heidi Küster und Michael Moll.</p>
<p>Jeden <b>Mittwoch um 18:00 Uhr</b> beten wir in St. Nikolaus für alle, die in der Woche zuvor beerdigt wurden.</p>
<h2>Gut zu wissen</h2>
<ul>
  <li>Die Feuerbestattung ist seit 1983 erlaubt. Für Krematorium, Friedhofskapelle, Kirche und Urnengrab gibt es eigene Feierformen.</li>
  <li>Die Kirche empfiehlt zusätzlich zur Begräbnisfeier eine Eucharistiefeier (Exequien).</li>
  <li>Bestattungen im Friedwald sieht die Kirche zurückhaltend, weil es kaum Erinnerungszeichen gibt.</li>
  <li>Bestattungen außerhalb Wipperfürths begleiten unsere Seelsorger in der Regel im Umkreis von etwa 25 km.</li>
</ul>
<h2>Friedhöfe</h2>
<div class="cards">
  <div class="card-s"><h3>Städtische Friedhöfe</h3><p>Westfriedhof, Wipperfeld, Agathaberg, Thier, Kreuzberg, Egen, Klaswipper</p></div>
  <div class="card-s"><h3>Katholische Friedhöfe</h3><p>Ommerborn, Hämmern, Niederwipper</p></div>
</div>
<h2 id="trauerbegleitung">Trauerbegleitung</h2>
<div class="cards">
  <div class="card-s"><h3>Trauertreff</h3><p>Jeden 3. Sonntag in geraden Monaten, 15–17 Uhr, im Hospizbüro, Wupperstraße 14.</p></div>
  <div class="card-s"><h3>Trauercafé am Westfriedhof</h3><p>Jeden 1. Sonntag im Monat, mit zwei ausgebildeten Ehrenamtlichen, manchmal mit einem Priester.</p></div>
  <div class="card-s"><h3>Ökumenischer Hospizdienst Wipperfürth/Kürten</h3><p>Wupperstraße 14, 51688 Wipperfürth<br>Koordination: Regina Löhr, Tel. {tel("02267 6809520")}<br>{mail("hospiz@oeku-ini.de")}</p></div>
  <div class="card-s"><h3>Sprechzeiten Hospiz</h3><p>Wipperfürth, Gaulstraße 34: Mo 10–12 Uhr, Do 16–18 Uhr<br>Kürten, K51, Bergstr. 31: 3. Di im Monat 9–11 Uhr</p></div>
</div>'''
    page("trauerfall.html", "Trauerfall", "Trauerfall in Wipperfürth: Beerdigung, Friedhöfe, Trauerbegleitung.",
         hero("Trauerfall", "Wenn ein Mensch stirbt, ist vieles zu regeln. Wir begleiten dich – Schritt für Schritt.", [("anliegen.html", "Anliegen"), (None, "Trauerfall")], "Abschied nehmen") + layout(main))


def build_messe():
    opts = "".join(f'<option>{e(c["name"])} – {e(c["place"])}</option>' for c in CHURCHES if not c.get("senior"))
    main = f'''
<p>Du kannst eine Heilige Messe für Verstorbene, zu einem Jahrestag oder für ein persönliches Anliegen feiern lassen. Die Intention wird in der Messe genannt.</p>
<div class="info"><b>Kosten</b>Messstipendium 5,00 € pro Intention. Zahlung im Pastoralbüro, per Post, über den Briefkasten oder im Kollektenkorb.</div>
<h2>Online anfragen</h2>
<p class="small muted">Das Formular stellt dir eine fertige Nachricht an das Pastoralbüro zusammen, die du kopieren oder in deinem E-Mail-Programm öffnen kannst. Auf dieser Website wird nichts gespeichert oder verschickt.</p>
<form class="msg" data-mailform data-subject="Messbestellung">
  <label>Kirche<select name="Kirche">{opts}</select></label>
  <label>Wunschdatum<input name="Datum" type="date" required></label>
  <label>Uhrzeit des Gottesdienstes<input name="Uhrzeit" placeholder="z. B. 18:00 – siehe Gottesdienstordnung"></label>
  <label>Intention / Anliegen<textarea name="Intention" required placeholder="z. B. für + Maria Muster (Jahrgedächtnis)"></textarea></label>
  <label>Dein Name<input name="Name" required autocomplete="name"></label>
  <label>Anschrift<input name="Anschrift" autocomplete="street-address"></label>
  <label>Telefon<input name="Telefon" type="tel" autocomplete="tel"></label>
  <button class="btn primary" type="submit">Nachricht zusammenstellen</button>
</form>
<h2>Andere Wege</h2>
<ul><li>persönlich im Pastoralbüro</li><li>telefonisch unter {tel(BUERO["tel"])}</li><li>mit dem Papierformular, das in den Kirchen ausliegt</li></ul>
<h2>Stiftungsmessen</h2>
<p>Für wiederkehrende Intentionen über 10 oder 25 Jahre plant das Pastoralbüro die jährliche Messe selbst ein. Bitte direkt im Büro melden.</p>'''
    page("messe-bestellen.html", "Messe bestellen", "Messintention bestellen in der Pfarrei St. Nikolaus Wipperfürth.",
         hero("Messe bestellen", "Für Verstorbene, zum Geburtstag oder für ein persönliches Anliegen.", [("anliegen.html", "Anliegen"), (None, "Messe bestellen")], "Messintention") + layout(main))


def build_kirchorte():
    cards = []
    for c in CHURCHES:
        if c.get("senior") or c.get("main"):
            continue
        lines = "".join(f"<li>{e(d)} {t} – {e(ti)}</li>" for d, t, ti, _ in plan_lines(c["id"]))
        addr = f'{c["addr"]}, 51688 Wipperfürth' if c["addr"] else f'{c["place"]}, Wipperfürth'
        q = f'{c["name"]} {c["addr"] or c["place"]} Wipperfürth'
        cards.append(f'''<article class="church" id="{c["id"]}"><span class="place">{e(c["place"])}</span><h3>{e(c["name"])}</h3>
<span class="addr">{e(addr)}</span><ul class="small" style="margin:6px 0 0;padding-left:18px">{lines}</ul>
<span class="small muted">Küsterdienst: {e(KUESTER.get(c["id"], "–"))}</span>
<div class="acts"><a class="btn primary" href="gottesdienste.html#ort-{c["id"]}">Gottesdienste</a><a class="btn ghost" href="https://www.openstreetmap.org/search?query={q.replace(" ", "%20")}">Karte</a></div></article>''')
    nik = "".join(f"<li>{e(d)} {t} – {e(ti)}</li>" for d, t, ti, _ in plan_lines("nik"))
    body = hero("Unsere Kirchorte", "Zehn Kirchen, eine Pfarrei: von der romanischen Pfarrkirche in der Altstadt bis zu den Dorfkirchen.", [(None, "Kirchorte")], "10 Kirchen · 1 Pfarrei") + f'''
<section class="block"><div class="wrap">
  <div class="feature">
    <div class="prose">
      <div class="eyebrow">Pfarrkirche</div>
      <h2 id="nik">St. Nikolaus, Wipperfürth</h2>
      <p class="muted">Kirchplatz 3, 51688 Wipperfürth</p>
      <h3>Geschichte</h3>
      <ul>
        <li><b>1143</b> gründen die Stiftsherren von St. Aposteln in Köln ein Filialstift und beginnen mit dem Bau.</li>
        <li><b>um 1205</b> verlassen sie den Ort wegen Überfällen im Thronstreit; die Stiftskirche wird Pfarrkirche.</li>
        <li><b>1254–1802</b> stellt das Kölner Apostelstift den Pfarrer.</li>
        <li><b>13. Jh.</b> Umbau mit sechsteiligen Kreuzrippengewölben und Seitenkapellen; das Taufbecken entsteht.</li>
        <li><b>1795</b> verliert die Kirche bei einem Stadtbrand Dächer, Chorflankentürmchen und einen Teil des Westturms.</li>
        <li><b>ab 1869</b> grundlegende Restaurierung, der Turm wird oben neu gebaut.</li>
      </ul>
      <p>Heute ist St. Nikolaus eine dreischiffige romanische Pfeilerbasilika. Sehenswert sind das Taufbecken aus dem frühen 13. Jahrhundert und das Grabmal des Bürgermeisters Hagedorn von 1623. Kirchenführer für Erwachsene und Kinder gibt es auf der <a href="{OFFICIAL}/orte-kirchlichen-lebens/kirchenorte/st.-nikolaus/">offiziellen Website</a>.</p>
    </div>
    <div class="side-card"><h3>Gottesdienste in St. Nikolaus</h3><ul class="small">{nik}</ul>
      <p class="small muted" style="margin-top:8px">Küsterdienst: Markus Löhr</p>
      <a class="btn primary" href="gottesdienste.html#ort-nik">Nächste Termine</a></div>
  </div>
  <h2 style="margin:56px 0 20px">Weitere Kirchen</h2>
  <div class="churches">{"".join(cards)}</div>
  <h2 style="margin:56px 0 12px">Weitere Orte</h2>
  <div class="cards">
    <div class="card-s"><h3>Seniorenzentren</h3><p>Franziskusheim (Sa 16:30), Senioren-Quartier (1. Do 16:00), DRK-Seniorenzentrum (Mo 10:30, alle 4 Wochen)</p></div>
    <div class="card-s"><h3>Krankenhauskapelle St. Josef</h3><p>Alte Kölner Str. 3 – Gottesdienste nach Ankündigung. Seelsorge: Georg Kalkum.</p></div>
    <div class="card-s"><h3>Friedhöfe</h3><p>Übersicht der städtischen und katholischen Friedhöfe.</p><a href="trauerfall.html">Zu den Friedhöfen →</a></div>
    <div class="card-s"><h3>Versammlungsräume</h3><p>Pfarrheime und Räume für Gruppen.</p><a href="{OFFICIAL}/orte-kirchlichen-lebens/versammlungsraeume/">Mehr →</a></div>
  </div>
</div></section>'''
    page("kirchorte.html", "Kirchorte", "Die zehn Kirchen der Pfarrei St. Nikolaus Wipperfürth mit Adressen und Gottesdiensten.", body)


GROUPS = [
    ("Messdiener:innen", "Am Altar mitwirken, Fahrten und Gemeinschaft – ab der Erstkommunion. Gruppen gibt es in Agathaberg, Hämmern, Neye, Kreuzberg, Niederwipper, Thier, Wipperfeld und Wipperfürth.", ["kinder", "jugend"], "Kontakt zur Leitung vor Ort über das Pastoralbüro"),
    ("Pfadfinder (DPSG)", "Stamm St. Engelbert Wipperfürth: draußen sein, Zeltlager, Verantwortung übernehmen.", ["kinder", "jugend"], 'Tel. ' + tel("0151 10347053") + " · " + mail("vorstand@dpsg-wipperfuerth.de")),
    ("Ferienfreizeit", "Gemeinsam unterwegs in den Sommerferien – mit erfahrenen Betreuer:innen.", ["kinder", "jugend"], f'<a href="{OFFICIAL}/gruppen/Jugend/ferienfreizeiten/ferienfreizeit-2026/">Infos zur Ferienfreizeit</a>'),
    ("Kinderchor „Nikolinis“", "Singen und Musik für Kinder in St. Nikolaus.", ["kinder", "musik"], "Stefan Barde, Tel. " + tel("02267 8818718")),
    ("Jugendchor „Kaleidoscope“", "Moderne geistliche Musik für Jugendliche und junge Erwachsene.", ["jugend", "musik"], "Stefan Barde, " + mail("stefan.barde@erzbistum-koeln.de")),
    ("Arbeitskreis „Junge Kirche“", "Ideen und Angebote von und für junge Menschen in der Pfarrei.", ["jugend"], "Beate Theunissen, Tel. " + tel("02267 7283")),
    ("Kanisa", "Neues geistliches Lied – auch mit eigenen musikalischen Gottesdiensten.", ["erw", "musik"], f'<a href="{OFFICIAL}/gruppen/choere/kanisa/">Mehr zu Kanisa</a>'),
    ("Kammerchor Wipperfürth e. V.", "Anspruchsvolle Chormusik für erfahrene Sänger:innen.", ["erw", "musik"], f'<a href="{OFFICIAL}/gruppen/choere/kammerchor-wipperfuerth-e.v./">Mehr zum Kammerchor</a>'),
    ("Kirchenchöre vor Ort", "In Agathaberg, Egen, Hämmern, Kreuzberg (mit Gospelchor), Neye, Niederwipper, St. Nikolaus, Thier und Wipperfeld.", ["erw", "sen", "musik"], f'<a href="{OFFICIAL}/gruppen/choere/ansprechpartner-unserer-choere/">Ansprechpartner der Chöre</a>'),
    ("Taizé-Gebet", "Gesänge, Stille und Gebet im Stil der Gemeinschaft von Taizé.", ["jugend", "erw", "musik"], f'<a href="{OFFICIAL}/gruppen/taize/">Termine</a>'),
    ("Familien", "Familiengottesdienste (3. So, 11:00) und Kleine-Leute-Gottesdienste (letzter So, 10:30) in Neye.", ["kinder", "erw"], '<a href="gottesdienste.html#art-fam">Termine</a>'),
    ("Frauen – kfd", "Katholische Frauengemeinschaft: Glaube, Austausch, Engagement.", ["erw", "sen"], f'<a href="{OFFICIAL}/gruppen/frauen-kfd/">Mehr zur kfd</a>'),
    ("Kolping", "Soziales Engagement, Bildung und Gemeinschaft für alle Generationen.", ["erw", "sen"], f'<a href="{OFFICIAL}/gruppen/kolping/">Mehr zu Kolping</a>'),
    ("Senior:innen", "Treffen, Ausflüge und Gottesdienste in den Seniorenzentren.", ["sen"], f'<a href="{OFFICIAL}/gruppen/senioren/">Mehr</a>'),
    ("Schützen", "Bruderschaften mit Tradition – Glaube, Sitte, Heimat.", ["erw"], f'<a href="{OFFICIAL}/gruppen/schuetzen/">Mehr</a>'),
    ("Öffentliche Bücherei (KÖB)", "Lesen, ausleihen, mithelfen – ein Ort für alle.", ["kinder", "erw", "sen"], f'<a href="{OFFICIAL}/orte-kirchlichen-lebens/institutionen/koeb/">Mehr zur KÖB</a>'),
]


def build_gruppen():
    gcards = "".join(f'<div class="group" data-groups="{" ".join(g)}"><h3>{e(n)}</h3><p>{e(d)}</p><p class="small" style="color:var(--ink)">{c}</p></div>' for n, d, g, c in GROUPS)
    kitas = [("St. Nikolaus", "Ringstr. 53", "02267 7283"), ("Don Bosco", "Don-Bosco-Weg 5", "02267 5237"),
             ("St. Raphael, Kreuzberg", "Westfalenstr. 38", "02267 5381"), ("St. Clemens, Wipperfeld (mit Waldgruppe)", "Dorfstraße 10", "02268 6943"),
             ("St. Anna, Thier", "Joh.-Wilh.-Roth-Str. 25", "02267 7466")]
    ktr = "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td><td>{tel(c)}</td></tr>" for a, b, c in kitas)
    body = hero("Finde deine Gruppe", "Singen, Zelten, Ministrieren, Diskutieren – oder einfach mal ab und zu helfen. In Wipperfürth ist für alle Generationen etwas dabei.", [(None, "Gruppen")], "Gemeinschaft &amp; Mitmachen") + f'''
<section class="block"><div class="wrap">
  <div class="filters" id="groupFilters">
    <button class="chip" type="button" data-g="all" aria-pressed="true">Alle</button>
    <button class="chip" type="button" data-g="kinder" aria-pressed="false">Kinder</button>
    <button class="chip" type="button" data-g="jugend" aria-pressed="false">Jugend</button>
    <button class="chip" type="button" data-g="erw" aria-pressed="false">Erwachsene</button>
    <button class="chip" type="button" data-g="sen" aria-pressed="false">Senior:innen</button>
    <button class="chip" type="button" data-g="musik" aria-pressed="false">Musik</button>
  </div>
  <div class="groups" id="groups">{gcards}</div>

  <div class="wrap layout" style="padding-left:0;padding-right:0">
  <div class="prose">
    <h2 id="ehrenamt">Ehrenamt – auch mal ab und zu</h2>
    <p>Du musst dich nicht für Jahre verpflichten. Gerade gesucht:</p>
    <ul>
      <li><b>Taufgeschenke überbringen</b> – neu getauften Kindern und ihren Familien einen Gruß der Gemeinde bringen.</li>
      <li id="schoepfung"><b>Schöpfungsbotschafter:in</b> – mit der Aktion „Klima+Kirche“ des Erzbistums und unserem Projekt Schöpfungsverantwortung (Beschluss des Pfarrgemeinderats 2022, nach „Laudato Si’“). Ansprechpersonen: Dr. Edwin Behrens, Birgit Baumhögger-Habbel und Gemeindereferent Georg Kalkum.</li>
      <li><b>Erstkommunion-Vorbereitung</b> – Projekte, Katechese oder Familienmessen mitgestalten.</li>
    </ul>
    <p>Wer mit Kindern und Jugendlichen arbeitet, nimmt an einer Präventionsschulung teil – wir unterstützen dich dabei.</p>
    <p><a class="btn primary" href="kontakt.html#anliegen-Ehrenamt">Ich möchte mitmachen</a></p>
    <h2 id="kitas">Katholische Kitas</h2>
    <p>Träger ist seit 1. August 2026 die Katholino gGmbH (St. Anna, Thier: Übergang für 2027 geplant).</p>
    <div class="tbl-wrap"><table class="tbl"><thead><tr><th>Kita</th><th>Adresse</th><th>Telefon</th></tr></thead><tbody>{ktr}</tbody></table></div>
    <h2>Gremien</h2>
    <p>Der <b>Pfarrgemeinderat</b> gestaltet das Gemeindeleben mit, der <b>Kirchenvorstand</b> verwaltet Vermögen und Gebäude. <a href="{OFFICIAL}/ansprechpartner/pfarrgemeinderat/">Pfarrgemeinderat</a> · <a href="{OFFICIAL}/ansprechpartner/kirchenvorstand/">Kirchenvorstand</a></p>
  </div>
  <aside>
    <div class="side-card"><h3>Kirchenmusik</h3><p><b>Stefan Barde</b>, Seelsorgebereichsmusiker<br>Tel. {tel("02267 8818718")}<br>{mail("stefan.barde@erzbistum-koeln.de")}</p></div>
    {office_card()}
  </aside>
  </div>
</div></section>'''
    page("gruppen.html", "Gruppen & Mitmachen", "Gruppen, Chöre, Jugend und Ehrenamt in der Pfarrei St. Nikolaus Wipperfürth.", body)


def build_hilfe():
    body = hero("Du bist nicht allein", "Kirche heißt: da sein, wenn es schwer wird. Und alles dafür tun, dass Kinder und Schutzbedürftige bei uns sicher sind.", [(None, "Hilfe")], "Hilfe &amp; Schutz") + f'''
<section class="block"><div class="wrap">
  <div class="help">
    <div class="card urgent"><h3>Akute Not</h3><p style="margin:6px 0 0">Seelsorglicher Notruf der Pfarrei</p>
      <a class="phone" href="tel:{BUERO["notruf_href"]}">{BUERO["notruf"]}</a>
      <p class="small" style="margin:0">Telefonseelsorge, anonym, kostenlos, rund um die Uhr: <a href="tel:08001110111">0800 111 0 111</a> · <a href="tel:08001110222">0800 111 0 222</a></p></div>
    <div class="card"><h3>Krank oder im Krankenhaus</h3><p>Krankensalbung, Kommunion und Besuch zu Hause, im Heim oder in der Helios-Klinik.</p><a href="krankensalbung.html">Zur Krankensalbung →</a><p class="small muted" style="margin-top:8px">Krankenhausseelsorge: Georg Kalkum, {tel("02195 684453")}</p></div>
    <div class="card"><h3>Trauer</h3><p>Beerdigung, Trauertreff, Trauercafé und Ökumenischer Hospizdienst.</p><a href="trauerfall.html#trauerbegleitung">Zur Trauerbegleitung →</a></div>
  </div>
  <div class="wrap layout" style="padding-left:0;padding-right:0">
  <div class="prose">
    <h2 id="praevention">Prävention &amp; Schutz vor Missbrauch</h2>
    <p>Alle, die bei uns mit Kindern und Jugendlichen arbeiten, werden geschult. Gemeinsam mit unseren Gruppen erarbeiten wir ein Institutionelles Schutzkonzept. Wenn du einen Verdacht hast oder dir etwas komisch vorkommt: Sprich mit einer der folgenden Personen. Kinder und Jugendliche können sich auch mit dem Beschwerdeformular melden.</p>
    <h3>In der Pfarrei</h3>
    <div class="cards">
      <div class="card-s"><h3>Monika Weber-Schmallenbach</h3><p>Präventionsfachkraft, Beratungsstelle Herbstmühle</p>Tel. {tel("02261 405776")} · Büro {tel("02267 3034")}</div>
      <div class="card-s"><h3>Lambert Schäfer</h3><p>Leitender Pfarrer</p>Tel. {tel("02267 8818713")}<br>{mail("lambert.schaefer@erzbistum-koeln.de")}</div>
    </div>
    <h3>Unabhängige Ansprechpersonen des Erzbistums (auch anonym)</h3>
    <div class="cards">
      <div class="card-s"><h3>Peter Binot</h3><p>Kriminalhauptkommissar a. D., psychologischer Berater</p>{tel("0172 2901534")}</div>
      <div class="card-s"><h3>Martin Gawlik</h3><p>Rechtsanwalt</p>{tel("0172 2901248")}</div>
      <div class="card-s"><h3>Birgit Röttgen</h3><p>Dipl.-Psychologin</p>{tel("01525 2825703")}</div>
    </div>
    <h3>Weitere Beratung</h3>
    <ul>
      <li><b>Courage</b> – Beratung für betroffene Mädchen und Jungen, Herbstmühle 3, Wipperfürth, {tel("02267 3034")}</li>
      <li><b>Zartbitter Köln e. V.</b>, Sachsenring 2–4, 50677 Köln, {tel("0221 312055")}</li>
    </ul>

    <h2 id="familie">Familie &amp; Beratung</h2>
    <div class="cards">
      <div class="card-s"><h3>Haus der Familie</h3><p>Kurse für werdende Eltern und Familien, Ehevorbereitung, Bildung zu Spiritualität, Gesundheit und Kultur.</p>Klosterplatz 2 · {tel("02267 871420")}<br><a href="https://www.hdf-wipperfuerth.de">hdf-wipperfuerth.de</a></div>
      <div class="card-s"><h3>Psychologische Beratungsstelle Herbstmühle</h3><p>Ehe-, Familien- und Lebensberatung.</p>{tel("02267 3034")}<br><a href="{OFFICIAL}/orte-kirchlichen-lebens/institutionen/psychologische-beratungsstelle/">Mehr</a></div>
    </div>
    <h2 id="caritas">Caritas</h2>
    <p>Die Caritas-Stelle der Pfarrei ist nach dem Tod von Diakon Zimmermann vorläufig nicht besetzt. In sozialer oder finanzieller Not wende dich bitte an Pfarrer Lambert Schäfer oder das Pastoralbüro – wir helfen weiter oder vermitteln die passende Stelle.</p>
  </div>
  <aside>{office_card()}</aside>
  </div>
</div></section>'''
    page("hilfe.html", "Hilfe & Schutz", "Notruf, Prävention, Trauer, Beratung und Caritas in Wipperfürth.", body)


def build_team():
    people = []
    for n, r, t, m, img in TEAM:
        ini = "".join(w[0] for w in n.split())
        av = f'<img src="{img}" alt="" loading="lazy">' if img else ini
        contact = (f'{tel(t)}' if t else "") + (f'{mail(m)}' if m else "") or '<span class="small muted">über das Pastoralbüro</span>'
        people.append(f'<div class="person"><div class="avatar">{av}</div><div><b>{e(n)}</b><span class="role">{e(r)}</span>{contact}</div></div>')
    body = hero("Ansprechpersonen", "Wir sind für dich da – direkt per Telefon oder E-Mail.", [(None, "Ansprechpersonen")], "Team") + f'''
<section class="block"><div class="wrap">
  <h2 style="margin-bottom:20px">Seelsorgeteam &amp; Verwaltung</h2>
  <div class="team">{"".join(people)}</div>
  <div class="wrap layout" style="padding-left:0;padding-right:0">
  <div class="prose">
    <h2>Pastoralbüro</h2>
    <p>Gudrun Spiller, Jutta Bach und Stefanie Knop (Pfarramtssekretärinnen) – {tel(BUERO["tel"])}, {mail(BUERO["mail"])}. <a href="kontakt.html">Öffnungszeiten</a></p>
    <h2>Kirchenmusik</h2>
    <div class="cards">
      <div class="card-s"><h3>Stefan Barde</h3><p>Seelsorgebereichsmusiker · Kinder- und Jugendchor</p>{tel("02267 8818718")}<br>{mail("stefan.barde@erzbistum-koeln.de")}</div>
      <div class="card-s"><h3>Jochen Malzkorn</h3><p>Organist und Chorleiter</p></div>
      <div class="card-s"><h3>Susanne Hebbecker</h3><p>Organistin und Chorleiterin</p></div>
    </div>
    <h2>Küsterdienste</h2>
    <div class="tbl-wrap"><table class="tbl"><thead><tr><th>Kirchen</th><th>Küster:in</th></tr></thead><tbody>
      <tr><td>St. Nikolaus, St. Michael (Neye)</td><td>Markus Löhr</td></tr>
      <tr><td>St. Johannes (Kreuzberg), St. Anna (Thier)</td><td>Andrea Agartz</td></tr>
      <tr><td>St. Agatha (Agathaberg)</td><td>Susanne Hebbecker</td></tr>
      <tr><td>St. Clemens (Wipperfeld), Egen, Hämmern, Niederwipper, Ommerborn</td><td>Heidi Küster</td></tr>
    </tbody></table></div>
    <p class="small muted">Kontakt zu Kirchenmusik und Küsterdiensten gern über das Pastoralbüro.</p>
    <h2>Gremien</h2>
    <p><a href="{OFFICIAL}/ansprechpartner/pfarrgemeinderat/">Pfarrgemeinderat</a> · <a href="{OFFICIAL}/ansprechpartner/kirchenvorstand/">Kirchenvorstand</a> · <a href="{OFFICIAL}/ansprechpartner/mitarbeitervertretung-mav/">Mitarbeitervertretung</a> · <a href="hilfe.html#praevention">Prävention</a></p>
  </div>
  <aside>{office_card()}</aside>
  </div>
</div></section>'''
    page("team.html", "Ansprechpersonen", "Seelsorgeteam, Pastoralbüro, Kirchenmusik und Küster der Pfarrei St. Nikolaus.", body)


def build_aktuelles():
    body = hero("Aktuelles", "Termine, Neuigkeiten und Mitmach-Aufrufe aus der Pfarrei. Alle Gottesdienständerungen stehen in den Pfarrnachrichten.", [(None, "Aktuelles")], "Neuigkeiten") + f'''
<section class="block"><div class="wrap">
  <div class="news">{news_cards()}</div>
  <div class="info" style="margin-top:28px"><b>Pfarrnachrichten</b>Die aktuellen Pfarrnachrichten mit allen Terminen und Änderungen erscheinen regelmäßig. <a href="{OFFICIAL}/aktuelles/pfarrnachichten/">Pfarrnachrichten öffnen</a></div>
</div></section>'''
    page("aktuelles.html", "Aktuelles", "Neuigkeiten und Termine der Pfarrei St. Nikolaus Wipperfürth.", body)


def build_kontakt():
    topics = ["Allgemeine Frage", "Taufe", "Hochzeit", "Firmung", "Sterbefall", "Wiedereintritt", "Gemeindereise", "Ehrenamt"]
    opts = "".join(f"<option>{t}</option>" for t in topics)
    main = f'''
<span class="status off" data-office-badge>Öffnungszeiten</span>
<div class="cards">
  <div class="card-s"><h3>Adresse</h3><p>Kath. Pfarrei St. Nikolaus<br>Pastoralbüro<br>Kirchplatz 1<br>51688 Wipperfürth</p><a href="https://www.openstreetmap.org/search?query=Kirchplatz%201%2C%2051688%20Wipperf%C3%BCrth">Auf der Karte zeigen</a></div>
  <div class="card-s"><h3>Erreichbarkeit</h3><p>Telefon {tel(BUERO["tel"])}<br>Fax {BUERO["fax"]}<br>{mail(BUERO["mail"])}</p><p>Notruf: <b>{tel(BUERO["notruf"])}</b></p></div>
</div>
<h2>Öffnungszeiten</h2>
<table class="hours" aria-label="Öffnungszeiten"><tbody id="hoursBody">
<tr><td>Montag</td><td>08:30–15:30</td></tr><tr><td>Dienstag</td><td>08:30–15:30</td></tr><tr><td>Mittwoch</td><td>08:30–12:30</td></tr>
<tr><td>Donnerstag</td><td>08:30–15:30</td></tr><tr><td>Freitag</td><td>08:30–15:30</td></tr><tr><td>Samstag</td><td>10:00–12:00 nur per E-Mail</td></tr><tr><td>Sonntag</td><td>geschlossen</td></tr>
</tbody></table>
<p class="small muted" style="margin-top:10px">In den Sommerferien Mo–Fr 08:30–12:30. An Heiligabend und Silvester geschlossen.</p>
<p>Im Büro für dich da: Gudrun Spiller, Jutta Bach und Stefanie Knop.</p>
<h2 id="nachricht">Nachricht schreiben</h2>
<p class="small muted">Das Formular stellt dir eine fertige Nachricht zusammen, die du kopieren oder in deinem E-Mail-Programm öffnen kannst. Auf dieser Website wird nichts gespeichert oder verschickt.</p>
<form class="msg" data-mailform>
  <label>Anliegen<select name="Anliegen" id="mTopic">{opts}</select></label>
  <label>Dein Name<input name="Name" required autocomplete="name"></label>
  <label>Telefon für Rückruf (optional)<input name="Telefon" type="tel" autocomplete="tel"></label>
  <label>Nachricht<textarea name="Nachricht" required placeholder="Worum geht es?"></textarea></label>
  <button class="btn primary" type="submit">Nachricht zusammenstellen</button>
</form>'''
    aside = f'''<div class="side-card"><h3>Direkt zum Seelsorger</h3><p>Alle Telefonnummern und E-Mail-Adressen des Teams.</p><a class="btn ghost" href="team.html">Ansprechpersonen</a></div>
<div class="side-card"><h3>Messe bestellen</h3><p>Eigenes Formular mit Kirche und Datum.</p><a class="btn ghost" href="messe-bestellen.html">Zur Messbestellung</a></div>
<div class="side-card" style="background:var(--accent-soft);border-color:transparent"><h3>Seelsorglicher Notruf</h3><p style="margin:0">Rund um die Uhr: <b>{tel(BUERO["notruf"])}</b></p></div>'''
    page("kontakt.html", "Kontakt", "Pastoralbüro der Pfarrei St. Nikolaus Wipperfürth: Adresse, Öffnungszeiten, Kontakt.",
         hero("Kontakt &amp; Pastoralbüro", "Für Anmeldungen, Messbestellungen, Bescheinigungen und alle Fragen.", [(None, "Kontakt")], "Pastoralbüro") + layout(main, aside))


def build_suche():
    body = hero("Suche", "Finde Themen auf dieser Website.", [(None, "Suche")]) + f'''
<section class="block"><div class="wrap prose">{search_box("q3")}<div id="searchAll" style="margin-top:24px"></div>
<noscript><p>Die Suche braucht JavaScript. Nutze sonst das Menü oder die <a href="anliegen.html">Übersicht der Anliegen</a>.</p></noscript></div></section>'''
    page("suche.html", "Suche", "Suche auf der Website der Pfarrei St. Nikolaus Wipperfürth.", body)


SEARCH_INDEX = [
    ("Gottesdienste & Messzeiten", "gottesdienste.html", "messe gottesdienst sonntag vorabend hochamt zeiten uhrzeit heute morgen wochenende"),
    ("Familiengottesdienst & Kleine Leute", "gottesdienste.html#art-fam", "familie kinder kleine leute familiengottesdienst"),
    ("Taufe", "taufe.html", "taufe taufen baby kind tauftreff pate patin taufsonntag"),
    ("Erstkommunion", "erstkommunion.html", "kommunion erstkommunion eucharistie 2027 dritte klasse"),
    ("Firmung", "firmung.html", "firmung firmen jugendliche firmkurs"),
    ("Hochzeit / Trauung", "hochzeit.html", "hochzeit heiraten trauung ehe taufbuchauszug unterlagen"),
    ("Beichte & Gespräch", "beichte.html", "beichte versöhnung gespräch reden seelsorge"),
    ("Krankensalbung", "krankensalbung.html", "krank krankensalbung krankenhaus besuch operation"),
    ("Trauerfall / Beerdigung", "trauerfall.html", "tod sterbefall beerdigung trauer begräbnis bestattung sechswochenamt hospiz"),
    ("Friedhöfe", "trauerfall.html", "friedhof friedhöfe grab westfriedhof"),
    ("Messe bestellen", "messe-bestellen.html", "messe bestellen messbestellung intention verstorbene stipendium"),
    ("Kirchorte", "kirchorte.html", "kirche kirchen orte adresse karte neye agathaberg kreuzberg thier wipperfeld egen hämmern niederwipper ommerborn"),
    ("Geschichte St. Nikolaus", "kirchorte.html#nik", "geschichte romanisch 1143 basilika taufbecken"),
    ("Messdiener", "gruppen.html", "messdiener ministranten jugend"),
    ("Pfadfinder & Ferienfreizeit", "gruppen.html", "pfadfinder dpsg zeltlager ferien freizeit"),
    ("Chöre & Kirchenmusik", "gruppen.html", "chor chöre singen musik kanisa gospel kaleidoscope nikolinis taizé orgel"),
    ("Ehrenamt / Mitmachen", "gruppen.html#ehrenamt", "ehrenamt helfen mitmachen engagement schöpfung klima"),
    ("Kitas", "gruppen.html#kitas", "kita kindergarten katholino"),
    ("Prävention & Schutz", "hilfe.html#praevention", "prävention schutz missbrauch kinderschutz ansprechperson"),
    ("Caritas & Beratung", "hilfe.html#caritas", "caritas hilfe not beratung geld familie haus der familie"),
    ("Seelsorglicher Notruf", "hilfe.html", "notruf notfall sterben akut telefonseelsorge"),
    ("Seelsorgeteam / Pfarrer", "team.html", "pfarrer kaplan pfarrvikar team schäfer seelsorger ansprechpartner verwaltung küster"),
    ("Pastoralbüro & Öffnungszeiten", "kontakt.html", "büro pfarrbüro pastoralbüro öffnungszeiten telefon email kontakt adresse"),
    ("Aktuelles & Pfarrnachrichten", "aktuelles.html", "aktuelles pfarrnachrichten news termine veranstaltungen stellen reise"),
    ("Wiedereintritt / Erwachsenentaufe", "anliegen.html", "wiedereintritt austritt erwachsene eintreten konversion"),
]


def build_data():
    data = {"churches": CHURCHES, "services": SERVICES, "search": SEARCH_INDEX}
    (OUT / "assets" / "data.js").write_text(
        "/* automatisch erzeugt von build.py – bitte dort ändern */\nwindow.PFARREI = " +
        json.dumps(data, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")


if __name__ == "__main__":
    build_data()
    for fn in [build_index, build_gottesdienste, build_anliegen, build_taufe, build_erstkommunion, build_firmung,
               build_hochzeit, build_beichte, build_krankensalbung, build_trauerfall, build_messe, build_kirchorte,
               build_gruppen, build_hilfe, build_team, build_aktuelles, build_kontakt, build_suche]:
        fn()
    print("Fertig:", ", ".join(sorted(p.name for p in OUT.glob("*.html"))))
