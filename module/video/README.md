# Video

Ein Video wird in der Lernplattform nicht als eigenes Element angelegt, sondern in ein Text- und Medienfeld oder in eine Textseite eingebettet. Diese Seite sagt, wie das ohne Doppelanzeige klappt.

## So bestellst du es bei der KI

„Setz in den zweiten Abschnitt ein Textfeld mit diesem YouTube-Video: (Adresse). Schreib darunter als Quelle: Titel, Kanal.“

## Das geht

- **Eingebettetes Video** in einem Textfeld oder einer Textseite, mit `iframe` und der Adresse `https://www.youtube-nocookie.com/embed/VIDEO-ID`. Das Video erscheint einmal.
- Die **Quelle** als reiner Text darunter, zum Beispiel: „Video: Titel (Kanal, YouTube), Ausschnitt 1:05 bis 2:09“.

Vorlage:

```html
<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/VIDEO-ID" title="Titel des Videos" frameborder="0" allowfullscreen></iframe>
<p>Video: Titel (Kanal, YouTube)</p>
```

## Wichtig: kein YouTube-Link neben dem Video

Die Lernplattform wandelt YouTube-Links in Texten automatisch in einen Videoplayer um. Steht neben dem eingebetteten Video noch ein Link auf `youtube.com/watch…` oder `youtu.be/…`, erscheint das Video **zweimal**, und der Link selbst ist nicht mehr zu sehen. Das gilt im Textfeld und in der Textseite. Die Quelle deshalb ohne Link und ohne Adresse schreiben. Die Klasse `nomediaplugin` am Link hilft nach Auskunft einer anderen KI in ByCS nicht; das haben wir nicht selbst geprüft.

`kursbau.py` gibt eine Warnung aus, wenn ein Inhalt beides enthält.

## Das geht noch nicht

- Hochgeladene Videodateien und Videos aus dem Medienspeicher von mebis: nicht untersucht, dafür braucht es ein Muster aus der Lernplattform.
- Andere Anbieter als YouTube: nicht getestet.

## Ungeklärt

Ein YouTube-Link allein (ohne `iframe`) wird zu einem Player. Ob dieser Player die datenschutzfreundliche Adresse `youtube-nocookie.com` nutzt, wissen wir nicht. Deshalb ist das `iframe` mit `youtube-nocookie.com` der empfohlene Weg.

## Getestet

Am 26.11.2026 mit einem Testkurs in der ByCS-Lernplattform (Moodle 5.2.4) geprüft: nur `iframe` ergibt ein Video, `iframe` plus Link ergibt zwei Videos (Textfeld und Textseite), nur ein Link ergibt ein Video.

## Für die KI

Kein eigener `typ`. Verwende `textfeld` oder `textseite` und setze die Vorlage oben in `html` ein. Schreibe niemals einen Link auf `youtube.com/watch…` oder `youtu.be/…` in denselben Inhalt wie das `iframe`. Schreibe die Quelle als reinen Text. Die `VIDEO-ID` ist der Teil nach `v=` im normalen YouTube-Link.
