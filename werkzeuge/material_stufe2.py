"""Erzeugt Arbeitsblätter (docx), Infoblätter (docx aus seiten/), BAB-Formular, Excel-Vorlage und Lehrkraft-Lösungen für Stufe 2.
Aufruf (aus dem Lernpfad-Ordner):  python3 werkzeuge/material_stufe2.py      (PDFs danach mit werkzeuge/pdfs.py)
"""
import re
import subprocess
import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side

sys.path.insert(0, str(Path(__file__).parent))
from daten import (JULI, AUGUST, ORDER, SP7, SCHLUESSEL, GRUNDLAGE, UMLAGE_FUHRPARK, UMLAGE_PLANUNG,  # noqa: E402
                   auswerten, umlage, fmt)
from material_stufe1 import (neues_dokument, tabelle, ueberschrift, rechenkasten, kopfzeile, schattieren)  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SP_KOPF = ["Fuhrpark", "Material", "Fertigungs-planung", "Fertigung I\nHandarbeit", "Fertigung II\nMaschinenplatz", "Verwaltung", "Vertrieb"]
GRAU = "D9D9D9"


def f0(x):
    return fmt(x, 0)


def quer(titel, untertitel="Montelli GmbH · Geschäftsbereich Outdoor · Exkurs Vollkostenrechnung"):
    d = neues_dokument(titel, untertitel)
    s = d.sections[0]
    s.orientation = WD_ORIENT.LANDSCAPE
    s.page_width, s.page_height = Cm(29.7), Cm(21)
    s.left_margin = s.right_margin = Cm(1.2)
    s.top_margin = s.bottom_margin = Cm(1.0)
    kopfzeile(d)
    return d


def hoch(titel, untertitel="Montelli GmbH · Geschäftsbereich Outdoor · Exkurs Vollkostenrechnung"):
    return neues_dokument(titel, untertitel)


def linien(d, n=2, breite=78):
    for _ in range(n):
        d.add_paragraph("_" * breite)


# ---------------------------------------------------------------- Tabellenbau für den BAB (Layout wie in der Vorlage)
def zelle(c, text="", fett=False, rechts=False, mitte=False, klein=False, grau=False):
    c.text = ""
    par = c.paragraphs[0]
    par.paragraph_format.space_after = Pt(0)
    zeilen = str(text).split("\n")
    for i, z in enumerate(zeilen):
        run = par.add_run(z)
        run.bold = fett
        run.font.size = Pt(8 if klein else 9)
        if i < len(zeilen) - 1:
            run.add_break()
    par.alignment = WD_ALIGN_PARAGRAPH.RIGHT if rechts else (WD_ALIGN_PARAGRAPH.CENTER if mitte else WD_ALIGN_PARAGRAPH.LEFT)
    if grau:
        schattieren(c, GRAU)


def bab_tabelle_start(d, links, breiten):
    t = d.add_table(rows=0, cols=9)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for i, w in enumerate(breiten):
        t.columns[i].width = Cm(w)
    return t


def bab_kopf(t, links, titel=None):
    if titel:
        r = t.add_row()
        c = r.cells[0].merge(r.cells[8])
        zelle(c, titel, fett=True, mitte=True)
    r1, r2 = t.add_row(), t.add_row()
    zelle(r1.cells[0].merge(r1.cells[1]), links[0], fett=True, mitte=True)
    zelle(r1.cells[2], "Allgemeine\nKostenstelle", fett=True, mitte=True, klein=True)
    zelle(r1.cells[3], "Haupt-\nkostenstelle", fett=True, mitte=True, klein=True)
    zelle(r1.cells[4], "Hilfs-\nkostenstelle", fett=True, mitte=True, klein=True)
    zelle(r1.cells[5].merge(r1.cells[6]), "Fertigungs-Hauptkostenstellen (FHS)", fett=True, mitte=True, klein=True)
    zelle(r1.cells[7], "Haupt-\nkostenstelle", fett=True, mitte=True, klein=True)
    zelle(r1.cells[8], "Haupt-\nkostenstelle", fett=True, mitte=True, klein=True)
    zelle(r2.cells[0], links[1], fett=True, mitte=True)
    zelle(r2.cells[1], links[2], fett=True, mitte=True)
    for i, k in enumerate(SP_KOPF):
        zelle(r2.cells[2 + i], k, fett=True, mitte=True, klein=True)


