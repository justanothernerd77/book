#!/usr/bin/env python3
"""Erzeugt die Abbildungen und Beetpläne des Buches als SVG.

Aufruf aus dem Repository-Wurzelverzeichnis:

    python3 abbildungen/erzeugen.py

Alle Grafiken teilen sich Farben und Schrift, damit sie im Buch einheitlich
wirken. Der Anbaukalender wird aus daten/kulturen.json erzeugt, damit Buch,
Kalender und App übereinstimmen.
"""

import json
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "abbildungen"

# ── Farben ──────────────────────────────────────────────────────────────
PAPER = "#fbfaf5"
INK = "#2b2b26"
MUTED = "#6b6b5e"
LINE = "#b9b6a5"
SOFT = "#efece0"

KOHL = "#6a8f3d"      # Feld 1: Kohl & Co.
FRUCHT = "#c4572f"    # Feld 2: Fruchtgemüse & Kartoffeln
WURZEL = "#d49a2a"    # Feld 3: Wurzeln & Zwiebeln
HUELSE = "#5b7fb0"    # Feld 4: Hülsenfrüchte & Bodenkur
DAUER = "#8a6fa8"     # Dauerkulturen

C_VORKULTUR = "#9a6a00"
C_DIREKTSAAT = "#2e6fb5"
C_PFLANZUNG = "#2f6a2a"
C_ERNTE = "#d4691c"

FONT = "Atkinson Hyperlegible, Segoe UI, Helvetica, Arial, sans-serif"


# ── Bausteine ───────────────────────────────────────────────────────────
def svg(w, h, body, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" font-family="{FONT}" role="img" '
        f'aria-label="{escape(title)}">\n'
        f"<title>{escape(title)}</title>\n"
        f'<rect width="{w}" height="{h}" fill="{PAPER}"/>\n'
        f"{body}</svg>\n"
    )


def rect(x, y, w, h, fill, stroke="none", sw=1, rx=0, extra=""):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>\n'
    )


def text(x, y, s, size=15, fill=INK, anchor="start", weight="normal", extra=""):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
        f'text-anchor="{anchor}" font-weight="{weight}" {extra}>{escape(s)}</text>\n'
    )


def lines(x, y, rows, size=15, fill=INK, anchor="start", weight="normal", lh=1.3):
    out = ""
    for i, r in enumerate(rows):
        out += text(x, y + i * size * lh, r, size, fill, anchor, weight)
    return out


def line(x1, y1, x2, y2, stroke=INK, sw=1.5, extra=""):
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
        f'stroke-width="{sw}" {extra}/>\n'
    )


def heading(w, title, sub=None):
    out = text(24, 38, title, 22, INK, weight="bold")
    if sub:
        out += text(24, 62, sub, 14, MUTED)
    return out


ARROW_DEF = (
    '<defs><marker id="pfeil" viewBox="0 0 10 10" refX="9" refY="5" '
    'markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
    f'<path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker></defs>\n'
)


def arrow(x1, y1, x2, y2, stroke=INK, sw=2):
    return line(x1, y1, x2, y2, stroke, sw, 'marker-end="url(#pfeil)"')


def save(name, content):
    (OUT / name).write_text(content, encoding="utf-8")
    print("geschrieben:", name)


# ── Kapitel 2: Zonen im Garten ──────────────────────────────────────────
def zonen():
    w, h = 820, 560
    b = heading(w, "Den Garten zonieren", "Je öfter Sie dort zu tun haben, desto näher ans Haus")
    # Grundstück
    gx, gy, gw, gh = 24, 84, 772, 452
    b += rect(gx, gy, gw, gh, "#f4f1e4", LINE, 1.5)
    # Zonenbänder (vom Haus oben links ausgehend)
    zones = [
        ("Zone 4 – selten", "#e3e8d3", gx, gy, gw, gh),
        ("Zone 3 – wöchentlich bis saisonal", "#e9ecd9", gx, gy, 560, 350),
        ("Zone 2 – mehrmals pro Woche", "#eef0e1", gx, gy, 400, 250),
        ("Zone 1 – täglich", "#f6f3e6", gx, gy, 250, 150),
    ]
    for name, col, x, y, zw, zh in zones:
        b += rect(x, y, zw, zh, col, LINE, 1, extra='stroke-dasharray="5 4"')
    # Haus
    b += rect(gx + 12, gy + 12, 110, 70, "#d8d2bd", INK, 1.5)
    b += text(gx + 67, gy + 52, "Haus", 15, INK, "middle", "bold")
    # Zone 1
    b += rect(gx + 135, gy + 18, 95, 44, "#cfe0b4", INK, 1, rx=4)
    b += lines(gx + 182, gy + 36, ["Kräuter,", "Salat"], 12, INK, "middle")
    b += f'<circle cx="{gx + 150}" cy="{gy + 105}" r="14" fill="#9fb8d0" stroke="{INK}"/>\n'
    b += text(gx + 172, gy + 110, "Regentonne", 12, INK)
    # Zone 2: vier Beete + Kompost
    for i, col in enumerate([KOHL, FRUCHT, WURZEL, HUELSE]):
        b += rect(gx + 262 + i * 32, gy + 20, 22, 110, col, INK, 1, rx=2, extra='fill-opacity="0.75"')
    b += text(gx + 322, gy + 150, "Gemüsebeete", 12, INK, "middle")
    b += rect(gx + 40, gy + 175, 110, 50, "#8a6a48", INK, 1, rx=3)
    b += text(gx + 95, gy + 205, "Kompost", 13, "#fff", "middle", "bold")
    b += rect(gx + 190, gy + 175, 90, 50, "#dfe7f0", INK, 1, rx=3)
    b += lines(gx + 235, gy + 196, ["Frühbeet /", "Gewächshaus"], 11, INK, "middle")
    # Zone 3
    b += rect(gx + 420, gy + 30, 120, 150, "#e8d9b0", INK, 1, rx=3)
    b += lines(gx + 480, gy + 100, ["Kartoffeln,", "Lagergemüse"], 12, INK, "middle")
    for cx, cy in [(gx + 80, gy + 300), (gx + 190, gy + 310), (gx + 300, gy + 295)]:
        b += f'<circle cx="{cx}" cy="{cy}" r="26" fill="#a8c47a" stroke="{INK}"/>\n'
    b += text(gx + 190, gy + 355, "Obstbäume", 12, INK, "middle")
    b += rect(gx + 400, gy + 270, 150, 20, "#b5537a", INK, 1, rx=8, extra='fill-opacity="0.6"')
    b += text(gx + 475, gy + 310, "Beerenhecke", 12, INK, "middle")
    # Zone 4
    b += rect(gx + 600, gy + 260, 150, 170, "#cdd8b2", INK, 1, rx=6, extra='stroke-dasharray="3 3"')
    b += lines(gx + 675, gy + 320, ["Wildecke,", "Totholz,", "Blühstreifen"], 12, INK, "middle")
    # Zonen direkt beschriften (unten rechts in jeder Zone)
    for name, col, x, y, zw, zh in zones:
        b += text(x + zw - 10, y + zh - 10, name, 12, MUTED, "end", "bold")
    return svg(w, h, b, "Zonierung eines Selbstversorger-Gartens")


