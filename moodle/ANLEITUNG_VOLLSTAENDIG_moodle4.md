# Exkurs Vollkostenrechnung – Moodle-Kurs von Hand einrichten

Normalerweise geht es schneller mit der Kurssicherung:
**Kurs › Mehr › Wiederverwendung › Wiederherstellen** → `exkurs-vollkostenrechnung_moodle4.mbz` hochladen → „In diesen Kurs, Inhalte hinzufügen“ → durchklicken. Diese Anleitung ist die Rückfallebene, falls Wiederherstellen nicht erlaubt ist.

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
- Lernpaket **★ Meilenstein 1: Kostenartenplan Montelli für August – Auftrag & Checkliste** – `lernpakete/exkurs-vollkostenrechnung_gm_scorm2004.zip` – Voraussetzung: „G2 · Kostenarten und Kostenartenplan (H)“ abgeschlossen
- Aufgabe **📤 Kostenartenplan August abgeben** – Voraussetzung: „G2 · Kostenarten und Kostenartenplan (H)“ abgeschlossen – Dateiabgabe, höchstens 2 Datei(en), Dateitypen .pdf,.docx, 100 Punkte, Abschluss: „Abgabe erforderlich“
  Beschreibung: Lade deinen ausgefüllten Kostenartenplan als **PDF** (z. B. gescanntes Arbeitsblatt) oder als **Word-Datei** hoch. Keine Bilder. Wenn du in Excel gearbeitet hast, speichere die Tabelle als PDF.
  Bewertungsmethode **Bewertungsraster** mit diesen Kriterien:
  - Kostenarten und Zuordnung: nicht erreicht (0 P.) · erreicht: Alle Kostenarten stehen im Plan. Einzel- und Gemeinkosten sind richtig zugeordnet. Die neutralen Konten sind nicht enthalten. Statt der Konten 6520 und 7510 stehen die kalkulatorischen Werte. (2 P.) · besonders gut: Alles ist fehlerfrei und ohne Hilfe erstellt. (3 P.)
  - Begründung der Zuordnung: nicht erreicht (0 P.) · erreicht: Für Hilfsstoffe und Gehälter steht je ein Satz, warum sie Gemeinkosten sind. (2 P.) · besonders gut: Du nennst zusätzlich ein Beispiel für Sondereinzelkosten und erklärst es. (3 P.)
  - Rechnung: nicht erreicht (0 P.) · erreicht: Alle Summen stimmen. Die Probe (Einzelkosten + Gemeinkosten = Gesamtkosten) ist gemacht. (2 P.) · besonders gut: Du erklärst, warum die Gesamtkosten niedriger sind als im Juli. (3 P.)
  - Darstellung: nicht erreicht (0 P.) · erreicht: Der Plan ist lesbar und vollständig. (2 P.) · besonders gut: Der Rechenweg ist nachvollziehbar notiert. (3 P.)

## Abschnitt „🚀 Der Betriebsabrechnungsbogen“

Voraussetzung am Abschnitt (Einschränkung: Aktivitätsabschluss bzw. Bewertung, verknüpft mit „mindestens eine“): „📤 Kostenartenplan August abgeben“ abgeschlossen.

