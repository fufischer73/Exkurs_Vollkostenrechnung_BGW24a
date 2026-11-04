"""Erzeugt die Arbeitsblätter (docx), Excel-Vorlagen (xlsx) und Lehrkraft-Lösungen für Stufe 1.
Aufruf (aus dem Lernpfad-Ordner):  python3 werkzeuge/material_stufe1.py
"""
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

sys.path.insert(0, str(Path(__file__).parent))
from daten import JULI, AUGUST, auswerten, fmt  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
GROUPS = [
    ("1 Materialkosten", ["Rohstoffe", "Vorprodukte/Fremdbauteile", "Hilfsstoffe", "Betriebsstoffe"], "Summe Materialkosten"),
    ("2 Personalkosten", ["Löhne", "Gehälter"], "Summe Personalkosten"),
    ("3 Kalkulatorische Kosten", ["Kalk. Abschreibungen", "Kalk. Zinsen"], "Summe kalkulatorische Kosten"),
    ("4 Sonstige Kosten", ["Fremdinstandhaltung", "Leasing", "Büromaterial"], "Summe sonstige Kosten"),
]


# ---------------------------------------------------------------- docx-Helfer
def schattieren(zelle, farbe="D9D9D9"):
    tcPr = zelle._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), farbe)
    tcPr.append(shd)


def neues_dokument(titel, untertitel=None):
    d = Document()
    s = d.sections[0]
    s.page_width, s.page_height = Cm(21), Cm(29.7)
    s.left_margin = s.right_margin = Cm(1.8)
    s.top_margin = s.bottom_margin = Cm(1.6)
    st = d.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10)
    p = d.add_paragraph()
    r = p.add_run(titel)
    r.bold = True
    r.font.size = Pt(15)
    if untertitel:
        p2 = d.add_paragraph(untertitel)
        p2.runs[0].font.size = Pt(9)
    d.add_paragraph("Name: ______________________________   Datum: ______________")
    return d


def tabelle(d, kopf, zeilen, breiten, rechts=(), fett_zeilen=(), leer_hoehe=None, grau=()):
    t = d.add_table(rows=1, cols=len(kopf))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, k in enumerate(kopf):
        c = t.rows[0].cells[i]
        c.text = ""
        r = c.paragraphs[0].add_run(k)
        r.bold = True
    for n, z in enumerate(zeilen):
        cells = t.add_row().cells
        for i, v in enumerate(z):
            cells[i].text = ""
            r = cells[i].paragraphs[0].add_run(str(v))
            if n in fett_zeilen:
                r.bold = True
            if i in rechts:
                cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        if n in grau:
            for c in cells:
                schattieren(c)
        if leer_hoehe:
            t.rows[-1].height = Cm(leer_hoehe)
    t.autofit = False
    for i, w in enumerate(breiten):
        t.columns[i].width = Cm(w)
    for row in t.rows:
        for i, w in enumerate(breiten):
            row.cells[i].width = Cm(w)
    d.add_paragraph()
    return t


def ueberschrift(d, text):
    p = d.add_paragraph()
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(11)


def guv_tabellen(d, m):
    ueberschrift(d, f"GuV-Konto Geschäftsbereich Outdoor – Monat {m['name']} (Beträge in €)")
    d.add_paragraph("Grau hinterlegte Zeilen sind neutral: Sie gehören nicht zur Produktion und werden hier nicht berücksichtigt.")
    a = auswerten(m)["guv"]
    auf = [(k, b, fmt(v), "neutral" if k in m["neutral"] else "") for k, b, v in m["guv"]["aufwand"]]
    grau = tuple(i for i, z in enumerate(auf) if z[3])
    auf.append(("", "Summe Aufwendungen", fmt(a["Aufwand"]), ""))
    tabelle(d, ["Konto", "Aufwendungen", "Betrag", "Hinweis"], auf, [2, 9, 3.2, 2.4], rechts=(2,),
            fett_zeilen=(len(auf) - 1,), grau=grau)
    ert = [(k, b, fmt(v), "neutral" if k in m["neutral"] else "") for k, b, v in m["guv"]["ertrag"]]
    grau = tuple(i for i, z in enumerate(ert) if z[3])
    ert.append(("", "Summe Erträge", fmt(a["Ertrag"]), ""))
    tabelle(d, ["Konto", "Erträge", "Betrag", "Hinweis"], ert, [2, 9, 3.2, 2.4], rechts=(2,),
            fett_zeilen=(len(ert) - 1,), grau=grau)
    d.add_paragraph(f"Gewinn des Monats: {fmt(a['Gewinn'])} €")