def zeile(t, label, werte, fett=False, grau=(), hoehe=0.55, summe=None, label_breit=False):
    r = t.add_row()
    r.height = Cm(hoehe)
    if label_breit:
        zelle(r.cells[0].merge(r.cells[1]), label, fett=fett)
        vorn = 2
    else:
        zelle(r.cells[0], label, fett=fett)
        zelle(r.cells[1], summe if summe is not None else "", rechts=True, fett=fett, grau=1 in grau)
        vorn = 2
    for i in range(7):
        v = werte[i] if werte else ""
        v = "" if v is None else v
        zelle(r.cells[vorn + i], v, rechts=True, fett=fett, grau=(2 + i) in grau)
    return r


def bab_formular(d, m, voll=False, monat="Juli"):
    """Der BAB wie in der Vorlage: Verteilung, Umlage, Zuschlagssätze, Maschinenstundensatz."""
    breiten = [4.6, 2.2] + [2.9] * 7
    t = bab_tabelle_start(d, None, breiten)
    bab_kopf(t, ("Gemeinkosten", "Gemeinkostenart", "Summe"), f"Betriebsabrechnungsbogen (BAB I) {monat} 20.. (Geschäftsjahr)")
    a = auswerten(m)
    prim, u1, zw, u2, end = a["umlage"]
    for art in ORDER:
        v = m["bab"][art]
        zeile(t, art, [f0(x) for x in v] if voll else None, summe=f0(sum(v)))
    zeile(t, "Summen", [f0(prim[k]) for k in SP7] if voll else None, fett=True, summe=f0(sum(prim.values())) if voll else "")
    z = zeile(t, "Umlage\nFuhrpark", None, grau=(1,), hoehe=0.75)
    if voll:
        for i, k in enumerate(SP7):
            zelle(z.cells[2 + i], f0(-prim[k]) if k == "Fuhrpark" else (("+" + f0(u1[k])) if u1.get(k) else "0"), rechts=True)
    else:
        zelle(z.cells[2], "↳", mitte=True)
    zeile(t, "Zwischensummen", [f0(zw[k]) for k in SP7] if voll else None, fett=True, grau=(1, 2))
    z = zeile(t, "Umlage\nFertigungsplanung", None, grau=(1, 2), hoehe=0.75)
    if voll:
        for i, k in enumerate(SP7):
            if k == "Fertigungsplanung":
                zelle(z.cells[2 + i], f0(-zw[k]), rechts=True)
            elif u2.get(k):
                zelle(z.cells[2 + i], "+" + f0(u2[k]), rechts=True)
    else:
        zelle(z.cells[4], "↳", mitte=True)
    zeile(t, "Summen", [f0(end[k]) for k in SP7] if voll else None, fett=True, grau=(1, 2, 4))
    # Zuschlagsgrundlagen, Sätze, Maschinenstunden
    r = a["saetze"]
    gr = [None, f0(a["fm"]), None, f0(m["fl1"]), f0(m["fl2"]), f0(r["HKdU"]), f0(r["HKdU"])] if voll else None
    zeile(t, "Zuschlagsgrundlagen (FM, FL, HKdU)", gr, grau=(2, 4), label_breit=True)
    sa = [None, f"{r['MGK %']:.2f} %".replace(".", ","), None, f"{r['FGK I %']:.2f} %".replace(".", ","),
          f"{r['Rest %']:.2f} %".replace(".", ","), f"{r['VwGK %']:.2f} %".replace(".", ","), f"{r['VtGK %']:.2f} %".replace(".", ",")] if voll else None
    zeile(t, "Zuschlagssätze für MGK, FGK, RGK, VwGK, VtGK (Ist)", sa, fett=True, grau=(2, 4), label_breit=True, hoehe=0.75)
    ms = [None] * 4 + [f"{m['masch_std']:,}".replace(",", "."), None, None] if voll else None
    zeile(t, "Maschinenstunden gesamt (Std.)", ms, grau=(2, 3, 4, 5, 7, 8), label_breit=True)
    msatz = [None] * 4 + [f"{r['Maschinenstundensatz']:.2f} €".replace(".", ","), None, None] if voll else None
    zeile(t, "Maschinenstundensatz (Istwert)", msatz, fett=True, grau=(2, 3, 4, 5, 7, 8), label_breit=True)
    d.add_paragraph()


