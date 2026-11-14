# Anleitung für die KI: Kurse für die ByCS-Lernplattform bauen

Dieses Repo erzeugt Kurssicherungen (`.mbz`) für die ByCS-Lernplattform (mebis, Moodle 5.2). Die Lehrkraft beschreibt einen Kurs, du schreibst daraus eine Kursbeschreibung als JSON und lässt `kursbau.py` die Sicherung erzeugen. Die Lehrkraft spielt die Datei in der Lernplattform über **Wiederherstellen** ein.

## Arbeitsweise

1. Kläre Titel, Kurzname und die Abschnitte mit ihren Inhalten. Frage nur nach, wenn eine Pflichtangabe fehlt.
2. Schreibe die Kursbeschreibung als JSON-Datei (Aufbau siehe unten, Muster in `beispiele/testkurs.json`).
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

Jeder Inhalt hat ein Feld `typ`. Felder mit HTML enthalten den Code so, wie er im Editor der Lernplattform unter „Quellcode“ stünde.

| `typ` | Pflichtfelder | Wahlfelder | Ergebnis in der Lernplattform |
|---|---|---|---|
| `textfeld` | `html` | – | Text- und Medienfeld |
| `textseite` | `name`, `html` | `beschreibung` | Textseite |
| `link` | `name`, `url` (nur `https://`) | `beschreibung`, `neues_fenster` (Standard `true`) | Link/URL |
| `aufgabe` | `name`, `anweisungen` (HTML) | `beschreibung`, `abgabe` (`datei`, `text` oder `beides`; Standard `datei`), `punkte` (Standard 100) | Aufgabe |
| `abstimmung` | `name`, `frage` (HTML), `optionen` (Liste, mindestens zwei) | `mehrfachauswahl` (Standard `false`) | Abstimmung |
| `unterabschnitt` | `name` | `inhalte` (wie oben, aber keine weiteren Unterabschnitte) | Unterabschnitt |

## HTML in Textfeldern und Textseiten

- Die mebis-eigenen Kästen funktionieren, z. B. `<div class="elements-boxes elements-boxes-tip elements-justboxes1-flavor " data-box-name="TIP"><p>Text</p></div>`.
- Bausteine mit Inline-Styles (Infokasten, Button usw.) aus dem Repo `sh-wsnes/test-mebis` können unverändert als `html` eingesetzt werden.
- Bilder nur über eine `https://`-Adresse einbinden. Dateien in die Sicherung zu packen, kann das Skript noch nicht.

## Grenzen

- Nicht unterstützt: Dateien und Bilder als Upload, Test, H5P, Buch, Glossar, Forum und alle übrigen Aktivitäten. Sag das der Lehrkraft, statt etwas Ähnliches zu erfinden.
- Inhalte **in** Unterabschnitten sind aus der Mustersicherung nicht belegt (dort waren die Unterabschnitte leer) und gelten als ungetestet.
- Termine, Gruppen, Abschlussbedingungen und Voraussetzungen setzt das Skript nicht. Die Lehrkraft stellt sie nach dem Wiederherstellen ein.

## Neue Aktivitätstypen ergänzen

Grundlage ist immer eine echte Sicherung aus der Lernplattform, die die Aktivität mit Inhalt enthält. Die XML-Struktur daraus in `kursbau.py` als weiteren Typ nachbauen, dann einen Testkurs erzeugen und die Struktur der erzeugten Dateien mit dem Original vergleichen. Erst nach einer erfolgreichen Wiederherstellung in der Lernplattform in die Tabelle oben aufnehmen. Details zum Dateiformat stehen in `doku/sicherungsformat.md`.
