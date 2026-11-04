"""Zahlengrundlage des Lernpfads (Montelli GmbH, Geschäftsbereich Outdoor/Rucksäcke).

Alle Werte sind für den Lernpfad frei konstruiert (keine Übernahme aus Lehrwerken) und werden hier
einmal zentral gehalten und geprüft. Aufruf:  python3 werkzeuge/daten.py   -> prüft Summen und Sätze.
"""

KST = ["Material", "Fertigung I", "Fertigung II (Maschinenplatz)", "Verwaltung", "Vertrieb"]

# --- Gemeinkostenarten je Kostenstelle (Verteilung aus dem BAB) ---------------------------------------------
# Reihenfolge der Werte: Material, Fertigung I, Fertigung II, Verwaltung, Vertrieb
JULI = {
    "name": "Juli",
    "guv": {  # Konto: (Bezeichnung, Betrag)   Zweckaufwand + neutrale Posten
        "aufwand": [
            ("6000", "Aufwendungen für Rohstoffe", 140000),
            ("6010", "Aufwendungen für Vorprodukte/Fremdbauteile", 60000),
            ("6020", "Aufwendungen für Hilfsstoffe", 8000),
            ("6030", "Aufwendungen für Betriebsstoffe", 18000),
            ("6160", "Fremdinstandhaltung", 8050),
            ("6200", "Löhne", 76500),
            ("6300", "Gehälter", 124100),
            ("6520", "Abschreibungen auf Sachanlagen", 58000),
            ("6710", "Leasingaufwendungen", 10200),
            ("6800", "Büromaterial", 3575),
            ("6990", "Periodenfremde Aufwendungen", 3450),
            ("7400", "Abschreibungen auf Finanzanlagen", 1600),
            ("7510", "Zinsaufwendungen", 22000),
        ],
        "ertrag": [
            ("5000", "Umsatzerlöse für eigene Erzeugnisse", 650000),
            ("5500", "Erträge aus Beteiligungen", 2500),
            ("5710", "Zinserträge", 1800),
        ],
    },
    "kalk": {"Abschreibungen": 65000, "Zinsen": 30000},
    "neutral": ["6990", "7400", "7510", "5500", "5710"],
    "fm": {"Rohstoffe": 140000, "Vorprodukte/Fremdbauteile": 60000},
    "fl1": 62500, "fl2": 14000, "masch_std": 1000,
    "bab": {
        "Hilfsstoffe":            [0, 7200, 800, 0, 0],
        "Betriebsstoffe":         [1200, 4800, 10000, 800, 1200],
        "Gehälter":               [28000, 20900, 2200, 46000, 27000],
        "Kalk. Abschreibungen":   [3200, 8000, 46000, 4000, 3800],
        "Kalk. Zinsen":           [3000, 4500, 18750, 2250, 1500],
        "Leasing":                [3000, 3600, 1200, 1200, 1200],
        "Fremdinstandhaltung":    [300, 1500, 6250, 0, 0],
        "Büromaterial":           [700, 125, 0, 1750, 1000],
    },
}

AUGUST = {
    "name": "August",
    "guv": {
        "aufwand": [
            ("6000", "Aufwendungen für Rohstoffe", 126000),
            ("6010", "Aufwendungen für Vorprodukte/Fremdbauteile", 54000),
            ("6020", "Aufwendungen für Hilfsstoffe", 7200),
            ("6030", "Aufwendungen für Betriebsstoffe", 16200),
            ("6160", "Fremdinstandhaltung", 5100),
            ("6200", "Löhne", 68600),
            ("6300", "Gehälter", 124100),
            ("6520", "Abschreibungen auf Sachanlagen", 57000),
            ("6710", "Leasingaufwendungen", 10200),
            ("6800", "Büromaterial", 3600),
            ("6990", "Periodenfremde Aufwendungen", 1250),
            ("7400", "Abschreibungen auf Finanzanlagen", 1600),
            ("7510", "Zinsaufwendungen", 22000),
        ],
        "ertrag": [
            ("5000", "Umsatzerlöse für eigene Erzeugnisse", 560000),
            ("5500", "Erträge aus Beteiligungen", 2500),
            ("5710", "Zinserträge", 1800),
        ],
    },
    "kalk": {"Abschreibungen": 65000, "Zinsen": 30000},
    "neutral": ["6990", "7400", "7510", "5500", "5710"],
    "fm": {"Rohstoffe": 126000, "Vorprodukte/Fremdbauteile": 54000},
    "fl1": 56000, "fl2": 12600, "masch_std": 900,
    "bab": {
        "Hilfsstoffe":            [0, 6500, 700, 0, 0],
        "Betriebsstoffe":         [1080, 4320, 9000, 720, 1080],
        "Gehälter":               [28000, 20900, 2200, 46000, 27000],
        "Kalk. Abschreibungen":   [3200, 8000, 46000, 4000, 3800],
        "Kalk. Zinsen":           [3000, 4500, 18750, 2250, 1500],
        "Leasing":                [3000, 3600, 1200, 1200, 1200],
        "Fremdinstandhaltung":    [0, 900, 4200, 0, 0],
        "Büromaterial":           [650, 100, 0, 1900, 950],
    },
}

