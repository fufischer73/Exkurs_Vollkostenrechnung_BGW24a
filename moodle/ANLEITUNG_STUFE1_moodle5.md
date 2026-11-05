# Exkurs Vollkostenrechnung – Moodle-Kurs von Hand einrichten

Normalerweise geht es schneller mit der Kurssicherung:
**Kurs › Mehr › Wiederverwendung › Wiederherstellen** → `exkurs-vollkostenrechnung_moodle5.mbz` hochladen → „In diesen Kurs, Inhalte hinzufügen“ → durchklicken. Diese Anleitung ist die Rückfallebene, falls Wiederherstellen nicht erlaubt ist.

## Vorbereitung

- Kurs › Einstellungen › **Abschlussverfolgung: Ja**
- Kursformat: Themen (Moodle 5: Unterabschnitte müssen von der Moodle-Administration aktiviert sein)

## Einstellungen für jedes Lernpaket

Aktivität **Lernpaket** (SCORM) anlegen, ZIP aus `lernpakete/` hochladen, dann:

- Darstellung: **Anzeige des Pakets: Aktuelles Fenster** · Breite 100 % · Höhe 500
- Darstellung: **Kursstruktur anzeigen: Deaktiviert** · **Navigation anzeigen: Nein** · **Struktur-Seite überspringen: Immer** · Versuchsstatus anzeigen: Nein
- Bewertung: Höchstbewertung 100, Bewertungsmethode: Höchste Bewertung
- Versuchsverwaltung: Beherrschungswert überschreibt Status: Ja
- Aktivitätsabschluss: **Bedingungen erfüllt** → **Status erforderlich: Abgeschlossen** (nur „abgeschlossen“ anhaken)
- Ausnahme Startseite und Einstufungstests: **kein Aktivitätsabschluss**; die Startseite außerdem Bewertung 0.

## Abschnitt „Allgemeines“ (ganz oben)

- Lernpaket **🧭 Mein Lernpfad – hier geht's los** – `lernpakete/exkurs-vollkostenrechnung_start_scorm2004.zip`

## Abschnitt „🌱 Von der GuV zu den Kosten“

- Lernpaket **G1 · Von der GuV zu den Einzel- und Gemeinkosten** – `lernpakete/exkurs-vollkostenrechnung_g1_scorm2004.zip`
- Lernpaket **G2 · Kostenarten und Kostenartenplan (H)** – `lernpakete/exkurs-vollkostenrechnung_g2_scorm2004.zip` – Voraussetzung: „G1 · Von der GuV zu den Einzel- und Gemeinkosten“ abgeschlossen
- Unterabschnitt **★ Meilenstein 1: Kostenartenplan Montelli für August** – Voraussetzung: „G2 · Kostenarten und Kostenartenplan (H)“ abgeschlossen
  - Lernpaket **★ Meilenstein 1: Kostenartenplan Montelli für August – Auftrag & Checkliste** – `lernpakete/exkurs-vollkostenrechnung_gm_scorm2004.zip`
  - Aufgabe **📤 Kostenartenplan August abgeben** – Dateiabgabe, höchstens 2 Datei(en), Dateitypen .pdf,.docx, 100 Punkte, Abschluss: „Abgabe erforderlich“
    Beschreibung: Lade deinen ausgefüllten Kostenartenplan als **PDF** (z. B. gescanntes Arbeitsblatt) oder als **Word-Datei** hoch. Keine Bilder. Wenn du in Excel gearbeitet hast, speichere die Tabelle als PDF.
    Bewertungsmethode **Bewertungsraster** mit diesen Kriterien:
    - Kostenarten und Zuordnung: nicht erreicht (0 P.) · erreicht: Alle Kostenarten stehen im Plan. Einzel- und Gemeinkosten sind richtig zugeordnet. Die neutralen Konten sind nicht enthalten. Statt der Konten 6520 und 7510 stehen die kalkulatorischen Werte. (2 P.) · besonders gut: Alles ist fehlerfrei und ohne Hilfe erstellt. (3 P.)
    - Begründung der Zuordnung: nicht erreicht (0 P.) · erreicht: Für Hilfsstoffe und Gehälter steht je ein Satz, warum sie Gemeinkosten sind. (2 P.) · besonders gut: Du nennst zusätzlich ein Beispiel für Sondereinzelkosten und erklärst es. (3 P.)
    - Rechnung: nicht erreicht (0 P.) · erreicht: Alle Summen stimmen. Die Probe (Einzelkosten + Gemeinkosten = Gesamtkosten) ist gemacht. (2 P.) · besonders gut: Du erklärst, warum die Gesamtkosten niedriger sind als im Juli. (3 P.)
    - Darstellung: nicht erreicht (0 P.) · erreicht: Der Plan ist lesbar und vollständig. (2 P.) · besonders gut: Der Rechenweg ist nachvollziehbar notiert. (3 P.)

