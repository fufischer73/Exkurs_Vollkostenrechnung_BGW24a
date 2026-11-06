# Moodle-Kurs: zwei Varianten für Moodle 4.5

Beide Sicherungen enthalten **alle Module** (Stufe 1 bis 4, Meilensteine mit Abgabe, beide Tests), ohne Einstufungstests: Jede Stufe öffnet erst nach der **Abgabe des Meilensteins** der vorigen Stufe.

| Datei | Aufbau | Wann nehmen? |
| --- | --- | --- |
| `exkurs-vollkostenrechnung_EIN-ABSCHNITT_moodle4-5.mbz` | **Ein Abschnitt**, darin die Startseite und **vier Unterabschnitte** (je Stufe einer) | wenn der Lernpfad nur einen Abschnitt eines Kurses belegen soll |
| `exkurs-vollkostenrechnung_VOLLSTAENDIG_moodle4.mbz` | **Vier Abschnitte** (je Stufe einer) plus „Allgemeines“ für die Startseite | Rückfallebene, falls Unterabschnitte nicht funktionieren |

## Voraussetzung für die Variante „ein Abschnitt“

Die Aktivität **Unterabschnitt** muss in Moodle aktiviert sein: *Website-Administration › Plugins › Aktivitäten › Aktivitäten verwalten* (Auge bei „Unterabschnitt“ offen). Die Sicherung ist mit der Versionsnummer 4.5 gebaut, damit Moodle keine Versionswarnung zeigt. Sie ist **noch nicht in Moodle getestet**.

## Einspielen

1. Leeren **Testkurs** anlegen (oder den Kurs, in den der Abschnitt soll).
2. **Mehr › Wiederverwendung › Wiederherstellen**, die `.mbz` hochladen.
3. **„In diesen Kurs, Inhalte hinzufügen“** wählen, dann Weiter, Weiter, Wiederherstellen. Vorhandene Inhalte bleiben, der Lernpfad kommt als neuer Abschnitt dazu. In einem Testkurs mit altem Stand: **„Den Inhalt dieses Kurses löschen und dann wiederherstellen“** (löscht alles in diesem Kurs).
4. Mit einem **Schüler:innen-Testkonto** durchklicken („Rolle wechseln“ zeigt keine Abschlüsse).

Nur **einmal** in einen Kurs wiederherstellen, sonst entsteht alles doppelt.

## Freischaltung

Einstufungstests gibt es nicht. Innerhalb einer Stufe öffnen die Module nacheinander. Die nächste Stufe öffnet nach der Abgabe des Meilensteins (die Bewertung muss nicht abgewartet werden). Stufe 4 öffnet nach der Abgabe des Meilensteins 3.

## Neu bauen

- Ein Abschnitt: `python3 werkzeuge/bauen_moodle_ein_abschnitt.py <pfad-zum-baukasten>`
- Vier Abschnitte: `python3 werkzeuge/bauen_ohne_einstufung.py <pfad-zum-baukasten> --moodle 4`
