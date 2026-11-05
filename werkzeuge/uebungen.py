"""Zahlengrundlage des Übungsbereichs (Stufe 4): vier Übungs-BABs der Montelli-Produktionen und die Herleitung des Maschinenstundensatzes.
Alle Zahlen sind für den Lernpfad frei konstruiert. Aufruf:  python3 werkzeuge/uebungen.py  -> prüft Summen und Schlüssel und gibt die Ergebnisse aus.
"""
from daten import fmt

# Art der Kostenstelle je Spalte (Beschriftung im BAB-Kopf)
AKS, HAUPT, HILFS, FERT = "Allgemeine Kostenstelle", "Hauptkostenstelle", "Hilfskostenstelle", "Fertigungs-Hauptkostenstelle"

# Aufbau je Übung:
#   sp: Kostenstellen (Spaltenreihenfolge), art: Art je Kostenstelle
#   zeilen: (Gemeinkostenart, Grundlage, Werte, Summe)   Summe=None -> Werte sind Beträge in €, sonst Schlüsselzahlen und Gesamtbetrag
#   umlage: Treppenstufen (von, Grundlage, {Stelle: Teile})
#   fert: Fertigungsstellen mit Löhnen (Stelle -> Fertigungslöhne); maschine: (Stelle für Maschinenkosten, Stelle für Restgemeinkosten, Stunden)
UE = {
    "u1": {
        "name": "Produktion Leder", "monat": "September", "titel": "Übungs-BAB 1: Produktion Leder",
        "sp": ["Fuhrpark", "Material", "Fertigung", "Verwaltung", "Vertrieb"],
        "art": [AKS, HAUPT, FERT, HAUPT, HAUPT],
        "zeilen": [
            ("Hilfsstoffe", "Belege", [0, 0, 36000, 0, 0], None),
            ("Betriebsstoffe", "Schlüssel (kWh)", [1, 2, 8, 2, 2], 30000),
            ("Gehälter", "Gehaltsliste", [2400, 4800, 6000, 14400, 7200], None),
            ("Kalk. Abschreibungen", "Anlagendatei", [1500, 2000, 14000, 4000, 1500], None),
            ("Kalk. Zinsen", "Schlüssel (Kapital)", [2, 2, 9, 4, 3], 16000),
            ("Miete", "m²", [20, 60, 200, 80, 40], 12000),
            ("Büromaterial", "Belege", [100, 250, 150, 800, 450], None),
        ],
        "umlage": [("Fuhrpark", "Transportaufträge", {"Material": 2, "Fertigung": 10, "Verwaltung": 5, "Vertrieb": 3})],
        "fm": 120000, "fl": {"Fertigung": 80000}, "bestand": 0, "maschine": None,
    },
    "u2": {
        "name": "Produktion Textil", "monat": "September", "titel": "Übungs-BAB 2: Produktion Textil",
        "sp": ["Fuhrpark", "Material", "Werkstatt", "Fertigung I", "Fertigung II", "Verwaltung", "Vertrieb"],
        "art": [AKS, HAUPT, HILFS, FERT, FERT, HAUPT, HAUPT],
        "zeilen": [
            ("Hilfsstoffe", "Belege", [0, 0, 0, 12000, 18000, 0, 0], None),
            ("Energie", "Schlüssel (kWh)", [1, 3, 2, 9, 8, 3, 2], 28000),
            ("Gehälter", "Gehaltsliste", [2000, 5500, 3200, 4000, 4500, 12800, 6000], None),
            ("Kalk. Abschreibungen", "Anlagendatei", [1200, 1800, 2500, 9000, 11500, 3000, 1000], None),
            ("Kalk. Zinsen", "Schlüssel (Kapital)", [1, 2, 1, 5, 6, 3, 2], 20000),
            ("Miete", "m²", [30, 90, 40, 200, 240, 100, 50], 15000),
            ("Büromaterial", "Belege", [200, 300, 100, 200, 200, 900, 450], None),
        ],
        "umlage": [("Fuhrpark", "Transportaufträge", {"Material": 2, "Werkstatt": 1, "Fertigung I": 6, "Fertigung II": 5, "Verwaltung": 4, "Vertrieb": 2}),
                   ("Werkstatt", "Wartungsstunden", {"Fertigung I": 6, "Fertigung II": 5})],
        "fm": 100000, "fl": {"Fertigung I": 42000, "Fertigung II": 56000}, "bestand": 0, "maschine": None,
    },
    "u3": {
        "name": "Produktion Kunststoffe", "monat": "Oktober", "titel": "Übungs-BAB 3: Produktion Kunststoffe",
        "sp": ["Fuhrpark", "Material", "Arbeitsvorbereitung", "Fertigung I", "Fertigung II", "Verwaltung", "Vertrieb"],
        "art": [AKS, HAUPT, HILFS, FERT, FERT, HAUPT, HAUPT],
        "zeilen": [
            ("Hilfsstoffe", "Belege", [0, 0, 0, 24000, 16000, 0, 0], None),
            ("Energie", "Schlüssel (kWh)", [2, 3, 1, 12, 9, 1, 2], 30000),
            ("Gehälter", "Gehaltsliste", [3000, 6000, 2500, 10000, 8000, 15000, 8500], None),
            ("Sozialkosten", "Gehaltsliste", [600, 1200, 500, 2000, 1600, 3000, 1700], None),
            ("Kalk. Abschreibungen", "Anlagendatei", [2000, 2500, 3000, 12000, 16000, 3500, 1000], None),
            ("Kalk. Zinsen", "Schlüssel (Kapital)", [2, 3, 1, 8, 10, 4, 2], 18000),
            ("Miete", "m²", [50, 100, 40, 260, 300, 150, 100], 20000),
            ("Sonstige Kosten", "Schlüssel", [1, 2, 1, 4, 3, 2, 2], 9000),
        ],
        "umlage": [("Fuhrpark", "Transportaufträge", {"Material": 4, "Arbeitsvorbereitung": 2, "Fertigung I": 12, "Fertigung II": 10, "Verwaltung": 8, "Vertrieb": 4}),
                   ("Arbeitsvorbereitung", "Planungsstunden", {"Fertigung I": 3, "Fertigung II": 4})],
        "fm": 130000, "fl": {"Fertigung I": 70000, "Fertigung II": 60000}, "bestand": 15000, "maschine": None,
    },
    "u4": {
        "name": "Produktion Leder (Zuschnittautomat)", "monat": "November", "titel": "Übungs-BAB 4: Zuschnittautomat und Bestandsmehrung",
        "sp": ["Fuhrpark", "Material", "Fertigung", "Zuschnittautomat", "Rest Automat", "Verwaltung", "Vertrieb"],
        "art": [AKS, HAUPT, FERT, FERT, FERT, HAUPT, HAUPT],
        "zeilen": [
            ("Hilfsstoffe", "Belege", [0, 0, 9000, 2000, 1000, 0, 0], None),
            ("Betriebsstoffe", "Schlüssel (kWh)", [1, 2, 4, 10, 1, 1, 1], 10000),
            ("Gehälter", "Gehaltsliste", [2000, 4000, 3000, 1500, 2500, 9000, 5000], None),
            ("Sozialkosten", "Gehaltsliste", [500, 1000, 750, 375, 625, 2250, 1250], None),
            ("Kalk. Abschreibungen", "Anlagendatei", [1000, 1500, 4000, 18000, 500, 2000, 1000], None),
            ("Kalk. Zinsen", "Schlüssel (Kapital)", [1, 1, 3, 12, 1, 1, 1], 12000),
            ("Miete", "m²", [30, 70, 200, 80, 20, 60, 40], 10000),
            ("Fremdinstandhaltung", "Belege", [400, 300, 1000, 3000, 0, 0, 0], None),
        ],
        "umlage": [("Fuhrpark", "Transportaufträge", {"Material": 3, "Fertigung": 5, "Zuschnittautomat": 4, "Rest Automat": 2, "Verwaltung": 2, "Vertrieb": 4})],
        "fm": 180000, "fl": {"Fertigung": 110000, "Rest Automat": 40000}, "bestand": -24000,
        "maschine": ("Zuschnittautomat", "Rest Automat", 400),
    },
}


