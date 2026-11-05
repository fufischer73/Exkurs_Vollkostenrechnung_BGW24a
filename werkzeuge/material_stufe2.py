"""Erzeugt Arbeitsblätter (docx), Infoblätter (docx aus seiten/), Excel-Vorlage und Lehrkraft-Lösungen für Stufe 2 (BAB).
Aufruf (aus dem Lernpfad-Ordner):  python3 werkzeuge/material_stufe2.py
PDFs entstehen mit werkzeuge/pdfs.py.
"""
import re
import subprocess
import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side

sys.path.insert(0, str(Path(__file__).parent))
from daten import (JULI, AUGUST, ORDER, SP7, HAUPT, SCHLUESSEL, UMLAGE_FUHRPARK, UMLAGE_PLANUNG,  # noqa: E402
                   MASCHINENABHAENGIG, auswerten, umlage, fmt)
from material_stufe1 import neues_dokument, tabelle, ueberschrift  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
KURZ = ["Fuhrpark", "Material", "Fertigungs-planung", "Fertigung I", "Fertigung II", "Verwaltung", "Vertrieb"]
DIREKT = [a for a in ORDER if a not in SCHLUESSEL]


def f0(x):
    return fmt(x, 0)


def quer(titel, untertitel="Montelli GmbH · Geschäftsbereich Outdoor · Exkurs Vollkostenrechnung"):
    d = neues_dokument(titel, untertitel)
    s = d.sections[0]
    s.orientation = WD_ORIENT.LANDSCAPE
    s.page_width, s.page_height = Cm(29.7), Cm(21)
    s.left_margin = s.right_margin = Cm(1.2)
    s.top_margin = s.bottom_margin = Cm(1.2)
    return d


def hoch(titel, untertitel="Montelli GmbH · Geschäftsbereich Outdoor · Exkurs Vollkostenrechnung"):
    return neues_dokument(titel, untertitel)


def linien(d, n=2, breite=78):
    for _ in range(n):
        d.add_paragraph("_" * breite)


# ---------------------------------------------------------------- Bausteine
def bab_tabelle(d, m, voll=False):
    bab = m["bab"]
    zeilen = []
    for art in ORDER:
        v = bab[art]
        zeilen.append([art, f0(sum(v))] + ([f0(x) for x in v] if voll else [""] * 7))
    prim = [sum(v[i] for v in bab.values()) for i in range(7)]
    zeilen.append(["Summe", f0(sum(prim))] + ([f0(x) for x in prim] if voll else [""] * 7))
    tabelle(d, ["Gemeinkostenart", "Summe"] + KURZ, zeilen, [4.6, 2.4] + [2.9] * 7, rechts=tuple(range(1, 9)),
            fett_zeilen=(len(zeilen) - 1,), leer_hoehe=None if voll else 0.8)


def belege_tabellen(d, m):
    ueberschrift(d, "Direkte Zuordnung (Belegauswertung, Beträge in €)")
    zeilen = [[k] + [f0(m["bab"][a][i]) for a in DIREKT] for i, k in enumerate(SP7)]
    tabelle(d, ["Kostenstelle"] + DIREKT, zeilen, [5.4] + [4.3] * 5, rechts=(1, 2, 3, 4, 5))
    ueberschrift(d, "Verteilungsschlüssel (Schlüsselzahlen)")
    kopf = ["Kostenstelle"] + [f"{a}: {SCHLUESSEL[a][0]}" for a in SCHLUESSEL]
    zeilen = [[k] + [str(SCHLUESSEL[a][1][i]) for a in SCHLUESSEL] for i, k in enumerate(SP7)]
    tabelle(d, kopf, zeilen, [6, 6.5, 8, 6], rechts=(1, 2, 3))


def umlage_schluessel_tabelle(d):
    zeilen = [[k, str(UMLAGE_FUHRPARK.get(k, "")) if k != "Fuhrpark" else "", str(UMLAGE_PLANUNG[k]) if k in UMLAGE_PLANUNG else "–"]
              for k in SP7 if k not in ("Fuhrpark",)]
    zeilen = [[a, b if b != "" else "", c] for a, b, c in zeilen]
    tabelle(d, ["Kostenstelle", "Fuhrpark: Transportaufträge", "Fertigungsplanung: Planungsstunden"], zeilen, [6, 7, 8], rechts=(1, 2))


