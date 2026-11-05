"""Erzeugt den Übungsbereich (Stufe 4): Arbeitsblätter (docx), Module (md), Lösungen, Info 9 und Testfragen.
Aufruf (aus dem Lernpfad-Ordner):  python3 werkzeuge/material_uebungen.py      (PDFs danach mit werkzeuge/pdfs.py)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from daten import fmt  # noqa: E402
from uebungen import (UE, MASCHINEN, STROM, PLATZ, ZINS, INST_PROZ, RICHTIG_FALSCH, AKS, HAUPT, HILFS, FERT,  # noqa: E402
                      loese, maschine_loese)
from material_stufe1 import tabelle, ueberschrift, rechenkasten  # noqa: E402
from material_stufe2 import zelle, quer, hoch  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ARTKURZ = {AKS: "Allgemeine\nKostenstelle", HAUPT: "Haupt-\nkostenstelle", HILFS: "Hilfs-\nkostenstelle", FERT: "Fertigungs-\nHauptkostenstelle"}
f0 = lambda x: fmt(x, 0)  # noqa: E731
pct = lambda x: f"{x:.2f} %".replace(".", ",")  # noqa: E731
eur = lambda x: f"{x:.2f} €".replace(".", ",")  # noqa: E731


def breiten(n):
    return [4.4, 2.2] + [round((27.0 - 6.6) / n, 2)] * n


def namen(u):
    return [k.replace(" ", "\n", 1) if len(k) > 11 else k for k in u["sp"]]


def tab_start(d, n):
    t = d.add_table(rows=0, cols=n + 2)
    t.style = "Table Grid"
    t.autofit = False
    for i, w in enumerate(breiten(n)):
        t.columns[i].width = __import__("docx.shared", fromlist=["Cm"]).Cm(w)
    return t


def kopf(t, u, titel, c1="Gemeinkostenart", c2="Summe"):
    n = len(u["sp"])
    if titel:
        r = t.add_row()
        zelle(r.cells[0].merge(r.cells[n + 1]), titel, fett=True, mitte=True)
    r1, r2 = t.add_row(), t.add_row()
    zelle(r1.cells[0].merge(r1.cells[1]), "Gemeinkosten", fett=True, mitte=True)
    for i, a in enumerate(u["art"]):
        zelle(r1.cells[2 + i], ARTKURZ[a], fett=True, mitte=True, klein=True)
    zelle(r2.cells[0], c1, fett=True, mitte=True)
    zelle(r2.cells[1], c2, fett=True, mitte=True)
    for i, k in enumerate(namen(u)):
        zelle(r2.cells[2 + i], k, fett=True, mitte=True, klein=True)


def zeile(t, u, label, werte, fett=False, grau=(), hoehe=0.48, summe=None, breit=False):
    n = len(u["sp"])
    r = t.add_row()
    r.height = __import__("docx.shared", fromlist=["Cm"]).Cm(hoehe)
    if breit:
        zelle(r.cells[0].merge(r.cells[1]), label, fett=fett)
    else:
        zelle(r.cells[0], label, fett=fett)
        zelle(r.cells[1], "" if summe is None else summe, rechts=True, fett=fett, grau=("s" in grau))
    for i in range(n):
        v = werte[i] if werte else ""
        zelle(r.cells[2 + i], "" if v is None else v, rechts=True, fett=fett, grau=i in grau)
    return r


def verteilung_tab(d, u, e):
    t = tab_start(d, len(u["sp"]))
    kopf(t, u, None, c2="Verteilungs-grundlage")
    for art, grundlage, werte, betraege, gesamt in e["zeilen"]:
        r = t.add_row()
        r.height = __import__("docx.shared", fromlist=["Cm"]).Cm(0.48)
        zelle(r.cells[0], art)
        zelle(r.cells[1], grundlage, mitte=True, klein=True)
        schluessel = grundlage.startswith("Schlüssel") or grundlage == "m²"
        for i, v in enumerate(werte):
            zelle(r.cells[2 + i], str(v) if schluessel else f0(v), rechts=True)
    d.add_paragraph()


def umlage_schl_tab(d, u):
    n = len(u["sp"])
    t = tab_start(d, n)
    kopf(t, u, None, c1="Vorkostenstelle", c2="Umlage-grundlage")
    for von, grundlage, teile in u["umlage"]:
        r = t.add_row()
        r.height = __import__("docx.shared", fromlist=["Cm"]).Cm(0.7)
        zelle(r.cells[0], von)
        zelle(r.cells[1], grundlage, mitte=True, klein=True)
        for i, k in enumerate(u["sp"]):
            zelle(r.cells[2 + i], str(teile[k]) if k in teile else "", mitte=True, grau=k not in teile)
    d.add_paragraph()


def bab_form(d, u, e, voll=False):
    n = len(u["sp"])
    sp = u["sp"]
    t = tab_start(d, n)
    kopf(t, u, f"Betriebsabrechnungsbogen (BAB I) {u['monat']} 20.. – {u['name']}")
    for art, grundlage, werte, betraege, gesamt in e["zeilen"]:
        zeile(t, u, art, [f0(x) for x in betraege] if voll else None, summe=f0(gesamt))
    zeile(t, u, "Summen", [f0(e["prim"][k]) for k in sp] if voll else None, fett=True, summe=f0(e["gesamt"]) if voll else "")
    erledigt = set()
    schritte = e["schritte"]
    for i, s in enumerate(schritte):
        grau = tuple(j for j, k in enumerate(sp) if k in erledigt)
        z = zeile(t, u, "Umlage\n" + s["von"], None, grau=("s",) + grau, hoehe=0.66)
        vi = sp.index(s["von"])
        if voll:
            for j, k in enumerate(sp):
                if k == s["von"]:
                    zelle(z.cells[2 + j], f0(-s["betrag"]), rechts=True)
                elif k in s["anteil"]:
                    zelle(z.cells[2 + j], "+" + f0(s["anteil"][k]) if s["anteil"][k] else "0", rechts=True)
        else:
            zelle(z.cells[2 + vi], "↳", mitte=True)
        erledigt.add(s["von"])
        grau = tuple(j for j, k in enumerate(sp) if k in erledigt)
        letzte = i == len(schritte) - 1
        zeile(t, u, "Summen" if letzte else "Zwischensummen", [f0(s["danach"][k]) for k in sp] if voll else None, fett=True,
              grau=("s",) + grau)
    # Zuschlagsgrundlagen und Sätze
    fl, mas = u["fl"], u["maschine"]
    end = e["end"]
    grund, satz = [], []
    for k, a in zip(sp, u["art"]):
        if k == "Material":
            grund.append(f0(u["fm"])); satz.append(pct(e["saetze"]["MGK"]))
        elif k in ("Verwaltung", "Vertrieb"):
            grund.append(f0(e["hkdu"])); satz.append(pct(e["saetze"]["VwGK" if k == "Verwaltung" else "VtGK"]))
        elif k in fl:
            grund.append(f0(fl[k]))
            if mas and k == mas[1]:
                satz.append(pct(e["saetze"]["Rest"]))
            else:
                satz.append(pct(e["saetze"].get("FGK " + k, e["saetze"].get("FGK", 0))))
        else:
            grund.append(None); satz.append(None)
    grau = tuple(j for j, k in enumerate(sp) if k not in fl and k not in ("Material", "Verwaltung", "Vertrieb"))
    zeile(t, u, "Zuschlagsgrundlagen (FM, FL, HKdU)", grund if voll else None, grau=grau, breit=True)
    zeile(t, u, "Zuschlagssätze für MGK, FGK, RGK, VwGK, VtGK (Ist)", satz if voll else None, fett=True, grau=grau, breit=True, hoehe=0.66)
    if mas:
        mi = sp.index(mas[0])
        andere = tuple(j for j in range(n) if j != mi)
        zeile(t, u, "Maschinenstunden gesamt (Std.)", [f0(mas[2]) if j == mi else None for j in range(n)] if voll else None, grau=andere, breit=True)
        zeile(t, u, "Maschinenstundensatz (Istwert)", [eur(e["saetze"]["Maschinenstundensatz"]) if j == mi else None for j in range(n)] if voll else None,
              fett=True, grau=andere, breit=True)
    d.add_paragraph()


def neben(d, u, e, voll=False):
    st = e["end"]
    fm = u["fm"]
    werte = [f"{fm:,.2f}", f"{st['Material']:,.2f}", f"{fm + st['Material']:,.2f}", f"{e['fl_sum']:,.2f}", f"{e['gk_fert']:,.2f}",
             f"{e['fl_sum'] + e['gk_fert']:,.2f}", f"{e['hkde']:,.2f}", f"{max(u['bestand'], 0):,.2f}", f"{max(-u['bestand'], 0):,.2f}",
             f"{e['hkdu']:,.2f}"]
    werte = [w.replace(",", "X").replace(".", ",").replace("X", ".") for w in werte]
    z = ["Fertigungsmaterial (FM)", "+ Materialgemeinkosten (MGK)", "= Materialkosten (MK)", "Fertigungslöhne (FL), alle Fertigungsstellen",
         "+ Fertigungsgemeinkosten (FGK), alle Fertigungsstellen", "= Fertigungskosten (FK)", "= Herstellkosten der Erzeugung (HKdE)",
         "+ Bestandsminderungen", "− Bestandsmehrungen", "= Herstellkosten des Umsatzes (HKdU)"]
    rows = [(t, werte[i] if voll else "") for i, t in enumerate(z)]
    fett = tuple(i for i, t in enumerate(z) if t.startswith("="))
    tabelle(d, ["Nebenrechnung: Herstellkosten des Umsatzes (HKdU)", "Betrag in €"], rows, [12, 5], rechts=(1,), fett_zeilen=fett,
            leer_hoehe=None if voll else 0.7)


def saetze_kasten(d, u):
    sp = u["sp"]
    zeilen = [("MGK-Zuschlagssatz", "Gemeinkosten Material × 100 ÷ Fertigungsmaterial", "%")]
    mas = u["maschine"]
    for k in u["fl"]:
        if mas and k == mas[1]:
            zeilen.append(("Restgemeinkosten-Satz", f"Gemeinkosten {k} × 100 ÷ Fertigungslöhne {k}", "%"))
        else:
            zeilen.append((f"FGK-Zuschlagssatz ({k})", f"Gemeinkosten {k} × 100 ÷ Fertigungslöhne {k}", "%"))
    if mas:
        zeilen.insert(2, ("Maschinenstundensatz", f"Gemeinkosten {mas[0]} ÷ Maschinenstunden", "€ je h"))
    zeilen += [("VwGK-Zuschlagssatz", "Gemeinkosten Verwaltung × 100 ÷ HKdU", "%"), ("VtGK-Zuschlagssatz", "Gemeinkosten Vertrieb × 100 ÷ HKdU", "%")]
    rechenkasten(d, zeilen, breiten=(5.0, 7.0, 8.0, 3.4), hoehe=1.3)


# ---------------------------------------------------------------- Dokumente
SITUATION = {
    "u1": "Frau Petersen: „Für die **Produktion Leder** soll die monatliche Betriebsabrechnung für den **September** durchgeführt werden. Die Gemeinkosten stammen schon aus dem Kostenartenplan. Die Lagerbestände sind gegenüber dem Vormonat unverändert.“",
    "u2": "Frau Petersen: „Auch für die **Produktion Textil** brauche ich den BAB für den **September**. Die Gemeinkosten stammen aus dem Kostenartenplan. Die Lagerbestände sind unverändert. Hier gibt es eine Hilfskostenstelle, die **Werkstatt**.“",
    "u3": "Frau Petersen: „Für die **Produktion Kunststoffe** brauche ich den BAB für den **Oktober**. Die Gemeinkosten stammen aus dem Kostenartenplan. Die Lagerbestände an fertigen und unfertigen Erzeugnissen haben sich gegenüber dem Vormonat um **15.000 € verringert**.“",
    "u4": "Frau Petersen: „Für die **Produktion Leder** mit dem **Zuschnittautomaten** brauche ich den BAB für den **November**. Die Gemeinkosten stammen aus dem Kostenartenplan. Die Lagerbestände an fertigen Erzeugnissen haben sich gegenüber dem Vormonat um **24.000 € erhöht**. Der Zuschnittautomat lief **400 Stunden**.“",
}


def angaben(u):
    z = [f"Fertigungsmaterial: {f0(u['fm'])} €"]
    for k, v in u["fl"].items():
        z.append(f"Fertigungslöhne {k}: {f0(v)} €")
    if u["maschine"]:
        z.append(f"Maschinenlaufzeit {u['maschine'][0]}: {u['maschine'][2]} Stunden")
    if u["bestand"] > 0:
        z.append(f"Bestandsminderung: {f0(u['bestand'])} €")
    elif u["bestand"] < 0:
        z.append(f"Bestandsmehrung: {f0(-u['bestand'])} €")
    else:
        z.append("Bestandsveränderungen: keine")
    return z


def ab(u, e, pfad):
    d = quer(f"Arbeitsblatt {u['titel']}")
    d.add_paragraph(SITUATION[u["id"]].replace("**", "").replace("„", "„"))
    d.add_paragraph("Folgende Einzelkosten und Angaben sind angefallen: " + "; ".join(angaben(u)) + ".")
    d.add_paragraph("a) Verteile die Gemeinkosten auf die Kostenstellen.   b) Verrechne die innerbetrieblichen Leistungen.   "
                    "c) Ermittle die Kalkulationssätze.")
    ueberschrift(d, "Verteilung der Gemeinkosten (Beträge in €, bei „Schlüssel“ und „m²“ Schlüsselzahlen)")
    verteilung_tab(d, u, e)
    d.add_page_break()
    ueberschrift(d, "Schlüssel zur Verrechnung innerbetrieblicher Leistungen")
    umlage_schl_tab(d, u)
    bab_form(d, u, e)
    d.add_page_break()
    neben(d, u, e)
    ueberschrift(d, "Kalkulationssätze")
    saetze_kasten(d, u)
    d.save(pfad)


def md_tab(kopf_, rows):
    return "\n".join(["| " + " | ".join(kopf_) + " |", "| " + " | ".join(["---"] * len(kopf_)) + " |"] + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows])


def md_loesung(u, e):
    sp = u["sp"]
    kopf_ = ["Gemeinkostenart", "Summe"] + [k.replace(" ", " ") for k in sp]
    rows = [[z[0], f0(z[4])] + [f0(x) for x in z[3]] for z in e["zeilen"]]
    rows.append(["**Summe**", f"**{f0(e['gesamt'])}**"] + [f"**{f0(e['prim'][k])}**" for k in sp])
    out = ["**Schritt 1: Verteilung**", "", md_tab(kopf_, rows), ""]
    out.append("**Schritt 2: Umlage**")
    out.append("")
    for s in e["schritte"]:
        teile = sum(s["teile"].values())
        verteilt = ", ".join(f"{k} {f0(a)} €" for k, a in s["anteil"].items())
        out.append(f"- {s['von']} {f0(s['betrag'])} € ÷ {teile} Teile = **{f0(s['je'])} € je Teil** → {verteilt}")
    out.append("")
    hs = [k for k in sp if e["end"][k]]
    out.append(md_tab(["Endsummen"] + hs, [["Gemeinkosten nach Umlage"] + [f0(e["end"][k]) for k in hs]]))
    out += ["", "**Schritt 3: Kalkulationssätze**", ""]
    st = e["saetze"]
    zeilen = []
    mas = u["maschine"]
    zeilen.append(["MGK-Zuschlagssatz", f"{f0(e['end']['Material'])} × 100 ÷ {f0(u['fm'])}", pct(st["MGK"])])
    for k, fl in u["fl"].items():
        if mas and k == mas[1]:
            zeilen.append(["Restgemeinkosten-Satz", f"{f0(e['end'][k])} × 100 ÷ {f0(fl)}", pct(st["Rest"])])
        else:
            zeilen.append([f"FGK-Zuschlagssatz ({k})", f"{f0(e['end'][k])} × 100 ÷ {f0(fl)}", pct(st.get('FGK ' + k, st.get('FGK', 0)))])
    if mas:
        zeilen.insert(2, ["Maschinenstundensatz", f"{f0(e['end'][mas[0]])} ÷ {mas[2]} h", eur(st["Maschinenstundensatz"])])
    zeilen.append(["VwGK-Zuschlagssatz", f"{f0(e['end']['Verwaltung'])} × 100 ÷ {f0(e['hkdu'])}", pct(st["VwGK"])])
    zeilen.append(["VtGK-Zuschlagssatz", f"{f0(e['end']['Vertrieb'])} × 100 ÷ {f0(e['hkdu'])}", pct(st["VtGK"])])
    out += [md_tab(["Satz", "Rechnung", "Ergebnis"], zeilen), ""]
    nb = [["Fertigungsmaterial", f0(u["fm"])], ["+ Materialgemeinkosten", f0(e["end"]["Material"])], ["= Materialkosten", f0(u["fm"] + e["end"]["Material"])],
          ["Fertigungslöhne (alle Fertigungsstellen)", f0(e["fl_sum"])], ["+ Fertigungsgemeinkosten (alle Fertigungsstellen)", f0(e["gk_fert"])],
          ["= Fertigungskosten", f0(e["fl_sum"] + e["gk_fert"])], ["= Herstellkosten der Erzeugung", f0(e["hkde"])],
          ["+ Bestandsminderungen", f0(max(u["bestand"], 0))], ["− Bestandsmehrungen", f0(max(-u["bestand"], 0))],
          ["**= Herstellkosten des Umsatzes**", f"**{f0(e['hkdu'])}**"]]
    out += ["**Nebenrechnung: Herstellkosten des Umsatzes**", "", md_tab(["Zeile", "Betrag in €"], nb)]
    return "\n".join(out)


def md_verteilung(u, e):
    sp = u["sp"]
    kopf_ = ["Gemeinkostenart", "Verteilungsgrundlage"] + [k.replace(" ", " ") for k in sp]
    rows = []
    for art, grundlage, werte, betraege, gesamt in e["zeilen"]:
        schluessel = grundlage.startswith("Schlüssel") or grundlage == "m²"
        rows.append([art, grundlage] + [str(v) if schluessel else f0(v) for v in werte])
    return md_tab(kopf_, rows)


def md_umlage(u):
    sp = u["sp"]
    kopf_ = ["Vorkostenstelle", "Umlagegrundlage"] + [k.replace(" ", " ") for k in sp]
    rows = []
    for von, grundlage, teile in u["umlage"]:
        rows.append([von, grundlage] + [str(teile[k]) if k in teile else "–" for k in sp])
    return md_tab(kopf_, rows)


MINUTEN = {"u1": 40, "u2": 40, "u3": 45, "u4": 45}
LERNZIELE = {
    "u1": ["einen BAB mit einer allgemeinen Kostenstelle selbstständig erstellen,", "Zuschlagssätze für Material, Fertigung, Verwaltung und Vertrieb berechnen."],
    "u2": ["eine Hilfskostenstelle im Treppenstufenverfahren umlegen,", "Fertigungsgemeinkosten für zwei Fertigungsstellen getrennt berechnen."],
    "u3": ["einen BAB mit zwei Vorkostenstellen erstellen,", "die Herstellkosten des Umsatzes bei einer Bestandsminderung berechnen."],
    "u4": ["Maschinenstundensatz und Restgemeinkosten-Satz im BAB ermitteln,", "die Herstellkosten des Umsatzes bei einer Bestandsmehrung berechnen."],
}
INFO_HILFE = ("Wenn du nicht weiterkommst: Info 4 (Verteilen), Info 5 (Umlage) und Info 6 (Kalkulationssätze) unter „Extras“ oder als PDF: "
              "[Info 4](material/Info-4-verteilung.pdf) · [Info 5](material/Info-5-umlage.pdf) · [Info 6](material/Info-6-kalkulationssaetze.pdf)")


def modul(u, e, nr):
    schritte = e["schritte"]
    aufg = ("a) **Verteile** die Gemeinkosten auf die Kostenstellen.\nb) **Verrechne** die innerbetrieblichen Leistungen "
            f"({' und '.join(s['von'] for s in schritte)}).\nc) **Ermittle** die Kalkulationssätze und die Herstellkosten des Umsatzes.")
    md = f"""---
