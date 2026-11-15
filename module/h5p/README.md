# H5P

Interaktive Übungen wie Lückentext, Multiple Choice oder Zuordnung. Die Lernplattform speichert den Inhalt einer H5P-Übung als Text zusammen mit dem Namen des Inhaltstyps; den Programmcode hat sie selbst. Deshalb kann die KI H5P-Übungen erzeugen, ohne Pakete zu bauen.

## So bestellst du es bei der KI

„Mach einen H5P-Lückentext zur Weimarer Republik mit fünf Lücken.“

## Das geht

Diese Inhaltstypen kennt die Lernplattform mit genau diesen Versionsnummern (aus einer Sicherung der Lernplattform). Zu jedem liegt ein fertiges deutsches Muster im Ordner [`muster/`](muster/); die KI nimmt es als Vorlage und ersetzt nur die Inhalte.

| Inhaltstyp | `bibliothek` | Muster | Bilder nötig | Stand |
|---|---|---|---|---|
| Lückentext | `H5P.Blanks 1.14` | [`beispiel.json`](beispiel.json) | nein | getestet |
| Multiple Choice | `H5P.MultiChoice 1.16` | [`muster/H5P.MultiChoice.json`](muster/H5P.MultiChoice.json) | nein | noch nicht getestet |
| Drag the Words | `H5P.DragText 1.10` | [`muster/H5P.DragText.json`](muster/H5P.DragText.json) | nein | noch nicht getestet |
| Mark the Words | `H5P.MarkTheWords 1.11` | [`muster/H5P.MarkTheWords.json`](muster/H5P.MarkTheWords.json) | nein | noch nicht getestet |
| Find the Words | `H5P.FindTheWords 1.4` | [`muster/H5P.FindTheWords.json`](muster/H5P.FindTheWords.json) | nein | noch nicht getestet |
| Single Choice Set | `H5P.SingleChoiceSet 1.11` | [`muster/H5P.SingleChoiceSet.json`](muster/H5P.SingleChoiceSet.json) | nein | noch nicht getestet |
| Sort the Paragraphs | `H5P.SortParagraphs 0.11` | [`muster/H5P.SortParagraphs.json`](muster/H5P.SortParagraphs.json) | nein | noch nicht getestet |
| Quiz (Question Set) | `H5P.QuestionSet 1.21` | [`muster/H5P.QuestionSet.json`](muster/H5P.QuestionSet.json) | nein | noch nicht getestet |
| Drag and Drop | `H5P.DragQuestion 1.15` | [`muster/H5P.DragQuestion.json`](muster/H5P.DragQuestion.json) | nein (hier mit Text) | noch nicht getestet |
| Memory | `H5P.MemoryGame 1.3` | [`muster/H5P.MemoryGame.json`](muster/H5P.MemoryGame.json) | ja | noch nicht getestet |
| Image Pairing | `H5P.ImagePair 1.4` | [`muster/H5P.ImagePair.json`](muster/H5P.ImagePair.json) | ja | noch nicht getestet |
| Image Sequencing | `H5P.ImageSequencing 1.1` | [`muster/H5P.ImageSequencing.json`](muster/H5P.ImageSequencing.json) | ja | noch nicht getestet |

- Lücken im Lückentext werden mit Sternchen markiert: `Die Hauptstadt ist *Berlin*.` Mehrere richtige Antworten mit `/`: `*Berlin/berlin*`, Tipp mit `:`: `*Berlin:Beginnt mit B*`. Dasselbe gilt für Drag the Words und Mark the Words.
- Bilder im Inhalt: Datei im Feld `dateien` nennen, im Inhalt steht dann `images/NAME`. Die Muster zeigen, wie.

## Das geht noch nicht

- Inhaltstypen, deren Versionsnummer auf der Lernplattform nicht bekannt ist. Die Nummer steht in einer Kurssicherung, die eine solche Übung enthält. Bekannt sind die Typen aus der Tabelle oben. Noch ohne Muster aus der Lernplattform: Wahr/Falsch (True/False), Dialog Cards, Flashcards, Image Hotspots, Fill in the Blanks mit Bild u. a.
- Zusammengesetzte Typen wie Course Presentation oder Interactive Video: möglich, aber aufwendig und ungetestet.

## Getestet

Lückentext: am 15.11.2026 in der ByCS-Lernplattform (Moodle 5.2.4) wiederhergestellt und geprüft. Die übrigen Typen sind eingebaut, aber noch nicht in der Lernplattform geprüft.

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

Verwende nur Bibliotheksversionen aus der Tabelle oben oder aus einer Kurssicherung der Lehrkraft. Eine geratene Version führt zu einer kaputten Aktivität. Gehe vom Muster des Inhaltstyps aus (Ordner `muster/`) und ändere nur Inhalte; alle Beschriftungen bleiben deutsch.

Ein Kurs, der nur dieses Element enthält: [`beispiel.json`](beispiel.json).