def umlage_tabelle(d, m=None):
    rows = []
    if m:
        prim, u1, zw, u2, end = umlage(m)
        for k in SP7:
            if k == "Fuhrpark":
                rows.append([k, f0(prim[k]), f0(-prim[k]), "0", "", "0"])
            elif k == "Fertigungsplanung":
                rows.append([k, f0(prim[k]), "+" + f0(u1[k]), f0(zw[k]), f0(-zw[k]), "0"])
            else:
                rows.append([k, f0(prim[k]), "+" + f0(u1[k]) if u1.get(k) else "0", f0(zw[k]),
                             "+" + f0(u2[k]) if u2.get(k) else "", f0(end[k])])
    else:
        rows = [[k, "", "", "", "", ""] for k in SP7]
    tabelle(d, ["Kostenstelle", "Nach Schritt 1", "Umlage Fuhrpark", "Zwischensumme", "Umlage Fert.-planung", "Endsumme"],
            rows, [5, 4.2, 4.2, 4.2, 4.6, 4.2], rechts=(1, 2, 3, 4, 5), leer_hoehe=None if m else 0.8)


def nebenrechnung(d, werte=None):
    z = ["Fertigungsmaterial", "+ Materialgemeinkosten (MGK)", "= Materialkosten", "Fertigungslöhne (Handarbeit)",
         "+ Fertigungsgemeinkosten (FGK)", "= Fertigungskosten I", "Maschinenabhängige Fertigungsgemeinkosten",
         "+ Fertigungslöhne des Maschinenplatzes", "+ Restgemeinkosten", "= Fertigungskosten II", "= Herstellkosten der Erzeugung",
         "+ Bestandsminderungen / − Bestandsmehrungen", "= Herstellkosten des Umsatzes"]
    rows = [(t, werte[i] if werte else "") for i, t in enumerate(z)]
    fett = tuple(i for i, t in enumerate(z) if t.startswith("="))
    tabelle(d, ["Nebenrechnung", "Betrag in €"], rows, [10, 5], rechts=(1,), fett_zeilen=fett, leer_hoehe=None if werte else 0.7)


def neben_werte(m):
    a = auswerten(m)
    fm, fl1, fl2 = a["fm"], m["fl1"], m["fl2"]
    mgk, fgk1, _, vw, vt = a["spalten"]
    masch, rest = a["masch"]
    mk, fk1, fk2 = fm + mgk, fl1 + fgk1, masch + fl2 + rest
    return [fmt(fm), fmt(mgk), fmt(mk), fmt(fl1), fmt(fgk1), fmt(fk1), fmt(masch), fmt(fl2), fmt(rest), fmt(fk2),
            fmt(mk + fk1 + fk2), fmt(0), fmt(a["saetze"]["HKdU"])]


# ---------------------------------------------------------------- Arbeitsblätter
BEREICHE = ["Einkauf, Wareneingang und Lager", "Fuhrpark: Gabelstapler und Lieferwagen für alle Bereiche",
            "Fertigungsplanung: Arbeitsvorbereitung für die Fertigung", "Zuschneiden, Nähen und Montage von Hand",
            "Zuschnitt- und Nähautomat", "Geschäftsführung, Personal, Finanzbuchhaltung, Controlling", "Marketing und Verkauf"]
LOES_KST = [("Material", "Hauptkostenstelle"), ("Fuhrpark", "allgemeine Kostenstelle"), ("Fertigungsplanung", "Hilfskostenstelle"),
            ("Fertigung I (Handarbeit)", "Hauptkostenstelle"), ("Fertigung II (Maschinenplatz)", "Hauptkostenstelle"),
            ("Verwaltung", "Hauptkostenstelle"), ("Vertrieb", "Hauptkostenstelle")]


def ab_b1(pfad):
    d = hoch("Arbeitsblatt B1 · Brücke: Kostenstellen der Montelli")
    ueberschrift(d, "Aufgabe 1 · Kostenstellen einordnen")
    d.add_paragraph("Ordne jeden Bereich einer Kostenstelle zu und gib die Art an: allgemeine Kostenstelle, Hilfskostenstelle "
                    "oder Hauptkostenstelle (Material, Fertigung, Verwaltung, Vertrieb).")
    tabelle(d, ["Nr.", "Bereich", "Kostenstelle", "Art"], [(str(i + 1), b, "", "") for i, b in enumerate(BEREICHE)],
            [1, 7.2, 4.5, 4.3], leer_hoehe=1.0)
    ueberschrift(d, "Aufgabe 2 · Der Kopf des BAB")
    d.add_paragraph("Schreibe die sieben Kostenstellen in der richtigen Reihenfolge von links nach rechts in den Kopf. "
                    "Markiere die Hauptkostenstellen.")
    t = d.add_table(rows=2, cols=7)
    t.style = "Table Grid"
    t.rows[0].height = Cm(1.6)
    for c, txt in zip(t.rows[1].cells, ["Art:"] * 7):
        c.text = txt
    d.save(pfad)