titel: "{u['titel']}"
minuten: {MINUTEN[u['id']]}
review: entwurf
lernziele:
  - {LERNZIELE[u['id']][0]}
  - {LERNZIELE[u['id']][1]}
quellen: [q-lehrwerk]
---
:::notiz Freiwillige Übung
Dieses Modul gehört zum Übungsbereich. Du brauchst es nicht für die Meilensteine. Wer sicherer werden möchte, übt hier an neuen Zahlen.
:::

## Die Situation

{SITUATION[u['id']]}

## Dein Arbeitsauftrag

{aufg}

**Angaben:**

""" + "\n".join(f"- {a}" for a in angaben(u)) + f"""

**Verteilung der Gemeinkosten im Monat {u['monat']}.** Bei Belegen, Gehaltsliste und Anlagendatei stehen **Beträge in €**, bei „Schlüssel“ und „m²“ **Schlüsselzahlen**:

{md_verteilung(u, e)}

**Schlüssel zur Verrechnung innerbetrieblicher Leistungen** (Teile je Kostenstelle):

{md_umlage(u)}

:::material material/AB-{u['id']}-{u['datei']}.pdf Arbeitsblatt {u['titel']} (Querformat, PDF)
Mit BAB-Formular, Nebenrechnung und Rechenkästen. Als Word: [AB-{u['id']}-{u['datei']}.docx](material/AB-{u['id']}-{u['datei']}.docx)
:::

