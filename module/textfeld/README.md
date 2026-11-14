# Text- und Medienfeld

Ein Text, der direkt auf der Kursseite steht, ohne dass man etwas anklicken muss. Geeignet für Überschriften, Hinweise, Arbeitsaufträge in einem Satz und gestaltete Kästen.

## So bestellst du es bei der KI

„Setz in den ersten Abschnitt ein Textfeld mit einem Tipp-Kasten: Lest zuerst die Einführung.“

## Das geht

- Text mit Formatierung, Listen, Tabellen, Emojis
- die Kästen der Lernplattform (Tipp, Hinweis usw.)
- gestaltete Bausteine aus dem Repo `sh-wsnes/test-mebis` (Infokasten, Button)
- Bilder, die über eine Internetadresse (`https://`) erreichbar sind

## Das geht noch nicht

- hochgeladene Bilder und Dateien

## Getestet

Am 14.11.2026 mit dem Testkurs (`beispiele/testkurs.json`) erzeugt, in der ByCS-Lernplattform (Moodle 5.2.4) wiederhergestellt und geprüft. Einstellungen, die der Testkurs nicht verwendet, sind ungeprüft.

## Für die KI

`typ`: `textfeld`

| Feld | Pflicht/Wahl | Bedeutung |
|---|---|---|
| `html` | Pflicht | Inhalt als HTML, so wie er im Editor unter „Quellcode“ stünde |

Der Name des Textfelds entsteht automatisch aus den ersten 50 Zeichen des Textes.

Ein Kurs, der nur dieses Element enthält: [`beispiel.json`](beispiel.json).