def verteilungs_tabelle(d, m):
    """Kombinierte Tabelle wie in der Vorlage „Verteilung der Gemeinkosten“: Kostenstellen waagerecht, Gemeinkostenarten senkrecht."""
    breiten = [4.6, 2.9] + [2.8] * 7
    t = bab_tabelle_start(d, None, breiten)
    bab_kopf(t, ("Gemeinkosten", "Gemeinkostenart", "Verteilungs-grundlage"))
    for art in ORDER:
        r = t.add_row()
        r.height = Cm(0.62)
        zelle(r.cells[0], art)
        zelle(r.cells[1], GRUNDLAGE[art], mitte=True, klein=True)
        werte = SCHLUESSEL[art][1] if art in SCHLUESSEL else m["bab"][art]
        for i, v in enumerate(werte):
            zelle(r.cells[2 + i], str(v) if art in SCHLUESSEL else f0(v), rechts=True)
    d.add_paragraph()


def umlage_schluessel(d):
    """Umlageschlüssel wie in der Vorlage: Vorkostenstellen als Zeilen, graue Felder für nicht beteiligte Stellen."""
    breiten = [4.6, 2.9] + [2.8] * 7
    t = bab_tabelle_start(d, None, breiten)
    bab_kopf(t, ("Vorkostenstellen", "Vorkosten-stelle", "Umlage-grundlage"))
    r = t.add_row()
    r.height = Cm(0.8)
    zelle(r.cells[0], "Fuhrpark")
    zelle(r.cells[1], "Transport-aufträge", mitte=True, klein=True)
    zelle(r.cells[2], "", grau=True)
    for i, k in enumerate(SP7[1:], start=1):
        zelle(r.cells[2 + i], str(UMLAGE_FUHRPARK.get(k, 0)), mitte=True)
    r = t.add_row()
    r.height = Cm(0.8)
    zelle(r.cells[0], "Fertigungsplanung")
    zelle(r.cells[1], "Planungs-stunden", mitte=True, klein=True)
    for i, k in enumerate(SP7):
        if k in UMLAGE_PLANUNG:
            zelle(r.cells[2 + i], str(UMLAGE_PLANUNG[k]), mitte=True)
        else:
            zelle(r.cells[2 + i], "", grau=True)
    d.add_paragraph()


def nebenrechnung(d, werte=None):
    z = ["Fertigungsmaterial (FM)", "+ Materialgemeinkosten (MGK)", "= Materialkosten (MK)", "Fertigungslöhne Handarbeit (FL)",
         "+ Fertigungsgemeinkosten (FGK)", "= Fertigungskosten I", "Maschinenabhängige Fertigungsgemeinkosten",
         "+ Fertigungslöhne des Maschinenplatzes", "+ Restgemeinkosten", "= Fertigungskosten II", "= Herstellkosten der Erzeugung (HKdE)",
         "+ Bestandsminderungen", "− Bestandsmehrungen", "= Herstellkosten des Umsatzes (HKdU)"]
    rows = [(t, (werte[i] if werte else "")) for i, t in enumerate(z)]
    fett = tuple(i for i, t in enumerate(z) if t.startswith("="))
    tabelle(d, ["Nebenrechnung: Herstellkosten des Umsatzes (HKdU)", "Betrag in €"], rows, [11, 5], rechts=(1,), fett_zeilen=fett,
            leer_hoehe=None if werte else 0.75)


def neben_werte(m):
    a = auswerten(m)
    fm, fl1, fl2 = a["fm"], m["fl1"], m["fl2"]
    mgk, fgk1, _, vw, vt = a["spalten"]
    masch, rest = a["masch"]
    mk, fk1, fk2 = fm + mgk, fl1 + fgk1, masch + fl2 + rest
    return [fmt(fm), fmt(mgk), fmt(mk), fmt(fl1), fmt(fgk1), fmt(fk1), fmt(masch), fmt(fl2), fmt(rest), fmt(fk2),
            fmt(mk + fk1 + fk2), fmt(0), fmt(0), fmt(a["saetze"]["HKdU"])]


