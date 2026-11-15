# Aufbau einer Kurssicherung der ByCS-Lernplattform

Stand: Mustersicherung vom 14.11.2026, Moodle 5.2.4 (Build 20261005), Sicherungsversion 5.2, Kursformat `topics`.

Eine `.mbz`-Datei ist ein gzip-komprimiertes tar-Archiv. Es beginnt mit der Datei `.ARCHIVE_INDEX` (Liste aller Einträge mit Größe und Zeitstempel), danach folgen Ordner und Dateien.

## Dateien

| Pfad | Inhalt |
|---|---|
| `moodle_backup.xml` | Inhaltsverzeichnis: Version, Kursdaten, Liste aller Aktivitäten und Abschnitte, Einstellungen der Sicherung |
| `course/course.xml` | Kursname, Format, Formatoptionen |
| `course/*.xml` | Einschreibemethoden, Rollen, Filter, Kalender (ohne Nutzerdaten fast leer) |
| `sections/section_ID/section.xml` | ein Abschnitt: Nummer, Name, Beschreibung, Reihenfolge der Aktivitäten (`sequence`) |
| `activities/TYP_ID/TYP.xml` | Inhalt der Aktivität |
| `activities/TYP_ID/module.xml` | Platzierung und Sichtbarkeit der Aktivität |
| `activities/TYP_ID/{inforef,grades,roles,filters,calendar,grade_history}.xml` | Verweise und Bewertung, meist leer |
| `files.xml`, `files/xx/HASH` | hochgeladene Dateien, abgelegt unter ihrer SHA1-Prüfsumme |
| `gradebook.xml`, `roles.xml`, `groups.xml`, `questions.xml`, … | Kursweite Daten |

## Regeln, die das Skript einhält

- Jede ID ist nur innerhalb der Sicherung von Bedeutung. Beim Wiederherstellen vergibt die Lernplattform neue IDs.
- Fehlende Werte stehen als `$@NULL@$`.
- HTML steht maskiert im XML (`&lt;p&gt;`).
- Abschnitt 0 ist der oberste Abschnitt ohne Namen.
- Ein Unterabschnitt besteht aus zwei Teilen: einer Aktivität `subsection` im Elternabschnitt und einem eigenen Abschnitt mit `component` = `mod_subsection` und `itemid` = ID der Aktivität. Diese Abschnitte tragen die Nummern nach den Hauptabschnitten. In `moodle_backup.xml` verweist `parentcmid` auf die Aktivität.
- Hochgeladene Dateien liegen unter `files/XX/PRÜFSUMME` (SHA1, XX = die ersten zwei Zeichen) und werden in `files.xml` beschrieben: Kontext der Aktivität, `component` (z. B. `mod_label`), `filearea` (`intro`, `content`, `introattachment`), Ordnerpfad und Name. Jeder Ordner bekommt zusätzlich einen Eintrag mit Dateiname `.` und der Prüfsumme der leeren Datei; diese liegt nicht im Archiv. Die Aktivität verweist in `inforef.xml` unter `fileref` auf ihre Dateien. Im HTML steht `@@PLUGINFILE@@/NAME` statt der Adresse.
- Eine Aufgabe braucht zusätzlich `grading.xml`, einen Bewertungsaspekt in `grades.xml` und den Verweis darauf in `inforef.xml`.
- Die Herkunft der Sicherung (`original_wwwroot`) ist absichtlich eine fremde Adresse. Die Lernplattform behandelt die Datei dann wie eine Sicherung von einer anderen Moodle-Instanz und übernimmt keine IDs.

- Glossareinträge gehören in Moodle zu den Nutzerdaten (`userinfo`). Eine Sicherung ohne Nutzerdaten enthält sie nicht, und eine Wiederherstellung überspringt sie. Das Glossar ist deshalb nicht umsetzbar.

## In der Mustersicherung enthalten, vom Skript noch nicht erzeugt

`aichat`, `data`, `feedback`, `glossary`, `learningmap`, `lightboxgallery`, `quiz`, `ratingallocate`, `unilabel`, `wiki`, `workshop`.

Die Mustersicherung selbst liegt nicht im Repo, weil sie Angaben zur Schule und zum Nutzerkonto enthält.
