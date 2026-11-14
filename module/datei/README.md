# Datei

Eine einzelne Datei zum Herunterladen oder Ansehen, zum Beispiel ein Arbeitsblatt als PDF.

## So bestellst du es bei der KI

„Leg das Arbeitsblatt als PDF in den Abschnitt ‚Material‘.“ Dazu die Datei im Chat hochladen oder ihren Speicherort nennen.

## Das geht

- jede Dateiart (PDF, Bild, Word, Audio …)
- eine Beschreibung unter dem Namen
- Anzeige automatisch, eingebettet, in neuem Fenster oder nur als Download

## Das geht noch nicht

- mehrere Dateien in einem Element (dafür gibt es das Verzeichnis)

## Getestet

Noch nicht in der Lernplattform getestet.

## Für die KI

`typ`: `datei`

| Feld | Pflicht/Wahl | Bedeutung |
|---|---|---|
| `name` | Pflicht | Name auf der Kursseite |
| `datei` | Pflicht | Pfad zur Datei, bezogen auf den Ordner der Kursbeschreibung |
| `beschreibung` | Wahl | HTML |
| `anzeige` | Wahl | `automatisch` (Standard), `einbetten`, `neues_fenster` oder `erzwingen` (Download) |

Ein Kurs, der nur dieses Element enthält: [`beispiel.json`](beispiel.json).
