"""Erzeugt lehrkraft/Freigabe-Checkliste.docx. Aufruf (aus dem Lernpfad-Ordner): python3 werkzeuge/freigabe_checkliste.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from material_stufe1 import neues_dokument, tabelle, ueberschrift  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MODULE = [
    ("G1", "Von der GuV zu den Einzel- und Gemeinkosten", "45", "Definition Aufwand/Kosten; neutrale Posten (Zinsen als betriebsfremd) nur als Info; Leitfrage mit Werten der Lernsituation; GuV-Zahlen"),
    ("G2", "Kostenarten, Einzel- und Gemeinkosten vertiefen (H)", "70", "Kalkulatorische Kosten und Überleitung 229.925 → 266.925 €; kein Unternehmerlohn bei der GmbH; Kostenstellen direkt/Schlüssel"),
    ("MS 1", "Kostenartenplan August", "45", "Raster, Abgabe als PDF oder Word; Lösung in lehrkraft/"),
    ("B1", "Der BAB: Gemeinkosten verteilen", "60", "Fünf Kostenstellen (Fertigung II = Maschinenplatz); Schlüsselzahlen sind eigene Annahmen"),
    ("B2", "Zuschlagssätze Material und Fertigung (H)", "45", "Zuschlagsgrundlage Fertigung I = nur Handarbeitslöhne"),
    ("B3", "Der Maschinenplatz", "45", "Trennung maschinenabhängig / Rest; Einstieg mit 608,57 %"),
    ("B4", "Herstellkosten des Umsatzes, Verwaltung/Vertrieb (H)", "45", "Keine Bestandsveränderungen; Summe 20,30 % statt 20 %"),
    ("MS 2", "BAB August", "90", "Umfang realistisch? Auswertungsfragen, Raster"),
    ("BX", "Erweiterung: Vorkostenstellen (freiwillig)", "45", "Treppenstufenverfahren = Stufenleiterverfahren; Reihenfolge; Ergebnis mit Absicht wie Juli"),
    ("T1", "Ist- und Normalsätze", "30", "Vier Monate statt üblicher zwölf; Plus zur Kostenunterdeckung ist weiterführend"),
    ("T2", "Zuschlagskalkulation bis zu den Selbstkosten", "45", "Ergebnis 108,60 € wie in der Lernsituation"),
    ("T3", "Vom Selbstkostenpreis zum Listenverkaufspreis (H)", "45", "„im Hundert“ bei Skonto und Rabatt; Ergebnis 149,28 €"),
    ("MS 3", "Kalkulation Explorer", "45", "Zahlen (117,89 €) und Vergleich mit 149 € in der Artikelliste"),
    ("Test", "Lernerfolgskontrolle (Moodle-Test)", "20", "10 Fragen, Zufallszahlen, Reihenfolge-Frage braucht Moodle ab 4.4"),
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
    d = neues_dokument("Freigabe-Checkliste: Exkurs Vollkostenrechnung", "Stand 05.11.2026 · alle Module auf „geprüft“, noch keines freigegeben")
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