def ab_b2(pfad):
    d = quer("Arbeitsblatt B2 · BAB Schritt 1: Gemeinkosten verteilen (Juli)")
    ueberschrift(d, "Gemeinkosten aus dem Kostenartenplan Juli")
    tabelle(d, ["Gemeinkostenart", "Summe in €", "Verteilung"], [
        ("Hilfsstoffe", "8.000", "direkt (Belege)"), ("Betriebsstoffe", "18.000", "Schlüssel: Verbrauch in kWh"),
        ("Gehälter", "124.100", "direkt (Gehaltsliste)"), ("Kalk. Abschreibungen", "65.000", "direkt (Anlagendatei)"),
        ("Kalk. Zinsen", "30.000", "Schlüssel: gebundenes Kapital"), ("Fremdinstandhaltung", "8.050", "direkt (Rechnungen)"),
        ("Leasing", "10.200", "Schlüssel: Fläche in m²"), ("Büromaterial", "3.575", "direkt (Bestellungen)"),
        ("Summe", "266.925", "")], [6, 3.5, 8], rechts=(1,), fett_zeilen=(8,))
    belege_tabellen(d, JULI)
    ueberschrift(d, "Aufgabe · BAB Juli, Schritt 1 (Beträge in €)")
    d.add_paragraph("Verteile die Gemeinkosten auf die Kostenstellen. Probe: Zeilensummen = Kostenartenplan, Summe aller Spalten = 266.925 €.")
    bab_tabelle(d, JULI)
    d.save(pfad)


def ab_b3(pfad):
    d = quer("Arbeitsblatt B3 · BAB Schritt 2: Innerbetriebliche Leistungen verrechnen (Juli)")
    prim = umlage(JULI)[0]
    ueberschrift(d, "Gemeinkosten nach Schritt 1 (aus B2, Beträge in €)")
    tabelle(d, SP7_KOPF, [[f0(prim[k]) for k in SP7]], [3.9] * 7, rechts=tuple(range(7)))
    ueberschrift(d, "Umlageschlüssel")
    umlage_schluessel_tabelle(d)
    ueberschrift(d, "Aufgabe · Umlage im Treppenstufenverfahren")
    d.add_paragraph("1. Umlage Fuhrpark auf alle anderen Stellen, Zwischensummen bilden.  2. Umlage Fertigungsplanung auf Fertigung I und II.  "
                    "Probe: Vorkostenstellen = 0 €, Summe der Hauptkostenstellen = 266.925 €.")
    umlage_tabelle(d)
    d.save(pfad)


SP7_KOPF = ["Fuhrpark", "Material", "Fertigungsplanung", "Fertigung I", "Fertigung II", "Verwaltung", "Vertrieb"]


def bezug_tabelle(d, m):
    a = auswerten(m)
    tabelle(d, ["Bezugsgröße", "Wert"], [
        ("Fertigungsmaterial (Rohstoffe + Vorprodukte/Fremdbauteile)", fmt(a["fm"]) + " €"),
        ("Fertigungslöhne Handarbeit (Fertigung I)", fmt(m["fl1"]) + " €"),
        ("Fertigungslöhne Maschinenplatz (Fertigung II)", fmt(m["fl2"]) + " €"),
        ("Maschinenstunden Maschinenplatz", f"{m['masch_std']} h"), ("Bestandsveränderungen", "keine")], [11, 5], rechts=(1,))