:::aufgabe basis {MINUTEN[u['id']] - 5} 1 · BAB erstellen
Erstelle den BAB im Formular, berechne die Kalkulationssätze und die Nebenrechnung.

:::loesung Hilfe: Info-Seiten
{INFO_HILFE}
:::

:::loesung Lösung
{md_loesung(u, e)}
:::
:::
"""
    return md


# ---------------------------------------------------------------- Übung 5: Maschinenstundensatz herleiten
def ab_u5(pfad):
    d = quer("Arbeitsblatt Übung 5: Maschinenstundensatz herleiten", "Montelli GmbH · Übungsbereich · Exkurs Vollkostenrechnung")
    d.add_paragraph("Die Montelli GmbH arbeitet mit drei Automaten, die jeweils als eigene Kostenstelle geführt werden. "
                    "Berechne die jährlichen Maschinengemeinkosten und die Maschinenstundensätze für die Angebotskalkulation.")
    ueberschrift(d, "Herstellerangaben")
    kopf_ = [""] + [m["name"] for m in MASCHINEN]
    zeilen = [("Anschaffungskosten in €",) + tuple(f0(m["ak"]) for m in MASCHINEN),
              ("Wiederbeschaffungskosten in €",) + tuple(f0(m["wbw"]) for m in MASCHINEN),
              ("Nutzungsdauer in Jahren",) + tuple(str(m["nd"]) for m in MASCHINEN),
              ("Platzbedarf in m²",) + tuple(str(m["m2"]) for m in MASCHINEN),
              ("Maximale Laufzeit in Stunden/Jahr",) + tuple(f0(m["max_h"]) for m in MASCHINEN),
              ("Stillstandszeiten/Umrüstung in Stunden/Jahr",) + tuple(str(m["still"]) for m in MASCHINEN),
              ("Instandhaltung in Stunden/Jahr",) + tuple(str(m["inst_h"]) for m in MASCHINEN),
              ("Elektrischer Anschlusswert in kW",) + tuple(str(m["kw"]) for m in MASCHINEN)]
    tabelle(d, kopf_, zeilen, [9, 5, 5, 5], rechts=(1, 2, 3))
    d.add_paragraph(f"Informationen aus dem Controlling: Strom {str(STROM).replace('.', ',')} € je kWh · Platzkosten {PLATZ} € je m² und Monat · "
                    f"kalkulatorischer Zinssatz {ZINS} % vom durchschnittlich gebundenen Kapital (halbe Anschaffungskosten) · "
                    f"Instandhaltungskosten {INST_PROZ} % der Wiederbeschaffungskosten je Jahr.")
    ueberschrift(d, "Berechnung der Maschinengemeinkosten (je Jahr)")
    rows = [("Kalkulatorische Abschreibung/Jahr", "Wiederbeschaffungskosten ÷ Nutzungsdauer"),
            ("Kalkulatorische Zinsen/Jahr", "Anschaffungskosten ÷ 2 × Zinssatz"),
            ("Instandhaltungskosten/Jahr", "Wiederbeschaffungskosten × 5 %"),
            ("Raumkosten/Jahr", "m² × Platzkosten × 12 Monate"),
            ("Produktive Laufzeit in Stunden/Jahr", "Max. Laufzeit − Stillstand − Instandhaltung"),
            ("Energiekosten/Jahr", "kW × produktive Laufzeit × Strompreis"),
            ("Summe Maschinengemeinkosten/Jahr", "Summe der fünf Kostenarten"),
            ("Maschinenstundensatz", "Summe ÷ produktive Laufzeit")]
    tabelle(d, ["Berechnung", "Formel"] + [m["name"] for m in MASCHINEN], [(a, b, "", "", "") for a, b in rows], [5.6, 7.2, 4.8, 4.8, 4.8],
            leer_hoehe=1.0, fett_zeilen=(6, 7))
    d.save(pfad)


def loes_u5_md():
    rs = [maschine_loese(m) for m in MASCHINEN]
    rows = [["Kalk. Abschreibung/Jahr"] + [f0(r["afa"]) for r in rs], ["Kalk. Zinsen/Jahr"] + [f0(r["zins"]) for r in rs],
            ["Instandhaltungskosten/Jahr"] + [f0(r["inst"]) for r in rs], ["Raumkosten/Jahr"] + [f0(r["raum"]) for r in rs],
            ["Produktive Laufzeit (h/Jahr)"] + [f0(r["lauf"]) for r in rs], ["Energiekosten/Jahr"] + [f0(r["energie"]) for r in rs],
            ["**Summe Maschinengemeinkosten/Jahr**"] + [f"**{f0(r['summe'])}**" for r in rs],
            ["**Maschinenstundensatz**"] + [f"**{eur(r['satz'])} je h**" for r in rs]]
    return md_tab([""] + [m["name"] for m in MASCHINEN], rows), rs


def modul_u5():
    tab, rs = loes_u5_md()
    herst = md_tab([""] + [m["name"] for m in MASCHINEN], [
        ["Anschaffungskosten in €"] + [f0(m["ak"]) for m in MASCHINEN], ["Wiederbeschaffungskosten in €"] + [f0(m["wbw"]) for m in MASCHINEN],
        ["Nutzungsdauer in Jahren"] + [str(m["nd"]) for m in MASCHINEN], ["Platzbedarf in m²"] + [str(m["m2"]) for m in MASCHINEN],
        ["Maximale Laufzeit (h/Jahr)"] + [f0(m["max_h"]) for m in MASCHINEN], ["Stillstand/Umrüstung (h/Jahr)"] + [str(m["still"]) for m in MASCHINEN],
        ["Instandhaltung (h/Jahr)"] + [str(m["inst_h"]) for m in MASCHINEN], ["Anschlusswert in kW"] + [str(m["kw"]) for m in MASCHINEN]])
    auftrag = 3 * rs[0]["satz"] + 2 * rs[1]["satz"]
    a3 = round(rs[0]["satz"], 2) * 3 + round(rs[1]["satz"], 2) * 2
    return f"""---
