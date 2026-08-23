# Der Selbstversorger-Garten

**Vom ersten Beet zur ganzjährigen Ernte – Buch, Anbaukalender und App**

Dieses Repository enthält das Projekt „Der Selbstversorger-Garten" mit drei
geplanten Produkten auf gemeinsamer inhaltlicher Basis:

1. **Buch** – das Manuskript (Ordner [`kapitel/`](kapitel/), Rohentwurf fertig)
2. **Anbaukalender** – Aussaat-/Pflanz-/Erntekalender, gespeist aus dem
   Kulturen-Datensatz
3. **App** – Garten-Planer mit Kulturdatenbank, Erinnerungen und
   Fruchtfolge-Logik

Es richtet sich an Einsteigerinnen und Einsteiger genauso wie an Gärtner mit
ersten Erfahrungen, die ihre Ernte planvoll ausbauen wollen.

## Recherche und Datengrundlage

- [`recherche/anbau-kulturen.md`](recherche/anbau-kulturen.md) – Recherche:
  Welche Kulturen lohnen sich im mitteleuropäischen Selbstversorger-Garten?
  Mit Auswahlkriterien, Kategorie-Tabellen, Winteranbau-Schwerpunkt,
  Konsequenzen für Kalender/App und Quellenliste.
- [`daten/kulturen.json`](daten/kulturen.json) – maschinenlesbarer Datensatz
  mit 88 Kulturen (Gemüse, Kräuter, Beeren, Baumobst, Indoor): botanische
  Familie, Nährstoffbedarf, Monatsfenster für Vorkultur/Direktsaat/
  Pflanzung/Ernte, Lagerdauer, Konservierung, Schwierigkeit, Menge pro
  Person. Gemeinsame Datenquelle für Kalender und App.

## Aufbau des Manuskripts

Die Kapitel liegen als einzelne Markdown-Dateien im Ordner [`kapitel/`](kapitel/):

| Nr. | Kapitel | Datei |
|----:|---------|-------|
| – | Vorwort | [`kapitel/00-vorwort.md`](kapitel/00-vorwort.md) |
| 1 | Warum Selbstversorgung? | [`kapitel/01-warum-selbstversorgung.md`](kapitel/01-warum-selbstversorgung.md) |
| 2 | Den Garten planen | [`kapitel/02-den-garten-planen.md`](kapitel/02-den-garten-planen.md) |
| 3 | Der Boden – das Fundament | [`kapitel/03-der-boden.md`](kapitel/03-der-boden.md) |
| 4 | Beete anlegen: Flachbeet, Hochbeet, Hügelbeet | [`kapitel/04-beete-anlegen.md`](kapitel/04-beete-anlegen.md) |
| 5 | Aussaat und Jungpflanzenanzucht | [`kapitel/05-aussaat-und-anzucht.md`](kapitel/05-aussaat-und-anzucht.md) |
| 6 | Gemüse für Selbstversorger | [`kapitel/06-gemuese-fuer-selbstversorger.md`](kapitel/06-gemuese-fuer-selbstversorger.md) |
| 7 | Obst und Beeren | [`kapitel/07-obst-und-beeren.md`](kapitel/07-obst-und-beeren.md) |
| 8 | Kräuter im Selbstversorger-Garten | [`kapitel/08-kraeuter.md`](kapitel/08-kraeuter.md) |
| 9 | Mischkultur und Fruchtfolge | [`kapitel/09-mischkultur-und-fruchtfolge.md`](kapitel/09-mischkultur-und-fruchtfolge.md) |
| 10 | Kompost und natürliche Düngung | [`kapitel/10-kompost-und-duengung.md`](kapitel/10-kompost-und-duengung.md) |
| 11 | Pflanzengesundheit ohne Chemie | [`kapitel/11-pflanzengesundheit.md`](kapitel/11-pflanzengesundheit.md) |
| 12 | Das Gartenjahr – Monat für Monat | [`kapitel/12-das-gartenjahr.md`](kapitel/12-das-gartenjahr.md) |
| 13 | Ernten, Lagern, Haltbarmachen | [`kapitel/13-ernten-lagern-haltbarmachen.md`](kapitel/13-ernten-lagern-haltbarmachen.md) |
| 14 | Saatgut selbst gewinnen | [`kapitel/14-saatgut-gewinnen.md`](kapitel/14-saatgut-gewinnen.md) |
| 15 | Ausblick: Selbstversorgung als Lebensstil | [`kapitel/15-ausblick.md`](kapitel/15-ausblick.md) |

Die geplante Struktur mit Kurzbeschreibung jedes Kapitels steht in
[`gliederung.md`](gliederung.md).

## Status

**Buch:** Erster vollständiger Rohentwurf aller Kapitel. Offene Arbeiten:

- [ ] Lektorat und sprachlicher Feinschliff
- [ ] Abbildungen, Skizzen und Beetpläne
- [ ] Regionale Anpassungen (Klimazonen, Höhenlagen)
- [ ] Register / Stichwortverzeichnis

**Kalender & App:** Recherche, Kulturen-Datensatz (v0.1) und ein interaktiver
HTML-Prototyp liegen vor.

- [x] Interaktiver Kalender-Prototyp: [`app/kalender.html`](app/kalender.html)
      – eigenständige HTML-Datei (Daten eingebettet), Monats- und
      Jahresansicht, Filter (Suche, Kategorie, Schwierigkeit, lagerfähig),
      Detail-Dialog je Kultur, helles und dunkles Farbschema; im Browser
      öffnen, kein Server nötig
- [x] Beetplan mit Fruchtfolge-Check: Beete anlegen, Kulturen pro Jahr
      zuweisen (mit Jahresnavigation), automatische Warnung, wenn dieselbe
      Pflanzenfamilie innerhalb von 3 Jahren erneut auf ein Beet käme,
      Nährstoffbedarfs-Bilanz je Beet; Speicherung lokal im Browser
      (localStorage), Beispieldaten über „Beispiel laden"
- [ ] Datensatz-Review (Zeitfenster gegen weitere Quellen prüfen, Sorten ergänzen)
- [ ] Druck-/PDF-Jahreskalender aus `daten/kulturen.json` generieren
- [ ] App-Ausbau: Staffelsaat-Erinnerungen, Lagen-Offset ±2–4 Wochen,
      Export/Import des Beetplans, Plattform-Entscheidung