def ab_b4(pfad):
    d = hoch("Arbeitsblatt B4 · BAB Schritt 3: Zuschlagssätze und Maschinenplatz (Juli)")
    ueberschrift(d, "Angaben")
    bezug_tabelle(d, JULI)
    d.add_paragraph("Gemeinkosten nach der Umlage: Material 39.400 € · Fertigung I 50.625 € · Fertigung II 85.200 €")
    i2 = SP7.index("Fertigung II")
    rows = [(a, fmt(JULI["bab"][a][i2], 0) + " €") for a in ORDER] + [("Umlage Fuhrpark und Fertigungsplanung", "2.000 €"), ("Summe nach Umlage", "85.200 €")]
    tabelle(d, ["Fertigung II: Gemeinkostenart", "Betrag"], rows, [11, 5], rechts=(1,), fett_zeilen=(len(rows) - 1,))
    ueberschrift(d, "Aufgabe 1 · Material und Fertigung I")
    d.add_paragraph("MGK-Satz = Gemeinkosten Material × 100 ÷ Fertigungsmaterial = ____________________ = ________ %")
    d.add_paragraph("FGK-Satz (Fertigung I) = Gemeinkosten Fertigung I × 100 ÷ Fertigungslöhne Handarbeit = ____________________ = ________ %")
    d.add_paragraph("Bedeutung: Auf 100 € ____________________ entfallen ________ € ____________________.")
    d.add_paragraph("Auftrag: Fertigungsmaterial 4.200 €, Fertigungslöhne Handarbeit 2.600 €. MGK = __________ €, FGK = __________ €.")
    ueberschrift(d, "Aufgabe 2 · Maschinenplatz")
    d.add_paragraph("Denkanstoß: Gemeinkosten Fertigung II × 100 ÷ Maschinenplatzlöhne = ____________ %. Was fällt dir auf?")
    linien(d, 1)
    d.add_paragraph("Maschinenabhängige Gemeinkosten: __________ €   Restgemeinkosten: __________ €   (zusammen 85.200 €)")
    d.add_paragraph("Maschinenstundensatz = maschinenabhängige Gemeinkosten ÷ Maschinenstunden = ____________________ = ________ € je h")
    d.add_paragraph("Restgemeinkosten-Satz = Restgemeinkosten × 100 ÷ Maschinenplatzlöhne = ____________________ = ________ %")
    d.add_paragraph("Auftrag: 2 Maschinenstunden, Maschinenplatzlöhne 28 €. Maschinenkosten = __________ €, Restgemeinkosten = __________ €.")
    d.save(pfad)


def ab_b5(pfad):
    d = hoch("Arbeitsblatt B5 · Herstellkosten des Umsatzes, Verwaltung und Vertrieb (Juli)")
    ueberschrift(d, "Angaben")
    bezug_tabelle(d, JULI)
    d.add_paragraph("Gemeinkosten: Material 39.400 € · Fertigung I 50.625 € · Maschinenabhängig (Fertigung II) 81.000 € · Restgemeinkosten 4.200 € · "
                    "Verwaltung 56.000 € · Vertrieb 35.700 €")
    ueberschrift(d, "Aufgabe 1 · Nebenrechnung")
    nebenrechnung(d)
    ueberschrift(d, "Aufgabe 2 · Verwaltung und Vertrieb")
    d.add_paragraph("VwGK-Satz = Gemeinkosten Verwaltung × 100 ÷ Herstellkosten des Umsatzes = ____________________ = ________ %")
    d.add_paragraph("VtGK-Satz = Gemeinkosten Vertrieb × 100 ÷ Herstellkosten des Umsatzes = ____________________ = ________ %")
    d.add_paragraph("Summe beider Sätze: ________ %   (Lernsituation: 20 %)")
    d.save(pfad)


FRAGEN = [
    "Wie viele Gemeinkosten fielen in den Vorkostenstellen Fuhrpark und Fertigungsplanung an?",
    "Auf welche Höhe beliefen sich die Gemeinkosten der Hauptkostenstellen nach der Verrechnung der innerbetrieblichen Leistungen?",
    "Wie hoch war der MGK-Zuschlagssatz und was sagt dieser Wert aus?",
    "Wie hoch wären die Materialgemeinkosten für einen Auftrag mit Fertigungsmaterial von 3.000 €?",
    "Wie hoch war der FGK-Zuschlagssatz der Fertigung I und was sagt er aus?",
    "Wie hoch wären die Fertigungsgemeinkosten für einen Auftrag mit Fertigungslöhnen (Handarbeit) von 5.200 €?",
    "Wie hoch war der Maschinenstundensatz und was sagt er aus?",
    "Wie hoch wären die Maschinenkosten, wenn der Maschinenplatz für einen Auftrag 2,5 Stunden benötigt wird?",
    "Was sagt der Restgemeinkosten-Zuschlagssatz des Maschinenplatzes aus?",
    "Wie hoch wären die Restgemeinkosten für einen Auftrag mit Maschinenplatzlöhnen von 3.600 €?",
    "Wie hoch waren die Herstellkosten des Umsatzes im Juli?",
    "Wie hoch waren der VwGK- und der VtGK-Zuschlagssatz und was sagen sie aus?",
    "Wie erklärst du dir die Differenz zwischen den Gesamtkosten aus dem Kostenartenplan und den Herstellkosten des Umsatzes?",
]
ANTW = [
    "Fuhrpark 11.000 €, Fertigungsplanung 3.000 € (nach der ersten Umlage 4.000 €).",
    "Material 39.400 €, Fertigung I 50.625 €, Fertigung II 85.200 €, Verwaltung 56.000 €, Vertrieb 35.700 € (zusammen 266.925 €).",
    "19,70 %. Auf 100 € Fertigungsmaterial entfallen 19,70 € Materialgemeinkosten.",
    "3.000 € × 19,70 ÷ 100 = 591,00 €.",
    "81,00 %. Auf 100 € Fertigungslöhne der Handarbeit entfallen 81 € Fertigungsgemeinkosten.",
    "5.200 € × 81 ÷ 100 = 4.212,00 €.",
    "81,00 € je Stunde. Pro Stunde Laufzeit verursacht der Maschinenplatz 81 € maschinenabhängige Gemeinkosten.",
    "2,5 h × 81 €/h = 202,50 €.",
    "30,00 %. Auf 100 € Maschinenplatzlöhne entfallen 30 € Restgemeinkosten (nicht von der Laufzeit abhängig, auch umgelegte Kosten).",
    "3.600 € × 30 ÷ 100 = 1.080,00 €.",
    "451.725,00 €.",
    "VwGK 12,40 %: Auf 100 € Herstellkosten des Umsatzes entfallen 12,40 € Verwaltungsgemeinkosten. VtGK 7,90 %: 7,90 € Vertriebsgemeinkosten.",
    "543.425 € − 451.725 € = 91.700 €: die Verwaltungs- (56.000 €) und Vertriebsgemeinkosten (35.700 €). Selbstkosten = HKdU + Verwaltungs- und Vertriebsgemeinkosten.",
]


