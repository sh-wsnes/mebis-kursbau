# Text- und Medienfeld

Ein Text, der direkt auf der Kursseite steht, ohne dass man etwas anklicken muss. Geeignet für Überschriften, Hinweise, Arbeitsaufträge in einem Satz und gestaltete Kästen.

## So bestellst du es bei der KI

„Setz in den ersten Abschnitt ein Textfeld mit einem Tipp-Kasten: Lest zuerst die Einführung.“

## Das geht

- Text mit Formatierung, Listen, Tabellen, Emojis
- die Kästen der Lernplattform (Tipp, Hinweis usw.)
- gestaltete Bausteine aus dem Repo `sh-wsnes/test-mebis` (Infokasten, Button)
- Bilder, die über eine Internetadresse (`https://`) erreichbar sind
- hochgeladene Bilder (Datei mitgeben, siehe unten)

## Das geht noch nicht


## Getestet

Hochgeladene Dateien: noch nicht in der Lernplattform getestet. Alles andere: am 14.11.2026 mit dem Testkurs (`beispiele/testkurs.json`) erzeugt, in der ByCS-Lernplattform (Moodle 5.2.4) wiederhergestellt und geprüft. Einstellungen, die der Testkurs nicht verwendet, sind ungeprüft.

## Für die KI

`typ`: `textfeld`

| Feld | Pflicht/Wahl | Bedeutung |
|---|---|---|
| `html` | Pflicht | Inhalt als HTML, so wie er im Editor unter „Quellcode“ stünde |

Der Name des Textfelds entsteht automatisch aus den ersten 50 Zeichen des Textes.
| `dateien` | Wahl | Liste von Dateipfaden (Bilder), bezogen auf den Ordner der Kursbeschreibung |

Hochgeladene Bilder: Datei in `dateien` nennen und im HTML mit `<img src="@@PLUGINFILE@@/DATEINAME">` einbinden. Die Lernplattform ersetzt `@@PLUGINFILE@@` beim Wiederherstellen durch die richtige Adresse.

Ein Kurs, der nur dieses Element enthält: [`beispiel.json`](beispiel.json).
