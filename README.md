# Exkurs Vollkostenrechnung – Montelli GmbH (BGW24a · BRC)

Lernpfad für Moodle (Abschnitt mit Unterabschnitten) und Web-Version, gebaut mit dem
[Lernpfad-Baukasten](https://github.com/dclausen01/Lernpfad-baukasten).

**Stand:** Stufe 1 „Von der GuV zu den Kosten“ und Stufe 2 „Der Betriebsabrechnungsbogen“ (Entwurf). Stufe 3 (Kostenträgerrechnung) folgt.

| Ordner | Inhalt |
| --- | --- |
| `kurs.yaml`, `module/` | Kursbeschreibung und Module |
| `material/` | Arbeitsblätter (docx) und Excel-Vorlagen (xlsx) für Schüler:innen |
| `lehrkraft/` | Lösungen und Erwartungshorizonte (nicht an Schüler:innen) |
| `werkzeuge/` | Zahlengrundlage der Montelli GmbH (`daten.py`, rechnet und prüft alle Summen) und Erzeugung der Materialien |

Alle Zahlen sind für die Montelli GmbH neu konstruiert. Das Westermann-Material (Crome KG) diente nur als Strukturvorlage.
Neu bauen: `python3 werkzeuge/material_stufe1.py` und `werkzeuge/material_stufe2.py`, dann `python3 <baukasten>/skripte/alles.py .`