# ── Kapitel 4: Querschnitte ─────────────────────────────────────────────
def legende_schichten(x, y, eintraege, size=14, abstand=48):
    """Beschriftete Farbfelder, jede Beschriftung höchstens zwei Zeilen."""
    out = ""
    for i, (col, zeilen) in enumerate(eintraege):
        yy = y + i * abstand
        out += rect(x, yy - 13, 18, 18, col, INK, 0.8)
        out += lines(x + 28, yy, zeilen, size, INK)
    return out


def pflanzen(x0, x1, y, schritt=70):
    out = ""
    for px in range(int(x0), int(x1), schritt):
        out += (f'<path d="M{px},{y} q-10,-28 -18,-34 M{px},{y} q10,-30 16,-36 M{px},{y} v-40" '
                f'stroke="{KOHL}" stroke-width="4" fill="none" stroke-linecap="round"/>\n')
    return out


def hochbeet():
    w, h = 820, 560
    b = heading(w, "Hochbeet im Querschnitt", "Befüllung in vier Schichten, von unten nach oben")
    x, y, bw = 60, 130, 320
    layers = [
        ("#4a3a2c", 70, ["Pflanzschicht: reifer Kompost", "und Gartenerde (20–25 cm)"]),
        ("#6e4f35", 55, ["halbreifer Kompost oder", "angerotteter Mist (15–20 cm)"]),
        ("#8aa35a", 42, ["Grassoden umgedreht, Laub,", "Grünschnitt (10–15 cm)"]),
        ("#9b7650", 80, ["grober Gehölzschnitt,", "Äste (20–30 cm)"]),
    ]
    cy = y
    for col, lh, _ in layers:
        b += rect(x, cy, bw, lh, col, INK, 0.8)
        cy += lh
    total = cy - y
    b += rect(x - 14, y - 20, 14, total + 20, "#c89f6a", INK, 1)
    b += rect(x + bw, y - 20, 14, total + 20, "#c89f6a", INK, 1)
    b += line(x + 2, y - 10, x + 2, y + total, "#2e6fb5", 3, 'stroke-dasharray="6 4"')
    b += line(x + bw - 2, y - 10, x + bw - 2, y + total, "#2e6fb5", 3, 'stroke-dasharray="6 4"')
    yb = y + total
    b += line(x - 14, yb + 4, x + bw + 14, yb + 4, "#555", 3, 'stroke-dasharray="2 3"')
    b += rect(x - 40, yb + 8, bw + 80, 40, "#bda77f", "none")
    b += text(x + bw / 2, yb + 34, "gewachsener Boden", 13, INK, "middle")
    b += pflanzen(x + 40, x + bw - 20, y)
    b += legende_schichten(470, 150, [(c, z) for c, _, z in layers], 14, 58)
    ly = yb + 78
    b += line(24, ly - 5, 60, ly - 5, "#2e6fb5", 3, 'stroke-dasharray="6 4"')
    b += text(70, ly, "Noppenfolie an den Innenwänden (nicht auf den Boden)", 13, MUTED)
    b += line(24, ly + 19, 60, ly + 19, "#555", 3, 'stroke-dasharray="2 3"')
    b += text(70, ly + 24, "Wühlmausdraht, Maschenweite höchstens 13 mm", 13, MUTED)
    b += text(24, ly + 50, "Breite 120 cm, Höhe 70–90 cm · die Füllung sackt im ersten Jahr um 10–20 cm – jährlich Kompost nachfüllen", 13, MUTED)
    return svg(w, h, b, "Hochbeet im Querschnitt")


def nodig():
    w, h = 820, 400
    b = heading(w, "No-Dig-Beet anlegen", "Bewuchs ersticken statt umgraben – sofort bepflanzbar")
    x, y, bw = 60, 170, 360
    b += pflanzen(x + 40, x + bw - 20, y, 80)
    b += rect(x, y, bw, 60, "#4a3a2c", INK, 0.8)
    b += rect(x - 10, y + 60, bw + 20, 8, "#c9a46a", INK, 0.8)
    b += rect(x - 36, y + 68, bw + 72, 18, "#8aa35a", "none")
    for gx in range(x - 32, x + bw + 36, 12):
        b += line(gx, y + 68, gx + 4, y + 58, "#6f8a44", 2)
    b += rect(x - 36, y + 86, bw + 72, 90, "#bda77f", "none")
    eintraege = [
        ("#4a3a2c", ["10–15 cm reifer Kompost – hier", "wird gesät und gepflanzt"]),
        ("#c9a46a", ["Wellpappe, überlappend", "(10–15 cm), gründlich gewässert"]),
        ("#8aa35a", ["alte Grasnarbe – gemäht,", "bleibt liegen und verrottet"]),
        ("#bda77f", ["gewachsener Boden –", "wird nicht bewegt"]),
    ]
    b += legende_schichten(480, 130, eintraege, 14, 58)
    return svg(w, h, b, "Aufbau eines No-Dig-Beetes")


