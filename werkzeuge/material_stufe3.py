"""Erzeugt Arbeitsblätter (docx), Excel-Vorlage (xlsx) und Lehrkraft-Lösungen für Stufe 3 (Kalkulation).
Aufruf (aus dem Lernpfad-Ordner):  python3 werkzeuge/material_stufe3.py
"""
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side

sys.path.insert(0, str(Path(__file__).parent))
from daten import ISTSAETZE, NORMAL, SAETZE_NAMEN, BUSINESS_DELUXE, EXPLORER, kalkulation, fmt  # noqa: E402
from material_stufe1 import neues_dokument, tabelle, ueberschrift  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
EXPLORER_PARAM = (18, 2, 5)  # Gewinn, Skonto, Rabatt in %

ZEILEN = [  # (Beschriftung, Schlüssel in kalkulation(), Bemerkung für die Lösung, Zwischensumme?)
    ("Fertigungsmaterial", "Fertigungsmaterial", "", False),
    ("+ Materialgemeinkosten", "MGK", "20 % vom Hundert (von Fertigungsmaterial)", False),
    ("= Materialkosten", "Materialkosten", "", True),
    ("Fertigungslöhne", "Fertigungslöhne", "", False),
    ("+ Fertigungsgemeinkosten", "FGK", "80 % vom Hundert (von Fertigungslöhnen)", False),
    ("= Fertigungskosten I", "Fertigungskosten I", "", True),
    ("Maschinenabhängige Fertigungsgemeinkosten", "Maschinenkosten", "Maschinenstunden × 80,00 € je h", False),
    ("+ Fertigungslöhne des Maschinenplatzes", "Maschinenlöhne", "Maschinenstunden × 14,00 € je h", False),
    ("+ Restgemeinkosten", "Restgemeinkosten", "30 % vom Hundert (von Maschinenplatzlöhnen)", False),
    ("= Fertigungskosten II", "Fertigungskosten II", "", True),
    ("Herstellkosten (Material- und Fertigungskosten I und II)", "Herstellkosten", "", True),
    ("+ Verwaltungs- und Vertriebsgemeinkosten", "Verwaltung/Vertrieb", "20 % vom Hundert (von Herstellkosten)", False),
    ("= Selbstkosten", "Selbstkosten", "", True),
    ("+ Gewinnzuschlag", "Gewinn", "vom Hundert (von Selbstkosten)", False),
    ("= Barverkaufspreis", "Barverkaufspreis", "", True),
    ("+ Kundenskonto", "Skonto", "im Hundert (vom Zielverkaufspreis)", False),
    ("= Zielverkaufspreis", "Zielverkaufspreis", "", True),
    ("+ Kundenrabatt", "Rabatt", "im Hundert (vom Listenverkaufspreis)", False),
    ("= Listenverkaufspreis (netto)", "Listenverkaufspreis", "", True),
]


def schema_tabelle(d, werte=None, bem=None):
    rows = []
    for t, k, b, _ in ZEILEN:
        rows.append((t, fmt(werte[k]) if werte else "", (bem or {}).get(k, b) if werte else ""))
    fett = tuple(i for i, z in enumerate(ZEILEN) if z[3])
    tabelle(d, ["Kalkulationsschema", "Betrag in €", "Bemerkungen"], rows, [7.2, 3.0, 7.0], rechts=(1,),
            fett_zeilen=fett, leer_hoehe=None if werte else 0.75)


def ab_t1(pfad):
    d = neues_dokument("Arbeitsblatt T1 · Normalsätze", "Montelli GmbH · Exkurs Vollkostenrechnung")
    ueberschrift(d, "Aufgabe 1 · Normalsätze berechnen")
    d.add_paragraph("Normalsatz = Summe der Istsätze ÷ Anzahl der Monate")
    rows = []
    for i, n in enumerate(SAETZE_NAMEN):
        rows.append([n] + [f"{v[i]:.2f}".replace(".", ",") for v in ISTSAETZE.values()] + [""])
    rows = [r[:-1] + ["", ""] for r in rows]
    tabelle(d, ["Satz"] + list(ISTSAETZE) + ["Rechnung (Summe ÷ 4)", "Normalsatz"], rows, [4.6, 1.4, 1.4, 1.4, 1.4, 4.2, 2.6],
            rechts=(1, 2, 3, 4, 6), leer_hoehe=1.3)
    ueberschrift(d, "Aufgabe 2 · Vergleich mit der Lernsituation")
    d.add_paragraph("Vergleiche deine Normalsätze mit Info 2 der Lernsituation „Preise kalkulieren“. Was fällt dir auf?")
    for _ in range(2):
        d.add_paragraph("_" * 78)
    ueberschrift(d, "Aufgabe 3 · Ein gemeinsamer Satz für Verwaltung und Vertrieb")
    d.add_paragraph("Wie kommst du auf den gemeinsamen Satz der Lernsituation?  ________ % + ________ % = ________ %")
    d.save(pfad)


