"""Erzeugt Arbeitsblatt (docx), Excel-Vorlage (xlsx) und Lösung für die Erweiterung (Vorkostenstellen).
Aufruf (aus dem Lernpfad-Ordner):  python3 werkzeuge/material_erweiterung.py
"""
import sys
from pathlib import Path

from docx.enum.section import WD_ORIENT
from docx.shared import Cm
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side

sys.path.insert(0, str(Path(__file__).parent))
from daten import (VK_STELLEN, VK_BAB, VK_SCHL_FUHRPARK, VK_SCHL_PLANUNG, vorkostenumlage, fmt)  # noqa: E402
from material_stufe1 import neues_dokument, tabelle, ueberschrift  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ORDER = list(VK_BAB)


def f0(x):
    return fmt(x, 0)


def quer(titel):
    d = neues_dokument(titel, "Montelli GmbH · Exkurs Vollkostenrechnung · Erweiterung (freiwillig)")
    s = d.sections[0]
    s.orientation = WD_ORIENT.LANDSCAPE
    s.page_width, s.page_height = Cm(29.7), Cm(21)
    s.left_margin = s.right_margin = Cm(1.2)
    s.top_margin = s.bottom_margin = Cm(1.2)
    return d


def ab(pfad):
    d = quer("Arbeitsblatt BX · Vorkostenstellen und Umlage (Treppenstufenverfahren)")
    ueberschrift(d, "BAB Juli nach Schritt 1 (Beträge in €)")
    kopf = ["Gemeinkostenart", "Summe"] + ["Fuhrpark", "Material", "Fertigungs-planung", "Fertigung I", "Fertigung II", "Verwaltung", "Vertrieb"]
    rows = [[a, f0(sum(v))] + [f0(x) for x in v] for a, v in VK_BAB.items()]
    prim = [sum(v[i] for v in VK_BAB.values()) for i in range(7)]
    rows.append(["Summe", f0(sum(prim))] + [f0(x) for x in prim])
    tabelle(d, kopf, rows, [4.6, 2.2] + [3.0] * 7, rechts=tuple(range(1, 9)), fett_zeilen=(len(rows) - 1,))
    ueberschrift(d, "Umlageschlüssel")
    rows = [[k, str(VK_SCHL_FUHRPARK.get(k, "")) if k != "Fuhrpark" else "", str(VK_SCHL_PLANUNG.get(k, "")) if k in VK_SCHL_PLANUNG else "–"]
            for k in VK_STELLEN]
    rows = [r for r in rows if r[0] != "Fuhrpark"]
    tabelle(d, ["Kostenstelle", "Fuhrpark: Transportaufträge", "Fertigungsplanung: Planungsstunden"], rows, [6, 6.5, 8], rechts=(1, 2))
    ueberschrift(d, "Aufgabe · Umlage durchführen")
    leer = [[k, "", "", "", "", ""] for k in VK_STELLEN]
    tabelle(d, ["Kostenstelle", "Nach Schritt 1", "Umlage Fuhrpark", "Zwischensumme", "Umlage Fertigungsplanung", "Endsumme"],
            leer, [5, 3.8, 3.8, 3.8, 4.4, 3.8], leer_hoehe=0.8)
    d.add_paragraph("Probe: Summe der Endsummen der Hauptkostenstellen = ______________ €  (soll 266.925 € sein)")
    d.add_paragraph("MGK-Satz = Gemeinkosten Material × 100 ÷ Fertigungsmaterial = ____________ %     "
                    "FGK-Satz (Fertigung I) = Gemeinkosten Fertigung I × 100 ÷ Fertigungslöhne Handarbeit = ____________ %")
    d.save(pfad)