def huegelbeet():
    w, h = 820, 500
    b = heading(w, "Hügelbeet im Querschnitt", "Ein Kern aus Gehölzschnitt, darüber Schichten wie im Hochbeet")
    cx, base = 250, 340
    layers = [
        (220, 110, "#4a3a2c", ["Aushub + reifer Kompost", "(Pflanzschicht)"]),
        (196, 92, "#6e4f35", ["halbreifer Kompost", "oder Mist"]),
        (172, 72, "#b8864b", ["Laub, Grünmasse"]),
        (148, 52, "#8aa35a", ["Grassoden, umgedreht"]),
        (118, 32, "#9b7650", ["Kern aus Ästen und", "grobem Holz"]),
    ]
    for rx, ry, col, _ in layers:
        b += f'<path d="M{cx - rx},{base} A{rx},{ry + 40} 0 0 1 {cx + rx},{base} Z" fill="{col}" stroke="{INK}" stroke-width="0.8"/>\n'
    b += rect(20, base, 460, 70, "#bda77f", "none")
    b += f'<path d="M{cx - 118},{base} q118,46 236,0" fill="#9b7650" stroke="{INK}" stroke-width="0.8"/>\n'
    b += text(cx, base + 60, "30–40 cm tiefe Mulde, 1,5 m breit", 13, INK, "middle")
    b += legende_schichten(520, 130, [(c, z) for _, _, c, z in layers], 14, 56)
    b += text(24, 470, "Höhe 60–80 cm, quer zur Falllinie bepflanzen · Kuppe für Tomaten und Kürbis, Flanken für Kohl und Salat", 13, MUTED)
    return svg(w, h, b, "Hügelbeet im Querschnitt")


# ── Kapitel 9: Fruchtfolge und Beetpläne ────────────────────────────────
FELDER = [
    ("Kohl & Co.", "Starkzehrer · 3–4 l/m² Kompost", KOHL, ["Kohlarten, Sellerie", "Salat als Lückenfüller", "Spinat, Radieschen vorweg"]),
    ("Fruchtgemüse & Kartoffeln", "Starkzehrer · 3–4 l/m² Kompost", FRUCHT, ["Kartoffel, Tomate, Paprika", "Zucchini, Kürbis, Gurke", "Zuckermais"]),
    ("Wurzeln & Zwiebeln", "Mittelzehrer · 2–3 l/m² Kompost", WURZEL, ["Möhre, Pastinake, Rote Bete", "Zwiebel, Knoblauch, Lauch", "Mangold, Fenchel"]),
    ("Hülsenfrüchte & Bodenkur", "Schwachzehrer · kein Kompost", HUELSE, ["Erbsen, Bohnen, Salate", "danach Phacelia oder Klee", "nie Senf vor dem Kohl!"]),
]


def fruchtfolge():
    w, h = 820, 600
    b = ARROW_DEF + heading(w, "Das Vier-Felder-System", "Jedes Jahr rückt jede Gruppe ein Beet weiter")
    pos = [(60, 100), (440, 100), (440, 350), (60, 350)]
    bw, bh = 320, 200
    for (x, y), (name, sub, col, items) in zip(pos, FELDER):
        b += rect(x, y, bw, bh, col, INK, 1.2, rx=8, extra='fill-opacity="0.16"')
        b += rect(x, y, bw, 34, col, "none", rx=8)
        b += rect(x, y + 20, bw, 14, col, "none")
        i = FELDER.index((name, sub, col, items)) + 1
        b += text(x + 14, y + 23, f"Feld {i} – {name}", 15, "#fff", weight="bold")
        b += text(x + 14, y + 58, sub, 13, MUTED)
        b += lines(x + 14, y + 88, ["• " + t for t in items], 14, INK, lh=1.45)
    # Pfeile im Kreis
    b += arrow(385, 200, 435, 200)
    b += arrow(600, 305, 600, 345)
    b += arrow(435, 450, 385, 450)
    b += arrow(220, 345, 220, 305)
    b += text(410, 575, "Kreuzblütler → Nachtschatten/Kürbis → Dolden/Gänsefuß/Lauch → Hülsenfrüchtler: keine Familie zweimal hintereinander", 13, MUTED, "middle")
    return svg(w, h, b, "Vier-Felder-Fruchtfolge")


def beetplan_vier():
    w, h = 820, 430
    b = heading(w, "Beetplan: vier Beete à 1,2 × 3 m", "So wandern die Gruppen über vier Jahre")
    order = [0, 1, 2, 3]
    start = {"A": 0, "B": 1, "C": 2, "D": 3}
    x0, y0, cw, ch = 110, 110, 170, 64
    for j in range(4):
        b += text(x0 + j * cw + cw / 2, y0 - 14, f"Jahr {j + 1}", 15, INK, "middle", "bold")
    for i, bed in enumerate("ABCD"):
        y = y0 + i * (ch + 10)
        b += text(x0 - 20, y + ch / 2 + 6, f"Beet {bed}", 15, INK, "end", "bold")
        for j in range(4):
            name, sub, col, items = FELDER[(start[bed] + j) % 4]
            x = x0 + j * cw
            b += rect(x + 4, y, cw - 8, ch, col, INK, 0.8, rx=6, extra='fill-opacity="0.85"')
            short = name.replace(" & ", " &\n").split("\n")
            b += lines(x + cw / 2, y + (28 if len(short) == 2 else 38), short, 13, "#fff", "middle", "bold")
    b += text(24, 410, "Vorkulturen (Spinat, Radieschen) und Nachkulturen (Feldsalat, Grünkohl) kommen in dasselbe Feld wie die Hauptkultur.", 13, MUTED)
    return svg(w, h, b, "Beetplan für vier Beete über vier Jahre")


def reihen():
    w, h = 820, 400
    b = heading(w, "Reihen-Mischkultur im Feld „Wurzeln & Zwiebeln“", "Ein Beet 1,2 m breit, Reihen längs; Draufsicht")
    x, y, bw, bh = 60, 90, 700, 250
    b += rect(x, y, bw, bh, "#6e4f35", INK, 1, rx=4, extra='fill-opacity="0.25"')
    rows = [
        ("Zwiebeln", WURZEL, "o"),
        ("Möhren + Salat-Markiersaat", "#e0873a", "|"),
        ("Zwiebeln", WURZEL, "o"),
        ("Möhren + Salat-Markiersaat", "#e0873a", "|"),
        ("Rote Bete", "#8b2a4a", "o"),
        ("Pflücksalat, danach Feldsalat", KOHL, "*"),
    ]
    step = bh / (len(rows) + 1)
    for i, (lab, col, sym) in enumerate(rows):
        ry = y + step * (i + 1)
        b += line(x + 20, ry, x + bw - 20, ry, LINE, 1, 'stroke-dasharray="4 4"')
        for px in range(x + 40, x + bw - 180, 26 if sym == "|" else 34):
            if sym == "o":
                b += f'<circle cx="{px}" cy="{ry}" r="7" fill="{col}"/>\n'
            elif sym == "|":
                b += rect(px - 2, ry - 9, 4, 18, col, "none", rx=2)
            else:
                b += f'<circle cx="{px}" cy="{ry}" r="9" fill="{col}" fill-opacity="0.8"/>\n'
        b += rect(x + bw - 175, ry - 11, 165, 22, PAPER, "none", rx=4)
        b += text(x + bw - 168, ry + 5, lab, 12, INK)
    b += text(x + bw / 2, y + bh + 26, "Reihenabstand 20–25 cm · Zwiebeln im Juli ernten, dann haben die Möhren Platz · Feldsalat folgt im September", 13, MUTED, "middle")
    return svg(w, h, b, "Reihen-Mischkultur mit Zwiebeln und Möhren")


