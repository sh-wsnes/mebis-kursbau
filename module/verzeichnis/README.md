# Verzeichnis

Ein Ordner mit mehreren Dateien, auf Wunsch mit Unterordnern. Geeignet für Materialsammlungen.

## So bestellst du es bei der KI

„Mach ein Verzeichnis ‚Material‘ mit dem Arbeitsblatt und den beiden Bildern, die Bilder in einen Unterordner ‚Bilder‘.“

## Das geht

- beliebig viele Dateien
- Unterordner, auch verschachtelt
- aufgeklappt (Standard) oder eingeklappt auf der Kursseite

## Das geht noch nicht

- Schüler dürfen Dateien hochladen

## Getestet

Noch nicht in der Lernplattform getestet.

## Für die KI

`typ`: `verzeichnis`

| Feld | Pflicht/Wahl | Bedeutung |
|---|---|---|
| `name` | Pflicht | Name auf der Kursseite |
| `dateien` | Pflicht | Liste, siehe unten |
| `beschreibung` | Wahl | HTML |
| `aufgeklappt` | Wahl | `true` (Standard) oder `false` |

Ein Eintrag in `dateien` ist entweder ein Pfad (`"dateien/arbeitsblatt.pdf"`, landet im Hauptordner) oder ein Objekt mit `pfad` und `ordner` (`{"pfad": "dateien/bild.png", "ordner": "Bilder/Weitere"}`).

Ein Kurs, der nur dieses Element enthält: [`beispiel.json`](beispiel.json).
