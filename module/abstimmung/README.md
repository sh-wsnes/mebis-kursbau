# Abstimmung

Eine einzelne Frage mit vorgegebenen Antworten, aus denen die Klasse auswählt. Geeignet für Stimmungsbilder, Themenwahl und schnelle Rückmeldungen.

## So bestellst du es bei der KI

„Mach eine Abstimmung: Wie schwer war die Aufgabe? Leicht, mittel, schwer.“

## Das geht

- beliebig viele Antwortmöglichkeiten (mindestens zwei)
- Einfach- oder Mehrfachauswahl

## Das geht noch nicht

- Begrenzung der Stimmen je Antwort
- Zeitfenster
- Veröffentlichung der Ergebnisse für die Klasse (nach dem Wiederherstellen einstellbar)

## Getestet

Am 14.11.2026 mit dem Testkurs (`beispiele/testkurs.json`) erzeugt, in der ByCS-Lernplattform (Moodle 5.2.4) wiederhergestellt und geprüft. Einstellungen, die der Testkurs nicht verwendet, sind ungeprüft.

## Für die KI

`typ`: `abstimmung`

| Feld | Pflicht/Wahl | Bedeutung |
|---|---|---|
| `name` | Pflicht | Name der Abstimmung |
| `frage` | Pflicht | Frage als HTML |
| `optionen` | Pflicht | Liste der Antworten, mindestens zwei |
| `mehrfachauswahl` | Wahl | `true` oder `false` (Standard) |

Ein Kurs, der nur dieses Element enthält: [`beispiel.json`](beispiel.json).