def neutral_leer(d, anzahl=6):
    ueberschrift(d, "Aufgabe 1 · Neutrale Posten")
    d.add_paragraph("Welche Konten sind neutral? Trage sie ein und gib die Art an (betriebsfremd, periodenfremd, außerordentlich).")
    tabelle(d, ["Konto", "Bezeichnung", "Betrag in €", "Art"], [("", "", "", "")] * anzahl, [2, 6.5, 3, 4.5], leer_hoehe=0.8)
    d.add_paragraph("Neutrale Erträge: ______________ €    − Neutrale Aufwendungen: ______________ €")
    d.add_paragraph("= Neutrales Ergebnis: ______________ €")


def neutral_loesung(d, m):
    rows = [(k, b, fmt(v), "") for k, b, v in m["guv"]["aufwand"] + m["guv"]["ertrag"] if k in m["neutral"]]
    arten = {"6990": "periodenfremd", "7400": "betriebsfremd", "7510": "betriebsfremd", "5500": "betriebsfremd",
             "5710": "betriebsfremd"}
    rows = [(k, b, v, arten[k]) for k, b, v, _ in rows]
    tabelle(d, ["Konto", "Bezeichnung", "Betrag in €", "Art"], rows, [2, 6.5, 3, 4.5], rechts=(2,))
    a = auswerten(m)["guv"]
    d.add_paragraph(f"Neutrale Erträge {fmt(a['Neutral Ertrag'])} € − neutrale Aufwendungen {fmt(a['Neutral Aufwand'])} € "
                    f"= neutrales Ergebnis {fmt(a['Neutrales Ergebnis'])} €")


def plan_zeilen(m=None, mit_werte=False):
    a = auswerten(m) if m else None
    zeilen, fett = [], []
    for gruppe, arten, summe in GROUPS:
        zeilen.append((gruppe, "", "", ""))
        fett.append(len(zeilen) - 1)
        g = e = 0
        for art in arten:
            if mit_werte:
                ges, ein = a["kosten"][art]
                zeilen.append(("   " + art, fmt(ges), fmt(ein) if ein else "", fmt(ges - ein) if ges - ein else ""))
                g += ges
                e += ein
            else:
                zeilen.append(("   " + art, "", "", ""))
        zeilen.append((summe, fmt(g) if mit_werte else "", fmt(e) if mit_werte and e else "",
                       fmt(g - e) if mit_werte and g - e else ""))
        fett.append(len(zeilen) - 1)
    zeilen.append(("Gesamtsummen", fmt(a["gesamt"]) if mit_werte else "", fmt(a["einzel"]) if mit_werte else "",
                   fmt(a["gk"]) if mit_werte else ""))
    fett.append(len(zeilen) - 1)
    return zeilen, fett


def plan_tabelle(d, m=None, mit_werte=False):
    zeilen, fett = plan_zeilen(m, mit_werte)
    tabelle(d, ["Kostenart", "Gesamtkosten", "Einzelkosten", "Gemeinkosten"], zeilen, [7, 3.4, 3.4, 3.4],
            rechts=(1, 2, 3), fett_zeilen=tuple(fett), leer_hoehe=None if mit_werte else 0.75)


# ---------------------------------------------------------------- Arbeitsblätter
def zweckaufwand(m):
    return [(k, b, v) for k, b, v in m["guv"]["aufwand"] if k not in m["neutral"]]


EINZEL_KONTEN = {"6000", "6010", "6200"}


