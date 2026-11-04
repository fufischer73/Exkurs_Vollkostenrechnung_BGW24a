"""Erzeugt die Arbeitsblätter (docx), Excel-Vorlagen (xlsx) und Lehrkraft-Lösungen für Stufe 1.
Aufruf (aus dem Lernpfad-Ordner):  python3 werkzeuge/material_stufe1.py
"""
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt
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


def tabelle(d, kopf, zeilen, breiten, rechts=(), fett_zeilen=(), leer_hoehe=None):
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
    auf = [(k, b, fmt(v)) for k, b, v in m["guv"]["aufwand"]]
    a = auswerten(m)["guv"]
    auf.append(("", "Summe Aufwendungen", fmt(a["Aufwand"])))
    tabelle(d, ["Konto", "Aufwendungen", "Betrag"], auf, [2, 10.5, 3.5], rechts=(2,), fett_zeilen=(len(auf) - 1,))
    ert = [(k, b, fmt(v)) for k, b, v in m["guv"]["ertrag"]]
    ert.append(("", "Summe Erträge", fmt(a["Ertrag"])))
    tabelle(d, ["Konto", "Erträge", "Betrag"], ert, [2, 10.5, 3.5], rechts=(2,), fett_zeilen=(len(ert) - 1,))
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
def ab_g1(pfad):
    d = neues_dokument("Arbeitsblatt G1 · Warum reicht die GuV nicht?", "Montelli GmbH · Exkurs Vollkostenrechnung · BGW24a")
    guv_tabellen(d, JULI)
    neutral_leer(d)
    d.save(pfad)


def ab_g2(pfad):
    d = neues_dokument("Arbeitsblatt G2 · Kostenartenplan Juli", "Montelli GmbH · Geschäftsbereich Outdoor · Exkurs Vollkostenrechnung")
    ueberschrift(d, "Hilfe: Diese Zahlen kannst du verwenden")
    a = auswerten(JULI)
    d.add_paragraph("Zweckaufwendungen aus der GuV Juli (neutrale Konten 6990, 7400, 7510 sind schon weggelassen):")
    info = [(k, b, fmt(v)) for k, b, v in JULI["guv"]["aufwand"] if k not in JULI["neutral"]]
    tabelle(d, ["Konto", "Bezeichnung", "Betrag in €"], info, [2, 10.5, 3.5], rechts=(2,))
    d.add_paragraph("Statt Konto 6520 gilt: kalkulatorische Abschreibungen 65.000,00 €. "
                    "Statt Konto 7510 gilt: kalkulatorische Zinsen 30.000,00 €.")
    ueberschrift(d, "Aufgabe · Kostenartenplan Juli ausfüllen")
    d.add_paragraph("Trage Gesamtkosten, Einzelkosten und Gemeinkosten ein und bilde die Summen. "
                    "Probe: Einzelkosten + Gemeinkosten = Gesamtkosten.")
    plan_tabelle(d)
    d.save(pfad)


def ab_gm(pfad):
    d = neues_dokument("Arbeitsblatt Meilenstein 1 · GuV August und Kostenartenplan",
                       "Montelli GmbH · Geschäftsbereich Outdoor · Exkurs Vollkostenrechnung")
    guv_tabellen(d, AUGUST)
    neutral_leer(d)
    ueberschrift(d, "Aufgabe 2 · Kostenartenplan August")
    d.add_paragraph("Kalkulatorische Werte für August: Abschreibungen 65.000,00 €, Zinsen 30.000,00 € "
                    "(sie ersetzen die Konten 6520 und 7510).")
    plan_tabelle(d)
    d.add_paragraph("Probe: Einzelkosten + Gemeinkosten = Gesamtkosten?   ☐ ja   ☐ nein")
    ueberschrift(d, "Aufgabe 3 · Vergleich mit Juli (2–3 Sätze)")
    d.add_paragraph("Die Gesamtkosten im Juli waren 543.425,00 €. Warum sind sie im August niedriger? "
                    "Welche Kosten sinken, welche bleiben gleich?")
    for _ in range(4):
        d.add_paragraph("_" * 78)
    d.save(pfad)


def loesungen(pfad):
    d = neues_dokument("Lehrkraft: Lösungen Stufe 1", "Nicht an Schüler:innen weitergeben.")
    ueberschrift(d, "G1 · Neutrale Posten Juli")
    neutral_loesung(d, JULI)
    ueberschrift(d, "G2 · Kostenartenplan Juli")
    plan_tabelle(d, JULI, True)
    ueberschrift(d, "Meilenstein 1 · Neutrale Posten August")
    neutral_loesung(d, AUGUST)
    ueberschrift(d, "Meilenstein 1 · Kostenartenplan August")
    plan_tabelle(d, AUGUST, True)
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
    loesungen(ROOT / "lehrkraft/Loesungen-Stufe-1.docx")
    print("✓ Material erzeugt")


if __name__ == "__main__":
    main()