def ab_b6(pfad):
    d = hoch("Arbeitsblatt B6 · Auswertung des BAB (Juli)")
    d.add_paragraph("Beantworte die Fragen mit deinem BAB aus den Modulen B2 bis B5. Rechenwege bitte notieren.")
    for i, f in enumerate(FRAGEN):
        d.add_paragraph(f"{i + 1}. {f}")
        linien(d, 2)
    d.save(pfad)


def ab_bm(pfad):
    d = quer("Arbeitsblatt Meilenstein 2 · BAB und Zuschlagssätze August")
    ueberschrift(d, "Bezugsgrößen August")
    bezug_tabelle(d, AUGUST)
    belege_tabellen(d, AUGUST)
    d.add_paragraph("Die Verteilungsschlüssel (Schlüsselzahlen) und die Umlageschlüssel gelten unverändert wie im Juli:")
    umlage_schluessel_tabelle(d)
    ueberschrift(d, "Aufgabe 1 · BAB August, Schritt 1 (Beträge in €)")
    d.add_paragraph("Summen je Zeile aus dem Kostenartenplan August: Hilfsstoffe 7.200 · Betriebsstoffe 16.200 · Gehälter 124.100 · "
                    "Kalk. Abschreibungen 65.000 · Kalk. Zinsen 30.000 · Fremdinstandhaltung 5.100 · Leasing 10.200 · Büromaterial 3.600")
    bab_tabelle(d, AUGUST)
    ueberschrift(d, "Aufgabe 2 · Umlage")
    umlage_tabelle(d)
    ueberschrift(d, "Aufgabe 3 · Maschinenplatz und Zuschlagssätze")
    d.add_paragraph("Maschinenabhängige Gemeinkosten (Fertigung II): __________ €   Restgemeinkosten (inkl. Umlagen): __________ €")
    tabelle(d, ["Satz", "Rechnung", "Ergebnis"], [("MGK-Satz", "", ""), ("FGK-Satz (Fertigung I)", "", ""), ("Maschinenstundensatz", "", ""),
                                                   ("Restgemeinkosten-Satz", "", "")], [6, 15, 5], leer_hoehe=0.8)
    ueberschrift(d, "Aufgabe 4 · Herstellkosten des Umsatzes, Verwaltung und Vertrieb")
    nebenrechnung(d)
    tabelle(d, ["Satz", "Rechnung", "Ergebnis"], [("VwGK-Satz", "", ""), ("VtGK-Satz", "", "")], [6, 15, 5], leer_hoehe=0.8)
    ueberschrift(d, "Aufgabe 5 · Auswertung")
    for f in ["1. In welcher Hauptkostenstelle fällt nach der Umlage der größte Gemeinkostenbetrag an? Wie hoch ist er?",
              "2. Vergleiche die Sätze mit Juli. Welche sind gestiegen? Erkläre.",
              "3. Ein Kunde bestellt Rucksäcke mit Fertigungsmaterial von 3.000 €. Wie hoch sind die Materialgemeinkosten?",
              "4. Was bedeutet dein Maschinenstundensatz in einem Satz?"]:
        d.add_paragraph(f)
        linien(d, 2, 110)
    d.save(pfad)