def hochbeet_viertel():
    w, h = 820, 480
    b = heading(w, "Hochbeet (1,2 × 2 m) in vier Vierteln", "Erstes Jahr: überall Starkzehrer · ab dem zweiten Jahr rotieren die Viertel")
    x0, y0 = 60, 100
    qw, qh = 180, 150
    plan = [
        ("A", "Kohlrabi, Pak Choi,", "Salat", KOHL),
        ("B", "1 Tomate", "+ Basilikum", FRUCHT),
        ("C", "Möhren +", "Frühlingszwiebeln", WURZEL),
        ("D", "Zuckererbsen,", "danach Feldsalat", HUELSE),
    ]
    for idx, (q, l1, l2, col) in enumerate(plan):
        cx = x0 + (idx % 2) * qw
        cy = y0 + (idx // 2) * qh
        b += rect(cx, cy, qw, qh, col, INK, 1.2, extra='fill-opacity="0.8"')
        b += text(cx + 14, cy + 28, f"Viertel {q}", 15, "#fff", weight="bold")
        b += lines(cx + qw / 2, cy + 80, [l1, l2], 14, "#fff", "middle", "bold")
    b += rect(x0 - 10, y0 - 10, 2 * qw + 20, 2 * qh + 20, "none", "#c89f6a", 10, rx=4)
    b += text(x0 + qw, y0 + 2 * qh + 44, "Jahr 2 – Beispielbelegung", 14, INK, "middle", "bold")
    # Rotationstabelle rechts
    tx = 470
    b += text(tx, 120, "Jedes Jahr ein Viertel weiter:", 15, INK, weight="bold")
    seq = ["Kohl & Co.", "Fruchtgemüse", "Wurzeln & Zwiebeln", "Hülsenfrüchte"]
    cols = [KOHL, FRUCHT, WURZEL, HUELSE]
    for i, (s, c) in enumerate(zip(seq, cols)):
        yy = 150 + i * 44
        b += rect(tx, yy, 250, 32, c, "none", rx=6, extra='fill-opacity="0.85"')
        b += text(tx + 12, yy + 21, s, 14, "#fff", weight="bold")
        if i < 3:
            b += text(tx + 125, yy + 42, "↓", 14, MUTED, "middle")
    b += text(tx, 345, "danach wieder von vorn", 13, MUTED)
    b += lines(tx, 380, ["Nach 5–7 Jahren ist die Füllung Erde:", "oben ausräumen, neu schichten."], 13, MUTED)
    return svg(w, h, b, "Hochbeet in vier Vierteln")


# ── Kapitel 10: Kompost ─────────────────────────────────────────────────
def kompost():
    w, h = 820, 390
    b = heading(w, "Drei-Kammer-Kompost", "Eine Kammer wird befüllt, eine reift, eine wird geleert")
    x0, y0, bw, bh = 60, 110, 220, 190
    kammern = [
        ("1  Befüllen", "laufend Grün + Braun", ["Küchenabfälle", "Rasenschnitt", "Laub, Häcksel"], "#8aa35a"),
        ("2  Reifen", "nach 9–12 Monaten umsetzen", ["Rotte läuft,", "Würmer ziehen ein"], "#8a6a48"),
        ("3  Entnehmen", "nach 1–2 Jahren reif", ["dunkel, krümelig,", "riecht nach Waldboden"], "#4a3a2c"),
    ]
    for i, (t, s, items, col) in enumerate(kammern):
        x = x0 + i * (bw + 20)
        b += rect(x, y0, bw, bh, col, INK, 1.2, extra='fill-opacity="0.85"')
        for k in range(1, 6):
            b += line(x, y0 + k * bh / 6, x + bw, y0 + k * bh / 6, "#00000022", 1)
        b += text(x + bw / 2, y0 - 12, t, 16, INK, "middle", "bold")
        b += text(x + bw / 2, y0 + bh + 22, s, 13, MUTED, "middle")
        b += lines(x + bw / 2, y0 + 70, items, 14, "#fff", "middle", "bold")
    b += text(410, 370, "Halbschattiger Platz auf offenem Boden · je Kammer etwa 1 × 1 m · feucht wie ein ausgedrückter Schwamm", 13, MUTED, "middle")
    return svg(w, h, b, "Drei-Kammer-Kompost")


# ── Kapitel 8: Kräuterbeet ──────────────────────────────────────────────
def kraeuterbeet():
    w, h = 820, 490
    b = heading(w, "Küchen-Kräuterbeet an der Tür (1 × 2 m)", "Links mager und sonnig, rechts frisch und nährstoffreich · Draufsicht")
    x, y, bw, bh = 60, 100, 700, 320
    b += rect(x, y, bw / 2, bh, "#e8d9a8", INK, 1.2)
    b += rect(x + bw / 2, y, bw / 2, bh, "#6e4f35", INK, 1.2, extra='fill-opacity="0.35"')
    b += text(x + bw / 4, y - 10, "mager: Erde + ⅓ Sand/Splitt, kein Kompost", 13, MUTED, "middle")
    b += text(x + 3 * bw / 4, y - 10, "frisch: humose Erde mit Kompost", 13, MUTED, "middle")
    herbs = [
        ("Thymian", 80, 70, 30, "#9aa86a", False), ("Salbei", 260, 75, 40, "#9aa86a", False),
        ("Rosmarin im Topf", 170, 165, 28, "#9aa86a", True), ("Oregano", 80, 245, 32, "#9aa86a", False),
        ("Bohnenkraut", 260, 245, 30, "#9aa86a", False),
        ("Schnittlauch", 430, 70, 30, KOHL, False), ("Liebstöckel", 610, 80, 44, KOHL, False),
        ("Minze im Topf", 520, 165, 30, KOHL, True), ("Petersilie*", 430, 245, 32, KOHL, False),
        ("Kerbel", 610, 245, 28, KOHL, False),
    ]
    for name, cx, cy, r, col, topf in herbs:
        dash = 'stroke-dasharray="4 3"' if topf else ""
        b += (f'<circle cx="{x + cx}" cy="{y + cy}" r="{r}" fill="{col}" fill-opacity="0.85" '
              f'stroke="{INK}" stroke-width="{2 if topf else 0.8}" {dash}/>\n')
        b += text(x + cx, y + cy + r + 16, name, 13, INK, "middle")
    b += text(24, 455, "* Petersilie wandert jedes Jahr an eine neue Stelle. Basilikum, Dill und Koriander stehen im Gemüsebeet oder in Töpfen.", 13, MUTED)
    b += f'<circle cx="34" cy="475" r="7" fill="none" stroke="{INK}" stroke-width="2" stroke-dasharray="4 3"/>\n'
    b += text(48, 480, "gestrichelt: im eingesenkten Topf (Rosmarin zum Überwintern, Minze gegen Wuchern)", 13, MUTED)
    return svg(w, h + 10, b, "Küchen-Kräuterbeet")


# ── Kapitel 12: Anbaukalender aus dem Datensatz ─────────────────────────
KALENDER_KULTUREN = [
    "kartoffel", "tomate", "zucchini", "buschbohne", "erbse", "moehre", "rote_bete",
    "zwiebel", "knoblauch", "lauch", "gruenkohl", "kohlrabi", "salat", "spinat",
    "mangold", "feldsalat",
]
MONATE = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]


