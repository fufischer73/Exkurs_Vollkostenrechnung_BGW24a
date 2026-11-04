"""Erzeugt Arbeitsblätter (docx), Excel-Vorlage (xlsx) und Lehrkraft-Lösungen für Stufe 2 (BAB).
Aufruf (aus dem Lernpfad-Ordner):  python3 werkzeuge/material_stufe2.py
"""
import sys
from pathlib import Path

from docx.enum.section import WD_ORIENT
from docx.shared import Cm
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side

sys.path.insert(0, str(Path(__file__).parent))
from daten import JULI, AUGUST, ORDER, SCHLUESSEL, auswerten, fmt  # noqa: E402
from material_stufe1 import neues_dokument, tabelle, ueberschrift  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
KOEPFE = ["Material", "Fertigung I", "Fertigung II", "Verwaltung", "Vertrieb"]
DIREKT = [a for a in ORDER if a not in SCHLUESSEL]


def quer(titel, untertitel):
    d = neues_dokument(titel, untertitel)
    s = d.sections[0]
    s.orientation = WD_ORIENT.LANDSCAPE
    s.page_width, s.page_height = Cm(29.7), Cm(21)
    s.left_margin = s.right_margin = Cm(1.5)
    s.top_margin = s.bottom_margin = Cm(1.3)
    return d


def f0(x):
    return fmt(x, 0)


def bab_tabelle(d, m, voll=False):
    bab = m["bab"]
    zeilen = []
    for art in ORDER:
        v = bab[art]
        if voll:
            zeilen.append([art, f0(sum(v))] + [f0(x) for x in v])
        else:
            zeilen.append([art, f0(sum(v))] + [""] * 5)
    sp = auswerten(m)["spalten"]
    zeilen.append(["Summe", f0(sum(sp))] + ([f0(x) for x in sp] if voll else [""] * 5))
    tabelle(d, ["Gemeinkostenart", "Summe (Kostenartenplan)"] + KOEPFE, zeilen, [5.2, 3.6] + [3.4] * 5,
            rechts=(1, 2, 3, 4, 5, 6), fett_zeilen=(len(zeilen) - 1,), leer_hoehe=None if voll else 0.8)


def info_belege(d, m):
    ueberschrift(d, "Direkte Zuordnung (Belegauswertung, Beträge in €)")
    zeilen = [[a] + [f0(x) for x in m["bab"][a]] for a in DIREKT]
    tabelle(d, ["Gemeinkostenart"] + KOEPFE, zeilen, [6.5] + [3.8] * 5, rechts=(1, 2, 3, 4, 5))
    ueberschrift(d, "Verteilungsschlüssel")
    zeilen = [[k] + [str(SCHLUESSEL[a][1][i]) for a in ("Betriebsstoffe", "Kalk. Zinsen", "Leasing")]
              for i, k in enumerate(KOEPFE)]
    tabelle(d, ["Kostenstelle", "Betriebsstoffe: Verbrauch in kWh", "Kalk. Zinsen: gebundenes Kapital", "Leasing: Fläche in m²"],
            zeilen, [6, 6.5, 6.5, 5], rechts=(1, 2, 3))


def zeilen_linien(d, n=2):
    for _ in range(n):
        d.add_paragraph("_" * 110)


def nebenrechnung_tabelle(d, werte=None):
    z = ["Fertigungsmaterial", "+ Materialgemeinkosten (MGK)", "= Materialkosten",
         "Fertigungslöhne (Handarbeit)", "+ Fertigungsgemeinkosten (FGK)", "= Fertigungskosten I",
         "Maschinenabhängige Fertigungsgemeinkosten", "+ Fertigungslöhne des Maschinenplatzes", "+ Restgemeinkosten",
         "= Fertigungskosten II", "= Herstellkosten der Erzeugung", "+ Bestandsminderungen / − Bestandsmehrungen",
         "= Herstellkosten des Umsatzes"]
    rows = [(t, werte[i] if werte else "") for i, t in enumerate(z)]
    fett = tuple(i for i, t in enumerate(z) if t.startswith("="))
    tabelle(d, ["Nebenrechnung", "Betrag in €"], rows, [10, 5], rechts=(1,), fett_zeilen=fett, leer_hoehe=None if werte else 0.7)


