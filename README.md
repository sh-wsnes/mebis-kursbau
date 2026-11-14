# mebis-kursbau
Weil kein MCP besteht, sollen zum Kursbau auf der Lernplattform bycs hier die einzelnen Module so gesichert werden, dass eine KI darauf zugreifen kann. Die Module h5p sind noch nicht bearbeitet.

## Stand

`kursbau.py` erzeugt aus einer Kursbeschreibung eine Kurssicherung (`.mbz`), die in der Lernplattform über „Wiederherstellen“ eingespielt wird. Unterstützt sind bisher Abschnitte, Unterabschnitte, Text- und Medienfeld, Textseite, Link, Aufgabe, Abstimmung und Checkliste (Checkliste noch ungetestet).

Die Wiederherstellung eines erzeugten Testkurses in der Lernplattform hat am 14.11.2026 funktioniert, einschließlich Inhalten in Unterabschnitten.

## Benutzung

Die Arbeit übernimmt eine KI mit Zugriff auf dieses Repo. Ihre Anleitung steht in `CLAUDE.md`. Von Hand:

```
python3 kursbau.py beispiele/testkurs.json
```

## Inhalt

- `kursbau.py` – das Skript, braucht nur Python 3
- `beispiele/testkurs.json` – Muster einer Kursbeschreibung
- `CLAUDE.md` – Anleitung für die KI
- `doku/sicherungsformat.md` – Aufbau einer Kurssicherung

Vor dem Einsatz in echten Kursen in einem leeren Testkurs ausprobieren.
