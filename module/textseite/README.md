# Textseite

Eine eigene Seite mit Text, die über einen Eintrag auf der Kursseite geöffnet wird. Geeignet für längere Inhalte wie Infotexte oder Arbeitsblätter zum Lesen.

## So bestellst du es bei der KI

„Leg eine Textseite ‚Einführung‘ an mit einem kurzen Infotext zur Weimarer Republik.“

## Das geht

- alles, was auch im Text- und Medienfeld geht
- eine kurze Beschreibung, die auf der Kursseite unter dem Namen steht
- hochgeladene Bilder (Datei mitgeben, siehe unten)

## Das geht noch nicht


## Getestet

Am 14.11.2026, einschließlich hochgeladener Dateien, mit dem Testkurs (`beispiele/testkurs.json`) erzeugt, in der ByCS-Lernplattform (Moodle 5.2.4) wiederhergestellt und geprüft. Einstellungen, die der Testkurs nicht verwendet, sind ungeprüft.

## Für die KI

`typ`: `textseite`

| Feld | Pflicht/Wahl | Bedeutung |
|---|---|---|
| `name` | Pflicht | Name der Seite auf der Kursseite |
| `html` | Pflicht | Inhalt der Seite als HTML |
| `beschreibung` | Wahl | kurze Beschreibung als HTML |
| `dateien` | Wahl | Liste von Dateipfaden (Bilder), bezogen auf den Ordner der Kursbeschreibung |

Hochgeladene Bilder: Datei in `dateien` nennen und im HTML mit `<img src="@@PLUGINFILE@@/DATEINAME">` einbinden. Die Lernplattform ersetzt `@@PLUGINFILE@@` beim Wiederherstellen durch die richtige Adresse.

Ein Kurs, der nur dieses Element enthält: [`beispiel.json`](beispiel.json).