titel: "Übung 5: Maschinenstundensatz herleiten"
minuten: 40
review: entwurf
lernziele:
  - die Maschinengemeinkosten einer Maschine nach Kostenarten berechnen,
  - die produktive Laufzeit bestimmen,
  - den Maschinenstundensatz herleiten und anwenden.
quellen: [q-lehrwerk, q-maschinen]
---
:::notiz Freiwillige Übung
Dieses Modul gehört zum Übungsbereich. Du lernst, wie ein Maschinenstundensatz entsteht, der im BAB sonst fertig vorgegeben ist.
:::

## Die Situation

Frau Petersen: „Bei Montelli laufen drei Automaten, die jeweils als eigene Kostenstelle geführt werden. Im BAB brauche ich für jede Maschine einen **Maschinenstundensatz**. Die Herstellerangaben und die Infos des Controllings habe ich hier. Rechne die Sätze aus.“

## Dein Arbeitsauftrag

Berechne für die drei Automaten die jährlichen Maschinengemeinkosten und die zugehörigen Maschinenstundensätze für die Angebotskalkulation.

**Herstellerangaben:**

{herst}

**Informationen aus dem Controlling:** Strom {str(STROM).replace('.', ',')} € je kWh · Platzkosten {PLATZ} € je m² und Monat · kalkulatorischer Zinssatz {ZINS} % vom durchschnittlich gebundenen Kapital (halbe Anschaffungskosten) · Instandhaltungskosten {INST_PROZ} % der Wiederbeschaffungskosten je Jahr.

