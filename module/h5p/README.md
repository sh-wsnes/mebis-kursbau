# H5P

Interaktive Übungen wie Lückentext, Multiple Choice oder Zuordnung. Die Lernplattform speichert den Inhalt einer H5P-Übung als Text zusammen mit dem Namen des Inhaltstyps; den Programmcode hat sie selbst. Deshalb kann die KI H5P-Übungen erzeugen, ohne Pakete zu bauen.

## So bestellst du es bei der KI

„Mach einen H5P-Lückentext zur Weimarer Republik mit fünf Lücken.“

## Das geht

- **Lückentext** (`H5P.Blanks 1.14`): in der Lernplattform bestätigt. Lücken werden im Text mit Sternchen markiert: `Die Hauptstadt ist *Berlin*.` Mehrere richtige Antworten mit `/`: `*Berlin/berlin*`, Tipp mit `:`: `*Berlin:Beginnt mit B*`.
- Grundsätzlich jeder Inhaltstyp, dessen Name und Version die Lernplattform kennt. Die Felder des Inhalts (`inhalt`) richten sich nach dem Inhaltstyp; die KI kennt die gängigen Typen aus deren Beschreibung auf GitHub (`semantics.json`).
- Bilder im Inhalt (Feld `dateien`, Pfad im Inhalt dann `images/NAME`)

## Das geht noch nicht

- Inhaltstypen, deren Versionsnummer auf der Lernplattform nicht bekannt ist. Die Nummer steht in einer Kurssicherung, die eine solche Übung enthält. Bisher bekannt: `H5P.Blanks 1.14`.
- Zusammengesetzte Typen wie Course Presentation oder Interactive Video: möglich, aber aufwendig und ungetestet.

## Getestet

Am 15.11.2026 in der ByCS-Lernplattform (Moodle 5.2.4) wiederhergestellt und geprüft.

## Für die KI

`typ`: `h5p`

| Feld | Pflicht/Wahl | Bedeutung |
|---|---|---|
| `name` | Pflicht | Name auf der Kursseite |
| `bibliothek` | Pflicht | Inhaltstyp mit Version, z. B. `H5P.Blanks 1.14` |
| `inhalt` | Pflicht | die H5P-Parameter als Objekt, Aufbau wie `content.json` des Inhaltstyps |
| `beschreibung` | Wahl | HTML |
| `punkte` | Wahl | Höchstpunktzahl, Standard 10 |
| `dateien` | Wahl | Liste von Dateipfaden; sie landen im Ordner `images/` und werden im Inhalt als `images/NAME` angesprochen |

Verwende nur Bibliotheksversionen, die in dieser Datei als bekannt aufgeführt sind, oder solche aus einer Kurssicherung der Lehrkraft. Eine geratene Version führt zu einer kaputten Aktivität. Setze im Inhalt deutsche Beschriftungen für Buttons und Rückmeldungen, sonst erscheinen englische Standardtexte.

Ein Kurs, der nur dieses Element enthält: [`beispiel.json`](beispiel.json).