def ab_t2t3(pfad):
    d = neues_dokument("Arbeitsblatt T2 und T3 · Kalkulation Rucksack Business Deluxe",
                       "Montelli GmbH · Exkurs Vollkostenrechnung")
    ueberschrift(d, "Angaben (je Rucksack)")
    tabelle(d, ["Fertigungsmaterial", "Kosten"], [
        ("Außenmaterial (wasserabweisendes Gewebe)", "14,00 €"), ("Innenfutter", "5,00 €"), ("Reißverschlusssystem", "4,50 €"),
        ("Trage- und Gurtsystem (inkl. Polsterung)", "9,00 €"), ("Beschläge und Schnallen", "3,50 €"),
        ("Laptopfach-Polsterung", "4,00 €")], [11, 4], rechts=(1,))
    tabelle(d, ["Fertigungslöhne (Handarbeit)", "Lohn je Stunde", "Zeit je Rucksack"], [
        ("Lohngruppe 1 (Zuschnitt, Verpackung)", "13,00 €", "0,30 h"),
        ("Lohngruppe 2 (Nähen, Montage)", "14,00 €", "0,40 h"),
        ("Lohngruppe 3 (Verstärkungsnähte, Qualitätskontrolle)", "16,00 €", "0,20 h")], [9, 3, 3], rechts=(1, 2))
    d.add_paragraph("Maschinenplatz: 0,20 Maschinenstunden je Rucksack, Lohn der Bedienung (Lohngruppe 2) 14,00 € je Stunde.")
    d.add_paragraph("Normalsätze: MGK 20 %, FGK 80 %, Maschinenstundensatz 80 € je h, Restgemeinkosten 30 % (Maschinenplatzlöhne), "
                    "Verwaltung und Vertrieb 20 % (Herstellkosten). Gewinnzuschlag 20 %, Kundenskonto 3 %, Kundenrabatt 10 %.")
    ueberschrift(d, "Aufgabe · Kalkulationsschema (bis Selbstkosten in T2, ab Selbstkosten in T3)")
    schema_tabelle(d)
    d.save(pfad)


def ab_tm(pfad):
    d = neues_dokument("Arbeitsblatt Meilenstein 3 · Kalkulation Rucksack Explorer",
                       "Montelli GmbH · Exkurs Vollkostenrechnung")
    ueberschrift(d, "Angaben (je Rucksack Explorer)")
    tabelle(d, ["Fertigungsmaterial", "Kosten"], [
        ("Außenmaterial", "13,00 €"), ("Innenfutter", "4,00 €"), ("Reißverschlusssystem", "4,50 €"),
        ("Trage- und Gurtsystem (inkl. Polsterung)", "9,00 €"), ("Beschläge und Schnallen", "3,00 €"),
        ("Regenhülle", "3,00 €")], [11, 4], rechts=(1,))
    tabelle(d, ["Fertigungslöhne (Handarbeit)", "Lohn je Stunde", "Zeit je Rucksack"], [
        ("Lohngruppe 1", "13,00 €", "0,25 h"), ("Lohngruppe 2", "14,00 €", "0,35 h"), ("Lohngruppe 3", "16,00 €", "0,15 h")],
        [9, 3, 3], rechts=(1, 2))
    d.add_paragraph("Maschinenplatz: 0,15 Maschinenstunden, Lohn der Bedienung (Lohngruppe 2) 14,00 € je Stunde.")
    d.add_paragraph("Normalsätze wie in Modul T1. Gewinnzuschlag 18 %, Kundenskonto 2 %, Kundenrabatt 5 %.")
    ueberschrift(d, "Aufgabe 1 · Kalkulationsschema")
    schema_tabelle(d)
    ueberschrift(d, "Aufgabe 2 · Einzel- und Gemeinkosten")
    d.add_paragraph("Einzelkosten der Selbstkosten: ____________ €   Gemeinkosten: ____________ €   Anteil der Gemeinkosten: ______ %")
    ueberschrift(d, "Aufgabe 3 · Vergleich mit dem aktuellen Preis")
    d.add_paragraph("Der Explorer wird für 149,00 € verkauft. Was sagt der Vergleich mit deinem Ergebnis aus? Welche Fragen stellst du dir?")
    for _ in range(4):
        d.add_paragraph("_" * 78)
    d.save(pfad)