:::material material/AB-u5-maschinenstundensatz.pdf Arbeitsblatt Übung 5: Maschinenstundensatz herleiten (PDF)
Mit Formeln und Feldern für die Rechnung. Als Word: [AB-u5-maschinenstundensatz.docx](material/AB-u5-maschinenstundensatz.docx) · Info 9: [PDF](material/Info-9-maschinenstundensatz.pdf)
:::

:::aufgabe basis 30 1 · Maschinenstundensätze berechnen
Fülle die Tabelle auf dem Arbeitsblatt aus: fünf Kostenarten je Jahr, Summe, produktive Laufzeit und Maschinenstundensatz.

:::loesung Hilfe: So rechnest du
- **Kalkulatorische Abschreibung** = Wiederbeschaffungskosten ÷ Nutzungsdauer
- **Kalkulatorische Zinsen** = durchschnittlich gebundenes Kapital (Anschaffungskosten ÷ 2) × Zinssatz
- **Instandhaltungskosten** = Wiederbeschaffungskosten × Satz
- **Raumkosten** = m² × Platzkosten × 12 Monate
- **Produktive Laufzeit** = maximale Laufzeit − Stillstand − Instandhaltung
- **Energiekosten** = Anschlusswert × produktive Laufzeit × Strompreis (vereinfacht: volle Last)
- **Maschinenstundensatz** = Summe der Maschinengemeinkosten ÷ produktive Laufzeit

