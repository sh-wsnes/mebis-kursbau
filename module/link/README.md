# Link

Ein Eintrag auf der Kursseite, der eine Internetseite öffnet.

## So bestellst du es bei der KI

„Füg einen Link zur Schulhomepage ein.“

## Das geht

- Öffnen in einem neuen Fenster (Standard) oder im selben Fenster
- eine kurze Beschreibung unter dem Namen

## Das geht noch nicht

- Adressen ohne `https://`

## Getestet

Am 14.11.2026 mit dem Testkurs (`beispiele/testkurs.json`) erzeugt, in der ByCS-Lernplattform (Moodle 5.2.4) wiederhergestellt und geprüft. Einstellungen, die der Testkurs nicht verwendet, sind ungeprüft.

## Für die KI

`typ`: `link`

| Feld | Pflicht/Wahl | Bedeutung |
|---|---|---|
| `name` | Pflicht | Name des Links auf der Kursseite |
| `url` | Pflicht | Adresse, muss mit `https://` beginnen |
| `beschreibung` | Wahl | kurze Beschreibung als HTML |
| `neues_fenster` | Wahl | `true` (Standard) oder `false` |

Ein Kurs, der nur dieses Element enthält: [`beispiel.json`](beispiel.json).
