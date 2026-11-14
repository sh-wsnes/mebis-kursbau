# Kanban-Board

Eine Aufgabentafel nach der Kanban-Methode: Karten wandern durch Spalten wie „Zu erledigen“, „In Arbeit“, „Fertig“. Geeignet für Projektarbeit in Gruppen.

## So bestellst du es bei der KI

„Leg ein Kanban-Board ‚Projekt Zeitung‘ an.“

## Das geht

- Name und Beschreibung
- eigene Tafeln je Schüler zusätzlich oder ausschließlich

## Das geht noch nicht

- eigene Spaltennamen: Die Lernplattform legt die Spalten erst beim ersten Öffnen mit Standardnamen an; die Lehrkraft benennt sie danach um
- Karten vorab anlegen

## Getestet

Am 14.11.2026 in der ByCS-Lernplattform (Moodle 5.2.4) wiederhergestellt und geprüft.

## Für die KI

`typ`: `kanban`

| Feld | Pflicht/Wahl | Bedeutung |
|---|---|---|
| `name` | Pflicht | Name auf der Kursseite |
| `beschreibung` | Wahl | HTML |
| `eigene_tafeln` | Wahl | `keine` (Standard, eine gemeinsame Tafel), `zusaetzlich` oder `nur` |

Ein Kurs, der nur dieses Element enthält: [`beispiel.json`](beispiel.json).
