# Aufgabe

Schülerinnen und Schüler geben eine Arbeit ab, als Datei oder als Text direkt in der Lernplattform. Die Lehrkraft kann bewerten und Rückmeldung geben.

## So bestellst du es bei der KI

„Leg eine Aufgabe an: Fasse den Text in drei Sätzen zusammen. Abgabe als Text, 10 Punkte.“

## Das geht

- Aufgabenstellung, die sichtbar auf der Aufgabenseite steht
- ein zusätzlicher Hinweis, der erst beim Abgeben erscheint
- Abgabe als Datei, als Text oder beides
- Höchstpunktzahl

## Das geht noch nicht

- Abgabetermine und Fristen
- Gruppenabgaben
- Bewertungsraster (Rubrics)
- Dateien als Anhang zur Aufgabenstellung

## Getestet

Am 14.11.2026 mit dem Testkurs (`beispiele/testkurs.json`) erzeugt, in der ByCS-Lernplattform (Moodle 5.2.4) wiederhergestellt und geprüft. Einstellungen, die der Testkurs nicht verwendet, sind ungeprüft.

## Für die KI

`typ`: `aufgabe`

| Feld | Pflicht/Wahl | Bedeutung |
|---|---|---|
| `name` | Pflicht | Name der Aufgabe |
| `aufgabenstellung` | Pflicht | Aufgabentext als HTML, steht sichtbar auf der Aufgabenseite |
| `abgabehinweis` | Wahl | HTML, erscheint erst beim Abgeben |
| `abgabe` | Wahl | `datei` (Standard), `text` oder `beides` |
| `punkte` | Wahl | Höchstpunktzahl, Standard 100 |

Termine stellt die Lehrkraft nach dem Wiederherstellen in den Einstellungen der Aufgabe ein.

Ein Kurs, der nur dieses Element enthält: [`beispiel.json`](beispiel.json).