def neben_werte(m):
    a = auswerten(m)
    r = a["saetze"]
    fm, fl1, fl2 = a["fm"], m["fl1"], m["fl2"]
    mgk, fgk1, _, vw, vt = a["spalten"]
    masch, rest = a["masch"]
    mk = fm + mgk
    fk1 = fl1 + fgk1
    fk2 = masch + fl2 + rest
    return [fmt(fm), fmt(mgk), fmt(mk), fmt(fl1), fmt(fgk1), fmt(fk1), fmt(masch), fmt(fl2), fmt(rest), fmt(fk2),
            fmt(mk + fk1 + fk2), fmt(0), fmt(r["HKdU"])]


# ---------------------------------------------------------------- Arbeitsblätter
def ab_b1(pfad):
    d = quer("Arbeitsblatt B1 · BAB Juli, Schritt 1: Gemeinkosten verteilen", "Montelli GmbH · Geschäftsbereich Outdoor · Exkurs Vollkostenrechnung")
    info_belege(d, JULI)
    ueberschrift(d, "Aufgabe · Betriebsabrechnungsbogen (BAB) Juli (Beträge in €)")
    d.add_paragraph("Verteile die Gemeinkosten auf die Kostenstellen. Probe: Zeilensummen = Kostenartenplan, Summe aller Spalten = 266.925 €.")
    bab_tabelle(d, JULI)
    d.save(pfad)


def ab_b2b4(pfad):
    d = neues_dokument("Arbeitsblatt B2 bis B4 · Zuschlagssätze, Maschinenplatz, Herstellkosten",
                       "Montelli GmbH · Monat Juli · Exkurs Vollkostenrechnung")
    sp = auswerten(JULI)["spalten"]
    ueberschrift(d, "Bezugsgrößen Juli")
    tabelle(d, ["Bezugsgröße", "Wert"], [
        ("Fertigungsmaterial (Rohstoffe + Vorprodukte/Fremdbauteile)", "200.000,00 €"),
        ("Fertigungslöhne Handarbeit (Fertigung I)", "62.500,00 €"),
        ("Fertigungslöhne Maschinenplatz (Fertigung II)", "14.000,00 €"),
        ("Maschinenstunden", "1.000 h"),
        ("Bestandsveränderungen", "keine"),
    ], [11, 5], rechts=(1,))
    d.add_paragraph("Falls dein BAB aus B1 nicht stimmt, nimm diese Gemeinkosten je Kostenstelle: "
                    + ", ".join(f"{k} {fmt(v)} €" for k, v in zip(KOEPFE, sp)) + ".")
    ueberschrift(d, "B2 · Zuschlagssätze für Material und Fertigung I")
    d.add_paragraph("MGK-Satz = Gemeinkosten Material × 100 ÷ Fertigungsmaterial = __________________ = ________ %")
    d.add_paragraph("FGK-Satz (Fertigung I) = Gemeinkosten Fertigung I × 100 ÷ Fertigungslöhne Handarbeit = __________________ = ________ %")
    d.add_paragraph("Bedeutung: Auf 100 € ___________________ entfallen ________ € ___________________.")
    d.add_paragraph("Auftrag: Fertigungsmaterial 4.200 €, Fertigungslöhne Handarbeit 2.600 €. MGK = __________ €, FGK = __________ €.")
    ueberschrift(d, "B3 · Maschinenplatz")
    d.add_paragraph("Gemeinkosten Fertigung II (BAB): __________ € = maschinenabhängig __________ € + Rest __________ €")
    d.add_paragraph("Maschinenstundensatz = maschinenabhängige Gemeinkosten ÷ Maschinenstunden = __________________ = ________ € je h")
    d.add_paragraph("Restgemeinkosten-Satz = Restgemeinkosten × 100 ÷ Maschinenplatzlöhne = __________________ = ________ %")
    d.add_paragraph("Auftrag: 2 Maschinenstunden, Maschinenplatzlöhne 28 €. Maschinenkosten = __________ €, Restgemeinkosten = __________ €.")
    ueberschrift(d, "B4 · Herstellkosten des Umsatzes")
    nebenrechnung_tabelle(d)
    d.add_paragraph("VwGK-Satz = Gemeinkosten Verwaltung × 100 ÷ Herstellkosten des Umsatzes = __________________ = ________ %")
    d.add_paragraph("VtGK-Satz = Gemeinkosten Vertrieb × 100 ÷ Herstellkosten des Umsatzes = __________________ = ________ %")
    d.add_paragraph("Summe beider Sätze: ________ %  (Lernsituation: 20 %)")
    d.save(pfad)


