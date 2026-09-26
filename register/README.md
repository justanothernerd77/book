# Stichwortverzeichnis

`erzeugen.py` erzeugt `kapitel/16-stichwortverzeichnis.md` aus den
Kapiteltexten:

```
python3 register/erzeugen.py
```

- **Stichwörter** stehen mit ihren Suchmustern (reguläre Ausdrücke) in
  `STICHWORTE`. Neue Begriffe dort ergänzen; Siehe-Verweise als
  `"Porree": "→ Lauch"`.
- **Hauptstelle** (fett): für Gemüse, Obst und Kräuter das Porträtkapitel
  (6, 7 bzw. 8), sonst das Kapitel mit dem Begriff in einer Überschrift
  oder den meisten Nennungen. Ausnahmen in `HAUPTSTELLE`.
- Bei Begriffen, die in mehr als sechs Kapiteln vorkommen, werden nur
  Kapitel mit mindestens drei Nennungen aufgeführt.
- Nach jeder Textänderung das Skript erneut ausführen. Sobald das Buch
  gesetzt ist, lassen sich die Kapitelverweise durch Seitenzahlen ersetzen.