Mehr dazu: Info 9 unter „Extras“ oder als PDF: [Info 9 (PDF)](material/Info-9-maschinenstundensatz.pdf)
:::

:::loesung Lösung
{tab}
:::
:::

:::aufgabe plus 10 2 · Ein Auftrag
Ein Auftrag braucht **3 Stunden am Zuschnittautomaten** und **2 Stunden am Nähautomaten**. Wie hoch sind die Maschinenkosten des Auftrags?

:::loesung Lösung
3 h × {eur(rs[0]['satz'])} + 2 h × {eur(rs[1]['satz'])} = **{eur(a3)}**
:::
:::
"""


# ---------------------------------------------------------------- Übung 6: Richtig oder falsch
def ab_u6(pfad):
    d = hoch("Arbeitsblatt Übung 6: Richtig oder falsch?", "Montelli GmbH · Übungsbereich · Exkurs Vollkostenrechnung")
    d.add_paragraph("Kreuze an, ob die Aussagen richtig oder falsch sind. Korrigiere falsche Aussagen in einem Satz.")
    tabelle(d, ["Nr.", "Aussage", "richtig", "falsch", "Korrektur, wenn falsch"], [(str(i + 1), a, "", "", "") for i, (a, _, _) in enumerate(RICHTIG_FALSCH)],
            [0.9, 7.0, 1.4, 1.4, 6.7], leer_hoehe=1.6)
    d.save(pfad)


def modul_u6():
    liste = "\n".join(f"{i + 1}. {a}" for i, (a, _, _) in enumerate(RICHTIG_FALSCH))
    loes = md_tab(["Nr.", "Antwort", "Begründung"], [[str(i + 1), "richtig" if r else "falsch", b] for i, (a, r, b) in enumerate(RICHTIG_FALSCH)])
    return f"""---
