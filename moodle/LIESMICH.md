# Moodle-Kurs: vollständig (für Moodle 4.5)

`exkurs-vollkostenrechnung_VOLLSTAENDIG_moodle4.mbz` ist für das BBZ-Moodle (Version 4.5.12+) gebaut und enthält **alle freigegebenen Module**:

- Startseite „Mein Lernpfad“
- **Stufe 1:** G1, G2, Meilenstein 1 (mit Abgabe)
- **Stufe 2:** B1 bis B5, Meilenstein 2 (mit Abgabe)
- **Stufe 3:** T1 bis T3, Meilenstein 3 (mit Abgabe), **Lernerfolgskontrolle** (Moodle-Test, 10 Fragen)
- **Stufe 4 (freiwillig):** Übungen U1 bis U6 und der Test „Richtig oder falsch zum BAB“ (8 Fragen)

## Struktur in Moodle 4.5

Moodle 4.5 hat **keine Unterabschnitte** (die gibt es erst ab Moodle 5). Jede Stufe wird deshalb ein **eigener Abschnitt**; Lernpaket und Abgabe eines Meilensteins stehen untereinander im Abschnitt der Stufe. Die Startseite steht im obersten Abschnitt („Allgemeines“).

## Einspielen

1. Leeren **Testkurs** anlegen (oder den Kurs, in den die Abschnitte sollen).
2. **Mehr › Wiederverwendung › Wiederherstellen**, die `.mbz` hochladen.
3. **„In diesen Kurs, Inhalte hinzufügen“** wählen, dann Weiter, Weiter, Wiederherstellen.
4. Mit einem **Schüler:innen-Testkonto** durchklicken („Rolle wechseln“ zeigt keine Abschlüsse).

Nur **einmal** in einen Kurs wiederherstellen, sonst entsteht alles doppelt. Die Sicherungen von vorher (für Moodle 5) bitte **nicht mehr verwenden**: Moodle 4.5 warnt davor, weil sie für eine neuere Version gebaut waren.

## Freischaltung

Einstufungstests gibt es **nicht**. Jede Stufe öffnet erst, wenn die **Abgabe des Meilensteins der vorigen Stufe** erfolgt ist (die Bewertung muss nicht abgewartet werden). Innerhalb einer Stufe öffnen die Module nacheinander. Stufe 4 öffnet nach der Abgabe des Meilensteins 3.

Zum Neubauen: `python3 werkzeuge/bauen_ohne_einstufung.py <pfad-zum-baukasten> --moodle 4`.
