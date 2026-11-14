#!/usr/bin/env python3
"""kursbau.py - erzeugt aus einer Kursbeschreibung (JSON) eine Kurssicherung (.mbz)
für die ByCS-Lernplattform (Moodle 5.2).

Aufruf:   python3 kursbau.py kurs.json [ausgabe.mbz]

Das Format der Kursbeschreibung steht in CLAUDE.md. Das Skript braucht nur
Python 3, keine weiteren Pakete. Die XML-Vorlagen sind aus einer echten
Sicherung der ByCS-Lernplattform (Stand 14.11.2026) abgeleitet.
"""
import hashlib
import io
import json
import re
import sys
import tarfile
import time
from html import escape, unescape
from pathlib import Path

# Werte aus der Mustersicherung der ByCS-Lernplattform
MOODLE_VERSION = "2026042004"
MOODLE_RELEASE = "5.2.4 (Build: 20261005)"
BACKUP_VERSION = "2026042000"
BACKUP_RELEASE = "5.2"
MODULE_VERSION = "2026042000"
MAXBYTES = "524288000"
NULL = "$@NULL@$"
XML = '<?xml version="1.0" encoding="UTF-8"?>\n'

ROOT_SETTINGS = [
    ("users", 0), ("anonymize", 0), ("role_assignments", 0), ("activities", 1),
    ("blocks", 1), ("files", 1), ("filters", 1), ("comments", 0), ("badges", 1),
    ("calendarevents", 1), ("userscompletion", 0), ("logs", 0),
    ("grade_histories", 0), ("groups", 1), ("competencies", 0), ("customfield", 1),
    ("contentbankcontent", 1), ("xapistate", 0), ("legacyfiles", 1),
]

TYPEN = {
    "textfeld": "label", "textseite": "page", "link": "url", "aufgabe": "assign",
    "abstimmung": "choice", "unterabschnitt": "subsection",
}


class Fehler(Exception):
    pass


def x(text):
    """Text für XML maskieren (Moodle maskiert &, <, > und lässt Anführungszeichen stehen)."""
    return escape(str(text), quote=False)


def klartext(html):
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", html))).strip()


class Zaehler:
    def __init__(self, start):
        self.n = start

    def neu(self):
        self.n += 1
        return self.n