titel: "Übung 6: Richtig oder falsch?"
minuten: 15
review: entwurf
lernziele:
  - Aussagen zum BAB und zu den Kalkulationssätzen prüfen,
  - falsche Aussagen richtigstellen.
quellen: [q-lehrwerk]
---
:::notiz Freiwillige Übung
Dieses Modul gehört zum Übungsbereich. Danach kannst du in Moodle den kurzen **Test zum BAB** machen.
:::

## Die Situation

Herr Jessen fasst den Exkurs mit ein paar Aussagen zusammen. Frau Petersen bittet dich zu prüfen, welche stimmen.

## Dein Arbeitsauftrag

Prüfe die Aussagen. Kreuze an, ob sie **richtig** oder **falsch** sind, und stelle falsche Aussagen in einem Satz richtig.

{liste}

:::material material/AB-u6-richtig-falsch.pdf Arbeitsblatt Übung 6: Richtig oder falsch? (PDF)
Zum Ausdrucken. Als Word: [AB-u6-richtig-falsch.docx](material/AB-u6-richtig-falsch.docx)
:::

:::aufgabe basis 10 1 · Aussagen prüfen
Bearbeite die acht Aussagen auf dem Arbeitsblatt.

:::loesung Lösung
{loes}
:::
:::
"""


INFO9 = """---
titel: "Info 9: Maschinenstundensatz herleiten"
icon: "⚙️"
beschreibung: Maschinengemeinkosten nach Kostenarten und Maschinenstundensatz.
reihenfolge: 9
---
## Wie entsteht ein Maschinenstundensatz?

Der **Maschinenstundensatz** zeigt, wie viele Gemeinkosten eine Maschine **pro Stunde Laufzeit** verursacht. Man teilt die jährlichen Maschinengemeinkosten durch die **produktive Laufzeit**:

**Maschinenstundensatz = Maschinengemeinkosten je Jahr ÷ produktive Laufzeit in Stunden**

## Die Kostenarten der Maschine (je Jahr)

| Kostenart | Berechnung |
| --- | --- |
| Kalkulatorische Abschreibung | Wiederbeschaffungskosten ÷ Nutzungsdauer |
| Kalkulatorische Zinsen | durchschnittlich gebundenes Kapital (Anschaffungskosten ÷ 2) × Zinssatz |
| Instandhaltungskosten | Wiederbeschaffungskosten × Instandhaltungssatz |
| Raumkosten | Platzbedarf in m² × Platzkosten je m² und Monat × 12 |
| Energiekosten | Anschlusswert in kW × produktive Laufzeit × Strompreis je kWh |

## Die produktive Laufzeit

