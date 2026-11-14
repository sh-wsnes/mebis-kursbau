# Buch

Mehrere Seiten mit Inhaltsverzeichnis und Blättern-Funktion, gegliedert in Kapitel und Unterkapitel. Geeignet für längere Infotexte, die man nicht auf eine Textseite packen will.

## So bestellst du es bei der KI

„Mach ein Buch ‚Weimarer Republik‘ mit den Kapiteln Entstehung, Krisenjahre und Ende; unter Krisenjahre die Unterkapitel Inflation und Putschversuche.“

## Das geht

- beliebig viele Kapitel und Unterkapitel (eine Ebene)
- HTML in jedem Kapitel wie bei Textseiten, einschließlich Bilder aus dem Internet
- Nummerierung der Kapitel: Zahlen (Standard), Punkte, Einrückung oder keine

## Das geht noch nicht

- hochgeladene Bilder in Kapiteln
- versteckte Kapitel

## Getestet

Am 14.11.2026 in der ByCS-Lernplattform (Moodle 5.2.4) wiederhergestellt und geprüft, einschließlich Unterkapitel.

## Für die KI

`typ`: `buch`

| Feld | Pflicht/Wahl | Bedeutung |
|---|---|---|
| `name` | Pflicht | Name des Buchs auf der Kursseite |
| `kapitel` | Pflicht | Liste von Kapiteln, siehe unten |
| `beschreibung` | Wahl | HTML, steht auf der Kursseite unter dem Namen |
| `nummerierung` | Wahl | `zahlen` (Standard), `punkte`, `einrueckung` oder `keine` |

Ein Kapitel ist ein Objekt mit `titel`, `html` und dem Wahlfeld `unterkapitel` (`true`: gehört zum vorhergehenden Hauptkapitel). Das erste Kapitel kann kein Unterkapitel sein.

Ein Kurs, der nur dieses Element enthält: [`beispiel.json`](beispiel.json).
