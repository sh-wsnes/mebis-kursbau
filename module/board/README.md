# Board

Eine digitale Pinnwand mit Spalten, auf der Schülerinnen und Schüler Beiträge anheften: Text, Links, Bilder. Geeignet für Brainstorming, Sammeln von Ergebnissen und Feedbackrunden.

## So bestellst du es bei der KI

„Leg ein Board ‚Was wir schon wissen‘ an mit den Spalten Personen, Ereignisse und Begriffe.“

## Das geht

- beliebig viele Spalten mit eigenen Namen
- Beschreibung über dem Board
- Bewertung der Beiträge per Stern
- Schüler dürfen eigene Beiträge nachträglich ändern

## Das geht noch nicht

- Beiträge vorab anlegen (sie zählen als Nutzerdaten)
- Abgabefrist, Einzelmodus, Hintergrundbild

## Getestet

Noch nicht in der Lernplattform getestet.

## Für die KI

`typ`: `board`

| Feld | Pflicht/Wahl | Bedeutung |
|---|---|---|
| `name` | Pflicht | Name auf der Kursseite |
| `spalten` | Pflicht | Liste von Spaltennamen, mindestens einer |
| `beschreibung` | Wahl | HTML |
| `bewertung` | Wahl | `true`: Beiträge können bewertet werden; Standard `false` |
| `bearbeiten_erlaubt` | Wahl | `true`: Schüler dürfen ihre Beiträge ändern; Standard `false` |
| `farbe` | Wahl | Hintergrundfarbe wie in der Lernplattform benannt; Standard `gelb` |

Die Farbnamen stammen aus der Lernplattform (in der Mustersicherung stand `gelb`). Andere Werte sind ungeprüft.

Ein Kurs, der nur dieses Element enthält: [`beispiel.json`](beispiel.json).