def kalender():
    daten = json.loads((ROOT / "daten" / "kulturen.json").read_text(encoding="utf-8"))
    kulturen = {k["id"]: k for k in daten["kulturen"]}
    rows = [kulturen[i] for i in KALENDER_KULTUREN]
    lanes = [("vorkultur", "Vorkultur", C_VORKULTUR), ("direktsaat", "Direktsaat", C_DIREKTSAAT),
             ("pflanzung", "Pflanzung", C_PFLANZUNG), ("ernte", "Ernte", C_ERNTE)]
    x0, y0, cw, rh = 170, 110, 50, 34
    w = x0 + 12 * cw + 30
    h = y0 + len(rows) * rh + 70
    b = heading(w, "Anbaukalender für das Einsteiger-Sortiment", "Mitteleuropäische Flachlagen · aus dem Kulturen-Datensatz des Buches")
    for m, lab in enumerate(MONATE):
        if m % 2 == 0:
            b += rect(x0 + m * cw, y0 - 8, cw, len(rows) * rh + 8, SOFT)
        b += text(x0 + m * cw + cw / 2, y0 - 14, lab, 13, MUTED, "middle", "bold")
    for i, k in enumerate(rows):
        y = y0 + i * rh
        b += text(x0 - 12, y + rh / 2 + 4, k["name"].split(" (")[0], 14, INK, "end")
        b += line(x0, y + rh, x0 + 12 * cw, y + rh, LINE, 0.5)
        for li, (key, _, col) in enumerate(lanes):
            for m in k[key]:
                b += rect(x0 + (m - 1) * cw + 1, y + 6 + li * 6, cw - 2, 5, col, "none")
    ly = y0 + len(rows) * rh + 34
    for li, (_, lab, col) in enumerate(lanes):
        b += rect(x0 + li * 140, ly - 9, 24, 8, col)
        b += text(x0 + li * 140 + 32, ly, lab, 13, INK)
    return svg(w, h, b, "Anbaukalender für das Einsteiger-Sortiment")


# ── Pflanz- und Schnittskizzen ──────────────────────────────────────────
CUT = "#c0392b"
STAMM = "#7a5a3a"
BLATT = "#6a8f3d"
JUNG = "#8fbf4a"


def blatt(cx, cy, winkel, laenge=34, breite=12, col=BLATT):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{laenge / 2}" ry="{breite / 2}" fill="{col}" '
            f'transform="rotate({winkel} {cx} {cy})"/>\n')


def schnitt(x, y, winkel=0, laenge=26):
    """Rote Schnittmarke quer zum Trieb."""
    return (f'<line x1="{x - laenge / 2}" y1="{y}" x2="{x + laenge / 2}" y2="{y}" stroke="{CUT}" '
            f'stroke-width="4" stroke-linecap="round" transform="rotate({winkel} {x} {y})"/>\n')


def nummer(x, y, n, col=INK):
    return (f'<circle cx="{x}" cy="{y}" r="11" fill="{col}"/>\n'
            + text(x, y + 5, str(n), 13, "#fff", "middle", "bold"))


def schritte(x, y, eintraege, size=14, abstand=None):
    """Nummerierte Liste; jeder Eintrag ist eine Liste von Zeilen."""
    out = ""
    yy = y
    for i, zeilen in enumerate(eintraege, 1):
        out += nummer(x + 11, yy - 5, i)
        out += lines(x + 30, yy, zeilen, size, INK)
        yy += (abstand or (len(zeilen) * size * 1.3 + 14))
    return out


