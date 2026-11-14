# Datei

Eine einzelne Datei zum Herunterladen oder Ansehen, zum Beispiel ein Arbeitsblatt als PDF.

## So bestellst du es bei der KI

„Leg das Arbeitsblatt als PDF in den Abschnitt ‚Material‘.“ Dazu die Datei im Chat hochladen oder ihren Speicherort nennen.

## Das geht

- jede Dateiart (PDF, Bild, Word, Audio …)
- eine Beschreibung unter dem Namen
- Anzeige in neuem Fenster (Standard), eingebettet in die Kursseite oder nur als Download

## Das geht noch nicht

- mehrere Dateien in einem Element (dafür gibt es das Verzeichnis)

## Getestet

Am 14.11.2026 in der ByCS-Lernplattform (Moodle 5.2.4) wiederhergestellt und geprüft.

## Für die KI

`typ`: `datei`

| Feld | Pflicht/Wahl | Bedeutung |
|---|---|---|
| `name` | Pflicht | Name auf der Kursseite |
| `datei` | Pflicht | Pfad zur Datei, bezogen auf den Ordner der Kursbeschreibung |
| `beschreibung` | Wahl | HTML |
| `anzeige` | Wahl | `neues_fenster` (Standard), `einbetten` (in der Kursseite mit Navigation), `erzwingen` (Download) oder `automatisch` |

Ein Kurs, der nur dieses Element enthält: [`beispiel.json`](beispiel.json).
