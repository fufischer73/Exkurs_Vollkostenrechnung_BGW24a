"""Erzeugt lehrkraft/Freigabe-Checkliste.docx. Aufruf (aus dem Lernpfad-Ordner): python3 werkzeuge/freigabe_checkliste.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from material_stufe1 import neues_dokument, tabelle, ueberschrift  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MODULE = [
    ("G1", "Von der GuV zu den Einzel- und Gemeinkosten", "45", "freigegeben; Situation und Arbeitsauftrag zuerst, Info als Hilfe; neutrale Posten nur als Info (Zinsen betriebsfremd)"),
    ("G2", "Kostenarten und Kostenartenplan (H)", "55", "freigegeben; kalkulatorische Kosten und Überleitung 229.925 → 266.925 €; kein Unternehmerlohn bei der GmbH"),
    ("MS 1", "Kostenartenplan August", "40", "freigegeben; Raster, Abgabe als PDF oder Word"),
    ("B1", "Brücke: Wo fallen die Gemeinkosten an?", "25", "freigegeben; Fuhrpark und Fertigungsplanung sind für den Exkurs ergänzt (nicht im Organigramm der Einführung)"),
    ("B2", "BAB Schritt 1: Verteilung", "50", "freigegeben; BAB-Formular nach deiner Vorlage, Schlüsselzahlen sind eigene Annahmen"),
    ("B3", "BAB Schritt 2: Umlage", "40", "freigegeben; Treppenstufenverfahren, Umlagen zählen zu den Restgemeinkosten"),
    ("B4", "BAB Schritt 3: Zuschlagssätze und Maschinenplatz", "50", "freigegeben; Zuschlagsgrundlage Fertigung I nur Handarbeit, 608,57 %-Denkanstoß"),
    ("B5", "Herstellkosten des Umsatzes, Verwaltung/Vertrieb (H)", "35", "freigegeben; keine Bestandsveränderungen, 20,30 % statt 20 %"),
    ("MS 2", "Auswertung des BAB (B6)", "45", "freigegeben; Abgabe von BAB-Formular, Nebenrechnung und 13 Antworten"),
    ("T1", "Ist- und Normalsätze", "30", "freigegeben; vier Monate statt üblicher zwölf; Plus zur Kostenunterdeckung ist weiterführend"),
    ("T2", "Zuschlagskalkulation bis zu den Selbstkosten", "45", "freigegeben; Ergebnis 108,60 € wie in der Lernsituation"),
    ("T3", "Vom Selbstkostenpreis zum Listenverkaufspreis (H)", "40", "freigegeben; „im Hundert“ bei Skonto und Rabatt; Ergebnis 149,28 €"),
    ("MS 3", "Kalkulation Explorer", "40", "freigegeben; Zahlen (117,89 €) und Vergleich mit 149 € in der Artikelliste"),
    ("U1", "Übungs-BAB 1: Produktion Leder (freiwillig)", "40", "freigegeben; eine allgemeine Kostenstelle (Fuhrpark), Zahlen frei konstruiert"),
    ("U2", "Übungs-BAB 2: Produktion Textil (freiwillig)", "40", "freigegeben; Hilfskostenstelle Werkstatt, zwei Fertigungsstellen"),
    ("U3", "Übungs-BAB 3: Produktion Kunststoffe (freiwillig)", "45", "freigegeben; Arbeitsvorbereitung, Bestandsminderung 15.000 €"),
    ("U4", "Übungs-BAB 4: Zuschnittautomat (freiwillig)", "45", "freigegeben; Maschinenstundensatz, Restgemeinkosten, Bestandsmehrung 24.000 €"),
    ("U5", "Übung 5: Maschinenstundensatz herleiten (freiwillig)", "40", "freigegeben; Vereinfachungen (Energie mit vollem Anschlusswert, Zinsen auf halbe Anschaffungskosten); Fachaussage bitte prüfen"),
    ("U6", "Übung 6: Richtig oder falsch? (freiwillig)", "15", "freigegeben; acht Aussagen, dazu Moodle-Test"),
    ("Test", "Lernerfolgskontrolle (Moodle-Test)", "15", "10 Fragen, Zufallszahlen, Reihenfolge-Frage braucht Moodle ab 4.4"),
]
OFFEN = [
    "Websuche vom 05.11.2026: Die Fachaussagen (Treppenstufenverfahren, Maschinenstundensatz und Restgemeinkosten, Normalsätze, Skonto/Rabatt im Hundert, Herstellkosten des Umsatzes, Unternehmerlohn bei der GmbH) decken sich mit den gefundenen Lehr- und Fachseiten. Gelesen wurden nur die Suchtreffer, nicht die vollständigen Seiten. Die Quellen stehen deshalb in quellen.yaml auf „zu_pruefen“.",
    "Lehrplanbezug: Der Abgleich mit dem Lehrplan des Beruflichen Gymnasiums (BRC) fehlt, weil er nicht vorlag.",
    "Begriffe: Nenne ich „Herstellkosten“ (nicht „Herstellungskosten“ nach HGB) so, wie ihr es im Unterricht tut?",
    "Alle Zahlen, Schlüssel und Fälle sind für den Lernpfad frei konstruiert. Das Westermann-Material diente nur als Strukturvorlage.",
    "Moodle-Version: Ich habe mit Moodle 5 gebaut. Läuft bei euch Moodle 4, würden die Unterabschnitte entfallen.",
    "Ein Test des Kurses in Moodle (Wiederherstellen, als Schüler:in durchklicken) steht noch aus.",
]


def main():
    d = neues_dokument("Freigabe-Checkliste: Exkurs Vollkostenrechnung", "Stand 05.11.2026 · alle Module und Tests freigegeben")
    ueberschrift(d, "So gibst du frei")
    d.add_paragraph("Lies ein Modul in der Web-Version, prüfe die Punkte rechts und sage Claude: „Modul G1 ist freigegeben“ (oder „alles“). "
                    "Nur freigegebene Module kommen in den Moodle-Kurs. Nach einer größeren Änderung geht ein Modul zurück auf „geprüft“.")
    ueberschrift(d, "Module")
    tabelle(d, ["Nr.", "Titel", "Min", "Besonders prüfen", "OK"], [(a, b, c, e, "☐") for a, b, c, e in MODULE], [1.2, 4.6, 1.1, 8.6, 1.0])
    ueberschrift(d, "Offene Punkte")
    for o in OFFEN:
        d.add_paragraph("• " + o)
    d.save(ROOT / "lehrkraft/Freigabe-Checkliste.docx")
    print("✓ Freigabe-Checkliste erzeugt")


if __name__ == "__main__":
    main()