def bemerkungen_explorer():
    return {
        "MGK": "20 % vom Hundert (von Fertigungsmaterial)", "FGK": "80 % vom Hundert (von Fertigungslöhnen)",
        "Maschinenkosten": "0,15 h × 80,00 € je h", "Maschinenlöhne": "0,15 h × 14,00 € je h",
        "Restgemeinkosten": "30 % vom Hundert (von Maschinenplatzlöhnen)",
        "Verwaltung/Vertrieb": "20 % vom Hundert (von Herstellkosten)", "Gewinn": "18 % vom Hundert (von Selbstkosten)",
        "Skonto": "2 % im Hundert (vom Zielverkaufspreis): Barverkaufspreis ÷ 0,98",
        "Rabatt": "5 % im Hundert (vom Listenverkaufspreis): Zielverkaufspreis ÷ 0,95",
    }


def loesungen(pfad):
    d = neues_dokument("Lehrkraft: Lösungen Stufe 3", "Nicht an Schüler:innen weitergeben.")
    ueberschrift(d, "T1 · Normalsätze")
    tabelle(d, ["Satz", "Normalsatz"], [(n, f"{NORMAL[i]:.2f}".replace(".", ",")) for i, n in enumerate(SAETZE_NAMEN)], [9, 4], rechts=(1,))
    ueberschrift(d, "T2 und T3 · Business Deluxe")
    k = kalkulation(**BUSINESS_DELUXE)
    schema_tabelle(d, k, {"Maschinenkosten": "0,20 h × 80,00 € je h", "Maschinenlöhne": "0,20 h × 14,00 € je h",
                          "Gewinn": "20 % vom Hundert (von Selbstkosten)",
                          "Skonto": "3 % im Hundert (vom Zielverkaufspreis): 130,32 € ÷ 0,97",
                          "Rabatt": "10 % im Hundert (vom Listenverkaufspreis): 134,35 € ÷ 0,90"})
    ueberschrift(d, "Meilenstein 3 · Explorer")
    g, s, r = EXPLORER_PARAM
    e = kalkulation(EXPLORER["fm"], EXPLORER["lohn"], EXPLORER["masch_std"], EXPLORER["masch_lohn_satz"], g, s, r)
    schema_tabelle(d, e, bemerkungen_explorer())
    ek = e["Fertigungsmaterial"] + e["Fertigungslöhne"] + e["Maschinenlöhne"]
    gk = e["Selbstkosten"] - ek
    anteil = str(round(gk / e["Selbstkosten"] * 100, 1)).replace(".", ",")
    d.add_paragraph(f"Aufgabe 2: Einzelkosten {fmt(ek)} € (Fertigungsmaterial 36,50 + Fertigungslöhne 10,55 + Maschinenplatzlöhne 2,10), "
                    f"Gemeinkosten {fmt(gk)} €, Anteil {anteil} % der Selbstkosten (ähnlich dem Anteil in Modul G1).")
    d.add_paragraph("Aufgabe 3 (Erwartungshorizont): Der kostenorientierte Listenpreis (117,89 €) liegt deutlich unter dem aktuellen Preis (149,00 €). "
                    "Mögliche Fragen: Ist der Explorer bisher sehr profitabel? Zahlen Kunden den höheren Preis wegen Marke und Qualität? "
                    "Wie sieht es bei der Konkurrenz aus? Das führt zu den Teilen 2 bis 4 der Preispolitik (wettbewerbs- und nachfrageorientiert).")
    d.add_paragraph("Lernerfolgskontrolle: Moodle-Test aus fragen/abschluss.yaml, zehn Fragen, automatisch bewertet.")
    d.save(pfad)