def bezug_tabelle(d, m):
    a = auswerten(m)
    tabelle(d, ["Bezugsgröße", "Wert"], [
        ("Fertigungsmaterial (Rohstoffe + Vorprodukte/Fremdbauteile)", fmt(a["fm"]) + " €"),
        ("Fertigungslöhne Handarbeit (Fertigung I)", fmt(m["fl1"]) + " €"),
        ("Fertigungslöhne Maschinenplatz (Fertigung II)", fmt(m["fl2"]) + " €"),
        ("Maschinenstunden Maschinenplatz", f"{m['masch_std']:,} h".replace(",", ".")), ("Bestandsveränderungen", "keine")], [11, 5], rechts=(1,))


# ---------------------------------------------------------------- Arbeitsblätter
BEREICHE = ["Einkauf, Wareneingang und Lager", "Fuhrpark: Gabelstapler und Lieferwagen für alle Bereiche",
            "Fertigungsplanung: Arbeitsvorbereitung für die Fertigung", "Zuschneiden, Nähen und Montage von Hand",
            "Zuschnitt- und Nähautomat", "Geschäftsführung, Personal, Finanzbuchhaltung, Controlling", "Marketing und Verkauf"]
LOES_KST = [("Material", "Hauptkostenstelle"), ("Fuhrpark", "allgemeine Kostenstelle"), ("Fertigungsplanung", "Hilfskostenstelle"),
            ("Fertigung I (Handarbeit)", "Hauptkostenstelle"), ("Fertigung II (Maschinenplatz)", "Hauptkostenstelle"),
            ("Verwaltung", "Hauptkostenstelle"), ("Vertrieb", "Hauptkostenstelle")]


def ab_b1(pfad):
    d = hoch("Arbeitsblatt B1 · Brücke: Kostenstellen der Montelli")
    ueberschrift(d, "Aufgabe · Kostenstellen einordnen")
    d.add_paragraph("Ordne jeden Bereich einer Kostenstelle zu und gib die Art an: allgemeine Kostenstelle, Hilfskostenstelle "
                    "oder Hauptkostenstelle (Material, Fertigung, Verwaltung, Vertrieb).")
    tabelle(d, ["Nr.", "Bereich", "Kostenstelle", "Art"], [(str(i + 1), b, "", "") for i, b in enumerate(BEREICHE)],
            [1, 7.2, 4.5, 4.3], leer_hoehe=1.0)
    d.save(pfad)


def ab_b2(pfad):
    d = quer("Arbeitsblatt B2 · BAB Schritt 1: Verteilen der Gemeinkosten auf die Kostenstellen (Juli)")
    d.add_paragraph("Verteile mithilfe des Kostenartenplans, der folgenden Tabelle und der Verteilungsschlüssel alle Gemeinkosten des Juli auf die "
                    "einzelnen Kostenstellen der Montelli GmbH. Ermittle anschließend für jede Kostenstelle die Summe der Gemeinkosten.")
    ueberschrift(d, "Verteilung der Gemeinkosten im Monat Juli (Beträge in €, bei „Schlüssel“ und „m²“ Schlüsselzahlen)")
    verteilungs_tabelle(d, JULI)
    d.add_page_break()
    bab_formular(d, JULI)
    d.save(pfad)


def ab_bab_formular(pfad):
    d = quer("BAB-Formular Juli (Module B2 bis B5, Meilenstein 2)")
    bab_formular(d, JULI)
    d.save(pfad)


def ab_b3(pfad):
    d = quer("Arbeitsblatt B3 · BAB Schritt 2: Verrechnen innerbetrieblicher Leistungen (Juli)")
    d.add_paragraph("Da die Vorkostenstellen „Fuhrpark“ und „Fertigungsplanung“ die Hauptkostenstellen mit ihren Leistungen beliefern, legst du "
                    "die damit verbundenen Gemeinkosten verursachungsgerecht auf die Hauptkostenstellen um. Lege mithilfe des Schlüssels die "
                    "Gemeinkosten um und ermittle für jede Hauptkostenstelle die Summe der Gemeinkosten. Arbeite im BAB-Formular (Zeilen „Umlage“).")
    ueberschrift(d, "Schlüssel zur Verrechnung innerbetrieblicher Leistungen")
    umlage_schluessel(d)
    prim = umlage(JULI)[0]
    ueberschrift(d, "Rechnung zur Umlage")
    rechenkasten(d, [
        ("Summe der Schlüsselzahlen (Fuhrpark)", "Material + Planung + Fertigung I + Fertigung II + Verwaltung + Vertrieb", "Teile"),
        ("Betrag je Teil (Fuhrpark)", "Kosten Fuhrpark ÷ Summe der Schlüsselzahlen", "€"),
        ("Kosten Fertigungsplanung nach Umlage 1", "Kosten nach Schritt 1 + Anteil vom Fuhrpark", "€"),
        ("Summe der Schlüsselzahlen (Planung)", "Fertigung I + Fertigung II", "Teile"),
        ("Betrag je Teil (Planung)", "Kosten Fertigungsplanung ÷ Summe der Schlüsselzahlen", "€"),
    ], breiten=(6.4, 7.2, 8.0, 4.5), hoehe=1.2)
    d.add_paragraph("Falls dein BAB aus B2 nicht stimmt, nimm diese Summen (Schritt 1): " +
                    ", ".join(f"{k} {fmt(prim[k], 0)} €" for k in SP7) + ".")
    d.save(pfad)