def loesung(pfad):
    d = quer("Lehrkraft: Lösung Erweiterung (Vorkostenstellen)")
    prim, u1, zw, u2, end = vorkostenumlage()
    rows = []
    for k, p in zip(VK_STELLEN, prim):
        if k == "Fuhrpark":
            rows.append([k, f0(p), f0(-p), "0", "", "0"])
        elif k == "Fertigungsplanung":
            rows.append([k, f0(p), "+" + f0(u1[k]), f0(zw[k]), f0(-zw[k]), "0"])
        else:
            rows.append([k, f0(p), "+" + f0(u1[k]) if u1.get(k) else "0", f0(zw[k]), "+" + f0(u2[k]) if u2.get(k) else "", f0(end[k])])
    tabelle(d, ["Kostenstelle", "Nach Schritt 1", "Umlage Fuhrpark", "Zwischensumme", "Umlage Fertigungsplanung", "Endsumme"],
            rows, [5, 3.8, 3.8, 3.8, 4.4, 3.8], rechts=(1, 2, 3, 4, 5))
    d.add_paragraph("Endsummen der Hauptkostenstellen: Material 39.400, Fertigung I 50.625, Fertigung II 85.200, Verwaltung 56.000, "
                    "Vertrieb 35.700 (zusammen 266.925). Sätze: MGK 19,70 %, FGK I 81,00 % (wie in Stufe 2).")
    d.save(pfad)


def xlsx(pfad):
    wb = Workbook()
    ws = wb.active
    ws.title = "Umlage"
    gelb = PatternFill("solid", fgColor="FFF2CC")
    kopf = PatternFill("solid", fgColor="D9E2F3")
    rahmen = Border(*(Side(style="thin"),) * 4)
    ws["A1"] = "Umlage im Treppenstufenverfahren – Montelli GmbH, Juli"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "Gelbe Felder ausfüllen (Beträge nach Schritt 1 und Schlüsselzahlen). Umlagen und Summen rechnet die Tabelle."
    heads = ["Kostenstelle", "Nach Schritt 1 (€)", "Schlüssel Fuhrpark", "Umlage Fuhrpark (€)", "Zwischensumme (€)",
             "Schlüssel Fertigungsplanung", "Umlage Fertigungsplanung (€)", "Endsumme (€)"]
    for i, h in enumerate(heads):
        c = ws.cell(row=4, column=i + 1, value=h)
        c.font = Font(bold=True)
        c.fill = kopf
        c.border = rahmen
    r0 = 5
    for i, k in enumerate(VK_STELLEN):
        r = r0 + i
        ws.cell(row=r, column=1, value=k).border = rahmen
        for col in (2, 3, 6):
            c = ws.cell(row=r, column=col)
            c.border = rahmen
            if not (col in (3, 6) and k in ("Fuhrpark",)) and not (col == 6 and k not in ("Fertigung I", "Fertigung II")):
                c.fill = gelb
        # Umlage Fuhrpark
        if k == "Fuhrpark":
            ws.cell(row=r, column=4, value=f"=-B{r}")
        else:
            ws.cell(row=r, column=4, value=f'=IF(C{r}="",0,ROUND($B${r0}*C{r}/SUM($C${r0 + 1}:$C${r0 + 6}),2))')
        ws.cell(row=r, column=5, value=f"=B{r}+D{r}")
        # Umlage Fertigungsplanung
        if k == "Fertigungsplanung":
            ws.cell(row=r, column=7, value=f"=-E{r}")
        elif k in ("Fertigung I", "Fertigung II"):
            ws.cell(row=r, column=7, value=f'=IF(F{r}="",0,ROUND($E${r0 + 2}*F{r}/SUM($F${r0 + 3}:$F${r0 + 4}),2))')
        else:
            ws.cell(row=r, column=7, value=0)
        ws.cell(row=r, column=8, value=f"=E{r}+G{r}")
        for col in (2, 4, 5, 7, 8):
            ws.cell(row=r, column=col).number_format = "#,##0.00"
            ws.cell(row=r, column=col).border = rahmen
    rs = r0 + len(VK_STELLEN)
    ws.cell(row=rs, column=1, value="Summe").font = Font(bold=True)
    for col in (2, 4, 5, 7, 8):
        L = "ABCDEFGH"[col - 1]
        c = ws.cell(row=rs, column=col, value=f"=SUM({L}{r0}:{L}{rs - 1})")
        c.font = Font(bold=True)
        c.number_format = "#,##0.00"
        c.border = rahmen
    ws.column_dimensions["A"].width = 24
    for L in "BCDEFGH":
        ws.column_dimensions[L].width = 22
    wb.save(pfad)


def main():
    ab(ROOT / "material/AB-bx-vorkostenstellen.docx")
    xlsx(ROOT / "material/umlage-vorlage.xlsx")
    loesung(ROOT / "lehrkraft/Loesung-Erweiterung.docx")
    print("✓ Material Erweiterung erzeugt")


if __name__ == "__main__":
    main()
