# Feedback

Eine Umfrage mit mehreren Fragen, auf Wunsch anonym. Geeignet für Rückmeldungen zum Unterricht, zur Methode oder zur Gruppenarbeit. Anders als die Abstimmung kann ein Feedback viele Fragen verschiedener Art enthalten.

## So bestellst du es bei der KI

„Mach ein anonymes Feedback zur Projektwoche: Wie hat dir die Woche gefallen (Skala 1 bis 5), welche Station war am besten (Auswahl: A, B, C), und ein Textfeld für Wünsche.“

## Das geht

- Fragearten: Überschrift/Hinweistext, Einfachauswahl, Mehrfachauswahl, Auswahlliste, Skala (bewertete Auswahl), Zahl in einem Bereich, kurzer Text, langer Text
- anonym (Standard) oder mit Namen
- Pflichtfragen
- Mehrfachabgabe, Dankestext nach dem Absenden, Ergebnisse für Schüler sichtbar

## Das geht noch nicht

- Fragen, die von vorherigen Antworten abhängen
- Seitenumbrüche, Zeitfenster
- Vorlagen

## Getestet

Am 15.11.2026 in der ByCS-Lernplattform (Moodle 5.2.4) wiederhergestellt und geprüft.

## Für die KI

`typ`: `feedback`

| Feld | Pflicht/Wahl | Bedeutung |
|---|---|---|
| `name` | Pflicht | Name auf der Kursseite |
| `fragen` | Pflicht | Liste von Fragen, siehe unten |
| `beschreibung` | Wahl | HTML |
| `anonym` | Wahl | `true` (Standard) oder `false` |
| `pflicht` je Frage | Wahl | `true`: muss beantwortet werden |
| `mehrfach` | Wahl | `true`: mehrmals ausfüllbar; Standard `false` |
| `danke` | Wahl | HTML, erscheint nach dem Absenden |
| `ergebnisse_zeigen` | Wahl | `true`: Schüler sehen die Auswertung; Standard `false` |

Jede Frage hat `art` und `text`, dazu je nach Art:

| `art` | Zusätzliche Felder | In der Lernplattform |
|---|---|---|
| `ueberschrift` | – (`text` darf HTML sein) | Textfeld/Hinweis zwischen den Fragen |
| `einfachauswahl` | `optionen` (Liste) | Multiple Choice, eine Antwort |
| `mehrfachauswahl` | `optionen` | Multiple Choice, mehrere Antworten |
| `auswahlliste` | `optionen` | Multiple Choice als Dropdown |
| `skala` | `optionen` (von niedrig nach hoch) | Multiple Choice (skaliert), Werte 1 bis n |
| `zahl` | `von`, `bis` | Numerische Antwort |
| `kurztext` | – | Eingabezeile |
| `langtext` | – | Eingabebereich |

Ein Kurs, der nur dieses Element enthält: [`beispiel.json`](beispiel.json).