def ab_g1(pfad):
    d = neues_dokument("Arbeitsblatt G1 · Von der GuV zu den Einzel- und Gemeinkosten",
                       "Montelli GmbH · Exkurs Vollkostenrechnung · BGW24a")
    guv_tabellen(d, JULI)
    ueberschrift(d, "Aufgabe 1 · Kosten sortieren")
    d.add_paragraph("Sortiere die nicht grauen Aufwendungen in Einzelkosten und Gemeinkosten und bilde die Summen.")
    rows = [(k, b, fmt(v), "", "") for k, b, v in zweckaufwand(JULI)] + [("", "Summe", "", "", "")]
    tabelle(d, ["Konto", "Bezeichnung", "Betrag", "Einzelkosten", "Gemeinkosten"], rows, [1.6, 6.2, 2.8, 3.0, 3.0],
            rechts=(2, 3, 4), fett_zeilen=(len(rows) - 1,), leer_hoehe=0.65)
    d.add_paragraph("Einzelkosten: ____________ €     Gemeinkosten: ____________ €     Gesamt: ____________ €")
    d.add_paragraph("Anteil der Gemeinkosten an den Gesamtkosten: ______ %  (Gemeinkosten ÷ Gesamtkosten × 100)")
    ueberschrift(d, "Aufgabe 2 · Das Problem der Gemeinkosten")
    d.add_paragraph("Kann Frau Petersen die Gemeinkosten einfach „pro Rucksack“ in der GuV ablesen? Was braucht sie stattdessen?")
    for _ in range(3):
        d.add_paragraph("_" * 78)
    ueberschrift(d, "Aufgabe 3 (Plus) · Nur Einzelkosten kalkulieren?")
    d.add_paragraph("Der Preis soll nur aus den Einzelkosten plus 20 % Gewinn berechnet werden. Rechne für den Juli und beurteile.")
    for _ in range(3):
        d.add_paragraph("_" * 78)
    d.save(pfad)


FAELLE = [
    ("Außenmaterial (wasserabweisendes Gewebe) für den Business Deluxe", "Einzelkosten", "Fertigungsmaterial, direkt zurechenbar"),
    ("Nähgarn für alle Rucksäcke", "Gemeinkosten", "Hilfsstoff, nicht einzeln zurechenbar"),
    ("Lohn der Näherin, die den Business Deluxe montiert", "Einzelkosten", "Fertigungslohn, direkt am Rucksack"),
    ("Gehalt der Einkaufsleiterin", "Gemeinkosten", "Gehalt, nicht am Rucksack"),
    ("Strom für den Nähautomaten", "Gemeinkosten", "Betriebsstoff, nicht einzeln zurechenbar"),
    ("Reißverschlusssystem für den Business Deluxe", "Einzelkosten", "Fremdbauteil, direkt zurechenbar"),
    ("Leasingrate für den Gabelstapler im Lager", "Gemeinkosten", "gemeinsame Nutzung für alle Produkte"),
    ("Frachtkosten für eine Lieferung nur für Kunde Müller", "Einzelkosten", "Sondereinzelkosten des Vertriebs"),
    ("Reparatur des Nähautomaten durch eine Fremdfirma", "Gemeinkosten", "nutzt allen Rucksäcken auf der Maschine"),
    ("Kalkulatorische Zinsen", "Gemeinkosten", "gemeinsame Kosten des Betriebs"),
]
KST_FAELLE = [
    ("Gehalt der Einkaufsleiterin", "Material", "direkt (Gehaltsliste)"),
    ("Stromrechnung für das ganze Betriebsgelände (ein Zähler)", "mehrere Stellen", "Schlüssel, z. B. Verbrauch in kWh"),
    ("Gehalt der Buchhalterin", "Verwaltung", "direkt (Gehaltsliste)"),
    ("Rechnung für den Messestand des Marketings", "Vertrieb", "direkt (Rechnung)"),
    ("Leasingvertrag für das gesamte Gebäude", "mehrere Stellen", "Schlüssel, z. B. genutzte Fläche in m²"),
    ("Reparaturrechnung für den Nähautomaten", "Fertigung", "direkt (Rechnung)"),
]