def loese(u):
    sp, n = u["sp"], len(u["sp"])
    zeilen = []
    for art, grundlage, werte, summe in u["zeilen"]:
        if summe is None:
            betraege = list(werte)
            gesamt = sum(betraege)
        else:
            teile = sum(werte)
            assert summe % teile == 0, (u["titel"], art, summe, teile)
            je = summe // teile
            betraege = [w * je for w in werte]
            gesamt = summe
        assert sum(betraege) == gesamt, (u["titel"], art)
        zeilen.append((art, grundlage, werte, betraege, gesamt))
    prim = {k: sum(z[3][i] for z in zeilen) for i, k in enumerate(sp)}
    gesamt = sum(z[4] for z in zeilen)
    assert sum(prim.values()) == gesamt
    stand = dict(prim)
    schritte = []
    for von, grundlage, teile in u["umlage"]:
        t = sum(teile.values())
        assert stand[von] % t == 0, (u["titel"], von, stand[von], t)
        je = stand[von] // t
        anteil = {k: v * je for k, v in teile.items()}
        neu = dict(stand)
        neu[von] = 0
        for k, a in anteil.items():
            neu[k] += a
        schritte.append({"von": von, "grundlage": grundlage, "teile": teile, "je": je, "betrag": stand[von], "anteil": anteil, "danach": neu})
        stand = neu
    fl = u["fl"]
    fm = u["fm"]
    haupt = [k for k, a in zip(sp, u["art"]) if a in (HAUPT, FERT)]
    assert sum(stand[k] for k in haupt) == gesamt and all(stand[k] == 0 for k in sp if k not in haupt)
    fert = [k for k, a in zip(sp, u["art"]) if a == FERT]
    ergebnis = {"prim": prim, "gesamt": gesamt, "schritte": schritte, "end": stand, "zeilen": zeilen, "sp": sp}
    saetze = {"MGK": stand["Material"] / fm * 100}
    gk_fert = sum(stand[k] for k in fert)
    fl_sum = sum(fl.values())
    if u["maschine"]:
        mkst, rkst, std = u["maschine"]
        saetze["FGK"] = stand["Fertigung"] / fl["Fertigung"] * 100
        saetze["Maschinenstundensatz"] = stand[mkst] / std
        saetze["Rest"] = stand[rkst] / fl[rkst] * 100
    else:
        for k in fert:
            saetze["FGK " + k] = stand[k] / fl[k] * 100
    hkde = fm + stand["Material"] + fl_sum + gk_fert
    hkdu = hkde + u["bestand"]
    saetze["VwGK"] = stand["Verwaltung"] / hkdu * 100
    saetze["VtGK"] = stand["Vertrieb"] / hkdu * 100
    ergebnis.update({"saetze": saetze, "hkde": hkde, "hkdu": hkdu, "fl_sum": fl_sum, "gk_fert": gk_fert, "fert": fert})
    return ergebnis