def tomate_ausgeizen():
    w, h = 820, 520
    b = heading(w, "Tomate ausgeizen", "Eintriebig am Stab: Seitentriebe in den Blattachseln jung herausbrechen")
    sx, top, boden = 210, 100, 470
    b += rect(40, boden, 360, 40, "#bda77f", "none")
    b += line(sx + 24, top - 10, sx + 24, boden + 30, "#9a8f7a", 5)          # Stab
    b += line(sx, boden, sx, top, BLATT, 7)                                   # Haupttrieb
    for y in (150, 250, 350):                                                 # Bindestellen
        b += f'<path d="M{sx - 4},{y} q14,-8 30,0" stroke="#c9a46a" stroke-width="3" fill="none"/>\n'
    # Blätter (Fiederblätter) abwechselnd
    def fieder(y, richtung, gestrichelt=False):
        out = ""
        ex = sx + richtung * 120
        extra = 'stroke-dasharray="6 5"' if gestrichelt else ""
        out += line(sx, y, ex, y - 30, BLATT if not gestrichelt else LINE, 3, extra)
        for t in (0.35, 0.65, 1.0):
            lx = sx + (ex - sx) * t
            ly = y + (-30) * t
            col = BLATT if not gestrichelt else "#d8d5c6"
            out += blatt(lx, ly - 8, -30 * richtung, 30, 12, col)
            out += blatt(lx, ly + 8, 30 * richtung, 30, 12, col)
        return out
    b += fieder(420, -1, gestrichelt=True)
    b += fieder(360, 1)
    b += fieder(290, -1)
    b += fieder(220, 1)
    b += fieder(150, -1)
    # Fruchttraube links bei 320
    b += line(sx, 322, sx - 50, 330, BLATT, 3)
    for dx, dy in [(-55, 340), (-72, 348), (-44, 356), (-62, 364)]:
        b += f'<circle cx="{sx + dx}" cy="{dy}" r="9" fill="{FRUCHT}"/>\n'
    # Geiztrieb in der Achsel bei 360 rechts
    gx, gy = sx + 4, 352
    b += f'<path d="M{gx},{gy} q18,-20 34,-48" stroke="{JUNG}" stroke-width="5" fill="none" stroke-linecap="round"/>\n'
    b += blatt(gx + 32, gy - 50, -60, 20, 9, JUNG)
    b += blatt(gx + 22, gy - 30, 20, 18, 8, JUNG)
    b += f'<circle cx="{gx + 18}" cy="{gy - 26}" r="34" fill="none" stroke="{CUT}" stroke-width="2.5" stroke-dasharray="5 4"/>\n'
    # Beschriftungen
    b += line(gx + 52, gy - 26, 440, 200, CUT, 1.2)
    b += lines(448, 196, ["Geiztrieb in der Blattachsel:", "jung mit den Fingern ausbrechen"], 14, CUT, weight="bold")
    b += line(sx - 80, 350, 90, 470 - 150, MUTED, 1)
    b += lines(24, 300, ["Fruchttraube –", "bleibt stehen"], 13, INK)
    b += line(sx - 60, 400, 100, 430, MUTED, 1)
    b += lines(24, 450, ["untere Blätter bis zur", "ersten Traube entfernen"], 13, INK)
    b += lines(448, 290, [
        "• wöchentlich kontrollieren",
        "• Geiztriebe klein entfernen (unter 5 cm)",
        "• Haupttrieb am Stab locker anbinden",
        "• Ende August die Spitze kappen",
        "• Cocktail- und Wildtomaten dürfen",
        "  mehrtriebig wachsen",
    ], 14, INK, lh=1.55)
    return svg(w, h, b, "Tomate ausgeizen")


def obstbaum_pflanzen():
    w, h = 820, 540
    b = heading(w, "Obstbaum pflanzen", "Veredlungsstelle über der Erde, Pfahl auf der Wetterseite")
    cx, erde = 250, 330
    # Boden und Pflanzloch
    b += rect(30, erde, 440, 170, "#bda77f", "none")
    b += f'<path d="M{cx - 110},{erde} L{cx - 90},{erde + 110} L{cx + 90},{erde + 110} L{cx + 110},{erde} Z" fill="#8a6a48" fill-opacity="0.55" stroke="{INK}" stroke-width="1" stroke-dasharray="5 4"/>\n'
    # Wühlmauskorb
    b += f'<path d="M{cx - 80},{erde + 5} L{cx - 70},{erde + 95} L{cx + 70},{erde + 95} L{cx + 80},{erde + 5}" fill="none" stroke="#555" stroke-width="2" stroke-dasharray="2 4"/>\n'
    # Wurzeln
    for dx, dy in [(-60, 70), (-35, 85), (0, 90), (35, 85), (60, 70), (-50, 40), (50, 40)]:
        b += f'<path d="M{cx},{erde + 15} q{dx / 2},{dy / 3} {dx},{dy}" stroke="{STAMM}" stroke-width="3" fill="none"/>\n'
    # Mulch auf der Baumscheibe
    b += rect(cx - 110, erde - 8, 95, 8, "#7a5a3a", "none")
    b += rect(cx + 15, erde - 8, 95, 8, "#7a5a3a", "none")
    # Stamm mit Veredlungsstelle
    b += line(cx, erde + 15, cx, 170, STAMM, 10)
    b += f'<ellipse cx="{cx}" cy="{erde - 24}" rx="9" ry="6" fill="{STAMM}" stroke="{INK}" stroke-width="1"/>\n'
    # Krone
    for dx, dy in [(-60, -45), (60, -40), (-32, -70), (38, -72), (0, -85)]:
        b += line(cx, 185, cx + dx, 185 + dy, STAMM, 5)
    # Pfahl links (Westen) und Achterschlinge
    px = cx - 40
    b += line(px, erde + 100, px, 175, "#9a8f7a", 8)
    b += f'<path d="M{px},{215} C{px + 10},{203} {cx - 10},{227} {cx},{215} C{cx - 10},{203} {px + 10},{227} {px},{215}" stroke="#c9a46a" stroke-width="3" fill="none"/>\n'
    # Kompass
    b += text(40, 110, "W", 14, MUTED, weight="bold")
    b += line(58, 105, 120, 105, MUTED, 1.5)
    b += text(128, 110, "O", 14, MUTED, weight="bold")
    # Beschriftungen rechts
    # (Punkt am Baum, Beschriftung) – Beschriftungen gleichmäßig verteilt
    labels = [
        (215, ["Kokosstrick als Achterschlinge", "am Pfahl auf der Westseite"]),
        (erde - 24, ["Veredlungsstelle eine", "Handbreit über der Erde"]),
        (erde - 4, ["Baumscheibe mulchen,", "Stamm frei lassen"]),
        (erde + 55, ["Pflanzloch doppelt so breit wie der", "Wurzelballen, Sohle gelockert"]),
        (erde + 95, ["Wühlmauskorb aus verzinktem Draht", "(wo Wühlmäuse vorkommen)"]),
    ]
    for i, (py, zeilen) in enumerate(labels, 1):
        ly = 170 + (i - 1) * 64
        b += line(cx + 20, py, 474, ly - 5, LINE, 1, 'stroke-dasharray="3 3"')
        b += nummer(490, ly - 5, i)
        b += lines(510, ly, zeilen, 13, INK)
    b += text(24, 525, "Nach dem Pflanzen mit 20–30 Litern angießen und im ersten Sommer regelmäßig wässern.", 13, MUTED)
    return svg(w, h, b, "Obstbaum pflanzen")