def ab_g2(pfad):
    d = neues_dokument("Arbeitsblatt G2 · Zuordnung, Kostenartenplan Juli, Kostenstellen",
                       "Montelli GmbH · Geschäftsbereich Outdoor · Exkurs Vollkostenrechnung")
    ueberschrift(d, "Aufgabe 1 · Fälle zuordnen")
    d.add_paragraph("Einzelkosten oder Gemeinkosten? Begründe mit einem Stichwort.")
    rows = [(str(i + 1), f[0], "", "") for i, f in enumerate(FAELLE)]
    tabelle(d, ["Nr.", "Fall", "Einzel-/Gemeinkosten", "Begründung"], rows, [1, 7.2, 3.6, 4.8], leer_hoehe=0.9)
    ueberschrift(d, "Hilfe zu Aufgabe 2: Diese Zahlen kannst du verwenden")
    d.add_paragraph("Nicht graue Aufwendungen aus der GuV Juli:")
    info = [(k, b, fmt(v)) for k, b, v in zweckaufwand(JULI)]
    tabelle(d, ["Konto", "Bezeichnung", "Betrag in €"], info, [2, 10.5, 3.5], rechts=(2,))
    d.add_paragraph("Statt Konto 6520 gilt: kalkulatorische Abschreibungen 65.000,00 €. "
                    "Statt Konto 7510 gilt: kalkulatorische Zinsen 30.000,00 €.")
    ueberschrift(d, "Aufgabe 2 · Kostenartenplan Juli ausfüllen")
    d.add_paragraph("Trage Gesamtkosten, Einzelkosten und Gemeinkosten ein und bilde die Summen. "
                    "Probe: Einzelkosten + Gemeinkosten = Gesamtkosten.")
    plan_tabelle(d)
    ueberschrift(d, "Aufgabe 3 · Kostenstellen zuordnen")
    d.add_paragraph("Welche Kostenstelle? Direkt (Beleg) oder über einen Schlüssel? Nenne bei Schlüssel einen passenden Schlüssel.")
    rows = [(chr(97 + i), f[0], "", "") for i, f in enumerate(KST_FAELLE)]
    tabelle(d, ["", "Fall", "Kostenstelle", "direkt / Schlüssel"], rows, [0.8, 7.4, 3.6, 4.8], leer_hoehe=0.9)
    d.save(pfad)


def ab_gm(pfad):
    d = neues_dokument("Arbeitsblatt Meilenstein 1 · GuV August und Kostenartenplan",
                       "Montelli GmbH · Geschäftsbereich Outdoor · Exkurs Vollkostenrechnung")
    guv_tabellen(d, AUGUST)
    ueberschrift(d, "Aufgabe 1 · Kostenartenplan August")
    d.add_paragraph("Übernimm die nicht grauen Zweckaufwendungen. Kalkulatorische Werte für August: Abschreibungen 65.000,00 €, "
                    "Zinsen 30.000,00 € (sie ersetzen die Konten 6520 und 7510).")
    plan_tabelle(d)
    d.add_paragraph("Probe: Einzelkosten + Gemeinkosten = Gesamtkosten?   ☐ ja   ☐ nein")
    ueberschrift(d, "Aufgabe 2 · Begründung der Zuordnung")
    d.add_paragraph("Warum sind Hilfsstoffe Gemeinkosten? (ein Satz)")
    d.add_paragraph("_" * 78)
    d.add_paragraph("Warum sind Gehälter Gemeinkosten? (ein Satz)")
    d.add_paragraph("_" * 78)
    ueberschrift(d, "Aufgabe 3 · Vergleich mit Juli (2–3 Sätze)")
    d.add_paragraph("Die Gesamtkosten im Juli waren 543.425,00 €. Warum sind sie im August niedriger? "
                    "Welche Kosten sinken, welche bleiben gleich?")
    for _ in range(4):
        d.add_paragraph("_" * 78)
    d.save(pfad)


def plakat(pfad):
    d = Document()
    s = d.sections[0]
    s.orientation = WD_ORIENT.LANDSCAPE
    s.page_width, s.page_height = Cm(29.7), Cm(21)
    s.left_margin = s.right_margin = Cm(1.5)
    s.top_margin = s.bottom_margin = Cm(1.2)
    d.styles["Normal"].font.name = "Arial"
    p = d.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Der Weg von der GuV zum Verkaufspreis")
    r.bold = True
    r.font.size = Pt(30)
    p = d.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Montelli GmbH · Rucksack „Business Deluxe“")
    r.font.size = Pt(16)
    schritte = [
        ("1", "GuV", "Was wurde im Monat aufgewendet und erlöst?"),
        ("2", "Einzel- und Gemeinkosten", "Was kann ich einem Rucksack direkt zurechnen, was nicht?"),
        ("3", "Kostenstellen und BAB", "Wo fallen die Gemeinkosten an? Wie verteile ich sie?"),
        ("4", "Kalkulations-\nsätze", "Wie viel Gemeinkosten je 1 € Material oder Lohn?"),
        ("5", "Zuschlags-\nkalkulation", "Wie hoch sind die Selbstkosten eines Rucksacks?"),
        ("6", "Verkaufspreis", "Gewinn, Skonto, Rabatt: Wie hoch ist der Preis?"),
    ]
    stufen = [("Stufe 1", 0, 1), ("Stufe 2", 2, 3), ("Stufe 3", 4, 5)]
    t = d.add_table(rows=3, cols=6)
    t.style = "Table Grid"
    t.autofit = False
    for i, (nr, kopf, frage) in enumerate(schritte):
        for zeile, text, groesse, fett in ((0, f"{nr}", 26, True), (1, kopf, 14, True), (2, frage, 13, False)):
            c = t.rows[zeile].cells[i]
            c.width = Cm(4.45)
            c.text = ""
            pp = c.paragraphs[0]
            pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            rr = pp.add_run(text)
            rr.bold = fett
            rr.font.size = Pt(groesse)
            if zeile < 2:
                schattieren(c, "DDEBF7" if i < 2 else ("E2EFDA" if i < 4 else "FCE4D6"))
    t.rows[0].height = Cm(2.0)
    t.rows[1].height = Cm(2.6)
    t.rows[2].height = Cm(5.2)
    d.add_paragraph()
    p = d.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Stufe 1: Schritte 1 und 2   ·   Stufe 2: Schritte 3 und 4   ·   Stufe 3: Schritte 5 und 6")
    r.font.size = Pt(14)
    p = d.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Leitfrage: Woher kommen 20 %, 80 %, 30 %, 20 % und 80 € je Maschinenstunde?")
    r.bold = True
    r.font.size = Pt(20)
    r.font.color.rgb = RGBColor(0xC0, 0x39, 0x2B)
    d.save(pfad)