# ---------------------------------------------------------------- Übung 5: Maschinenstundensatz herleiten
MASCHINEN = [
    {"name": "Zuschnittautomat", "ak": 240000, "wbw": 264000, "nd": 8, "m2": 30, "max_h": 2000, "still": 250, "inst_h": 100, "kw": 20},
    {"name": "Nähautomat", "ak": 180000, "wbw": 198000, "nd": 6, "m2": 24, "max_h": 2000, "still": 200, "inst_h": 80, "kw": 15},
    {"name": "Stanzpresse", "ak": 120000, "wbw": 132000, "nd": 10, "m2": 20, "max_h": 2000, "still": 150, "inst_h": 50, "kw": 10},
]
STROM, PLATZ, ZINS, INST_PROZ = 0.15, 20, 6, 5


def maschine_loese(m):
    r = {}
    r["afa"] = m["wbw"] / m["nd"]
    r["zins"] = m["ak"] / 2 * ZINS / 100
    r["inst"] = m["wbw"] * INST_PROZ / 100
    r["raum"] = m["m2"] * PLATZ * 12
    r["lauf"] = m["max_h"] - m["still"] - m["inst_h"]
    r["energie"] = m["kw"] * r["lauf"] * STROM
    r["summe"] = r["afa"] + r["zins"] + r["inst"] + r["raum"] + r["energie"]
    r["satz"] = r["summe"] / r["lauf"]
    return r


RICHTIG_FALSCH = [
    ("Mit dem BAB werden die Einzelkosten je Kostenstelle ermittelt.", False,
     "Der BAB verteilt die **Gemeinkosten** auf die Kostenstellen. Einzelkosten werden den Produkten direkt zugerechnet."),
    ("Gemeinkosten werden stets mit einem Verteilungsschlüssel auf die Kostenstellen verteilt.", False,
     "Lässt sich ein Betrag über einen Beleg eindeutig zuordnen, wird er **direkt** verteilt. Nur gemeinsame Kosten brauchen einen Schlüssel."),
    ("Mit dem BAB werden zunächst die Ist-Kalkulationssätze ermittelt.", True,
     "Richtig. Der BAB eines Monats liefert Istsätze. Aus mehreren Monaten bildet man daraus die Normalsätze."),
    ("Prozentuale Zuschlagssätze sind Kalkulationssätze.", True, "Richtig. Kalkulationssätze sind Zuschlagssätze und Maschinenstundensätze."),
    ("Maschinenstundensätze sind keine Kalkulationssätze.", False, "Maschinenstundensätze sind Kalkulationssätze, die in Euro je Stunde angegeben werden."),
    ("Mit dem BAB wird die Entwicklung der Gemeinkosten in den Kostenstellen kontrolliert.", True,
     "Richtig. Der BAB zeigt Höhe und Entwicklung der Gemeinkosten je Kostenstelle zu Kontrollzwecken."),
    ("Zuschlagsgrundlage für die Vertriebsgemeinkosten sind die Herstellkosten des Umsatzes.", True,
     "Richtig. Verwaltung und Vertrieb arbeiten für alle Produkte und beziehen sich auf die Herstellkosten des Umsatzes."),
    ("Die Kosten der Vorkostenstellen bleiben im BAB bei den Vorkostenstellen stehen.", False,
     "Sie werden auf die Hauptkostenstellen **umgelegt**, damit sie in die Kalkulationssätze eingehen."),
]


if __name__ == "__main__":
    for k, u in UE.items():
        e = loese(u)
        print("==", u["titel"])
        print(" primär", e["prim"], "Summe", fmt(e["gesamt"], 0))
        for s in e["schritte"]:
            print(" Umlage", s["von"], s["betrag"], "je Teil", s["je"], s["anteil"])
        print(" end", e["end"])
        print(" Sätze", {a: round(b, 2) for a, b in e["saetze"].items()}, "HKdE", e["hkde"], "HKdU", e["hkdu"])
    for m in MASCHINEN:
        r = maschine_loese(m)
        print(m["name"], {a: round(b, 2) for a, b in r.items()})