def loesungen(pfad):
    d = quer("Lehrkraft: Lösungen Stufe 2", "Nicht an Schüler:innen weitergeben.")
    for m, titel in ((JULI, "Juli (B2 bis B6)"), (AUGUST, "August (Meilenstein 2)")):
        a = auswerten(m)
        r = a["saetze"]
        ueberschrift(d, f"BAB {titel}: Schritt 1")
        bab_tabelle(d, m, voll=True)
        ueberschrift(d, f"BAB {titel}: Schritt 2 (Umlage)")
        umlage_tabelle(d, m)
        d.add_paragraph(f"Maschinenabhängig (Fertigung II): {fmt(a['masch'][0])} € · Rest einschließlich Umlagen: {fmt(a['masch'][1])} € · "
                        f"Maschinenstunden: {m['masch_std']} h · Maschinenplatzlöhne: {fmt(m['fl2'])} €")
        tabelle(d, ["Satz", "Wert"], [
            ("MGK-Satz", f"{r['MGK %']:.2f} %".replace(".", ",")), ("FGK-Satz (Fertigung I)", f"{r['FGK I %']:.2f} %".replace(".", ",")),
            ("Maschinenstundensatz", f"{r['Maschinenstundensatz']:.2f} € je h".replace(".", ",")),
            ("Restgemeinkosten-Satz", f"{r['Rest %']:.2f} %".replace(".", ",")),
            ("VwGK-Satz", f"{r['VwGK %']:.2f} %".replace(".", ",")), ("VtGK-Satz", f"{r['VtGK %']:.2f} %".replace(".", ","))], [8, 6], rechts=(1,))
        nebenrechnung(d, neben_werte(m))
    ueberschrift(d, "B1: Lösung")
    tabelle(d, ["Nr.", "Bereich", "Kostenstelle", "Art"], [(str(i + 1), BEREICHE[i]) + LOES_KST[i] for i in range(7)], [1, 9, 5, 5])
    d.add_paragraph("Reihenfolge im BAB-Kopf: Fuhrpark | Material | Fertigungsplanung | Fertigung I | Fertigung II | Verwaltung | Vertrieb")
    ueberschrift(d, "B6: Auswertung Juli")
    tabelle(d, ["Nr.", "Antwort"], [(str(i + 1), ANTW[i]) for i in range(13)], [1, 24])
    mgk_aug = 3000 * auswerten(AUGUST)["saetze"]["MGK %"] / 100
    d.add_paragraph("Meilenstein 2, Auswertung August (Erwartungshorizont): 1. Größter Betrag in Fertigung II (81.240 €). "
                    "2. Alle Sätze sind höher als im Juli, weil die Menge (Fertigungsmaterial, Löhne, Maschinenstunden) sank und die Gemeinkosten "
                    "kaum (Abschreibungen, Zinsen, Gehälter, Leasing bleiben gleich). "
                    f"3. 3.000 € × 21,77 ÷ 100 = {fmt(round(mgk_aug, 2))} €. 4. Eine Maschinenstunde verursacht 85,61 € Maschinenkosten.")
    d.add_paragraph("Hinweis: Bei Rundung der Sätze auf zwei Dezimalstellen kann die Nachrechnung um wenige Cent abweichen. Das ist in Ordnung.")
    d.save(pfad)


# ---------------------------------------------------------------- Infoblätter aus seiten/*.md
def rahmen(tabelle_):
    tbl = tabelle_._tbl
    pr = tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for seite in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{seite}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "4")
        e.set(qn("w:color"), "808080")
        b.append(e)
    pr.append(b)


def info_docs():
    for md in sorted((ROOT / "seiten").glob("info-*.md")):
        text = md.read_text(encoding="utf-8")
        m = re.match(r"---\n(.*?)\n---\n(.*)", text, flags=re.S)
        titel = re.search(r'titel: "?(.*?)"?\n', m.group(1)).group(1)
        body = f"# {titel}\n\n*Montelli GmbH · Exkurs Vollkostenrechnung*\n\n" + m.group(2)
        nummer = md.stem.split("-")[1]
        name = "-".join(md.stem.split("-")[2:])
        ziel = ROOT / "material" / f"Info-{nummer}-{name}.docx"
        tmp = ROOT / "werkzeuge" / "_tmp_info.md"
        tmp.write_text(body, encoding="utf-8")
        subprocess.run(["pandoc", str(tmp), "-o", str(ziel)], check=True)
        tmp.unlink()
        d = Document(str(ziel))
        for stil in ("Normal", "Body Text", "First Paragraph", "Compact"):
            try:
                d.styles[stil].font.name = "Arial"
                d.styles[stil].font.size = Pt(10)
            except KeyError:
                pass
        for t in d.tables:
            rahmen(t)
        s = d.sections[0]
        s.left_margin = s.right_margin = Cm(2)
        d.save(str(ziel))