def ab_b4(pfad):
    d = hoch("Arbeitsblatt B4 · BAB Schritt 3: Zuschlagssätze und Maschinenplatz (Juli)")
    d.add_paragraph("Ermittle in diesem Schritt mithilfe des Infotextes die Kalkulationssätze für die Angebotskalkulation. Dir liegen für den Juli "
                    "diese Informationen vor:")
    for b in ["Einzelkosten (Fertigungsmaterial und Löhne) gemäß Kostenartenplan, Löhne: Fertigung I (Handarbeit) 62.500 €, Fertigung II (Maschinenplatz) 14.000 €;",
              "Fertigungsmaterial (Rohstoffe + Vorprodukte/Fremdbauteile): 200.000 €;",
              "der Maschinenplatz (Fertigung II) war 1.000 Stunden im Einsatz;",
              "keine Bestandsveränderungen an fertigen und unfertigen Erzeugnissen im Lager."]:
        d.add_paragraph("• " + b)
    ueberschrift(d, "Aufgabe 1 · Material und Fertigung I")
    rechenkasten(d, [
        ("MGK-Zuschlagssatz", "Gemeinkosten Material × 100 ÷ Fertigungsmaterial", "%"),
        ("FGK-Zuschlagssatz (Fertigung I)", "Gemeinkosten Fertigung I × 100 ÷ Fertigungslöhne Handarbeit", "%"),
    ], breiten=(4.2, 5.6, 4.6, 2.9), hoehe=1.5)
    d.add_paragraph("Bedeutung: Auf 100 € ______________________________ entfallen ________ € ______________________________.")
    rechenkasten(d, [
        ("MGK des Auftrags", "Fertigungsmaterial 4.200 € × MGK-Satz ÷ 100", "€"),
        ("FGK des Auftrags", "Fertigungslöhne 2.600 € × FGK-Satz ÷ 100", "€"),
    ], breiten=(4.2, 5.6, 4.6, 2.9), hoehe=1.5, kopf=("Auftrag", "Formel", "Rechnung", "Ergebnis"))
    ueberschrift(d, "Aufgabe 2 · Maschinenplatz (Fertigung II)")
    d.add_paragraph("Gemeinkosten der Fertigung II nach der Umlage: 85.200 €")
    rechenkasten(d, [
        ("Denkanstoß: Satz auf Löhne", "Gemeinkosten Fertigung II × 100 ÷ Maschinenplatzlöhne", "%"),
    ], breiten=(4.2, 5.6, 4.6, 2.9), hoehe=1.3)
    d.add_paragraph("Was fällt dir auf? ______________________________________________________________")
    rechenkasten(d, [
        ("Maschinenabhängige Gemeinkosten", "Betriebsstoffe + Abschreibungen + Zinsen + Fremdinstandhaltung (Fertigung II)", "€"),
        ("Restgemeinkosten", "Gemeinkosten Fertigung II − maschinenabhängige Gemeinkosten", "€"),
        ("Maschinenstundensatz", "Maschinenabhängige Gemeinkosten ÷ Maschinenstunden", "€ je h"),
        ("Restgemeinkosten-Zuschlagssatz", "Restgemeinkosten × 100 ÷ Maschinenplatzlöhne", "%"),
    ], breiten=(4.2, 5.6, 4.6, 2.9), hoehe=1.5)
    rechenkasten(d, [
        ("Maschinenkosten des Auftrags", "2 Maschinenstunden × Maschinenstundensatz", "€"),
        ("Restgemeinkosten des Auftrags", "Maschinenplatzlöhne 28 € × Restgemeinkosten-Satz ÷ 100", "€"),
    ], breiten=(4.2, 5.6, 4.6, 2.9), hoehe=1.5, kopf=("Auftrag", "Formel", "Rechnung", "Ergebnis"))
    d.save(pfad)


