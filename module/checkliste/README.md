# Checkliste

Eine Liste von Punkten zum Abhaken. Schülerinnen und Schüler sehen ihren Fortschritt, die Lehrkraft sieht ihn für die ganze Klasse.

## So bestellst du es bei der KI

„Erstell eine Checkliste ‚Bin ich fertig?‘ mit den Punkten: Text gelesen, Zusammenfassung abgegeben, Zusatzmaterial bearbeitet (freiwillig).“

## Das geht

- beliebig viele Punkte
- Punkte mit Link zu einer Internetseite
- freiwillige Punkte
- eingerückte Unterpunkte
- Schüler dürfen eigene Punkte ergänzen (Standard) oder nicht

## Das geht noch nicht

- Termine an einzelnen Punkten
- automatisches Abhaken, sobald eine Kursaktivität erledigt ist

## Getestet

Am 14.11.2026 mit dem Testkurs (`beispiele/testkurs.json`) erzeugt, in der ByCS-Lernplattform (Moodle 5.2.4) wiederhergestellt und geprüft. Einstellungen, die der Testkurs nicht verwendet, sind ungeprüft.

## Für die KI

`typ`: `checkliste`

| Feld | Pflicht/Wahl | Bedeutung |
|---|---|---|
| `name` | Pflicht | Name der Checkliste |
| `eintraege` | Pflicht | Liste der Punkte, siehe unten |
| `beschreibung` | Wahl | Einleitung als HTML |
| `eigene_eintraege` | Wahl | `true` (Standard) oder `false` |

Ein Eintrag ist entweder ein Text (`"Text gelesen"`) oder ein Objekt mit `text` und den Wahlfeldern `link` (nur `https://`), `optional` (`true` für freiwillige Punkte) und `einrueckung` (0 oder höher).

Ein Kurs, der nur dieses Element enthält: [`beispiel.json`](beispiel.json).