class Kurs:
    def __init__(self, spec):
        self.spec = spec
        self.jetzt = int(time.time())
        self.id = Zaehler(1000)
        self.dateien = {}          # Pfad im Archiv -> Inhalt (str)
        self.sections = []         # dicts: id, number, name, summary, sequence, parentcm
        self.activities = []       # dicts: modname, cmid, sectionid, title, insub
        self.settings = []         # (level, key, name) in Reihenfolge
        self.gradesort = 1
        self.pruefen()
        self.courseid = self.id.neu()
        self.coursectx = self.id.neu()
        self.gradecat = self.id.neu()
        self.bauen()

    # ---------- Prüfung der Eingabe ----------
    def pruefen(self):
        s = self.spec
        for feld in ("titel", "kurzname"):
            if not str(s.get(feld, "")).strip():
                raise Fehler(f'Pflichtangabe "{feld}" fehlt.')
        if not isinstance(s.get("abschnitte"), list) or not s["abschnitte"]:
            raise Fehler('"abschnitte" muss eine Liste mit mindestens einem Abschnitt sein.')
        for nr, a in enumerate(s["abschnitte"], 1):
            if not str(a.get("name", "")).strip():
                raise Fehler(f"Abschnitt {nr}: \"name\" fehlt.")
            self.inhalte_pruefen(a.get("inhalte", []), f"Abschnitt {nr}", False)
        self.inhalte_pruefen(s.get("allgemein", []), "allgemein", False)

    def inhalte_pruefen(self, inhalte, ort, in_unterabschnitt):
        pflicht = {
            "textfeld": ["html"], "textseite": ["name", "html"], "link": ["name", "url"],
            "aufgabe": ["name", "anweisungen"], "abstimmung": ["name", "frage", "optionen"],
            "unterabschnitt": ["name"],
        }
        for nr, i in enumerate(inhalte, 1):
            wo = f"{ort}, Inhalt {nr}"
            typ = i.get("typ")
            if typ not in TYPEN:
                raise Fehler(f'{wo}: unbekannter Typ "{typ}". Erlaubt: {", ".join(TYPEN)}.')
            for feld in pflicht[typ]:
                if not i.get(feld):
                    raise Fehler(f'{wo} ({typ}): Pflichtangabe "{feld}" fehlt.')
            if typ == "link" and not str(i["url"]).startswith("https://"):
                raise Fehler(f"{wo}: Die Adresse muss mit https:// beginnen.")
            if typ == "abstimmung" and (not isinstance(i["optionen"], list) or len(i["optionen"]) < 2):
                raise Fehler(f"{wo}: Eine Abstimmung braucht mindestens zwei Optionen.")
            if typ == "aufgabe" and i.get("abgabe", "datei") not in ("datei", "text", "beides"):
                raise Fehler(f'{wo}: "abgabe" muss datei, text oder beides sein.')
            if typ == "unterabschnitt":
                if in_unterabschnitt:
                    raise Fehler(f"{wo}: Unterabschnitte dürfen nicht verschachtelt werden.")
                self.inhalte_pruefen(i.get("inhalte", []), f"{wo} (Unterabschnitt)", True)

    # ---------- Aufbau ----------
    def bauen(self):
        s = self.spec
        haupt = [{"name": None, "beschreibung": "", "inhalte": s.get("allgemein", [])}] + s["abschnitte"]
        # Erst alle Hauptabschnitte nummerieren (0..n), Unterabschnitte bekommen die Nummern danach.
        geplant = []
        for nr, a in enumerate(haupt):
            sec = {"id": self.id.neu(), "number": nr, "name": a["name"],
                   "summary": a.get("beschreibung", ""), "sequence": [],
                   "parentcm": None, "itemid": None}
            self.sections.append(sec)
            geplant.append((sec, a.get("inhalte", [])))
        self.naechste_nummer = len(haupt)
        for sec, inhalte in geplant:
            self.settings.append(("section", f"section_{sec['id']}"))
            for inhalt in inhalte:
                self.aktivitaet(inhalt, sec, False)
        self.sections.sort(key=lambda sec: sec["number"])
        for sec in self.sections:
            self.section_schreiben(sec)
        self.kurs_schreiben()
        self.stammdateien()
        self.backup_xml()

    def aktivitaet(self, i, sec, insub):
        mod = TYPEN[i["typ"]]
        cmid, inst, ctx = self.id.neu(), self.id.neu(), self.id.neu()
        ordner = f"activities/{mod}_{cmid}"
        sec["sequence"].append(cmid)
        self.settings.append(("activity", f"{mod}_{cmid}"))
        inforef = "<inforef>\n</inforef>"
        grades = "  <grade_items>\n  </grade_items>\n"
        showdesc = 1

        if mod == "label":
            text = klartext(i["html"])
            name = text if len(text) <= 50 else text[:50] + "..."
            name = name or "Text- und Medienfeld"
            kern = (f"    <name>{x(name)}</name>\n    <intro>{x(i['html'])}</intro>\n"
                    f"    <introformat>1</introformat>\n    <timemodified>{self.jetzt}</timemodified>\n")
        elif mod == "page":
            name = i["name"]
            kern = (f"    <name>{x(name)}</name>\n    <intro>{x(i.get('beschreibung', ''))}</intro>\n"
                    f"    <introformat>1</introformat>\n    <content>{x(i['html'])}</content>\n"
                    "    <contentformat>1</contentformat>\n    <legacyfiles>0</legacyfiles>\n"
                    f"    <legacyfileslast>{NULL}</legacyfileslast>\n    <display>5</display>\n"
                    '    <displayoptions>a:2:{s:10:"printintro";s:1:"0";s:17:"printlastmodified";s:1:"0";}</displayoptions>\n'
                    f"    <revision>1</revision>\n    <timemodified>{self.jetzt}</timemodified>\n")
        elif mod == "url":
            name = i["name"]
            showdesc = 1 if i.get("beschreibung") else 0
            anzeige = 3 if i.get("neues_fenster", True) else 0
            kern = (f"    <name>{x(name)}</name>\n    <intro>{x(i.get('beschreibung', ''))}</intro>\n"
                    f"    <introformat>1</introformat>\n    <externalurl>{x(i['url'])}</externalurl>\n"
                    f"    <display>{anzeige}</display>\n    <displayoptions>a:0:{{}}</displayoptions>\n"
                    f"    <parameters>a:0:{{}}</parameters>\n    <timemodified>{self.jetzt}</timemodified>\n")
        elif mod == "choice":
            name = i["name"]
            optionen = "".join(
                f'      <option id="{self.id.neu()}">\n        <text>{x(o)}</text>\n'
                f"        <maxanswers>0</maxanswers>\n        <timemodified>{self.jetzt}</timemodified>\n      </option>\n"
                for o in i["optionen"])
            mehrfach = 1 if i.get("mehrfachauswahl") else 0
            kern = (f"    <name>{x(name)}</name>\n    <intro>{x(i['frage'])}</intro>\n    <introformat>1</introformat>\n"
                    "    <publish>0</publish>\n    <showresults>0</showresults>\n    <display>0</display>\n"
                    f"    <allowupdate>0</allowupdate>\n    <allowmultiple>{mehrfach}</allowmultiple>\n"
                    "    <showunanswered>0</showunanswered>\n    <limitanswers>0</limitanswers>\n"
                    f"    <timeopen>0</timeopen>\n    <timeclose>0</timeclose>\n    <timemodified>{self.jetzt}</timemodified>\n"
                    "    <completionsubmit>0</completionsubmit>\n    <showpreview>0</showpreview>\n"
                    "    <includeinactive>0</includeinactive>\n    <showavailable>0</showavailable>\n"
                    f"    <options>\n{optionen}    </options>\n    <answers>\n    </answers>\n")
        elif mod == "assign":
            name = i["name"]
            kern, grades, inforef = self.aufgabe(i, inst)
            self.dateien[f"{ordner}/grading.xml"] = (
                f'{XML}<areas>\n  <area id="{self.id.neu()}">\n    <areaname>submissions</areaname>\n'
                f"    <activemethod>{NULL}</activemethod>\n    <definitions>\n    </definitions>\n  </area>\n</areas>")
        else:  # subsection
            name = i["name"]
            showdesc = 0
            kern = f"    <name>{x(name)}</name>\n    <timemodified>0</timemodified>\n"
            unter = {"id": self.id.neu(), "number": self.naechste_nummer, "name": name, "summary": "",
                     "sequence": [], "parentcm": cmid, "itemid": inst}
            self.naechste_nummer += 1
            self.sections.append(unter)

        self.activities.append({"modname": mod, "cmid": cmid, "sectionid": sec["id"],
                                "title": name, "insub": insub})
        leer = NULL if mod == "subsection" else ""
        self.dateien[f"{ordner}/{mod}.xml"] = (
            f'{XML}<activity id="{inst}" moduleid="{cmid}" modulename="{mod}" contextid="{ctx}">\n'
            f'  <{mod} id="{inst}">\n{kern}  </{mod}>\n</activity>')
        self.dateien[f"{ordner}/module.xml"] = (
            f'{XML}<module id="{cmid}" version="{MODULE_VERSION}">\n  <modulename>{mod}</modulename>\n'
            f"  <sectionid>{sec['id']}</sectionid>\n  <sectionnumber>{sec['number']}</sectionnumber>\n"
            f"  <idnumber>{leer}</idnumber>\n  <added>{self.jetzt}</added>\n  <score>0</score>\n  <indent>0</indent>\n"
            "  <visible>1</visible>\n  <visibleoncoursepage>1</visibleoncoursepage>\n  <visibleold>1</visibleold>\n"
            "  <groupmode>0</groupmode>\n  <groupingid>0</groupingid>\n  <completion>0</completion>\n"
            f"  <completiongradeitemnumber>{NULL}</completiongradeitemnumber>\n  <completionpassgrade>0</completionpassgrade>\n"
            "  <completionview>0</completionview>\n  <completionexpected>0</completionexpected>\n"
            f"  <availability>{NULL}</availability>\n  <showdescription>{showdesc}</showdescription>\n"
            f"  <downloadcontent>1</downloadcontent>\n  <lang>{leer}</lang>\n  <enableaitools>{NULL}</enableaitools>\n"
            f"  <enabledaiactions>{NULL}</enabledaiactions>\n  <tags>\n  </tags>\n</module>")
        self.dateien[f"{ordner}/inforef.xml"] = XML + inforef
        self.dateien[f"{ordner}/grades.xml"] = (
            f"{XML}<activity_gradebook>\n{grades}  <grade_letters>\n  </grade_letters>\n</activity_gradebook>")
        self.dateien[f"{ordner}/roles.xml"] = (
            f"{XML}<roles>\n  <role_overrides>\n  </role_overrides>\n  <role_assignments>\n  </role_assignments>\n</roles>")
        self.dateien[f"{ordner}/filters.xml"] = (
            f"{XML}<filters>\n  <filter_actives>\n  </filter_actives>\n  <filter_configs>\n  </filter_configs>\n</filters>")
        self.dateien[f"{ordner}/calendar.xml"] = f"{XML}<events>\n</events>"
        self.dateien[f"{ordner}/grade_history.xml"] = (
            f"{XML}<grade_history>\n  <grade_grades>\n  </grade_grades>\n</grade_history>")

        if mod == "subsection":
            self.settings.append(("section", f"section_{unter['id']}"))
            for inhalt in i.get("inhalte", []):
                self.aktivitaet(inhalt, unter, True)

    def aufgabe(self, i, inst):
        punkte = int(i.get("punkte", 100))
        abgabe = i.get("abgabe", "datei")
        datei = 1 if abgabe in ("datei", "beides") else 0
        text = 1 if abgabe in ("text", "beides") else 0
        configs = [
            ("mbsaudio", "assignsubmission", "enabled", 0),
            ("file", "assignsubmission", "enabled", datei),
            ("file", "assignsubmission", "maxfilesubmissions", 20),
            ("file", "assignsubmission", "maxsubmissionsizebytes", MAXBYTES),
            ("file", "assignsubmission", "filetypeslist", ""),
            ("comments", "assignsubmission", "enabled", 1),
            ("onlinetext", "assignsubmission", "enabled", text),
            ("aif", "assignfeedback", "enabled", 0),
            ("comments", "assignfeedback", "enabled", 1),
            ("comments", "assignfeedback", "commentinline", 0),
            ("editpdf", "assignfeedback", "enabled", 0),
            ("file", "assignfeedback", "enabled", 1),
            ("offline", "assignfeedback", "enabled", 0),
        ]
        cfg = "".join(
            f'      <plugin_config id="{self.id.neu()}">\n        <plugin>{p}</plugin>\n        <subtype>{st}</subtype>\n'
            f"        <name>{n}</name>\n        <value>{v}</value>\n      </plugin_config>\n"
            for p, st, n, v in configs)
        nullen = lambda *namen: "".join(f"    <{n}>0</{n}>\n" for n in namen)
        kern = (
            f"    <name>{x(i['name'])}</name>\n    <intro>{x(i.get('beschreibung', ''))}</intro>\n    <introformat>1</introformat>\n"
            + nullen("alwaysshowdescription", "submissiondrafts", "sendnotifications", "sendlatenotifications")
            + "    <sendstudentnotifications>1</sendstudentnotifications>\n"
            + nullen("duedate", "cutoffdate", "gradingduedate", "allowsubmissionsfromdate")
            + f"    <grade>{punkte}</grade>\n    <timemodified>{self.jetzt}</timemodified>\n    <completionsubmit>1</completionsubmit>\n"
            + nullen("requiresubmissionstatement", "teamsubmission", "requireallteammemberssubmit",
                     "teamsubmissiongroupingid", "blindmarking", "hidegrader", "revealidentities")
            + "    <attemptreopenmethod>untilpass</attemptreopenmethod>\n    <maxattempts>1</maxattempts>\n"
            + nullen("markingworkflow", "markingallocation")
            + f"    <markercount>1</markercount>\n    <multimarkmethod>{NULL}</multimarkmethod>\n"
            + nullen("markinganonymous", "preventsubmissionnotingroup")
            + f"    <activity>{x(i['anweisungen'])}</activity>\n    <activityformat>1</activityformat>\n"
            + nullen("timelimit", "submissionattachments", "gradepenalty")
            + "".join(f"    <{n}>\n    </{n}>\n" for n in ("userflags", "allocatedmarkers", "submissions", "grades", "marks"))
            + f"    <plugin_configs>\n{cfg}    </plugin_configs>\n    <overrides>\n    </overrides>\n")
        gid = self.id.neu()
        self.gradesort += 1
        n = NULL
        grades = (
            f'  <grade_items>\n    <grade_item id="{gid}">\n      <categoryid>{self.gradecat}</categoryid>\n'
            f"      <itemname>{x(i['name'])}</itemname>\n      <itemtype>mod</itemtype>\n      <itemmodule>assign</itemmodule>\n"
            f"      <iteminstance>{inst}</iteminstance>\n      <itemnumber>0</itemnumber>\n      <iteminfo>{n}</iteminfo>\n"
            f"      <idnumber></idnumber>\n      <calculation>{n}</calculation>\n      <gradetype>1</gradetype>\n"
            f"      <grademax>{punkte}.00000</grademax>\n      <grademin>0.00000</grademin>\n      <scaleid>{n}</scaleid>\n"
            f"      <outcomeid>{n}</outcomeid>\n      <gradepass>0.00000</gradepass>\n      <multfactor>1.00000</multfactor>\n"
            "      <plusfactor>0.00000</plusfactor>\n      <aggregationcoef>0.00000</aggregationcoef>\n"
            "      <aggregationcoef2>0.00000</aggregationcoef2>\n      <weightoverride>0</weightoverride>\n"
            f"      <sortorder>{self.gradesort}</sortorder>\n      <display>0</display>\n      <decimals>{n}</decimals>\n"
            "      <hidden>0</hidden>\n      <locked>0</locked>\n      <locktime>0</locktime>\n      <needsupdate>0</needsupdate>\n"
            f"      <timecreated>{self.jetzt}</timecreated>\n      <timemodified>{self.jetzt}</timemodified>\n"
            "      <grade_grades>\n      </grade_grades>\n    </grade_item>\n  </grade_items>\n")
        inforef = (f"<inforef>\n  <grade_itemref>\n    <grade_item>\n      <id>{gid}</id>\n    </grade_item>\n"
                   "  </grade_itemref>\n</inforef>")
        return kern, grades, inforef

    def section_schreiben(self, sec):
        ordner = f"sections/section_{sec['id']}"
        name = NULL if sec["name"] is None else x(sec["name"])
        komponente = "mod_subsection" if sec["parentcm"] else NULL
        itemid = sec["itemid"] if sec["parentcm"] else NULL
        self.dateien[f"{ordner}/section.xml"] = (
            f'{XML}<section id="{sec["id"]}">\n  <number>{sec["number"]}</number>\n  <name>{name}</name>\n'
            f"  <summary>{x(sec['summary'])}</summary>\n  <summaryformat>1</summaryformat>\n"
            f"  <sequence>{','.join(map(str, sec['sequence']))}</sequence>\n  <visible>1</visible>\n"
            f"  <availabilityjson>{NULL}</availabilityjson>\n  <component>{komponente}</component>\n"
            f"  <itemid>{itemid}</itemid>\n  <timemodified>{self.jetzt}</timemodified>\n</section>")
        self.dateien[f"{ordner}/inforef.xml"] = f"{XML}<inforef>\n</inforef>"

    def kurs_schreiben(self):
        s, n = self.spec, NULL
        fmt = s.get("format", "topics")
        optionen = "".join(
            f"    <courseformatoption>\n      <format>{fmt}</format>\n      <sectionid>0</sectionid>\n"
            f"      <name>{name}</name>\n      <value>{wert}</value>\n    </courseformatoption>\n"
            for name, wert in (("coursedisplay", 0), ("hiddensections", 1)))
        self.dateien["course/course.xml"] = (
            f'{XML}<course id="{self.courseid}" contextid="{self.coursectx}">\n'
            f"  <shortname>{x(s['kurzname'])}</shortname>\n  <fullname>{x(s['titel'])}</fullname>\n  <idnumber></idnumber>\n"
            f"  <summary>{x(s.get('beschreibung', ''))}</summary>\n  <summaryformat>1</summaryformat>\n  <format>{fmt}</format>\n"
            f"  <showgrades>1</showgrades>\n  <newsitems>0</newsitems>\n  <startdate>{self.jetzt}</startdate>\n  <enddate>0</enddate>\n"
            f"  <marker>0</marker>\n  <maxbytes>{MAXBYTES}</maxbytes>\n  <legacyfiles>0</legacyfiles>\n  <showreports>0</showreports>\n"
            "  <visible>1</visible>\n  <groupmode>0</groupmode>\n  <groupmodeforce>0</groupmodeforce>\n"
            "  <defaultgroupingid>0</defaultgroupingid>\n  <lang></lang>\n  <theme></theme>\n"
            f"  <timecreated>{self.jetzt}</timecreated>\n  <timemodified>{self.jetzt}</timemodified>\n  <requested>0</requested>\n"
            "  <showactivitydates>0</showactivitydates>\n  <showcompletionconditions>0</showcompletionconditions>\n"
            f"  <pdfexportfont>{n}</pdfexportfont>\n  <enablecompletion>1</enablecompletion>\n  <completionnotify>0</completionnotify>\n"
            f"  <enableaitools>{n}</enableaitools>\n  <plugin_local_mbslicenseinfo_course>\n    <metainfos>\n    </metainfos>\n"
            "  </plugin_local_mbslicenseinfo_course>\n"
            f'  <category id="1">\n    <name>Kursbau</name>\n    <description></description>\n  </category>\n'
            f"  <tags>\n  </tags>\n  <customfields>\n  </customfields>\n  <courseformatoptions>\n{optionen}  </courseformatoptions>\n</course>")
        felder = "".join(f"      <{f}>{n}</{f}>\n" for f in (
            "customint2", "customint3", "customint4", "customint5", "customint6", "customint7", "customint8",
            "customchar1", "customchar2", "customchar3", "customdec1", "customdec2",
            "customtext1", "customtext2", "customtext3", "customtext4"))
        self.dateien["course/enrolments.xml"] = (
            f'{XML}<enrolments>\n  <enrols>\n    <enrol id="{self.id.neu()}">\n      <enrol>manual</enrol>\n      <status>0</status>\n'
            f"      <name>{n}</name>\n      <enrolperiod>0</enrolperiod>\n      <enrolstartdate>0</enrolstartdate>\n"
            "      <enrolenddate>0</enrolenddate>\n      <expirynotify>0</expirynotify>\n      <expirythreshold>86400</expirythreshold>\n"
            f"      <notifyall>0</notifyall>\n      <password>{n}</password>\n      <cost>{n}</cost>\n      <currency>{n}</currency>\n"
            f"      <roleid>5</roleid>\n      <customint1>0</customint1>\n{felder}"
            f"      <timecreated>{self.jetzt}</timecreated>\n      <timemodified>{self.jetzt}</timemodified>\n"
            "      <user_enrolments>\n      </user_enrolments>\n    </enrol>\n  </enrols>\n</enrolments>")
        self.dateien["course/inforef.xml"] = (
            f"{XML}<inforef>\n  <roleref>\n    <role>\n      <id>5</id>\n    </role>\n  </roleref>\n</inforef>")
        self.dateien["course/roles.xml"] = (
            f"{XML}<roles>\n  <role_overrides>\n  </role_overrides>\n  <role_assignments>\n  </role_assignments>\n</roles>")
        self.dateien["course/filters.xml"] = (
            f"{XML}<filters>\n  <filter_actives>\n  </filter_actives>\n  <filter_configs>\n  </filter_configs>\n</filters>")
        self.dateien["course/calendar.xml"] = f"{XML}<events>\n</events>"
        self.dateien["course/completiondefaults.xml"] = f"{XML}<course_completion_defaults>\n</course_completion_defaults>"
        self.dateien["course/contentbank.xml"] = f"{XML}<contents>\n</contents>"

    def stammdateien(self):
        n, d = NULL, self.dateien
        d["badges.xml"] = f"{XML}<badges>\n</badges>"
        d["completion.xml"] = f"{XML}<course_completion>\n</course_completion>"
        d["files.xml"] = f"{XML}<files>\n</files>"
        d["grade_history.xml"] = f"{XML}<grade_history>\n  <grade_grades>\n  </grade_grades>\n</grade_history>"
        d["groups.xml"] = (f"{XML}<groups>\n  <groupcustomfields>\n  </groupcustomfields>\n  <groupings>\n"
                           "    <groupingcustomfields>\n    </groupingcustomfields>\n  </groupings>\n</groups>")
        d["outcomes.xml"] = f"{XML}<outcomes_definition>\n</outcomes_definition>"
        d["questions.xml"] = f"{XML}<question_categories>\n</question_categories>"
        d["scales.xml"] = f"{XML}<scales_definition>\n</scales_definition>"
        d["roles.xml"] = (
            f'{XML}<roles_definition>\n  <role id="5">\n    <name>Schüler</name>\n    <shortname>student</shortname>\n'
            f"    <nameincourse>{n}</nameincourse>\n"
            "    <description>&lt;p&gt;Students generally have fewer privileges within a course.&lt;/p&gt;</description>\n"
            "    <sortorder>11</sortorder>\n    <archetype>student</archetype>\n  </role>\n</roles_definition>")
        d["gradebook.xml"] = (
            f'{XML}<gradebook>\n  <attributes>\n  </attributes>\n  <grade_categories>\n    <grade_category id="{self.gradecat}">\n'
            f"      <parent>{n}</parent>\n      <depth>1</depth>\n      <path>/{self.gradecat}/</path>\n      <fullname>?</fullname>\n"
            "      <aggregation>11</aggregation>\n      <keephigh>0</keephigh>\n      <droplow>0</droplow>\n"
            "      <aggregateonlygraded>1</aggregateonlygraded>\n      <aggregateoutcomes>0</aggregateoutcomes>\n"
            f"      <timecreated>{self.jetzt}</timecreated>\n      <timemodified>{self.jetzt}</timemodified>\n      <hidden>0</hidden>\n"
            f'    </grade_category>\n  </grade_categories>\n  <grade_items>\n    <grade_item id="{self.id.neu()}">\n'
            f"      <categoryid>{n}</categoryid>\n      <itemname>{n}</itemname>\n      <itemtype>course</itemtype>\n"
            f"      <itemmodule>{n}</itemmodule>\n      <iteminstance>{self.gradecat}</iteminstance>\n      <itemnumber>{n}</itemnumber>\n"
            f"      <iteminfo>{n}</iteminfo>\n      <idnumber>{n}</idnumber>\n      <calculation>{n}</calculation>\n"
            f"      <gradetype>1</gradetype>\n      <grademax>100.00000</grademax>\n      <grademin>0.00000</grademin>\n"
            f"      <scaleid>{n}</scaleid>\n      <outcomeid>{n}</outcomeid>\n      <gradepass>0.00000</gradepass>\n"
            "      <multfactor>1.00000</multfactor>\n      <plusfactor>0.00000</plusfactor>\n"
            "      <aggregationcoef>0.00000</aggregationcoef>\n      <aggregationcoef2>0.00000</aggregationcoef2>\n"
            f"      <weightoverride>0</weightoverride>\n      <sortorder>1</sortorder>\n      <display>0</display>\n"
            f"      <decimals>{n}</decimals>\n      <hidden>0</hidden>\n      <locked>0</locked>\n      <locktime>0</locktime>\n"
            f"      <needsupdate>0</needsupdate>\n      <timecreated>{self.jetzt}</timecreated>\n"
            f"      <timemodified>{self.jetzt}</timemodified>\n      <grade_grades>\n      </grade_grades>\n    </grade_item>\n"
            "  </grade_items>\n  <grade_letters>\n  </grade_letters>\n  <grade_settings>\n    <grade_setting id=\"\">\n"
            "      <name>minmaxtouse</name>\n      <value>1</value>\n    </grade_setting>\n  </grade_settings>\n</gradebook>")
        d["moodle_backup.log"] = ""

    def backup_xml(self):
        s = self.spec
        self.dateiname = f"sicherung-moodle2-course-{self.courseid}-{slug(s['kurzname'])}-" \
                         f"{time.strftime('%Y%m%d-%H%M', time.localtime(self.jetzt))}-nu.mbz"
        akt = "".join(
            f"        <activity>\n          <moduleid>{a['cmid']}</moduleid>\n          <sectionid>{a['sectionid']}</sectionid>\n"
            f"          <modulename>{a['modname']}</modulename>\n          <title>{x(a['title'])}</title>\n"
            f"          <directory>activities/{a['modname']}_{a['cmid']}</directory>\n"
            f"          <insubsection>{'1' if a['insub'] else ''}</insubsection>\n        </activity>\n"
            for a in self.activities)
        # Reihenfolge wie im Original: Abschnitt 0, Unterabschnitte, dann die übrigen Hauptabschnitte
        reihenfolge = sorted(self.sections, key=lambda c: (c["number"] != 0, not c["parentcm"], c["number"]))
        sec = "".join(
            f"        <section>\n          <sectionid>{c['id']}</sectionid>\n"
            f"          <title>{x(c['name']) if c['name'] is not None else c['number']}</title>\n"
            f"          <directory>sections/section_{c['id']}</directory>\n"
            f"          <parentcmid>{c['parentcm'] or ''}</parentcmid>\n"
            f"          <modname>{'subsection' if c['parentcm'] else ''}</modname>\n        </section>\n"
            for c in reihenfolge)
        einst = "".join(
            f"      <setting>\n        <level>root</level>\n        <name>{n}</name>\n        <value>{v}</value>\n      </setting>\n"
            for n, v in [("filename", self.dateiname)] + ROOT_SETTINGS)
        for level, key in self.settings:
            for endung, wert in (("included", 1), ("userinfo", 0)):
                einst += (f"      <setting>\n        <level>{level}</level>\n        <{level}>{key}</{level}>\n"
                          f"        <name>{key}_{endung}</name>\n        <value>{wert}</value>\n      </setting>\n")
        kennung = hashlib.md5(f"{self.dateiname}{self.jetzt}".encode()).hexdigest()
        self.dateien["moodle_backup.xml"] = (
            f"{XML}<moodle_backup>\n  <information>\n    <name>{self.dateiname}</name>\n"
            f"    <moodle_version>{MOODLE_VERSION}</moodle_version>\n    <moodle_release>{MOODLE_RELEASE}</moodle_release>\n"
            f"    <backup_version>{BACKUP_VERSION}</backup_version>\n    <backup_release>{BACKUP_RELEASE}</backup_release>\n"
            f"    <backup_date>{self.jetzt}</backup_date>\n    <mnet_remoteusers>0</mnet_remoteusers>\n"
            "    <include_files>1</include_files>\n"
            "    <include_file_references_to_external_content>0</include_file_references_to_external_content>\n"
            "    <original_wwwroot>https://kursbau.invalid</original_wwwroot>\n"
            f"    <original_site_identifier_hash>{hashlib.md5(b'mebis-kursbau').hexdigest()}</original_site_identifier_hash>\n"
            f"    <original_course_id>{self.courseid}</original_course_id>\n"
            f"    <original_course_format>{s.get('format', 'topics')}</original_course_format>\n"
            f"    <original_course_fullname>{x(s['titel'])}</original_course_fullname>\n"
            f"    <original_course_shortname>{x(s['kurzname'])}</original_course_shortname>\n"
            f"    <original_course_startdate>{self.jetzt}</original_course_startdate>\n"
            "    <original_course_enddate>0</original_course_enddate>\n"
            f"    <original_course_contextid>{self.coursectx}</original_course_contextid>\n"
            "    <original_system_contextid>1</original_system_contextid>\n"
            f'    <details>\n      <detail backup_id="{kennung}">\n        <type>course</type>\n        <format>moodle2</format>\n'
            "        <interactive>1</interactive>\n        <mode>10</mode>\n        <execution>1</execution>\n"
            "        <executiontime>0</executiontime>\n      </detail>\n    </details>\n"
            f"    <contents>\n      <activities>\n{akt}      </activities>\n      <sections>\n{sec}      </sections>\n"
            f"      <course>\n        <courseid>{self.courseid}</courseid>\n        <title>{x(s['kurzname'])}</title>\n"
            "        <directory>course</directory>\n      </course>\n    </contents>\n"
            f"    <settings>\n{einst}    </settings>\n  </information>\n</moodle_backup>")

    # ---------- Archiv ----------
    def packen(self, ziel):
        pfade = sorted(self.dateien)
        ordner = sorted({str(p) + "/" for pfad in pfade for p in Path(pfad).parents if str(p) != "."})
        daten = {p: self.dateien[p].encode("utf-8") for p in pfade}
        zeilen = [f"{o}\td\t0\t?" for o in ordner] + [f"{p}\tf\t{len(daten[p])}\t{self.jetzt}" for p in pfade]
        index = (f"Moodle archive file index. Count: {len(zeilen)}\n" + "\n".join(zeilen) + "\n").encode("utf-8")
        with tarfile.open(ziel, "w:gz", format=tarfile.USTAR_FORMAT) as tar:
            def rein(name, inhalt, ist_ordner=False):
                info = tarfile.TarInfo(name.rstrip("/"))
                info.mtime = self.jetzt
                if ist_ordner:
                    info.type, info.mode = tarfile.DIRTYPE, 0o755
                    tar.addfile(info)
                else:
                    info.size, info.mode = len(inhalt), 0o644
                    tar.addfile(info, io.BytesIO(inhalt))
            rein(".ARCHIVE_INDEX", index)
            for o in ordner:
                rein(o, b"", True)
            for p in pfade:
                rein(p, daten[p])


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "kurs"


def main(argv):
    if len(argv) not in (2, 3):
        print(__doc__)
        return 2
    try:
        spec = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
        kurs = Kurs(spec)
    except (Fehler, json.JSONDecodeError, OSError) as f:
        print(f"Fehler: {f}")
        return 1
    ziel = Path(argv[2]) if len(argv) == 3 else Path(kurs.dateiname)
    kurs.packen(ziel)
    print(f"Erzeugt: {ziel}  ({len(kurs.sections)} Abschnitte, {len(kurs.activities)} Aktivitäten)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