def pflanzschnitt():
    w, h = 820, 480
    b = heading(w, "Pflanzschnitt beim Apfel", "Ein Mitteltrieb, drei bis vier flache Leitäste, alles Konkurrierende raus")
    def baum(cx, nachher):
        out = rect(cx - 150, 420, 300, 20, "#bda77f", "none")
        out += line(cx, 420, cx, 150, STAMM, 9)                       # Mitteltrieb
        aeste = [(-1, 300, 110, 55), (1, 280, 115, 50), (-1, 240, 95, 45), (1, 215, 90, 40)]
        for richt, y, dx, dy in aeste:
            ex, ey = cx + richt * dx, y - dy
            if nachher:
                kx, ky = cx + richt * dx * 0.67, y - dy * 0.67
                out += line(cx, y, kx, ky, STAMM, 5)
                out += line(kx, ky, ex, ey, LINE, 3, 'stroke-dasharray="4 4"')
                out += schnitt(kx, ky, 90 + (-35 if richt > 0 else 35), 18)
            else:
                out += line(cx, y, ex, ey, STAMM, 5)
        # Konkurrenztrieb steil neben der Spitze
        if nachher:
            out += line(cx + 4, 200, cx + 30, 120, LINE, 4, 'stroke-dasharray="4 4"')
            out += schnitt(cx + 8, 190, 20, 18)
        else:
            out += line(cx + 4, 200, cx + 30, 120, STAMM, 5)
        out += text(cx, 465, "nachher" if nachher else "vorher", 15, INK, "middle", "bold")
        return out
    b += baum(210, False)
    b += baum(560, True)
    b += text(410, 280, "→", 36, MUTED, "middle")
    b += lines(705, 150, ["Leitäste um", "ein Drittel", "einkürzen,", "Schnitt über", "einem nach", "außen zeigenden", "Auge"], 12, MUTED, lh=1.35)
    b += lines(345, 120, ["steiler Konkurrenz-", "trieb: ganz entfernen"], 12, CUT)
    return svg(w, h, b, "Pflanzschnitt beim Apfel")


def johannisbeere():
    w, h = 820, 470
    b = heading(w, "Johannisbeere schneiden", "Jährlich die zwei, drei ältesten Triebe bodennah entfernen")
    cx, boden = 215, 400
    b += rect(24, boden, 400, 40, "#bda77f", "none")
    triebe = [
        (-150, 250, "alt"), (-110, 170, "mittel"), (-70, 140, "jung"), (-30, 120, "alt"),
        (10, 110, "mittel"), (50, 125, "jung"), (90, 150, "mittel"), (130, 185, "alt"),
        (165, 245, "jung"), (-5, 150, "jung"),
    ]
    farben = {"jung": JUNG, "mittel": STAMM, "alt": "#4a4a44"}
    staerke = {"jung": 3, "mittel": 5, "alt": 7}
    for dx, hy, alter in triebe:
        ex = cx + dx
        b += (f'<path d="M{cx + dx * 0.08},{boden} Q{cx + dx * 0.5},{hy + 60} {ex},{hy}" '
              f'stroke="{farben[alter]}" stroke-width="{staerke[alter]}" fill="none" stroke-linecap="round"/>\n')
        if alter == "alt":
            b += schnitt(cx + dx * 0.08, boden - 10, 0, 22)
        else:
            for t in (0.5, 0.75, 1.0):
                bx = cx + dx * 0.08 + (ex - cx - dx * 0.08) * t
                by = boden + (hy - boden) * t
                b += blatt(bx + 8, by, 20, 16, 9, BLATT)
    eintraege = [
        (JUNG, 3, ["einjährige Triebe – stehen lassen", "(bei Schwarzer Johannisbeere Fruchtholz)"]),
        (STAMM, 5, ["zwei- bis dreijährige Triebe – tragen bei", "Roter und Weißer Johannisbeere am besten"]),
        ("#4a4a44", 7, ["älteste Triebe – bodennah abschneiden"]),
    ]
    yy = 150
    for col, sw, zeilen in eintraege:
        b += line(450, yy - 5, 490, yy - 5, col, sw)
        b += lines(502, yy, zeilen, 13, INK)
        yy += 58
    b += schnitt(470, yy - 5, 0, 22)
    b += text(502, yy, "Schnittstelle", 13, CUT, weight="bold")
    b += lines(450, yy + 40, ["Ziel: 8–12 Bodentriebe unterschiedlichen", "Alters. Schnitt nach der Ernte oder im", "Spätwinter."], 13, MUTED)
    return svg(w, h, b, "Johannisbeere schneiden")


def himbeeren():
    w, h = 820, 470
    b = heading(w, "Himbeeren schneiden", "Sommer- und Herbstsorten tragen an verschiedenem Holz")
    def panel(x0, titel, sommer):
        out = text(x0 + 170, 100, titel, 16, INK, "middle", "bold")
        boden = 380
        out += rect(x0, boden, 340, 30, "#bda77f", "none")
        for dy in (240, 150):
            out += line(x0 + 10, dy, x0 + 330, dy, "#888", 1.5)
        out += line(x0 + 20, boden, x0 + 20, 130, "#9a8f7a", 5)
        out += line(x0 + 320, boden, x0 + 320, 130, "#9a8f7a", 5)
        for i, rx in enumerate(range(x0 + 60, x0 + 300, 40)):
            alt = (i % 2 == 0)
            if sommer:
                col = STAMM if alt else JUNG
                out += line(rx, boden, rx + 6, 140 if alt else 170, col, 5 if alt else 4)
                if alt:
                    out += schnitt(rx, boden - 8, 0, 20)
                    for fy in (180, 210):
                        out += f'<circle cx="{rx + 12}" cy="{fy}" r="5" fill="{FRUCHT}" fill-opacity="0.35"/>\n'
                else:
                    for fy in (200, 250, 300):
                        out += blatt(rx + 10, fy, 25, 16, 8, BLATT)
            else:
                out += line(rx, boden, rx + 6, 150, STAMM, 5)
                out += schnitt(rx, boden - 6, 0, 20)
        return out
    b += panel(40, "Sommerhimbeere", True)
    b += panel(440, "Herbsthimbeere", False)
    b += lines(40, 432, ["Nach der Ernte: abgetragene (braune) Ruten bodennah", "raus, 8–10 kräftige junge Ruten je Meter anbinden."], 13, INK)
    b += lines(440, 432, ["Im Spätwinter: alle Ruten bodennah abmähen –", "im Sommer wachsen neue, die ab August tragen."], 13, INK)
    return svg(w, h, b, "Himbeeren schneiden")