def ab_b5(pfad):
    d = hoch("Arbeitsblatt B5 · Herstellkosten des Umsatzes, Verwaltung und Vertrieb (Juli)")
    d.add_paragraph("Für die Nebenrechnung zur Ermittlung der Herstellkosten des Umsatzes nutzt du das folgende Schema. Es gab im Juli keine "
                    "Bestandsveränderungen.")
    bezug_tabelle(d, JULI)
    d.add_paragraph("Gemeinkosten: Material 39.400 € · Fertigung I 50.625 € · maschinenabhängig (Fertigung II) 81.000 € · Restgemeinkosten 4.200 € · "
                    "Verwaltung 56.000 € · Vertrieb 35.700 €")
    nebenrechnung(d)
    ueberschrift(d, "Verwaltung und Vertrieb")
    rechenkasten(d, [
        ("VwGK-Zuschlagssatz", "Gemeinkosten Verwaltung × 100 ÷ HKdU", "%"),
        ("VtGK-Zuschlagssatz", "Gemeinkosten Vertrieb × 100 ÷ HKdU", "%"),
        ("Summe beider Sätze", "VwGK + VtGK (Lernsituation: 20 %)", "%"),
    ], breiten=(4.2, 5.6, 4.6, 2.9), hoehe=1.5)
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
    d = hoch("Arbeitsblatt Meilenstein 2 · Auswertung des BAB (Juli)")
    d.add_paragraph("Beantworte die Fragen mit deinem fertigen BAB aus den Modulen B2 bis B5. Notiere Rechnung und Antwort in den Feldern. "
                    "Zur Abgabe gehören drei Teile: das BAB-Formular, die Nebenrechnung (HKdU) und dieses Arbeitsblatt.")
    rows = [(str(i + 1), f, "", "") for i, f in enumerate(FRAGEN)]
    tabelle(d, ["Nr.", "Frage", "Rechnung", "Antwort / Ergebnis"], rows, [0.9, 6.6, 4.8, 4.9], leer_hoehe=2.2)
    d.save(pfad)


def loesungen(pfad):
    d = quer("Lehrkraft: Lösungen Stufe 2", "Nicht an Schüler:innen weitergeben.")
    a = auswerten(JULI)
    r = a["saetze"]
    ueberschrift(d, "BAB Juli (B2 bis B5): Verteilung, Umlage, Zuschlagssätze")
    bab_formular(d, JULI, voll=True)
    tabelle(d, ["Satz", "Wert"], [
        ("MGK-Satz", f"{r['MGK %']:.2f} %".replace(".", ",")), ("FGK-Satz (Fertigung I)", f"{r['FGK I %']:.2f} %".replace(".", ",")),
        ("Maschinenstundensatz", f"{r['Maschinenstundensatz']:.2f} € je h".replace(".", ",")),
        ("Restgemeinkosten-Satz", f"{r['Rest %']:.2f} %".replace(".", ",")),
        ("VwGK-Satz", f"{r['VwGK %']:.2f} %".replace(".", ",")), ("VtGK-Satz", f"{r['VtGK %']:.2f} %".replace(".", ","))], [8, 6], rechts=(1,))
    d.add_paragraph(f"Maschinenabhängig (Fertigung II): {fmt(a['masch'][0])} € · Restgemeinkosten einschließlich Umlagen: {fmt(a['masch'][1])} €")
    nebenrechnung(d, neben_werte(JULI))
    ueberschrift(d, "B1: Lösung")
    tabelle(d, ["Nr.", "Bereich", "Kostenstelle", "Art"], [(str(i + 1), BEREICHE[i]) + LOES_KST[i] for i in range(7)], [1, 9, 5, 5])
    ueberschrift(d, "Meilenstein 2: Auswertung Juli")
    tabelle(d, ["Nr.", "Antwort"], [(str(i + 1), ANTW[i]) for i in range(13)], [1, 24])
    b = auswerten(AUGUST)["saetze"]
    d.add_paragraph("Hintergrund (nicht im Pfad berechnet): Für den August hat das Rechnungswesen MGK 21,77 %, FGK I 88,16 %, Maschinenstundensatz 85,61 € je h, "
                    f"Restgemeinkosten {b['Rest %']:.2f} %, VwGK {b['VwGK %']:.2f} %, VtGK {b['VtGK %']:.2f} % ermittelt. T1 nutzt den MGK-Satz.".replace(".", ",", 0))
    d.add_paragraph("Hinweis: Bei Rundung der Sätze auf zwei Dezimalstellen kann die Nachrechnung um wenige Cent abweichen. Das ist in Ordnung.")
    d.save(pfad)