- Lernpaket **B1 · Brücke: Wo fallen die Gemeinkosten an?** – `lernpakete/exkurs-vollkostenrechnung_b1_scorm2004.zip`
- Lernpaket **B2 · BAB Schritt 1: Gemeinkosten auf die Kostenstellen verteilen** – `lernpakete/exkurs-vollkostenrechnung_b2_scorm2004.zip` – Voraussetzung: „B1 · Brücke: Wo fallen die Gemeinkosten an?“ abgeschlossen
- Lernpaket **B3 · BAB Schritt 2: Innerbetriebliche Leistungen verrechnen** – `lernpakete/exkurs-vollkostenrechnung_b3_scorm2004.zip` – Voraussetzung: „B2 · BAB Schritt 1: Gemeinkosten auf die Kostenstellen verteilen“ abgeschlossen
- Lernpaket **B4 · BAB Schritt 3: Zuschlagssätze und Maschinenstundensatz** – `lernpakete/exkurs-vollkostenrechnung_b4_scorm2004.zip` – Voraussetzung: „B3 · BAB Schritt 2: Innerbetriebliche Leistungen verrechnen“ abgeschlossen
- Lernpaket **B5 · BAB Schritt 3: Herstellkosten des Umsatzes, Verwaltung und Vertrieb (H)** – `lernpakete/exkurs-vollkostenrechnung_b5_scorm2004.zip` – Voraussetzung: „B4 · BAB Schritt 3: Zuschlagssätze und Maschinenstundensatz“ abgeschlossen
- Lernpaket **★ Meilenstein 2: Auswertung des BAB – Auftrag & Checkliste** – `lernpakete/exkurs-vollkostenrechnung_b6_scorm2004.zip` – Voraussetzung: „B5 · BAB Schritt 3: Herstellkosten des Umsatzes, Verwaltung und Vertrieb (H)“ abgeschlossen
- Aufgabe **📤 BAB und Auswertung abgeben** – Voraussetzung: „B5 · BAB Schritt 3: Herstellkosten des Umsatzes, Verwaltung und Vertrieb (H)“ abgeschlossen – Dateiabgabe, höchstens 2 Datei(en), Dateitypen .pdf,.docx, 100 Punkte, Abschluss: „Abgabe erforderlich“
  Beschreibung: Lade dein fertiges **BAB-Formular**, die **Nebenrechnung** und das **Arbeitsblatt mit den Antworten** als **PDF** (z. B. gescannte Arbeitsblätter) oder als **Word-Datei** hoch. Keine Bilder. Wenn du in Excel gearbeitet hast, speichere die Tabelle als PDF.
  Bewertungsmethode **Bewertungsraster** mit diesen Kriterien:
  - Verteilung und Umlage: nicht erreicht (0 P.) · erreicht: Alle Gemeinkosten sind richtig auf die sieben Kostenstellen verteilt und die Vorkostenstellen richtig umgelegt. Zeilen- und Spaltenprobe stimmen. Fuhrpark und Fertigungsplanung stehen auf 0 €. (2 P.) · besonders gut: Die Rechenwege der Schlüssel sind notiert. (3 P.)
  - Zuschlagssätze und Maschinenstundensatz: nicht erreicht (0 P.) · erreicht: MGK, FGK I, Maschinenstundensatz und Restgemeinkosten-Satz sind richtig berechnet und gerundet. (2 P.) · besonders gut: Du erklärst einen Satz in einem Satz („Auf 100 € … entfallen …“). (3 P.)
  - Herstellkosten und Verwaltung/Vertrieb: nicht erreicht (0 P.) · erreicht: Die Nebenrechnung ist vollständig und stimmig. VwGK- und VtGK-Satz sind richtig. (2 P.) · besonders gut: Du nennst die Wirkung von Bestandsveränderungen mit eigenem Beispiel. (3 P.)
  - Auswertung: nicht erreicht (0 P.) · erreicht: Alle 13 Fragen sind beantwortet. Die Bedeutung der Sätze ist richtig erklärt und die Auftragsrechnungen stimmen. (2 P.) · besonders gut: Du erklärst die Differenz der Kosten (Frage 13) mit eigenen Worten und Zahlen. (3 P.)
  - Darstellung: nicht erreicht (0 P.) · erreicht: Alle drei Teile sind lesbar und vollständig. (2 P.) · besonders gut: Die Rechenwege sind durchgehend nachvollziehbar. (3 P.)

## Abschnitt „🏆 Von den Kosten zum Verkaufspreis“

Voraussetzung am Abschnitt (Einschränkung: Aktivitätsabschluss bzw. Bewertung, verknüpft mit „mindestens eine“): „📤 BAB und Auswertung abgeben“ abgeschlossen.

- Lernpaket **T1 · Ist- und Normalsätze** – `lernpakete/exkurs-vollkostenrechnung_t1_scorm2004.zip`
- Lernpaket **T2 · Zuschlagskalkulation bis zu den Selbstkosten** – `lernpakete/exkurs-vollkostenrechnung_t2_scorm2004.zip` – Voraussetzung: „T1 · Ist- und Normalsätze“ abgeschlossen
- Lernpaket **T3 · Vom Selbstkostenpreis zum Listenverkaufspreis (H)** – `lernpakete/exkurs-vollkostenrechnung_t3_scorm2004.zip` – Voraussetzung: „T2 · Zuschlagskalkulation bis zu den Selbstkosten“ abgeschlossen
- Lernpaket **★ Meilenstein 3: Kalkulation für den Rucksack Explorer – Auftrag & Checkliste** – `lernpakete/exkurs-vollkostenrechnung_tm_scorm2004.zip` – Voraussetzung: „T3 · Vom Selbstkostenpreis zum Listenverkaufspreis (H)“ abgeschlossen
- Aufgabe **📤 Kalkulation Explorer abgeben** – Voraussetzung: „T3 · Vom Selbstkostenpreis zum Listenverkaufspreis (H)“ abgeschlossen – Dateiabgabe, höchstens 2 Datei(en), Dateitypen .pdf,.docx, 100 Punkte, Abschluss: „Abgabe erforderlich“
  Beschreibung: Lade dein ausgefülltes Kalkulationsschema mit den Antworten auf die Auswertungsfragen als **PDF** (z. B. gescanntes Arbeitsblatt) oder als **Word-Datei** hoch. Keine Bilder. Wenn du in Excel gearbeitet hast, speichere die Tabelle als PDF.
  Bewertungsmethode **Bewertungsraster** mit diesen Kriterien:
  - Aufbau des Schemas: nicht erreicht (0 P.) · erreicht: Alle Zeilen stehen in der richtigen Reihenfolge. Die Zwischensummen (Materialkosten, Fertigungskosten I und II, Herstellkosten, Selbstkosten) sind enthalten. (2 P.) · besonders gut: Alle Zeilen sind ohne Hilfe und ohne Fehler aufgebaut. (3 P.)
  - Gemeinkosten und Maschinenplatz: nicht erreicht (0 P.) · erreicht: Die Zuschläge beziehen sich auf die richtigen Grundlagen. Maschinenkosten und Restgemeinkosten sind richtig berechnet. (2 P.) · besonders gut: Du erklärst in einem Satz, warum der Maschinenplatz einen eigenen Stundensatz hat. (3 P.)
  - Preisbildung: nicht erreicht (0 P.) · erreicht: Gewinn vom Hundert sowie Skonto und Rabatt im Hundert sind richtig gerechnet. Der Listenverkaufspreis stimmt. (2 P.) · besonders gut: Du führst eine Probe durch (rückwärts vom Listenpreis zum Barverkaufspreis). (3 P.)
  - Bemerkungen und Auswertung: nicht erreicht (0 P.) · erreicht: In der Bemerkungsspalte steht bei jeder Berechnung der Rechenweg. Die Fragen sind beantwortet. (2 P.) · besonders gut: Du begründest die Einordnung des Preises nachvollziehbar. (3 P.)
  - Darstellung: nicht erreicht (0 P.) · erreicht: Das Schema ist lesbar und vollständig. (2 P.) · besonders gut: Der Rechenweg ist durchgehend nachvollziehbar. (3 P.)