MASCHINENABHAENGIG = ["Betriebsstoffe", "Kalk. Abschreibungen", "Kalk. Zinsen", "Fremdinstandhaltung"]
REST_FERTIGUNG2 = ["Hilfsstoffe", "Gehälter", "Leasing", "Büromaterial"]


def fmt(x, nk=2):
    s = f"{x:,.{nk}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s


def auswerten(m):
    """Berechnet Kostenartenplan, BAB-Spalten und Kalkulationssätze eines Monats."""
    guv = m["guv"]
    auf = {k: v for k, _, v in guv["aufwand"]}
    kosten = {  # Kostenartenplan: (Gesamt, Einzel)
        "Rohstoffe": (auf["6000"], auf["6000"]),
        "Vorprodukte/Fremdbauteile": (auf["6010"], auf["6010"]),
        "Hilfsstoffe": (auf["6020"], 0),
        "Betriebsstoffe": (auf["6030"], 0),
        "Löhne": (auf["6200"], auf["6200"]),
        "Gehälter": (auf["6300"], 0),
        "Kalk. Abschreibungen": (m["kalk"]["Abschreibungen"], 0),
        "Kalk. Zinsen": (m["kalk"]["Zinsen"], 0),
        "Fremdinstandhaltung": (auf["6160"], 0),
        "Leasing": (auf["6710"], 0),
        "Büromaterial": (auf["6800"], 0),
    }
    gesamt = sum(g for g, _ in kosten.values())
    einzel = sum(e for _, e in kosten.values())
    gk = gesamt - einzel
    bab = m["bab"]
    # Zeilen = Gemeinkostenarten müssen zum Kostenartenplan passen
    for art, vals in bab.items():
        assert sum(vals) == kosten[art][0], (m["name"], art, sum(vals), kosten[art])
    spalten = [sum(v[i] for v in bab.values()) for i in range(5)]
    assert sum(spalten) == gk, (sum(spalten), gk)
    fm = sum(m["fm"].values())
    assert fm + m["fl1"] + m["fl2"] == einzel, (fm, m["fl1"], m["fl2"], einzel)
    assert m["fl1"] + m["fl2"] == kosten["Löhne"][0]
    mask = [sum(bab[a][2] for a in MASCHINENABHAENGIG), sum(bab[a][2] for a in REST_FERTIGUNG2)]
    assert sum(mask) == spalten[2]
    mgk, fgk1, _, vw, vt = spalten
    r = {
        "MGK %": mgk / fm * 100,
        "FGK I %": fgk1 / m["fl1"] * 100,
        "Maschinenstundensatz": mask[0] / m["masch_std"],
        "Rest %": mask[1] / m["fl2"] * 100,
    }
    hkdu = fm + mgk + m["fl1"] + fgk1 + mask[0] + m["fl2"] + mask[1]
    r["HKdU"] = hkdu
    r["VwGK %"] = vw / hkdu * 100
    r["VtGK %"] = vt / hkdu * 100
    sk = hkdu + vw + vt
    assert sk == gesamt, (sk, gesamt)
    r["Selbstkosten"] = sk
    erg = {
        "Aufwand": sum(v for _, _, v in guv["aufwand"]),
        "Ertrag": sum(v for _, _, v in guv["ertrag"]),
    }
    erg["Gewinn"] = erg["Ertrag"] - erg["Aufwand"]
    neutral_auf = sum(v for k, _, v in guv["aufwand"] if k in m["neutral"])
    neutral_ert = sum(v for k, _, v in guv["ertrag"] if k in m["neutral"])
    erg["Neutral Aufwand"] = neutral_auf
    erg["Neutral Ertrag"] = neutral_ert
    erg["Neutrales Ergebnis"] = neutral_ert - neutral_auf
    return {"kosten": kosten, "gesamt": gesamt, "einzel": einzel, "gk": gk, "spalten": spalten,
            "masch": mask, "saetze": r, "guv": erg, "fm": fm}


if __name__ == "__main__":
    for m in (JULI, AUGUST):
        a = auswerten(m)
        print("==", m["name"])
        print("Kosten gesamt", fmt(a["gesamt"]), "Einzel", fmt(a["einzel"]), "Gemein", fmt(a["gk"]))
        print("Spalten", a["spalten"], "Masch/Rest", a["masch"])
        for k, v in a["saetze"].items():
            print(f"  {k}: {v:,.4f}")
        print("GuV", a["guv"])