# ---------------------------------------------------------------- Excel
def xlsx_bab(pfad):
    wb = Workbook()
    ws = wb.active
    ws.title = "BAB"
    gelb = PatternFill("solid", fgColor="FFF2CC")
    kopf = PatternFill("solid", fgColor="D9E2F3")
    rh = Border(*(Side(style="thin"),) * 4)
    fmt2 = "#,##0.00"
    ws["A1"] = "Betriebsabrechnungsbogen (BAB) – Montelli GmbH, Geschäftsbereich Outdoor"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "Gelbe Felder ausfüllen. Summen, Umlage, Sätze und Herstellkosten rechnet die Tabelle (Beträge in €)."
    heads = ["Gemeinkostenart", "Summe (Kostenartenplan)"] + SP7_KOPF + ["Probe"]
    for i, h in enumerate(heads):
        c = ws.cell(row=4, column=i + 1, value=h)
        c.font = Font(bold=True)
        c.fill = kopf
        c.border = rh
    r0 = 5
    for i, art in enumerate(ORDER):
        r = r0 + i
        ws.cell(row=r, column=1, value=art).border = rh
        for col in range(2, 10):
            c = ws.cell(row=r, column=col)
            c.fill = gelb
            c.border = rh
            c.number_format = fmt2
        ws.cell(row=r, column=10, value=f'=IF(B{r}="","",IF(ROUND(B{r}-SUM(C{r}:I{r}),2)=0,"stimmt","stimmt nicht"))')
    rs = r0 + len(ORDER)  # Summenzeile (13)
    ws.cell(row=rs, column=1, value="Summe (Schritt 1)").font = Font(bold=True)
    for col in range(2, 10):
        L = "ABCDEFGHI"[col - 1]
        c = ws.cell(row=rs, column=col, value=f"=SUM({L}{r0}:{L}{rs - 1})")
        c.font = Font(bold=True)
        c.number_format = fmt2
        c.border = rh
    ws.cell(row=rs, column=10, value=f'=IF(ROUND(B{rs}-SUM(C{rs}:I{rs}),2)=0,"stimmt","stimmt nicht")')
    # Umlage
    k1, u1, z1, k2, u2, en = rs + 2, rs + 3, rs + 4, rs + 5, rs + 6, rs + 7
    ws.cell(row=k1, column=1, value="Schlüssel Umlage Fuhrpark (Transportaufträge)")
    ws.cell(row=u1, column=1, value="Umlage Fuhrpark")
    ws.cell(row=z1, column=1, value="Zwischensummen").font = Font(bold=True)
    ws.cell(row=k2, column=1, value="Schlüssel Umlage Fertigungsplanung (Planungsstunden)")
    ws.cell(row=u2, column=1, value="Umlage Fertigungsplanung")
    ws.cell(row=en, column=1, value="Endsummen").font = Font(bold=True)
    for col in range(4, 10):  # D..I: Schlüssel Fuhrpark
        L = "ABCDEFGHI"[col - 1]
        c = ws.cell(row=k1, column=col)
        c.fill = gelb
        c.border = rh
        ws.cell(row=u1, column=col, value=f'=IF({L}{k1}="",0,ROUND($C${rs}*{L}{k1}/SUM($D${k1}:$I${k1}),2))')
    ws.cell(row=u1, column=3, value=f"=-C{rs}")
    for col in (6, 7):  # F, G: Schlüssel Planung
        c = ws.cell(row=k2, column=col)
        c.fill = gelb
        c.border = rh
        L = "ABCDEFGHI"[col - 1]
        ws.cell(row=u2, column=col, value=f'=IF({L}{k2}="",0,ROUND($E${z1}*{L}{k2}/SUM($F${k2}:$G${k2}),2))')
    ws.cell(row=u2, column=5, value=f"=-E{z1}")
    for col in range(3, 10):
        L = "ABCDEFGHI"[col - 1]
        ws.cell(row=z1, column=col, value=f"={L}{rs}+{L}{u1}").font = Font(bold=True)
        if col not in (5, 6, 7):
            ws.cell(row=u2, column=col, value=0)
        ws.cell(row=en, column=col, value=f"={L}{z1}+{L}{u2}").font = Font(bold=True)
    for r in (u1, z1, u2, en):
        for col in range(3, 10):
            ws.cell(row=r, column=col).number_format = fmt2
            ws.cell(row=r, column=col).border = rh
    # Bezugsgrößen
    b = en + 2
    ws.cell(row=b, column=1, value="Bezugsgrößen").font = Font(bold=True)
    labels = ["Fertigungsmaterial (€)", "Fertigungslöhne Handarbeit, Fertigung I (€)", "Fertigungslöhne Maschinenplatz (€)",
              "Maschinenstunden (h)", "Bestandsveränderung (+ Minderung / − Mehrung, €)",
              "davon maschinenabhängige Gemeinkosten Fertigung II (€)"]
    for i, t in enumerate(labels):
        ws.cell(row=b + 1 + i, column=1, value=t)
        c = ws.cell(row=b + 1 + i, column=2)
        c.fill = gelb
        c.border = rh
        c.number_format = fmt2
    fm, fl1, fl2, std, best, mab = [f"B{b + 1 + i}" for i in range(6)]
    rest = b + 7
    ws.cell(row=rest, column=1, value="Restgemeinkosten Fertigung II inkl. Umlagen (€)")
    ws.cell(row=rest, column=2, value=f"=G{en}-{mab}").number_format = fmt2
    # Nebenrechnung
    n = rest + 2
    ws.cell(row=n, column=1, value="Nebenrechnung Herstellkosten des Umsatzes").font = Font(bold=True)
    zeilen = [
        ("Fertigungsmaterial", f"={fm}"), ("+ Materialgemeinkosten", f"=D{en}"), ("= Materialkosten", f"=B{n + 1}+B{n + 2}"),
        ("Fertigungslöhne (Handarbeit)", f"={fl1}"), ("+ Fertigungsgemeinkosten", f"=F{en}"), ("= Fertigungskosten I", f"=B{n + 4}+B{n + 5}"),
        ("Maschinenabhängige Fertigungsgemeinkosten", f"={mab}"), ("+ Fertigungslöhne Maschinenplatz", f"={fl2}"),
        ("+ Restgemeinkosten", f"=B{rest}"), ("= Fertigungskosten II", f"=B{n + 7}+B{n + 8}+B{n + 9}"),
        ("= Herstellkosten der Erzeugung", f"=B{n + 3}+B{n + 6}+B{n + 10}"),
        ("+ Bestandsminderungen / − Bestandsmehrungen", f"={best}"), ("= Herstellkosten des Umsatzes", f"=B{n + 11}+B{n + 12}"),
    ]
    for i, (t, f) in enumerate(zeilen):
        ws.cell(row=n + 1 + i, column=1, value=(" " + t) if t.startswith(("=", "+")) else t)
        c = ws.cell(row=n + 1 + i, column=2, value=f)
        c.number_format = fmt2
        if t.startswith("="):
            ws.cell(row=n + 1 + i, column=1).font = Font(bold=True)
            c.font = Font(bold=True)
    hk = f"B{n + 13}"
    s = n + 15
    ws.cell(row=s, column=1, value="Zuschlagssätze").font = Font(bold=True)
    saetze = [
        ("MGK-Satz (%)", f'=IF({fm}="","",D{en}/{fm}*100)'), ("FGK-Satz Fertigung I (%)", f'=IF({fl1}="","",F{en}/{fl1}*100)'),
        ("Maschinenstundensatz (€ je h)", f'=IF({std}="","",{mab}/{std})'), ("Restgemeinkosten-Satz (%)", f'=IF({fl2}="","",B{rest}/{fl2}*100)'),
        ("VwGK-Satz (%)", f'=IF({hk}=0,"",H{en}/{hk}*100)'), ("VtGK-Satz (%)", f'=IF({hk}=0,"",I{en}/{hk}*100)'),
    ]
    for i, (t, f) in enumerate(saetze):
        ws.cell(row=s + 1 + i, column=1, value=t)
        ws.cell(row=s + 1 + i, column=2, value=f).number_format = fmt2
    ws.column_dimensions["A"].width = 52
    for L in "BCDEFGHIJ":
        ws.column_dimensions[L].width = 17
    wb.save(pfad)


def main():
    m = ROOT / "material"
    ab_b1(m / "AB-b1-kostenstellen.docx")
    ab_b2(m / "AB-b2-verteilung.docx")
    ab_b3(m / "AB-b3-umlage.docx")
    ab_b4(m / "AB-b4-saetze.docx")
    ab_b5(m / "AB-b5-herstellkosten.docx")
    ab_b6(m / "AB-b6-auswertung.docx")
    ab_bm(m / "AB-bm-bab-august.docx")
    info_docs()
    xlsx_bab(m / "bab-vorlage.xlsx")
    loesungen(ROOT / "lehrkraft/Loesungen-Stufe-2.docx")
    print("✓ Material Stufe 2 erzeugt")


if __name__ == "__main__":
    main()