def ab_bm(pfad):
    d = quer("Arbeitsblatt Meilenstein 2 · BAB und Zuschlagssätze August", "Montelli GmbH · Geschäftsbereich Outdoor · Exkurs Vollkostenrechnung")
    a = auswerten(AUGUST)
    ueberschrift(d, "Bezugsgrößen August")
    tabelle(d, ["Bezugsgröße", "Wert"], [
        ("Fertigungsmaterial (Rohstoffe + Vorprodukte/Fremdbauteile)", fmt(a["fm"]) + " €"),
        ("Fertigungslöhne Handarbeit (Fertigung I)", fmt(AUGUST["fl1"]) + " €"),
        ("Fertigungslöhne Maschinenplatz (Fertigung II)", fmt(AUGUST["fl2"]) + " €"),
        ("Maschinenstunden", f"{AUGUST['masch_std']} h"),
        ("Bestandsveränderungen", "keine"),
    ], [11, 5], rechts=(1,))
    info_belege(d, AUGUST)
    d.add_paragraph("Die Verteilungsschlüssel (Schlüsselzahlen) gelten unverändert wie im Juli.")
    ueberschrift(d, "Aufgabe 1 · BAB August (Beträge in €)")
    bab_tabelle(d, AUGUST)
    ueberschrift(d, "Aufgabe 2 · Maschinenplatz und Zuschlagssätze")
    tabelle(d, ["Satz", "Rechnung", "Ergebnis"], [
        ("MGK-Satz", "", ""), ("FGK-Satz (Fertigung I)", "", ""), ("Maschinenstundensatz", "", ""),
        ("Restgemeinkosten-Satz", "", ""), ("VwGK-Satz", "", ""), ("VtGK-Satz", "", ""),
    ], [6, 14, 4], leer_hoehe=0.8)
    d.add_paragraph("Maschinenabhängige Gemeinkosten (Fertigung II): __________ €   Restgemeinkosten: __________ €")
    ueberschrift(d, "Aufgabe 3 · Nebenrechnung Herstellkosten des Umsatzes")
    nebenrechnung_tabelle(d)
    ueberschrift(d, "Aufgabe 4 · Auswertung")
    for f in ["1. In welcher Kostenstelle fällt der größte Gemeinkostenbetrag an? Wie hoch ist er?",
              "2. Vergleiche die Sätze mit Juli. Welche sind gestiegen? Erkläre.",
              "3. Ein Kunde bestellt Rucksäcke mit Fertigungsmaterial von 3.000 €. Wie hoch sind die Materialgemeinkosten?",
              "4. Was bedeutet dein Maschinenstundensatz in einem Satz?"]:
        d.add_paragraph(f)
        zeilen_linien(d, 2)
    d.save(pfad)


