# Tagebuch (Journal)

Ein persönlicher Text je Schülerin oder Schüler, den nur die Lehrkraft liest und kommentieren kann. Der Eintrag lässt sich über längere Zeit fortschreiben. Geeignet für Lerntagebücher, Reflexionen und Schreibaufträge, die nicht als Abgabe bewertet werden sollen.

## So bestellst du es bei der KI

„Leg ein Tagebuch ‚Lerntagebuch‘ an mit dem Auftrag: Schreibe nach jeder Stunde drei Sätze …“

## Das geht

- Schreibauftrag, der sichtbar über dem Eintrag steht
- Höchstpunktzahl für die Rückmeldung
- Bearbeitungszeitraum in Tagen ab Kursbeginn (Standard: unbegrenzt)

## Das geht noch nicht

- Dateien im Schreibauftrag

## Getestet

Noch nicht in der Lernplattform getestet.

## Für die KI

`typ`: `tagebuch`

| Feld | Pflicht/Wahl | Bedeutung |
|---|---|---|
| `name` | Pflicht | Name auf der Kursseite |
| `schreibauftrag` | Pflicht | HTML, steht über dem Eingabefeld |
| `punkte` | Wahl | Höchstpunktzahl, Standard 100 |
| `tage` | Wahl | Bearbeitungszeitraum in Tagen, Standard 0 (unbegrenzt) |

Ein Kurs, der nur dieses Element enthält: [`beispiel.json`](beispiel.json).