def loesungen(pfad):
    d = neues_dokument("Lehrkraft: Lösungen Stufe 1", "Nicht an Schüler:innen weitergeben.")
    ueberschrift(d, "G1 · Aufgabe 1: Kosten sortieren (GuV-Werte Juli)")
    rows = []
    e = g = 0
    for k, b, v in zweckaufwand(JULI):
        if k in EINZEL_KONTEN:
            rows.append((k, b, fmt(v), fmt(v), ""))
            e += v
        else:
            rows.append((k, b, fmt(v), "", fmt(v)))
            g += v
    rows.append(("", "Summe", fmt(e + g), fmt(e), fmt(g)))
    tabelle(d, ["Konto", "Bezeichnung", "Betrag", "Einzelkosten", "Gemeinkosten"], rows, [1.6, 6.2, 2.8, 3.0, 3.0],
            rechts=(2, 3, 4), fett_zeilen=(len(rows) - 1,))
    d.add_paragraph(f"Gemeinkostenanteil: {fmt(g)} ÷ {fmt(e + g)} × 100 = {g / (e + g) * 100:.1f} %. "
                    f"Plus-Aufgabe: Erlös {fmt(e * 1.2)} €, Kosten {fmt(e + g)} €, Ergebnis {fmt(e * 1.2 - e - g)} €.")
    ueberschrift(d, "G2 · Aufgabe 1: Fälle")
    tabelle(d, ["Nr.", "Fall", "Zuordnung", "Begründung"], [(str(i + 1),) + f for i, f in enumerate(FAELLE)], [1, 6.2, 3, 5.2])
    ueberschrift(d, "G2 · Aufgabe 2: Kostenartenplan Juli")
    plan_tabelle(d, JULI, True)
    d.add_paragraph("Überleitung: Gemeinkosten G1 (GuV-Werte) 229.925,00 € − 58.000,00 € (bilanzielle Abschreibung) + 65.000,00 € "
                    "(kalk. Abschreibung) + 30.000,00 € (kalk. Zinsen) = 266.925,00 €.")
    ueberschrift(d, "G2 · Aufgabe 3: Kostenstellen")
    tabelle(d, ["", "Fall", "Kostenstelle", "direkt / Schlüssel"], [(chr(97 + i),) + f for i, f in enumerate(KST_FAELLE)], [0.8, 7, 3.4, 5])
    ueberschrift(d, "Meilenstein 1 · Kostenartenplan August")
    plan_tabelle(d, AUGUST, True)
    d.add_paragraph("Begründungen: Hilfsstoffe gehen ins Produkt ein, sind aber nicht einzeln messbar. Gehälter bekommen Mitarbeiter:innen, "
                    "die nicht unmittelbar an einem Rucksack arbeiten (Verwaltung, Einkauf, Vertrieb).")
    d.add_paragraph("Erwartungshorizont zum Vergleich mit Juli: Die Gesamtkosten sinken um 33.425,00 € auf 510.000,00 €. "
                    "Gesunken sind vor allem die mengenabhängigen Kosten: Fertigungsmaterial (Rohstoffe und Vorprodukte), "
                    "Hilfs- und Betriebsstoffe, Fertigungslöhne. Gleich bleiben die kalkulatorischen Abschreibungen und "
                    "Zinsen, die Gehälter und das Leasing – sie fallen unabhängig von der Produktionsmenge an. "
                    "(Hinweis: Das Thema fixe und variable Kosten ist nicht Teil dieses Exkurses. Der Hinweis dient nur als Impuls.)")
    d.add_paragraph("Raster: siehe Meilenstein-Seite im Pfad. Zuordnung: Rohstoffe, Vorprodukte/Fremdbauteile und Löhne sind "
                    "Einzelkosten, alles andere Gemeinkosten.")
    d.save(pfad)