def kuerbis_bestaeuben():
    w, h = 820, 420
    b = heading(w, "Kürbis von Hand bestäuben", "Für sortenreines Saatgut – alle Zucchini und Gartenkürbisse kreuzen sich")
    def bluete(cx, cy, weiblich):
        out = ""
        stiel_y = cy + 70
        out += line(cx, cy + 20, cx, stiel_y + 50, BLATT, 5)
        if weiblich:
            out += f'<ellipse cx="{cx}" cy="{cy + 38}" rx="14" ry="20" fill="#8fbf4a" stroke="{INK}" stroke-width="1"/>\n'
        for ang in (-40, -15, 15, 40):
            out += (f'<ellipse cx="{cx}" cy="{cy - 20}" rx="14" ry="36" fill="#f2b705" stroke="#c98f00" '
                    f'stroke-width="1" transform="rotate({ang} {cx} {cy + 10})"/>\n')
        out += text(cx, cy + 150, "weibliche Blüte" if weiblich else "männliche Blüte", 14, INK, "middle", "bold")
        out += text(cx, cy + 170, "mit kleinem Fruchtknoten" if weiblich else "langer Stiel, kein Fruchtknoten", 12, MUTED, "middle")
        return out
    b += bluete(130, 210, False)
    b += bluete(330, 210, True)
    b += f'<path d="M150,160 C200,110 270,110 310,150" stroke="{INK}" stroke-width="2" fill="none" marker-end="url(#pfeil)"/>\n'
    b = ARROW_DEF + b
    b += text(230, 112, "Pollen übertragen", 12, MUTED, "middle")
    b += schritte(450, 120, [
        ["Am Vorabend eine männliche und eine", "weibliche Blüte derselben Sorte suchen,", "die am nächsten Morgen aufgehen."],
        ["Beide mit Klebeband oder Gummiring", "verschließen."],
        ["Morgens die männliche Blüte pflücken,", "Blütenblätter abzupfen, Pollen auf die", "Narbe der weiblichen Blüte tupfen."],
        ["Weibliche Blüte wieder verschließen,", "Stiel mit einem Band markieren."],
    ], 13)
    return svg(w, h, b, "Kürbis von Hand bestäuben")


def spatenprobe():
    w, h = 820, 470
    b = heading(w, "Die Spatenprobe", "Ein spatentiefer Erdblock zeigt, wie es dem Boden geht")
    def block(x, gut):
        out = ""
        by, bh, bw = 110, 260, 240
        if gut:
            out += rect(x, by, bw, bh, "#4a3a2c", INK, 1.2, rx=4)
            out += rect(x, by + 180, bw, 80, "#6e4f35", "none")
            import random
            rnd = random.Random(3)
            for _ in range(60):
                cx, cy = x + rnd.randint(8, bw - 8), by + rnd.randint(8, bh - 8)
                out += f'<circle cx="{cx}" cy="{cy}" r="{rnd.randint(3, 6)}" fill="#5c4836"/>\n'
            for rx in (x + 50, x + 110, x + 180):
                out += f'<path d="M{rx},{by} q-10,80 5,160 q8,40 -4,90" stroke="#d9c7a0" stroke-width="2" fill="none"/>\n'
            for wx, wy in [(x + 80, by + 120), (x + 160, by + 200), (x + 40, by + 220)]:
                out += f'<path d="M{wx},{wy} q10,-8 20,0 q10,8 20,0" stroke="#c98a8a" stroke-width="5" fill="none" stroke-linecap="round"/>\n'
            titel, farbe = "gut: krümelig und belebt", KOHL
            punkte = ["dunkel, riecht nach Waldboden", "runde Krümel, zerfällt leicht", "Wurzeln wachsen senkrecht", "viele Regenwürmer und Gänge"]
        else:
            out += rect(x, by, bw, bh, "#6b5a48", INK, 1.2, rx=4)
            for i, yy in enumerate(range(by + 60, by + bh, 28)):
                out += line(x + 4, yy, x + bw - 4, yy, "#3f352b", 2)
            out += rect(x, by + 150, bw, 110, "#8a8f94", "none", extra='fill-opacity="0.55"')
            for fx, fy in [(x + 40, by + 190), (x + 150, by + 220), (x + 200, by + 175)]:
                out += f'<circle cx="{fx}" cy="{fy}" r="7" fill="#b5652e" fill-opacity="0.8"/>\n'
            out += f'<path d="M{x + 110},{by} v140 q0,10 60,12" stroke="#d9c7a0" stroke-width="2" fill="none"/>\n'
            titel, farbe = "Warnsignal: verdichtet", CUT
            punkte = ["grau oder rostfleckig", "waagerechte Platten, harte Schicht", "Wurzeln knicken waagerecht ab", "kaum Regenwürmer"]
        out += text(x + bw / 2, by - 12, titel, 15, farbe, "middle", "bold")
        out += lines(x, by + bh + 30, ["• " + p for p in punkte], 13, INK)
        return out
    b += block(80, True)
    b += block(480, False)
    return svg(w, h + 20, b, "Die Spatenprobe")


def main():
    OUT.mkdir(exist_ok=True)
    save("02-zonen.svg", zonen())
    save("04-hochbeet-querschnitt.svg", hochbeet())
    save("04-no-dig-beet.svg", nodig())
    save("04-huegelbeet.svg", huegelbeet())
    save("08-kraeuterbeet.svg", kraeuterbeet())
    save("09-vier-felder.svg", fruchtfolge())
    save("09-beetplan-vier-beete.svg", beetplan_vier())
    save("09-reihen-mischkultur.svg", reihen())
    save("09-hochbeet-viertel.svg", hochbeet_viertel())
    save("10-drei-kammer-kompost.svg", kompost())
    save("12-anbaukalender.svg", kalender())
    save("03-spatenprobe.svg", spatenprobe())
    save("06-tomate-ausgeizen.svg", tomate_ausgeizen())
    save("07-obstbaum-pflanzen.svg", obstbaum_pflanzen())
    save("07-pflanzschnitt.svg", pflanzschnitt())
    save("07-johannisbeere-schnitt.svg", johannisbeere())
    save("07-himbeeren-schnitt.svg", himbeeren())
    save("14-kuerbis-handbestaeubung.svg", kuerbis_bestaeuben())


if __name__ == "__main__":
    main()
