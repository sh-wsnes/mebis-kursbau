# Anleitung für die KI: Kurse für die ByCS-Lernplattform bauen

Dieses Repo erzeugt Kurssicherungen (`.mbz`) für die ByCS-Lernplattform (mebis, Moodle 5.2). Die Lehrkraft beschreibt einen Kurs, du schreibst daraus eine Kursbeschreibung als JSON und lässt `kursbau.py` die Sicherung erzeugen. Die Lehrkraft spielt die Datei in der Lernplattform über **Wiederherstellen** ein.

## Arbeitsweise

1. Kläre Titel, Kurzname und die Abschnitte mit ihren Inhalten. Frage nur nach, wenn eine Pflichtangabe fehlt.
2. Schreibe die Kursbeschreibung als JSON-Datei (Aufbau siehe unten, Muster mit allen Elementen in `beispiele/testkurs.json`, Einzelbeispiele in `module/`).
3. Führe aus: `python3 kursbau.py kurs.json`. Das Skript braucht nur Python 3. Bei einer Fehlermeldung die JSON-Datei korrigieren, nicht das Skript.
4. Gib der Lehrkraft die erzeugte `.mbz`-Datei und nenne den Einspielweg: in der Lernplattform einen leeren Kurs öffnen → **Mehr > Kurs wiederverwenden > Wiederherstellen** → Datei hochladen → den Schritten folgen.
5. Die Lehrkraft programmiert nicht. Erkläre nichts über JSON oder XML, wenn sie nicht danach fragt.

## Aufbau der Kursbeschreibung

```json
{
  "titel": "Voller Kursname",
  "kurzname": "kurzname",
  "allgemein": [ …Inhalte für den obersten Abschnitt ohne Überschrift… ],
  "abschnitte": [
    { "name": "Abschnittsname", "beschreibung": "<p>optional</p>", "inhalte": [ … ] }
  ]
}
```

`titel`, `kurzname` und mindestens ein Abschnitt mit `name` sind Pflicht. `allgemein`, `beschreibung` und `inhalte` dürfen fehlen. Das Kursformat ist das Themenformat (`topics`).

## Inhalte

Jeder Inhalt hat ein Feld `typ`. Die Felder jedes Typs stehen in der Beschreibung des Moduls. Lies vor dem Schreiben der Kursbeschreibung die Seiten der Module, die der Kurs braucht.

| `typ` | Element in der Lernplattform | Felder und Grenzen |
|---|---|---|
| `textfeld` | Text- und Medienfeld | [`module/textfeld/README.md`](module/textfeld/README.md) |
| `textseite` | Textseite | [`module/textseite/README.md`](module/textseite/README.md) |
| `link` | Link | [`module/link/README.md`](module/link/README.md) |
| `aufgabe` | Aufgabe | [`module/aufgabe/README.md`](module/aufgabe/README.md) |
| `abstimmung` | Abstimmung | [`module/abstimmung/README.md`](module/abstimmung/README.md) |
| `checkliste` | Checkliste | [`module/checkliste/README.md`](module/checkliste/README.md) |
| `buch` | Buch | [`module/buch/README.md`](module/buch/README.md) |
| `board` | Board (Pinnwand) | [`module/board/README.md`](module/board/README.md) |
| `kanban` | Kanban-Board | [`module/kanban/README.md`](module/kanban/README.md) |
| `tagebuch` | Tagebuch (Journal) | [`module/tagebuch/README.md`](module/tagebuch/README.md) |
| `datei` | Datei | [`module/datei/README.md`](module/datei/README.md) |
| `verzeichnis` | Verzeichnis | [`module/verzeichnis/README.md`](module/verzeichnis/README.md) |
| `unterabschnitt` | Unterabschnitt | [`module/unterabschnitt/README.md`](module/unterabschnitt/README.md) |

Felder mit HTML enthalten den Code so, wie er im Editor der Lernplattform unter „Quellcode“ stünde.

## HTML in Textfeldern und Textseiten

- Die mebis-eigenen Kästen funktionieren, z. B. `<div class="elements-boxes elements-boxes-tip elements-justboxes1-flavor " data-box-name="TIP"><p>Text</p></div>`.
- Bausteine mit Inline-Styles (Infokasten, Button usw.) aus dem Repo `sh-wsnes/test-mebis` können unverändert als `html` eingesetzt werden.
- Hochgeladene Bilder: Datei im Feld `dateien` nennen und im HTML mit `<img src="@@PLUGINFILE@@/DATEINAME">` einbinden. Bilder aus dem Internet gehen weiterhin über ihre `https://`-Adresse.

## Dateien

Dateipfade in der Kursbeschreibung sind relativ zum Ordner, in dem die JSON-Datei liegt. Lege die Dateien, die die Lehrkraft hochgeladen hat, neben die JSON-Datei (z. B. in einen Unterordner `dateien/`) und nenne sie mit diesem Pfad. Das Skript packt sie in die Sicherung. Fehlt eine Datei, bricht es mit einer Fehlermeldung ab.

## Grenzen

- Nicht unterstützt: Test, H5P, Forum und alle übrigen Aktivitäten. Sag das der Lehrkraft, statt etwas Ähnliches zu erfinden.
- Glossar: Einträge zählen in Moodle als Nutzerdaten und lassen sich über eine Sicherung ohne Nutzerdaten nicht übertragen. Ein Glossar kann deshalb nicht mit Inhalt erzeugt werden; die Lehrkraft legt es in der Lernplattform an.
- Termine, Gruppen, Abschlussbedingungen und Voraussetzungen setzt das Skript nicht. Die Lehrkraft stellt sie nach dem Wiederherstellen ein.

## Neue Aktivitätstypen ergänzen

Grundlage ist immer eine echte Sicherung aus der Lernplattform, die die Aktivität mit Inhalt enthält. Die XML-Struktur daraus in `kursbau.py` als weiteren Typ nachbauen, dann einen Testkurs erzeugen und die Struktur der erzeugten Dateien mit dem Original vergleichen. Lege für den Typ ein Verzeichnis `module/NAME/` mit `README.md` (Aufbau wie bei den vorhandenen Modulen) und `beispiel.json` an. Erst nach einer erfolgreichen Wiederherstellung in der Lernplattform das Testdatum eintragen und den Typ in die Tabelle oben sowie in die `README.md` des Repos aufnehmen. Details zum Dateiformat stehen in `doku/sicherungsformat.md`.