# ---------------------------------------------------------------- Excel
def xlsx_plan(pfad, monat):
    wb = Workbook()
    ws = wb.active
    ws.title = "Kostenartenplan"
    gelb = PatternFill("solid", fgColor="FFF2CC")
    kopf = PatternFill("solid", fgColor="D9E2F3")
    rahmen = Border(*(Side(style="thin"),) * 4)
    ws["A1"] = f"Kostenartenplan Montelli GmbH – Geschäftsbereich Outdoor – {monat}"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "Gelbe Felder ausfüllen. Summen und Probe rechnet die Tabelle."
    for i, k in enumerate(["Kostenart", "Gesamtkosten (€)", "Einzelkosten (€)", "Gemeinkosten (€)"]):
        c = ws.cell(row=4, column=i + 1, value=k)
        c.font = Font(bold=True)
        c.fill = kopf
        c.border = rahmen
    zeile = 5
    summenzeilen = []
    for gruppe, arten, summe in GROUPS:
        ws.cell(row=zeile, column=1, value=gruppe).font = Font(bold=True)
        zeile += 1
        start = zeile
        for art in arten:
            ws.cell(row=zeile, column=1, value="   " + art).border = rahmen
            for col in (2, 3, 4):
                c = ws.cell(row=zeile, column=col)
                c.fill = gelb
                c.border = rahmen
                c.number_format = '#,##0.00'
            zeile += 1
        ws.cell(row=zeile, column=1, value=summe).font = Font(bold=True)
        for col in (2, 3, 4):
            L = "ABCD"[col - 1]
            c = ws.cell(row=zeile, column=col, value=f"=SUM({L}{start}:{L}{zeile - 1})")
            c.font = Font(bold=True)
            c.number_format = '#,##0.00'
            c.border = rahmen
        summenzeilen.append(zeile)
        zeile += 1
    ws.cell(row=zeile, column=1, value="Gesamtsummen").font = Font(bold=True)
    for col in (2, 3, 4):
        L = "ABCD"[col - 1]
        c = ws.cell(row=zeile, column=col, value="=" + "+".join(f"{L}{r}" for r in summenzeilen))
        c.font = Font(bold=True)
        c.number_format = '#,##0.00'
        c.border = rahmen
    ws.cell(row=zeile + 2, column=1, value="Probe: Einzelkosten + Gemeinkosten = Gesamtkosten").font = Font(bold=True)
    ws.cell(row=zeile + 2, column=2,
            value=f'=IF(ROUND(C{zeile}+D{zeile}-B{zeile},2)=0,"Probe stimmt","Probe stimmt NICHT")')
    ws.column_dimensions["A"].width = 44
    for L in "BCD":
        ws.column_dimensions[L].width = 20
    wb.save(pfad)


def main():
    (ROOT / "material").mkdir(exist_ok=True)
    (ROOT / "lehrkraft").mkdir(exist_ok=True)
    ab_g1(ROOT / "material/AB-g1-guv-juli.docx")
    ab_g2(ROOT / "material/AB-g2-kostenartenplan.docx")
    ab_gm(ROOT / "material/AB-gm-guv-august.docx")
    xlsx_plan(ROOT / "material/kostenartenplan-juli.xlsx", "Juli")
    xlsx_plan(ROOT / "material/kostenartenplan-august.xlsx", "August")
    plakat(ROOT / "material/Plakat-Prozesskette.docx")
    loesungen(ROOT / "lehrkraft/Loesungen-Stufe-1.docx")
    print("✓ Material erzeugt")


if __name__ == "__main__":
    main()