def loesungen(pfad):
    d = quer("Lehrkraft: Lösungen Stufe 2", "Nicht an Schüler:innen weitergeben.")
    for m, titel in ((JULI, "Juli (B1 bis B4)"), (AUGUST, "August (Meilenstein 2)")):
        a = auswerten(m)
        r = a["saetze"]
        ueberschrift(d, f"BAB {titel}")
        bab_tabelle(d, m, voll=True)
        d.add_paragraph(f"Maschinenabhängig (Fertigung II): {fmt(a['masch'][0])} € · Rest: {fmt(a['masch'][1])} € · Maschinenstunden: {m['masch_std']} h · "
                        f"Maschinenplatzlöhne: {fmt(m['fl2'])} €")
        tabelle(d, ["Satz", "Wert"], [
            ("MGK-Satz", f"{r['MGK %']:.2f} %".replace(".", ",")),
            ("FGK-Satz (Fertigung I)", f"{r['FGK I %']:.2f} %".replace(".", ",")),
            ("Maschinenstundensatz", f"{r['Maschinenstundensatz']:.2f} € je h".replace(".", ",")),
            ("Restgemeinkosten-Satz", f"{r['Rest %']:.2f} %".replace(".", ",")),
            ("VwGK-Satz", f"{r['VwGK %']:.2f} %".replace(".", ",")),
            ("VtGK-Satz", f"{r['VtGK %']:.2f} %".replace(".", ",")),
        ], [8, 6], rechts=(1,))
        nebenrechnung_tabelle(d, neben_werte(m))
    d.add_paragraph("Auswertung August (Erwartungshorizont): 1. Größter Betrag in Fertigung II (82.050 €). "
                    "2. Alle Sätze sind höher als im Juli. Die Menge (Fertigungsmaterial, Löhne, Maschinenstunden) sank, "
                    "die Gemeinkosten blieben aber fast gleich, vor allem Abschreibungen, Zinsen, Gehälter und Leasing. "
                    "3. 3.000 € × 21,63 ÷ 100 = 648,90 €. 4. Eine Maschinenstunde verursacht 86,61 € Maschinenkosten.")
    d.add_paragraph("Hinweis: Bei Rundung der Sätze auf zwei Dezimalstellen kann die Nachrechnung um wenige Cent abweichen. Das ist in Ordnung.")
    d.save(pfad)


