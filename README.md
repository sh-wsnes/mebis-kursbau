# mebis-kursbau

Kurse für die ByCS-Lernplattform (mebis) mit Hilfe einer KI bauen: Du beschreibst den Kurs in normalen Worten, die KI erzeugt eine Sicherungsdatei, und du spielst sie in der Lernplattform ein.

Hintergrund: Für die Lernplattform gibt es keine Schnittstelle (MCP), über die eine KI direkt Kurse anlegen könnte. Dieses Repo geht deshalb den Weg über die Kurssicherung.

> **Hinweis für KI-Assistenten:** Lies zuerst [`CLAUDE.md`](CLAUDE.md). Dort steht, welche Datei die Lehrkraft bekommt (`.mbz` oder `.h5p`) und was zu tun ist, wenn du das Skript nicht ausführen kannst.

## So geht es

1. **Kurs beschreiben.** Öffne eine KI, die auf dieses Repo zugreifen und Programme ausführen kann (z. B. Claude), nenne ihr dieses Repo und beschreibe deinen Kurs: Titel, Abschnitte und was in jedem Abschnitt stehen soll.
2. **Datei erhalten.** Die KI gibt dir eine Datei mit der Endung `.mbz`. Willst du nur H5P-Übungen, fragt sie dich, ob du lieber eine `.mbz` oder eine `.h5p` möchtest. Die `.h5p` lädst du im Inhaltsspeicher hoch.
3. **Leeren Kurs anlegen.** Lege in der Lernplattform einen neuen, leeren Kurs an. So bleibt ein bestehender Kurs unberührt.
4. **Wiederherstellen.** Öffne im neuen Kurs die Funktion „Wiederherstellen“ (im Kursmenü unter „Mehr“ → „Kurs wiederverwenden“), lade die Datei hoch und folge den Schritten.
5. **Nacharbeiten.** Termine, Gruppen und Abschlussbedingungen stellst du danach wie gewohnt in der Lernplattform ein.

Ein Beispiel für eine Beschreibung:

> Bau mir einen Kurs „Weimarer Republik“ mit zwei Abschnitten. Im ersten eine Textseite mit einer Einführung und ein Link zur Schulhomepage. Im zweiten eine Aufgabe „Fasse die Einführung in drei Sätzen zusammen“ mit Textabgabe und eine Checkliste mit drei Punkten.

## Was die KI bauen kann

Abschnitte mit Namen und Beschreibung, dazu diese Elemente:

| Element | Wofür |
|---|---|
| [Text- und Medienfeld](module/textfeld/README.md) | Ein Text, der direkt auf der Kursseite steht, ohne dass man etwas anklicken muss. |
| [Textseite](module/textseite/README.md) | Eine eigene Seite mit Text, die über einen Eintrag auf der Kursseite geöffnet wird. |
| [Link](module/link/README.md) | Ein Eintrag auf der Kursseite, der eine Internetseite öffnet. |
| [Aufgabe](module/aufgabe/README.md) | Schülerinnen und Schüler geben eine Arbeit ab, als Datei oder als Text direkt in der Lernplattform. |
| [Abstimmung](module/abstimmung/README.md) | Eine einzelne Frage mit vorgegebenen Antworten, aus denen die Klasse auswählt. |
| [Checkliste](module/checkliste/README.md) | Eine Liste von Punkten zum Abhaken. |
| [Buch](module/buch/README.md) | Mehrere Seiten mit Kapiteln und Inhaltsverzeichnis. |
| [Board](module/board/README.md) | Pinnwand mit Spalten für Beiträge der Klasse. |
| [Kanban-Board](module/kanban/README.md) | Aufgabentafel für Projektarbeit. |
| [Tagebuch](module/tagebuch/README.md) | Persönlicher Text je Schüler, nur für die Lehrkraft sichtbar. |
| [Feedback](module/feedback/README.md) | Umfrage mit mehreren Fragen, auf Wunsch anonym. |
| [H5P](module/h5p/README.md) | Interaktive Übungen, bisher Lückentext. |
| [Datei](module/datei/README.md) | Eine einzelne Datei zum Herunterladen, z. B. ein Arbeitsblatt. |
| [Verzeichnis](module/verzeichnis/README.md) | Ein Ordner mit mehreren Dateien, auf Wunsch mit Unterordnern. |
| [Unterabschnitt](module/unterabschnitt/README.md) | Ein aufklappbarer Bereich innerhalb eines Abschnitts, der eigene Inhalte bündelt. |

Jede Seite beschreibt, was geht, was noch nicht geht und wann das Element zuletzt getestet wurde.

## Was noch fehlt

- Test und die übrigen Aktivitäten der Lernplattform
- weitere H5P-Inhaltstypen, die nicht in der Tabelle der H5P-Seite stehen (je ein Muster aus der Lernplattform nötig)
- Glossar mit Einträgen: Moodle behandelt Einträge als Nutzerdaten, die auf diesem Weg nicht mitkommen

## Stand

Alle Elemente wurden am 14.11.2026 bzw. 15.11.2026 mit einem Testkurs erzeugt, in der ByCS-Lernplattform (Moodle 5.2.4) wiederhergestellt und geprüft. Nicht jede einzelne Einstellung war Teil des Tests; die Modulseiten nennen die Grenzen. Nach einem Update der Lernplattform kann sich das ändern. Deshalb: neue Kurse immer zuerst in einen leeren Kurs einspielen.

## Für Technikinteressierte

- `kursbau.py` – das Skript, braucht nur Python 3: `python3 kursbau.py beispiele/testkurs.json`
- `CLAUDE.md` – Anleitung für die KI
- `module/` – Beschreibung und Einzelbeispiel je Element
- `beispiele/testkurs.json` – ein Kurs mit allen Elementen
- `doku/sicherungsformat.md` – Aufbau einer Kurssicherung

Lizenz: MIT, siehe `LICENSE`. Nutzung ohne Gewähr.