**Produktive Laufzeit = maximale Laufzeit − Stillstands- und Umrüstzeiten − Instandhaltungsstunden**

## Beispiel mit anderen Zahlen

Eine Maschine hat Wiederbeschaffungskosten von 100.000 € und eine Nutzungsdauer von 10 Jahren. Anschaffungskosten 90.000 €, Zinssatz 6 %. Die produktive Laufzeit beträgt 1.500 Stunden. Die übrigen Maschinengemeinkosten betragen zusammen 8.000 € je Jahr.

- Kalkulatorische Abschreibung: 100.000 € ÷ 10 = **10.000 €**
- Kalkulatorische Zinsen: 90.000 € ÷ 2 × 6 % = **2.700 €**
- Summe: 10.000 € + 2.700 € + 8.000 € = **20.700 €**
- Maschinenstundensatz: 20.700 € ÷ 1.500 h = **13,80 € je Stunde**

:::notiz Vereinfachung
Im Lernpfad rechnen wir die Energiekosten vereinfacht mit dem vollen Anschlusswert über die gesamte produktive Laufzeit. In der Praxis arbeitet man mit durchschnittlichen Verbrauchswerten.
:::

:::material material/Info-9-maschinenstundensatz.pdf Diese Info als PDF herunterladen
Zum Ausdrucken und Abheften.
:::
"""


def fragen_yaml():
    out = ["# Test zum BAB (Übungsbereich): richtig oder falsch, automatisch bewertet"]
    for i, (a, r, b) in enumerate(RICHTIG_FALSCH, start=1):
        a_ = a.replace('"', "'")
        b_ = b.replace("**", "").replace('"', "'")
        out += [f"- id: ub-{i:02d}", "  typ: single_choice", "  niveau: 1", "  review: entwurf",
                f'  aufgabe: "Richtig oder falsch? {a_}"', "  optionen:",
                f'    - {{text: "richtig", korrekt: {"true" if r else "false"}}}',
                f'    - {{text: "falsch", korrekt: {"true" if not r else "false"}}}',
                f'  erklaerung: "{b_}"', ""]
    return "\n".join(out)


def loesungen_docx(pfad):
    d = quer("Lehrkraft: Lösungen Übungsbereich", "Nicht an Schüler:innen weitergeben.")
    for k, u in UE.items():
        e = loese(u)
        ueberschrift(d, u["titel"])
        bab_form(d, u, e, voll=True)
        neben(d, u, e, voll=True)
    ueberschrift(d, "Übung 5: Maschinenstundensätze")
    rs = [maschine_loese(m) for m in MASCHINEN]
    rows = [("Kalk. Abschreibung/Jahr",) + tuple(f0(r["afa"]) for r in rs), ("Kalk. Zinsen/Jahr",) + tuple(f0(r["zins"]) for r in rs),
            ("Instandhaltungskosten/Jahr",) + tuple(f0(r["inst"]) for r in rs), ("Raumkosten/Jahr",) + tuple(f0(r["raum"]) for r in rs),
            ("Produktive Laufzeit (h/Jahr)",) + tuple(f0(r["lauf"]) for r in rs), ("Energiekosten/Jahr",) + tuple(f0(r["energie"]) for r in rs),
            ("Summe/Jahr",) + tuple(f0(r["summe"]) for r in rs), ("Maschinenstundensatz",) + tuple(eur(r["satz"]) for r in rs)]
    tabelle(d, [""] + [m["name"] for m in MASCHINEN], rows, [8, 5, 5, 5], rechts=(1, 2, 3), fett_zeilen=(6, 7))
    ueberschrift(d, "Übung 6: Richtig oder falsch")
    tabelle(d, ["Nr.", "Antwort", "Begründung"], [(str(i + 1), "richtig" if r else "falsch", b.replace("**", "")) for i, (a, r, b) in enumerate(RICHTIG_FALSCH)],
            [1, 3, 22])
    d.save(pfad)


DATEI = {"u1": "leder", "u2": "textil", "u3": "kunststoffe", "u4": "zuschnittautomat"}


def main():
    m = ROOT / "material"
    for k, u in UE.items():
        u["id"], u["datei"] = k, DATEI[k]
        e = loese(u)
        ab(u, e, m / f"AB-{k}-{DATEI[k]}.docx")
        (ROOT / "module" / f"{k}.md").write_text(modul(u, e, k), encoding="utf-8")
    ab_u5(m / "AB-u5-maschinenstundensatz.docx")
    (ROOT / "module" / "u5.md").write_text(modul_u5(), encoding="utf-8")
    ab_u6(m / "AB-u6-richtig-falsch.docx")
    (ROOT / "module" / "u6.md").write_text(modul_u6(), encoding="utf-8")
    (ROOT / "seiten" / "info-9-maschinenstundensatz.md").write_text(INFO9, encoding="utf-8")
    (ROOT / "fragen" / "ubung-bab.yaml").write_text(fragen_yaml(), encoding="utf-8")
    loesungen_docx(ROOT / "lehrkraft" / "Loesungen-Uebungen.docx")
    print("✓ Übungsbereich erzeugt")


if __name__ == "__main__":
    main()
