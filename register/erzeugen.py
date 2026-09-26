#!/usr/bin/env python3
"""Erzeugt das Stichwortverzeichnis (kapitel/16-stichwortverzeichnis.md).

Aufruf aus dem Repository-Wurzelverzeichnis:

    python3 register/erzeugen.py

Die Stichwörter und ihre Suchmuster stehen in STICHWORTE. Das Skript
durchsucht die Kapitel 1–15 und verweist auf Kapitelnummern; fett gedruckt
ist die Hauptstelle (das Stichwort steht dort in einer Überschrift oder
kommt dort am häufigsten vor). Seitenzahlen lassen sich erst nach dem Satz
eintragen.

Format je Eintrag:
    "Stichwort": [Suchmuster, ...]         Muster sind reguläre Ausdrücke
    "Stichwort": "→ Verweis"               reiner Siehe-Verweis
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KAPITEL = ROOT / "kapitel"
ZIEL = KAPITEL / "16-stichwortverzeichnis.md"

# Wortanfang ohne Buchstaben davor (auch Umlaute)
W = r"(?<![A-Za-zÄÖÜäöüß])"

STICHWORTE = {
    # ── Gemüse ──
    "Asia-Salate": [r"Asia-Salat", r"Mizuna"],
    "Aubergine": [r"Auberginen?"],
    "Blumenkohl": [r"Blumenkohl"],
    "Bohne": [r"Buschbohne", r"Stangenbohne", r"Bohnenzelt", W + r"Bohnen?\b"],
    "Brokkoli": [r"Brokkoli"],
    "Chinakohl": [r"Chinakohl"],
    "Dicke Bohne": [r"Dicke[n]? Bohne"],
    "Endivie": [r"Endivie"],
    "Erbse": [W + r"Erbsen?\b", r"Zuckererbse", r"Markerbse"],
    "Feldsalat": [r"Feldsalat"],
    "Fenchel": [r"Fenchel"],
    "Feuerbohne": [r"Feuerbohne"],
    "Grünkohl": [r"Grünkohl"],
    "Gurke": [W + r"Gurken?\b", r"Einlegegurke", r"Salzgurke"],
    "Kartoffel": [W + r"Kartoffel(n|s)?\b", r"Frühkartoffel", r"Lagerkartoffel"],
    "Knoblauch": [r"Knoblauch"],
    "Knollensellerie": "→ Sellerie",
    "Kohl": [W + r"Kohl\b", r"Kohlarten", r"Kopfkohl", r"Weißkohl", r"Rotkohl"],
    "Kohlrabi": [r"Kohlrabi"],
    "Kürbis": [r"Kürbis(?!gewächs)"],
    "Lauch": [W + r"Lauch\b", r"Porree", r"Winterlauch"],
    "Mais": [r"Zuckermais", W + r"Mais\b"],
    "Mangold": [r"Mangold"],
    "Möhre": [W + r"Möhren?\b", r"Lagermöhre"],
    "Pak Choi": [r"Pak Choi"],
    "Palmkohl": [r"Palmkohl"],
    "Paprika": [r"Paprika", r"Chili"],
    "Pastinake": [r"Pastinake"],
    "Porree": "→ Lauch",
    "Radicchio": [r"Radicchio"],
    "Radieschen": [r"Radieschen"],
    "Rettich": [r"Rettich"],
    "Rhabarber": [r"Rhabarber"],
    "Rosenkohl": [r"Rosenkohl"],
    "Rote Bete": [r"Rote[n]? Bete"],
    "Rucola": [r"Rucola"],
    "Salat": [W + r"Salat(e|s)?\b", r"Pflücksalat", r"Kopfsalat", r"Schnittsalat"],
    "Schalotte": [r"Schalotte"],
    "Schwarzwurzel": [r"Schwarzwurzel"],
    "Sellerie": [r"Sellerie"],
    "Spargel": [W + r"Spargel"],
    "Spinat": [W + r"Spinat"],
    "Steckrübe": [r"Steckrübe"],
    "Tomate": [W + r"Tomaten?\b", r"Tomatensoße"],
    "Topinambur": [r"Topinambur"],
    "Winterportulak": [r"Winterportulak", r"Postelein"],
    "Wirsing": [r"Wirsing"],
    "Zucchini": [r"Zucchini"],
    "Zuckerhut": [r"Zuckerhut"],
    "Zwiebel": [W + r"Zwiebeln?\b", r"Steckzwiebel", r"Wintersteckzwiebel"],
    # ── Obst ──
    "Apfel": [W + r"Äpfel", W + r"Apfel", r"Lageräpfel", r"Lagerapfel"],
    "Birne": [W + r"Birnen?\b"],
    "Brombeere": [r"Brombeere"],
    "Erdbeere": [r"Erdbeere"],
    "Haselnuss": [r"Haselnuss"],
    "Heidelbeere": [r"Heidelbeere"],
    "Himbeere": [r"Himbeere", r"Herbsthimbeere", r"Sommerhimbeere"],
    "Holunder": [r"Holunder"],
    "Johannisbeere": [r"Johannisbeere"],
    "Kirsche": [r"Kirsche(n)?\b", r"Süßkirsche", r"Sauerkirsche"],
    "Mini-Kiwi": [r"Mini-Kiwi"],
    "Pfirsich": [r"Pfirsich"],
    "Quitte": [r"Quitte"],
    "Stachelbeere": [r"Stachelbeere"],
    "Wein": [r"Weinrebe"],
    "Zwetschge": [r"Zwetschge", r"Pflaume"],
    # ── Kräuter ──
    "Basilikum": [r"Basilikum"],
    "Bärlauch": [r"Bärlauch"],
    "Dill": [W + r"Dill\b"],
    "Kapuzinerkresse": [r"Kapuzinerkresse"],
    "Koriander": [r"Koriander"],
    "Kresse": [r"Gartenkresse", W + r"Kresse\b"],
    "Liebstöckel": [r"Liebstöckel"],
    "Minze": [W + r"Minze", r"Pfefferminze"],
    "Oregano": [r"Oregano", r"Majoran"],
    "Petersilie": [r"Petersilie"],
    "Ringelblume": [r"Ringelblume"],
    "Rosmarin": [r"Rosmarin"],
    "Salbei": [r"Salbei"],
    "Schnittlauch": [r"Schnittlauch"],
    "Tagetes": [r"Tagetes"],
    "Teekräuter": [r"Teekräuter", r"Teemischung"],
    "Thymian": [r"Thymian"],
    "Wildkräuter": [r"Wildkräuter", r"Giersch", r"Brennnessel"],
    "Zitronenmelisse": [r"Zitronenmelisse", r"Melisse"],
    # ── Boden, Beete, Planung ──
    "Beetmaße": [r"120 cm", r"Beetbreite"],
    "Bodenarten": [r"Sandboden", r"Lehmboden", r"Tonboden", r"Schluff", r"Bodenart"],
    "Bodenleben": [r"Bodenleben", r"Mykorrhiza"],
    "Bodenprobe": [r"Bodenprobe", r"Bodenuntersuchung", r"Laboranalyse"],
    "Fingerprobe": [r"Fingerprobe"],
    "Frostlage": [r"Frostlage", r"Frostsenke", r"Kaltluft"],
    "Gartentagebuch": [r"Gartentagebuch"],
    "Hochbeet": [r"Hochbeet"],
    "Humus": [r"Humus"],
    "Hügelbeet": [r"Hügelbeet"],
    "Kleingarten": [r"Kleingarten"],
    "Kleinklima": [r"Kleinklima", r"Südwand"],
    "No-Dig-Beet": [r"No-Dig"],
    "pH-Wert": [r"pH-Wert", r"\bpH\b"],
    "Regenwasser": [r"Regenwasser", r"Regentonne", r"Zisterne"],
    "Regenwurm": [r"Regenwurm", r"Regenwürmer"],
    "Spatenprobe": [r"Spatenprobe"],
    "Verdichtung": [r"Verdichtung", r"verdichtet"],
    "Wege": [r"Hauptweg", r"Zwischenweg", r"Hackschnitzel"],
    "Werkzeug": [r"Werkzeug", r"Grabegabel", r"Sauzahn", r"Pendelhacke"],
    "Zeigerpflanzen": [r"Zeigerpflanze"],
    "Zonierung": [r"Zone 1", r"zonieren", r"Zonierung"],
    # ── Anbau ──
    "Abhärten": [r"[Aa]bhärten"],
    "Anhäufeln": [r"[Aa]nhäufeln"],
    "Anzucht": [r"Anzucht", r"Vorkultur"],
    "Ausgeizen": [r"[Aa]us(ge)?geiz", r"Geiztrieb"],
    "Direktsaat": [r"Direktsaat"],
    "Dunkelkeimer": "→ Lichtkeimer",
    "Eisheilige": [r"Eisheilige"],
    "Frühbeet": [r"Frühbeet"],
    "Folientunnel": [r"Folientunnel"],
    "Gewächshaus": [r"Gewächshaus"],
    "Keimprobe": [r"Keimprobe"],
    "Keimtemperatur": [r"Keimtemperatur", r"Bodentemperatur"],
    "Kulturschutznetz": [r"Kulturschutznetz", r"Maschenweite"],
    "Lichtkeimer": [r"Lichtkeimer", r"Dunkelkeimer"],
    "Markiersaat": [r"Markiersaat"],
    "Microgreens": [r"Microgreens", r"Sprossen"],
    "Nachkultur": [r"Nachkultur"],
    "Pikieren": [r"[Pp]ikier"],
    "Pflanzenlampe": [r"Pflanzenlampe", r"Pflanzen-LED", r"Vollspektrum"],
    "Staffelsaat": [r"Staffelsaat", r"gestaffelt"],
    "Vereinzeln": [r"[Vv]ereinzeln"],
    "Vlies": [W + r"Vlies"],
    "Vorkultur": "→ Anzucht",
    "Winteranbau": [r"Winteranbau", r"Wintergemüse", r"Wintersalat"],
    # ── Fruchtfolge und Mischkultur ──
    "Fruchtfolge": [r"Fruchtfolge"],
    "Gründüngung": [r"Gründüngung", r"Phacelia"],
    "Mischkultur": [r"Mischkultur"],
    "Pflanzenfamilien": [r"Pflanzenfamilie", r"Kreuzblütler", r"Doldenblütler",
                         r"Nachtschattengewächs", r"Hülsenfrüchtler", r"Lauchgewächs",
                         r"Kürbisgewächs", r"Korbblütler", r"Gänsefußgewächs"],
    "Starkzehrer": [r"Starkzehrer", r"Mittelzehrer", r"Schwachzehrer"],
    "Vier-Felder-System": [r"Vier-Felder"],
    "Mittelzehrer": "→ Starkzehrer",
    "Schwachzehrer": "→ Starkzehrer",
    # ── Düngung ──
    "Beinwell": [r"Beinwell"],
    "Bokashi": [r"Bokashi"],
    "Hornspäne": [r"Hornspäne", r"Hornmehl"],
    "Jauche": [r"Jauche"],
    "Kalk": [W + r"Kalk(en|ung)?\b", r"kohlensaurer Kalk", r"Algenkalk"],
    "Kompost": [r"Kompost"],
    "Mist": [W + r"Mist\b", r"Pferdemist", r"Rindermist", r"Hühnermist"],
    "Mulch": [r"Mulch"],
    "Nährstoffe": [r"Stickstoff", r"Phosphor", r"Kalium", r"Magnesium"],
    "Wurmkiste": [r"Wurmkiste"],
    # ── Pflanzengesundheit ──
    "Blattläuse": [r"Blattl[aä]us"],
    "Blütenendfäule": [r"Blütenendfäule"],
    "Braunfäule": [r"Braunfäule", r"Krautfäule"],
    "Drahtwurm": [r"Drahtwurm", r"Drahtwürmer"],
    "Erdflöhe": [r"Erdfl[oö]h"],
    "Kartoffelkäfer": [r"Kartoffelkäfer"],
    "Kohlfliege": [r"Kohlfliege"],
    "Kohlhernie": [r"Kohlhernie"],
    "Kohlweißling": [r"Kohlweißling"],
    "Lauchminierfliege": [r"Lauchminierfliege"],
    "Maulwurf": [r"Maulwurf"],
    "Mehltau": [r"Mehltau"],
    "Möhrenfliege": [r"Möhrenfliege"],
    "Monilia": [r"Monilia"],
    "Nützlinge": [r"Nützling", r"Marienkäfer", r"Schwebfliege", r"Florfliege", r"Igel"],
    "Pflanzenstärkung": [r"Pflanzenstärkung", r"Ackerschachtelhalm", r"Schachtelhalm"],
    "Rost": [r"Birnengitterrost", W + r"Rost\b"],
    "Schnecken": [r"Schnecke", r"Schneckenkorn", r"Schneckenzaun"],
    "Schorf": [r"Schorf"],
    "Wühlmaus": [r"Wühlm[aä]us"],
    "Zwiebelfliege": [r"Zwiebelfliege"],
    # ── Obstbau ──
    "Alternanz": [r"Alternanz"],
    "Ausdünnen": [r"[Aa]usdünnen"],
    "Befruchtung (Obst)": [r"Befruchter", r"selbstfruchtbar"],
    "Leimring": [r"Leimring"],
    "Obstbaumschnitt": [r"Obstbaumschnitt", r"Pflanzschnitt", r"Sommerschnitt", r"Winterschnitt", r"Kernobstschnitt"],
    "Spalierobst": [r"Spalier", r"Säulenobst", r"Säulenäpfel", r"Kordon"],
    "Unterlage": [r"Unterlage"],
    "Veredlung": [r"Veredlung"],
    "Weißanstrich": [r"Weißanstrich"],
    "Wildobst": [r"Wildobst", r"Felsenbirne", r"Aronia", r"Kornelkirsche", r"Sanddorn"],
    # ── Ernte und Vorrat ──
    "Blanchieren": [r"[Bb]lanchier"],
    "Botulismus": [r"Botulismus", r"botulinum"],
    "Einfrieren": [r"[Ee]infrieren", r"Tiefkühl"],
    "Einkochen": [r"[Ee]inkoch", r"Druckeinkocher"],
    "Einlegen": [r"[Ee]inlegen", r"Essig"],
    "Erdmiete": [r"Erdmiete"],
    "Fermentieren": [r"[Ff]ermentier", r"Sauerkraut", r"Milchsäure"],
    "Keller": [r"Keller", r"Speisekammer"],
    "Kräuteröl": [r"Kräuteröl", r"Knoblauchöl", r"in Öl"],
    "Lagerung": [r"Lagerung", r"einlagern", r"Lagergemüse"],
    "Marmelade": [r"Marmelade", r"Konfitüre"],
    "Phasin": [r"Phasin"],
    "Solanin": [r"Solanin"],
    "Trocknen": [r"[Tt]rocknen", r"Dörr"],
    "Vorratsplan": [r"Vorratsplan", r"Vorratsliste"],
    # ── Saatgut ──
    "F1-Hybride": [r"F1", r"Hybrid"],
    "Handbestäubung": [r"Handbestäubung", r"von Hand bestäub"],
    "Samenfeste Sorten": [r"samenfest"],
    "Saatgut": [r"Saatgut"],
    "Saatgut-Tausch": [r"Tauschbörse", r"Saatgut teilen", r"Saatgutbibliothek"],
    "Zweijährige Kulturen": [r"[Zz]weijährig"],
    # ── Jahreslauf und Allgemeines ──
    "Arbeitsaufwand": [r"Zeitaufwand", r"Arbeitsspitze", r"Stunden pro Woche"],
    "Flächenbedarf": [r"pro Person", r"Flächenbedarf"],
    "Hungerlücke": [r"Hungerlücke"],
    "Hühner": [r"Hühner", r"Huhn\b"],
    "Bienen": [r"Honigbiene", r"Wildbiene", r"Imker"],
    "Johanni": [r"Johanni"],
    "Klimawandel": [r"Klimawandel"],
    "Paragrafen": [r"Paragrafen"],
    "Phänologischer Kalender": [r"[Pp]hänolog", r"Zeigerpflanzen des"],
    "Solidarische Landwirtschaft": [r"Solawi", r"Solidarische Landwirtschaft"],
    "Spätfrost": [r"Spätfrost"],
    "Teilselbstversorgung": [r"Teilselbstversorgung", r"Ergänzungsgarten"],
}

# Heimatkapitel: Porträts von Gemüse (6), Obst (7) und Kräutern (8)
HEIMAT = {
    6: ["Asia-Salate", "Aubergine", "Blumenkohl", "Bohne", "Brokkoli", "Chinakohl",
        "Dicke Bohne", "Endivie", "Erbse", "Feldsalat", "Fenchel", "Grünkohl", "Gurke",
        "Kartoffel", "Knoblauch", "Kohl", "Kohlrabi", "Kürbis", "Lauch", "Mais",
        "Mangold", "Möhre", "Pak Choi", "Palmkohl", "Paprika", "Pastinake", "Radicchio",
        "Radieschen", "Rettich", "Rosenkohl", "Rote Bete", "Rucola", "Salat", "Schalotte",
        "Schwarzwurzel", "Sellerie", "Spargel", "Spinat", "Steckrübe", "Tomate",
        "Topinambur", "Winterportulak", "Wirsing", "Zucchini", "Zuckerhut", "Zwiebel"],
    7: ["Apfel", "Birne", "Brombeere", "Erdbeere", "Haselnuss", "Heidelbeere", "Himbeere",
        "Holunder", "Johannisbeere", "Kirsche", "Mini-Kiwi", "Pfirsich", "Quitte",
        "Rhabarber", "Stachelbeere", "Wein", "Zwetschge"],
    8: ["Basilikum", "Bärlauch", "Dill", "Kapuzinerkresse", "Koriander", "Kresse",
        "Liebstöckel", "Minze", "Oregano", "Petersilie", "Ringelblume", "Rosmarin",
        "Salbei", "Schnittlauch", "Thymian", "Zitronenmelisse"],
}

# Hauptstelle von Hand festlegen, wo die Zählung in die Irre führt
HAUPTSTELLE = {
    "Ausgeizen": {6},
    "Hochbeet": {4},
    "Tagetes": {9},
}
for _kap, _woerter in HEIMAT.items():
    for _w in _woerter:
        HAUPTSTELLE.setdefault(_w, {_kap})


def kapitel_lesen():
    """Liefert {Nummer: (Text, Überschriften-Text)} für Vorwort (0) und Kapitel 1–15."""
    daten = {}
    for datei in sorted(KAPITEL.glob("[0-9][0-9]-*.md")):
        nr = int(datei.name[:2])
        if not 0 <= nr <= 15:
            continue
        inhalt = datei.read_text(encoding="utf-8")
        # Bildverweise und Abbildungsunterschriften nicht mitzählen
        inhalt = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", inhalt)
        inhalt = re.sub(r"^\*Abbildung .*\*$", "", inhalt, flags=re.M)
        ueberschriften = "\n".join(re.findall(r"^#{1,4} .*$", inhalt, flags=re.M))
        daten[nr] = (inhalt, ueberschriften)
    return daten


def fundstellen(wort, muster, daten):
    """Liefert [(Kapitel, Hauptstelle?)] für ein Stichwort."""
    regex = re.compile("|".join(f"(?:{m})" for m in muster))
    zaehlung = {}
    in_ueberschrift = set()
    for nr, (text, ueb) in daten.items():
        n = len(regex.findall(text))
        if n:
            zaehlung[nr] = n
        if regex.search(ueb):
            in_ueberschrift.add(nr)
    if not zaehlung:
        return []
    # Hauptstelle: Kapitel mit dem Begriff in einer Überschrift und vielen
    # Nennungen; sonst das Kapitel mit den meisten Nennungen.
    spitze = max(zaehlung.values())
    haupt = {nr for nr in in_ueberschrift if zaehlung.get(nr, 0) >= spitze / 2}
    if wort in HAUPTSTELLE:
        haupt = HAUPTSTELLE[wort] & set(zaehlung)
    if not haupt:
        haupt = {max(sorted(zaehlung), key=lambda nr: zaehlung[nr])}
    # Bei häufigen Begriffen nur Kapitel mit mehreren Nennungen
    schwelle = 3 if len(zaehlung) > 6 else 1
    kapitel = sorted(nr for nr, n in zaehlung.items() if n >= schwelle or nr in haupt)
    return [(nr, nr in haupt) for nr in kapitel]


def sortierschluessel(wort):
    ersatz = str.maketrans({"Ä": "A", "Ö": "O", "Ü": "U", "ä": "a", "ö": "o", "ü": "u", "ß": "ss"})
    return wort.translate(ersatz).lower()


def main():
    daten = kapitel_lesen()
    eintraege = []
    fehlend = []
    for wort, muster in STICHWORTE.items():
        if isinstance(muster, str):
            eintraege.append((wort, f"*siehe* {muster.lstrip('→ ').strip()}"))
            continue
        treffer = fundstellen(wort, muster, daten)
        if not treffer:
            fehlend.append(wort)
            continue
        teile = [f"**{nr or 'V'}**" if haupt else str(nr or "V") for nr, haupt in treffer]
        eintraege.append((wort, ", ".join(teile)))

    eintraege.sort(key=lambda e: sortierschluessel(e[0]))
    zeilen = [
        "# Stichwortverzeichnis",
        "",
        "Die Zahlen verweisen auf die **Kapitel** (V = Vorwort); fett gedruckt",
        "ist die Hauptstelle. Seitenzahlen werden nach dem Satz ergänzt.",
        "",
        "<!-- Automatisch erzeugt mit register/erzeugen.py – nicht von Hand bearbeiten. -->",
    ]
    buchstabe = None
    for wort, verweis in eintraege:
        b = sortierschluessel(wort)[0].upper()
        if b != buchstabe:
            buchstabe = b
            zeilen += ["", f"## {b}", ""]
        zeilen.append(f"- {wort} {verweis}")
    ZIEL.write_text("\n".join(zeilen) + "\n", encoding="utf-8")
    print(f"{len(eintraege)} Einträge geschrieben nach {ZIEL.relative_to(ROOT)}")
    if fehlend:
        print("Ohne Fundstelle:", ", ".join(fehlend))


if __name__ == "__main__":
    main()