# ---------------------------------------------------------------- Excel
def xlsx_bab(pfad):
    wb = Workbook()
    ws = wb.active
    ws.title = "BAB"
    gelb = PatternFill("solid", fgColor="FFF2CC")
    kopf = PatternFill("solid", fgColor="D9E2F3")
    rahmen = Border(*(Side(style="thin"),) * 4)
    ws["A1"] = "Betriebsabrechnungsbogen (BAB) – Montelli GmbH, Geschäftsbereich Outdoor"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "Gelbe Felder ausfüllen. Summen, Sätze und Herstellkosten rechnet die Tabelle (Beträge in €)."
    heads = ["Gemeinkostenart", "Summe (Kostenartenplan)"] + KOEPFE + ["Probe"]
    for i, h in enumerate(heads):
        c = ws.cell(row=4, column=i + 1, value=h)
        c.font = Font(bold=True)
        c.fill = kopf
        c.border = rahmen
    r0 = 5
    for i, art in enumerate(ORDER):
        r = r0 + i
        ws.cell(row=r, column=1, value=art).border = rahmen
        for col in range(2, 8):
            c = ws.cell(row=r, column=col)
            c.fill = gelb
            c.border = rahmen
            c.number_format = "#,##0.00"
        ws.cell(row=r, column=8, value=f'=IF(B{r}="","",IF(ROUND(B{r}-SUM(C{r}:G{r}),2)=0,"stimmt","stimmt nicht"))')
    rs = r0 + len(ORDER)
    ws.cell(row=rs, column=1, value="Summe").font = Font(bold=True)
    for col in range(2, 8):
        L = "ABCDEFG"[col - 1]
        c = ws.cell(row=rs, column=col, value=f"=SUM({L}{r0}:{L}{rs - 1})")
        c.font = Font(bold=True)
        c.number_format = "#,##0.00"
        c.border = rahmen
    ws.cell(row=rs, column=8, value=f'=IF(ROUND(B{rs}-SUM(C{rs}:G{rs}),2)=0,"stimmt","stimmt nicht")')
    # Bezugsgrößen
    b = rs + 2
    ws.cell(row=b, column=1, value="Bezugsgrößen").font = Font(bold=True)
    labels = ["Fertigungsmaterial (€)", "Fertigungslöhne Handarbeit, Fertigung I (€)", "Fertigungslöhne Maschinenplatz (€)",
              "Maschinenstunden (h)", "Bestandsveränderung (+ Minderung / − Mehrung, €)",
              "davon maschinenabhängige Gemeinkosten Fertigung II (€)"]
    for i, t in enumerate(labels):
        ws.cell(row=b + 1 + i, column=1, value=t)
        c = ws.cell(row=b + 1 + i, column=2)
        c.fill = gelb
        c.border = rahmen
        c.number_format = "#,##0.00"
    fm, fl1, fl2, std, best, mab = [f"B{b + 1 + i}" for i in range(6)]
    rest = b + 7
    ws.cell(row=rest, column=1, value="Restgemeinkosten Fertigung II (€)")
    ws.cell(row=rest, column=2, value=f"=E{rs}-{mab}").number_format = "#,##0.00"
    # Nebenrechnung
    n = rest + 2
    ws.cell(row=n, column=1, value="Nebenrechnung Herstellkosten des Umsatzes").font = Font(bold=True)
    zeilen = [
        ("Fertigungsmaterial", f"={fm}"),
        ("+ Materialgemeinkosten", f"=C{rs}"),
        ("= Materialkosten", f"=B{n + 1}+B{n + 2}"),
        ("Fertigungslöhne (Handarbeit)", f"={fl1}"),
        ("+ Fertigungsgemeinkosten", f"=D{rs}"),
        ("= Fertigungskosten I", f"=B{n + 4}+B{n + 5}"),
        ("Maschinenabhängige Fertigungsgemeinkosten", f"={mab}"),
        ("+ Fertigungslöhne Maschinenplatz", f"={fl2}"),
        ("+ Restgemeinkosten", f"=B{rest}"),
        ("= Fertigungskosten II", f"=B{n + 7}+B{n + 8}+B{n + 9}"),
        ("= Herstellkosten der Erzeugung", f"=B{n + 3}+B{n + 6}+B{n + 10}"),
        ("+ Bestandsminderungen / − Bestandsmehrungen", f"={best}"),
        ("= Herstellkosten des Umsatzes", f"=B{n + 11}+B{n + 12}"),
    ]
    for i, (t, f) in enumerate(zeilen):
        ws.cell(row=n + 1 + i, column=1, value=(" " + t) if t.startswith(("=", "+")) else t)
        c = ws.cell(row=n + 1 + i, column=2, value=f)
        c.number_format = "#,##0.00"
        if t.startswith("="):
            ws.cell(row=n + 1 + i, column=1).font = Font(bold=True)
            c.font = Font(bold=True)
    hk = f"B{n + 13}"
    # Sätze
    s = n + 15
    ws.cell(row=s, column=1, value="Zuschlagssätze").font = Font(bold=True)
    saetze = [
        ("MGK-Satz (%)", f'=IF({fm}="","",C{rs}/{fm}*100)'),
        ("FGK-Satz Fertigung I (%)", f'=IF({fl1}="","",D{rs}/{fl1}*100)'),
        ("Maschinenstundensatz (€ je h)", f'=IF({std}="","",{mab}/{std})'),
        ("Restgemeinkosten-Satz (%)", f'=IF({fl2}="","",B{rest}/{fl2}*100)'),
        ("VwGK-Satz (%)", f'=IF({hk}=0,"",F{rs}/{hk}*100)'),
        ("VtGK-Satz (%)", f'=IF({hk}=0,"",G{rs}/{hk}*100)'),
    ]
    for i, (t, f) in enumerate(saetze):
        ws.cell(row=s + 1 + i, column=1, value=t)
        ws.cell(row=s + 1 + i, column=2, value=f).number_format = "#,##0.00"
    ws.column_dimensions["A"].width = 52
    for L in "BCDEFGH":
        ws.column_dimensions[L].width = 18
    wb.save(pfad)


def main():
    ab_b1(ROOT / "material/AB-b1-bab-verteilung.docx")
    ab_b2b4(ROOT / "material/AB-b2-b4-zuschlagssaetze.docx")
    ab_bm(ROOT / "material/AB-bm-bab-august.docx")
    xlsx_bab(ROOT / "material/bab-vorlage.xlsx")
    loesungen(ROOT / "lehrkraft/Loesungen-Stufe-2.docx")
    print("✓ Material Stufe 2 erzeugt")


if __name__ == "__main__":
    main()
