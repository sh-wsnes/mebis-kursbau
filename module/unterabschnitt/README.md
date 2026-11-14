# Unterabschnitt

Ein aufklappbarer Bereich innerhalb eines Abschnitts, der eigene Inhalte bündelt. Geeignet für Zusatzmaterial oder für Stationen innerhalb einer Stunde.

## So bestellst du es bei der KI

„Pack das Zusatzmaterial im Abschnitt ‚Aufgaben‘ in einen Unterabschnitt.“

## Das geht

- alle anderen Module als Inhalt

## Das geht noch nicht

- Unterabschnitte in Unterabschnitten

## Getestet

Am 14.11.2026 mit dem Testkurs (`beispiele/testkurs.json`) erzeugt, in der ByCS-Lernplattform (Moodle 5.2.4) wiederhergestellt und geprüft. Einstellungen, die der Testkurs nicht verwendet, sind ungeprüft.

## Für die KI

`typ`: `unterabschnitt`

| Feld | Pflicht/Wahl | Bedeutung |
|---|---|---|
| `name` | Pflicht | Name des Unterabschnitts |
| `inhalte` | Wahl | Liste von Inhalten wie in einem Abschnitt |

Ein Kurs, der nur dieses Element enthält: [`beispiel.json`](beispiel.json).