def xlsx_kalkulation(pfad):
    wb = Workbook()
    ws = wb.active
    ws.title = "Kalkulation"
    gelb = PatternFill("solid", fgColor="FFF2CC")
    kopf = PatternFill("solid", fgColor="D9E2F3")
    rahmen = Border(*(Side(style="thin"),) * 4)
    ws["A1"] = "Zuschlagskalkulation – Montelli GmbH"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "Gelbe Felder ausfüllen. Jede Zeile wird auf zwei Dezimalstellen gerundet."
    eingaben = [
        ("Fertigungsmaterial (€ je Stück)", None), ("Fertigungslöhne Handarbeit (€ je Stück)", None),
        ("Maschinenstunden je Stück (h)", None), ("Lohn Maschinenplatz (€ je Stunde)", None),
        ("MGK-Satz (%)", None), ("FGK-Satz (%)", None), ("Maschinenstundensatz (€ je h)", None),
        ("Restgemeinkosten-Satz (%)", None), ("VwGK + VtGK zusammen (%)", None),
        ("Gewinnzuschlag (%)", None), ("Kundenskonto (%)", None), ("Kundenrabatt (%)", None),
    ]
    ws.cell(row=4, column=1, value="Eingaben").font = Font(bold=True)
    for i, (t, _) in enumerate(eingaben):
        r = 5 + i
        ws.cell(row=r, column=1, value=t).border = rahmen
        c = ws.cell(row=r, column=2)
        c.fill = gelb
        c.border = rahmen
        c.number_format = "#,##0.00"
    fm, fl, std, lsatz, mgk, fgk, mss, rest, vv, gew, sko, rab = [f"$B${5 + i}" for i in range(12)]
    z0 = 5 + len(eingaben) + 2
    for i, h in enumerate(["Kalkulationsschema", "Betrag (€)"]):
        c = ws.cell(row=z0, column=i + 1, value=h)
        c.font = Font(bold=True)
        c.fill = kopf
        c.border = rahmen
    R = {}
    namen = ["fm", "mgk", "mk", "fl", "fgk", "fk1", "mkosten", "mlohn", "rest", "fk2", "hk", "vv", "sk", "gew", "bar", "ziel_sko",
             "ziel", "list_rab", "lvp"]
    for i, n in enumerate(namen):
        R[n] = z0 + 1 + i
    f = {
        "fm": f"=ROUND({fm},2)", "mgk": f"=ROUND(B{R['fm']}*{mgk}/100,2)", "mk": f"=B{R['fm']}+B{R['mgk']}",
        "fl": f"=ROUND({fl},2)", "fgk": f"=ROUND(B{R['fl']}*{fgk}/100,2)", "fk1": f"=B{R['fl']}+B{R['fgk']}",
        "mkosten": f"=ROUND({std}*{mss},2)", "mlohn": f"=ROUND({std}*{lsatz},2)", "rest": f"=ROUND(B{R['mlohn']}*{rest}/100,2)",
        "fk2": f"=B{R['mkosten']}+B{R['mlohn']}+B{R['rest']}", "hk": f"=B{R['mk']}+B{R['fk1']}+B{R['fk2']}",
        "vv": f"=ROUND(B{R['hk']}*{vv}/100,2)", "sk": f"=B{R['hk']}+B{R['vv']}",
        "gew": f"=ROUND(B{R['sk']}*{gew}/100,2)", "bar": f"=B{R['sk']}+B{R['gew']}",
        "ziel_sko": f"=ROUND(B{R['ziel']}-B{R['bar']},2)", "ziel": f"=ROUND(B{R['bar']}/(1-{sko}/100),2)",
        "list_rab": f"=ROUND(B{R['lvp']}-B{R['ziel']},2)", "lvp": f"=ROUND(B{R['ziel']}/(1-{rab}/100),2)",
    }
    labels = {
        "fm": "Fertigungsmaterial", "mgk": " + Materialgemeinkosten", "mk": " = Materialkosten", "fl": "Fertigungslöhne",
        "fgk": " + Fertigungsgemeinkosten", "fk1": " = Fertigungskosten I", "mkosten": "Maschinenabhängige Fertigungsgemeinkosten",
        "mlohn": " + Fertigungslöhne des Maschinenplatzes", "rest": " + Restgemeinkosten", "fk2": " = Fertigungskosten II",
        "hk": " = Herstellkosten", "vv": " + Verwaltungs- und Vertriebsgemeinkosten", "sk": " = Selbstkosten",
        "gew": " + Gewinnzuschlag", "bar": " = Barverkaufspreis", "ziel_sko": " + Kundenskonto", "ziel": " = Zielverkaufspreis",
        "list_rab": " + Kundenrabatt", "lvp": " = Listenverkaufspreis (netto)",
    }
    for n in namen:
        ws.cell(row=R[n], column=1, value=labels[n]).border = rahmen
        c = ws.cell(row=R[n], column=2, value=f[n])
        c.number_format = "#,##0.00"
        c.border = rahmen
        if labels[n].strip().startswith("="):
            ws.cell(row=R[n], column=1).font = Font(bold=True)
            c.font = Font(bold=True)
    ws.column_dimensions["A"].width = 54
    ws.column_dimensions["B"].width = 18
    wb.save(pfad)


def main():
    ab_t1(ROOT / "material/AB-t1-normalsaetze.docx")
    ab_t2t3(ROOT / "material/AB-t2-t3-kalkulation.docx")
    ab_tm(ROOT / "material/AB-tm-kalkulation-explorer.docx")
    xlsx_kalkulation(ROOT / "material/kalkulation-vorlage.xlsx")
    loesungen(ROOT / "lehrkraft/Loesungen-Stufe-3.docx")
    print("✓ Material Stufe 3 erzeugt")


if __name__ == "__main__":
    main()
