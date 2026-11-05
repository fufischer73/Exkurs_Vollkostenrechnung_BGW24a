"""Erzeugt lehrkraft/Freigabe-Checkliste.docx. Aufruf (aus dem Lernpfad-Ordner): python3 werkzeuge/freigabe_checkliste.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from material_stufe1 import neues_dokument, tabelle, ueberschrift  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MODULE = [
    ("G1", "Von der GuV zu den Einzel- und Gemeinkosten", "45", "NEU, Entwurf: Situation und Arbeitsauftrag zuerst, Info als Hilfe; neutrale Posten nur als Info (Zinsen betriebsfremd)"),
    ("G2", "Kostenarten und Kostenartenplan (H)", "55", "NEU, Entwurf: kalkulatorische Kosten und Überleitung 229.925 → 266.925 €; kein Unternehmerlohn bei der GmbH"),
    ("MS 1", "Kostenartenplan August", "40", "geprüft: Raster, Abgabe als PDF oder Word"),
    ("B1", "Brücke: Wo fallen die Gemeinkosten an?", "25", "Entwurf: Fuhrpark und Fertigungsplanung sind für den Exkurs ergänzt (nicht im Organigramm der Einführung)"),
    ("B2", "BAB Schritt 1: Verteilung", "50", "Entwurf: BAB-Formular nach deiner Vorlage, Schlüsselzahlen sind eigene Annahmen"),
    ("B3", "BAB Schritt 2: Umlage", "40", "Entwurf: Treppenstufenverfahren, Umlagen zählen zu den Restgemeinkosten"),
    ("B4", "BAB Schritt 3: Zuschlagssätze und Maschinenplatz", "50", "Entwurf: Zuschlagsgrundlage Fertigung I nur Handarbeit, 608,57 %-Denkanstoß"),
    ("B5", "Herstellkosten des Umsatzes, Verwaltung/Vertrieb (H)", "35", "Entwurf: keine Bestandsveränderungen, 20,30 % statt 20 %"),
    ("MS 2", "Auswertung des BAB (B6)", "45", "Entwurf: Abgabe von BAB-Formular, Nebenrechnung und 13 Antworten"),
    ("T1", "Ist- und Normalsätze", "30", "NEU, Entwurf: vier Monate statt üblicher zwölf; Plus zur Kostenunterdeckung ist weiterführend"),
    ("T2", "Zuschlagskalkulation bis zu den Selbstkosten", "45", "NEU, Entwurf: Ergebnis 108,60 € wie in der Lernsituation"),
    ("T3", "Vom Selbstkostenpreis zum Listenverkaufspreis (H)", "40", "NEU, Entwurf: „im Hundert“ bei Skonto und Rabatt; Ergebnis 149,28 €"),
    ("MS 3", "Kalkulation Explorer", "40", "geprüft: Zahlen (117,89 €) und Vergleich mit 149 € in der Artikelliste"),
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
    d = neues_dokument("Freigabe-Checkliste: Exkurs Vollkostenrechnung", "Stand 05.11.2026 · alle Stufen im neuen Aufbau (Entwurf), noch kein Modul freigegeben")
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
