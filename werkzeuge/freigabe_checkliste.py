"""Erzeugt lehrkraft/Freigabe-Checkliste.docx. Aufruf (aus dem Lernpfad-Ordner): python3 werkzeuge/freigabe_checkliste.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from material_stufe1 import neues_dokument, tabelle, ueberschrift  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MODULE = [
    ("G1", "Von der GuV zu den Einzel- und Gemeinkosten", "40", "geprüft (wird noch auf Situation + Arbeitsauftrag zuerst angepasst)"),
    ("G2", "Kostenarten, Einzel- und Gemeinkosten vertiefen (H)", "50", "geprüft (wird noch angepasst)"),
    ("MS 1", "Kostenartenplan August", "35", "geprüft"),
    ("B1", "Brücke: Wo fallen die Gemeinkosten an?", "25", "NEU, Entwurf: Fuhrpark und Fertigungsplanung sind für den Exkurs ergänzt (nicht im Organigramm der Einführung)"),
    ("B2", "BAB Schritt 1: Verteilung", "50", "NEU, Entwurf: drei Hilfestufen, Schlüsselzahlen sind eigene Annahmen"),
    ("B3", "BAB Schritt 2: Umlage", "40", "NEU, Entwurf: Treppenstufenverfahren, Umlagen zählen zu den Restgemeinkosten"),
    ("B4", "BAB Schritt 3: Zuschlagssätze und Maschinenplatz", "50", "NEU, Entwurf: Zuschlagsgrundlage Fertigung I nur Handarbeit, 608,57 %-Denkanstoß"),
    ("B5", "Herstellkosten des Umsatzes, Verwaltung/Vertrieb (H)", "35", "NEU, Entwurf: keine Bestandsveränderungen, 20,30 % statt 20 %"),
    ("B6", "Auswertung des BAB", "35", "NEU, Entwurf: 13 Fragen zum fertigen BAB"),
    ("MS 2", "BAB August", "65", "NEU, Entwurf: mit Umlage, Umfang realistisch?"),
    ("T1", "Ist- und Normalsätze", "30", "Entwurf (August-Zahlen angepasst); vier Monate statt üblicher zwölf"),
    ("T2", "Zuschlagskalkulation bis zu den Selbstkosten", "45", "geprüft (wird noch angepasst)"),
    ("T3", "Vom Selbstkostenpreis zum Listenverkaufspreis (H)", "45", "geprüft (wird noch angepasst)"),
    ("MS 3", "Kalkulation Explorer", "45", "geprüft"),
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
    d = neues_dokument("Freigabe-Checkliste: Exkurs Vollkostenrechnung", "Stand 05.11.2026 · Stufe 2 neu aufgebaut (Entwurf), noch kein Modul freigegeben")
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