- Test **📝 Lernerfolgskontrolle: Von der GuV zum Verkaufspreis** – Voraussetzung: „★ Meilenstein 3: Kalkulation für den Rucksack Explorer – Auftrag & Checkliste“ abgeschlossen – 10 Fragen aus `fragen/` (Moodle-XML importieren, dann in den Test einfügen; Rechenaufgaben mit Varianten als Zufallsfrage aus ihrer Kategorie), Bewertung 10 Punkte, bestanden ab 60 %, Abschluss: „Bestehensgrenze erreichen“, Versuche unbegrenzt, Frageverhalten „Spätere Auswertung“

## Abschnitt „⭐ Übungen und Vertiefung (freiwillig)“

Voraussetzung am Abschnitt (Einschränkung: Aktivitätsabschluss bzw. Bewertung, verknüpft mit „mindestens eine“): „📤 Kalkulation Explorer abgeben“ abgeschlossen.

- Lernpaket **U1 · Übungs-BAB 1: Produktion Leder** – `lernpakete/exkurs-vollkostenrechnung_u1_scorm2004.zip`
- Lernpaket **U2 · Übungs-BAB 2: Produktion Textil** – `lernpakete/exkurs-vollkostenrechnung_u2_scorm2004.zip` – Voraussetzung: „U1 · Übungs-BAB 1: Produktion Leder“ abgeschlossen
- Lernpaket **U3 · Übungs-BAB 3: Produktion Kunststoffe** – `lernpakete/exkurs-vollkostenrechnung_u3_scorm2004.zip` – Voraussetzung: „U2 · Übungs-BAB 2: Produktion Textil“ abgeschlossen
- Lernpaket **U4 · Übungs-BAB 4: Zuschnittautomat und Bestandsmehrung** – `lernpakete/exkurs-vollkostenrechnung_u4_scorm2004.zip` – Voraussetzung: „U3 · Übungs-BAB 3: Produktion Kunststoffe“ abgeschlossen
- Lernpaket **U5 · Übung 5: Maschinenstundensatz herleiten** – `lernpakete/exkurs-vollkostenrechnung_u5_scorm2004.zip` – Voraussetzung: „U4 · Übungs-BAB 4: Zuschnittautomat und Bestandsmehrung“ abgeschlossen
- Lernpaket **U6 · Übung 6: Richtig oder falsch?** – `lernpakete/exkurs-vollkostenrechnung_u6_scorm2004.zip` – Voraussetzung: „U5 · Übung 5: Maschinenstundensatz herleiten“ abgeschlossen
- Test **📝 Test: Richtig oder falsch zum BAB** – Voraussetzung: „U6 · Übung 6: Richtig oder falsch?“ abgeschlossen – 8 Fragen aus `fragen/` (Moodle-XML importieren, dann in den Test einfügen; Rechenaufgaben mit Varianten als Zufallsfrage aus ihrer Kategorie), Bewertung 10 Punkte, bestanden ab 60 %, Abschluss: „Bestehensgrenze erreichen“, Versuche unbegrenzt, Frageverhalten „Direkte Auswertung“