# ---------------------------------------------------------------- Infoblätter aus seiten/*.md
def rahmen(tabelle_):
    pr = tabelle_._tbl.tblPr
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
        text_ohne = re.sub(r":::material.*?\n:::\n", "", m.group(2), flags=re.S)
        body = f"# {titel}\n\n*Montelli GmbH · Exkurs Vollkostenrechnung*\n\n" + text_ohne
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
        s.page_width, s.page_height = Cm(21), Cm(29.7)
        s.left_margin = s.right_margin = Cm(2)
        s.top_margin = s.bottom_margin = Cm(2)
        kopfzeile(d)
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
    heads = ["Gemeinkostenart", "Summe (Kostenartenplan)", "Fuhrpark", "Material", "Fertigungsplanung", "Fertigung I Handarbeit",
             "Fertigung II Maschinenplatz", "Verwaltung", "Vertrieb", "Probe"]
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
    rs = r0 + len(ORDER)
    ws.cell(row=rs, column=1, value="Summen (Schritt 1)").font = Font(bold=True)
    for col in range(2, 10):
        L = "ABCDEFGHI"[col - 1]
        c = ws.cell(row=rs, column=col, value=f"=SUM({L}{r0}:{L}{rs - 1})")
        c.font = Font(bold=True)
        c.number_format = fmt2
        c.border = rh
    ws.cell(row=rs, column=10, value=f'=IF(ROUND(B{rs}-SUM(C{rs}:I{rs}),2)=0,"stimmt","stimmt nicht")')
    k1, u1, z1, k2, u2, en = rs + 2, rs + 3, rs + 4, rs + 5, rs + 6, rs + 7
    for r, t in ((k1, "Schlüssel Umlage Fuhrpark (Transportaufträge)"), (u1, "Umlage Fuhrpark"), (z1, "Zwischensummen"),
                 (k2, "Schlüssel Umlage Fertigungsplanung (Planungsstunden)"), (u2, "Umlage Fertigungsplanung"), (en, "Summen (Endsummen)")):
        ws.cell(row=r, column=1, value=t)
    for r in (z1, en):
        ws.cell(row=r, column=1).font = Font(bold=True)
    for col in range(4, 10):
        L = "ABCDEFGHI"[col - 1]
        c = ws.cell(row=k1, column=col)
        c.fill = gelb
        c.border = rh
        ws.cell(row=u1, column=col, value=f'=IF({L}{k1}="",0,ROUND($C${rs}*{L}{k1}/SUM($D${k1}:$I${k1}),2))')
    ws.cell(row=u1, column=3, value=f"=-C{rs}")
    for col in (6, 7):
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
    b = en + 2
    ws.cell(row=b, column=1, value="Bezugsgrößen").font = Font(bold=True)
    labels = ["Fertigungsmaterial (€)", "Fertigungslöhne Handarbeit, Fertigung I (€)", "Fertigungslöhne Maschinenplatz, Fertigung II (€)",
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
    ab_bab_formular(m / "BAB-Formular-Juli.docx")
    ab_b3(m / "AB-b3-umlage.docx")
    ab_b4(m / "AB-b4-saetze.docx")
    ab_b5(m / "AB-b5-herstellkosten.docx")
    ab_b6(m / "AB-b6-auswertung.docx")
    info_docs()
    xlsx_bab(m / "bab-vorlage.xlsx")
    loesungen(ROOT / "lehrkraft/Loesungen-Stufe-2.docx")
    print("✓ Material Stufe 2 erzeugt")


if __name__ == "__main__":
    main()
