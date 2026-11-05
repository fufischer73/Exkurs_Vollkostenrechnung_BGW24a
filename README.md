# Exkurs Vollkostenrechnung – Montelli GmbH (BGW24a · BRC)

Lernpfad für Moodle (Abschnitt mit Unterabschnitten) und Web-Version, gebaut mit dem
[Lernpfad-Baukasten](https://github.com/dclausen01/Lernpfad-baukasten).

**Stand:** Stufe 1 „Von der GuV zu den Kosten“ , Stufe 2 „Der Betriebsabrechnungsbogen“ und Stufe 3 „Von den Kosten zum Verkaufspreis“ (alle freigegeben) mit Lernerfolgskontrolle (Moodle-Test) sowie die freiwillige Stufe 4 „Übungen und Vertiefung“.

| Ordner | Inhalt |
| --- | --- |
| `kurs.yaml`, `module/` | Kursbeschreibung und Module |
| `material/` | Arbeitsblätter (docx) und Excel-Vorlagen (xlsx) für Schüler:innen |
| `lehrkraft/` | Lösungen und Erwartungshorizonte (nicht an Schüler:innen) |
| `werkzeuge/` | Zahlengrundlage der Montelli GmbH (`daten.py`, rechnet und prüft alle Summen) und Erzeugung der Materialien |

Alle Zahlen sind für die Montelli GmbH neu konstruiert. Das Westermann-Material (Crome KG) diente nur als Strukturvorlage.
Neu bauen: `werkzeuge/material_*.py` (Arbeitsblätter) und dann `python3 werkzeuge/bauen_ohne_einstufung.py <baukasten> --moodle 4` (Web-Version und Moodle-Kurs ohne Einstufungstests).

`vorschau/vorschau.zip` enthält die Web-Version zum Ansehen (entpacken, `web/index.html` öffnen).

**Moodle:** `moodle/exkurs-vollkostenrechnung_VOLLSTAENDIG_moodle4.mbz` ist der vollständige Kurs (siehe `moodle/LIESMICH.md`).
