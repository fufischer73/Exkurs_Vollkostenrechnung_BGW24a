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

ORDER = ["Hilfsstoffe", "Betriebsstoffe", "Gehälter", "Kalk. Abschreibungen", "Kalk. Zinsen",
         "Fremdinstandhaltung", "Leasing", "Büromaterial"]

# Verteilungsschlüssel (gelten in Juli und August unverändert); alle übrigen Zeilen werden direkt (per Beleg) zugeordnet
SCHLUESSEL = {
    "Betriebsstoffe": ("Verbrauch in kWh (Schlüsselzahlen)", [3, 12, 25, 2, 3]),
    "Kalk. Zinsen": ("Anteil am gebundenen Kapital (Schlüsselzahlen)", [4, 6, 25, 3, 2]),
    "Leasing": ("genutzte Fläche in m²", [100, 120, 40, 40, 40]),
}

# Bezugsgrößen je Monat (aus dem Kostenartenplan, der Lohnbuchhaltung und dem Arbeitsplan)
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


# --- Erweiterung: Vorkostenstellen (Fuhrpark, Fertigungsplanung) mit Umlage im Treppenstufenverfahren ----------------
VK_STELLEN = ["Fuhrpark", "Material", "Fertigungsplanung", "Fertigung I", "Fertigung II", "Verwaltung", "Vertrieb"]
# Ergebnis von Schritt 1 (Verteilung der Gemeinkostenarten), Juli – Spalten wie VK_STELLEN
VK_BAB = {
    "Hilfsstoffe":          [0, 0, 0, 7200, 800, 0, 0],
    "Betriebsstoffe":       [3000, 1200, 0, 3800, 8000, 800, 1200],
    "Gehälter":             [1000, 25500, 6500, 15900, 2200, 46000, 27000],
    "Kalk. Abschreibungen": [5000, 3200, 0, 8000, 43000, 4000, 1800],
    "Kalk. Zinsen":         [0, 3000, 1500, 4000, 17750, 2250, 1500],
    "Fremdinstandhaltung":  [1500, 300, 0, 0, 6250, 0, 0],
    "Leasing":              [1500, 1500, 0, 3600, 1200, 1200, 1200],
    "Büromaterial":         [0, 700, 0, 125, 0, 1750, 1000],
}
# Umlageschlüssel (Teile je Kostenstelle)
VK_SCHL_FUHRPARK = {"Material": 4, "Fertigungsplanung": 1, "Fertigung I": 3, "Fertigung II": 2, "Verwaltung": 0, "Vertrieb": 2}
VK_SCHL_PLANUNG = {"Fertigung I": 5, "Fertigung II": 4}


def vorkostenumlage():
    """Treppenstufenverfahren: erst Fuhrpark auf alle anderen Stellen, dann Fertigungsplanung auf die Fertigung."""
    prim = [sum(v[i] for v in VK_BAB.values()) for i in range(7)]
    z = dict(zip(VK_STELLEN, prim))
    teile = sum(VK_SCHL_FUHRPARK.values())
    u1 = {k: z["Fuhrpark"] * t / teile for k, t in VK_SCHL_FUHRPARK.items()}
    zw = {k: z[k] + u1.get(k, 0) for k in VK_STELLEN}
    zw["Fuhrpark"] = 0
    teile2 = sum(VK_SCHL_PLANUNG.values())
    u2 = {k: zw["Fertigungsplanung"] * t / teile2 for k, t in VK_SCHL_PLANUNG.items()}
    end = {k: zw[k] + u2.get(k, 0) for k in VK_STELLEN}
    end["Fertigungsplanung"] = 0
    return prim, u1, zw, u2, end


def pruefe_vorkosten():
    for art, vals in VK_BAB.items():
        assert sum(vals) == sum(JULI["bab"][art]), art
    prim, u1, zw, u2, end = vorkostenumlage()
    sp = auswerten(JULI)["spalten"]
    assert [end["Material"], end["Fertigung I"], end["Fertigung II"], end["Verwaltung"], end["Vertrieb"]] == sp, (end, sp)
    assert sum(prim) == 266925 and abs(sum(end.values()) - 266925) < 1e-9


# --- Stufe 3: Ist-Sätze der letzten vier Monate und daraus gebildete Normalsätze ---------------------------------
ISTSAETZE = {  # Monat: (MGK %, FGK I %, Maschinenstundensatz €/h, Rest %, VwGK %, VtGK %)
    "April": (20.3, 79.5, 79.5, 29.5, 11.6, 8.2),
    "Mai":   (20.1, 80.5, 80.0, 30.5, 12.2, 7.8),
    "Juni":  (19.9, 79.0, 79.5, 30.0, 11.8, 8.1),
    "Juli":  (19.7, 81.0, 81.0, 30.0, 12.4, 7.9),
}
NORMAL = (20.0, 80.0, 80.0, 30.0, 12.0, 8.0)   # MGK, FGK I, Maschinenstundensatz, Rest, VwGK, VtGK
SAETZE_NAMEN = ["MGK-Satz (%)", "FGK-Satz Fertigung I (%)", "Maschinenstundensatz (€ je h)",
                "Restgemeinkosten-Satz (%)", "VwGK-Satz (%)", "VtGK-Satz (%)"]


def pruefe_normal():
    for i, soll in enumerate(NORMAL):
        mittel = sum(v[i] for v in ISTSAETZE.values()) / len(ISTSAETZE)
        assert abs(mittel - soll) < 1e-9, (SAETZE_NAMEN[i], mittel, soll)
    # Juli-Ist muss zur Auswertung von Stufe 2 passen (zwei Dezimalstellen)
    r = auswerten(JULI)["saetze"]
    j = ISTSAETZE["Juli"]
    assert round(r["MGK %"], 2) == j[0] and round(r["FGK I %"], 2) == j[1] and round(r["Maschinenstundensatz"], 2) == j[2]
    assert round(r["Rest %"], 2) == j[3] and round(r["VwGK %"], 1) == j[4] and round(r["VtGK %"], 1) == j[5]


def runden(x):
    from decimal import Decimal, ROUND_HALF_UP
    return float(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def kalkulation(fm, lohn, masch_std, masch_lohn_satz, gewinn=20, skonto=3, rabatt=10):
    """Zuschlagskalkulation mit den Normalsätzen. lohn = Fertigungslöhne Handarbeit (Summe je Stück)."""
    mgk_s, fgk_s, mss, rest_s, vw_s, vt_s = NORMAL
    z = {}
    z["Fertigungsmaterial"] = runden(fm)
    z["MGK"] = runden(z["Fertigungsmaterial"] * mgk_s / 100)
    z["Materialkosten"] = runden(z["Fertigungsmaterial"] + z["MGK"])
    z["Fertigungslöhne"] = runden(lohn)
    z["FGK"] = runden(z["Fertigungslöhne"] * fgk_s / 100)
    z["Fertigungskosten I"] = runden(z["Fertigungslöhne"] + z["FGK"])
    z["Maschinenkosten"] = runden(masch_std * mss)
    z["Maschinenlöhne"] = runden(masch_std * masch_lohn_satz)
    z["Restgemeinkosten"] = runden(z["Maschinenlöhne"] * rest_s / 100)
    z["Fertigungskosten II"] = runden(z["Maschinenkosten"] + z["Maschinenlöhne"] + z["Restgemeinkosten"])
    z["Herstellkosten"] = runden(z["Materialkosten"] + z["Fertigungskosten I"] + z["Fertigungskosten II"])
    z["Verwaltung/Vertrieb"] = runden(z["Herstellkosten"] * (vw_s + vt_s) / 100)
    z["Selbstkosten"] = runden(z["Herstellkosten"] + z["Verwaltung/Vertrieb"])
    z["Gewinn"] = runden(z["Selbstkosten"] * gewinn / 100)
    z["Barverkaufspreis"] = runden(z["Selbstkosten"] + z["Gewinn"])
    z["Zielverkaufspreis"] = runden(z["Barverkaufspreis"] / (1 - skonto / 100))
    z["Skonto"] = runden(z["Zielverkaufspreis"] - z["Barverkaufspreis"])
    z["Listenverkaufspreis"] = runden(z["Zielverkaufspreis"] / (1 - rabatt / 100))
    z["Rabatt"] = runden(z["Listenverkaufspreis"] - z["Zielverkaufspreis"])
    return z


# Business Deluxe (Lernsituation „Preise kalkulieren“, Info 2)
BUSINESS_DELUXE = dict(fm=40.00, lohn=0.30 * 13 + 0.40 * 14 + 0.20 * 16, masch_std=0.20, masch_lohn_satz=14.0)
# Zweiter Rucksack für Meilenstein 3 (eigene Zahlen)
EXPLORER = dict(fm=36.50, lohn=0.25 * 13 + 0.35 * 14 + 0.15 * 16, masch_std=0.15, masch_lohn_satz=14.0)


def pruefe_schluessel(m):
    for art, (_, teile) in SCHLUESSEL.items():
        vals = m["bab"][art]
        summe = sum(vals)
        assert summe % sum(teile) == 0, (m["name"], art)
        je = summe // sum(teile)
        assert vals == [t * je for t in teile], (m["name"], art, vals, teile)


if __name__ == "__main__":
    pruefe_schluessel(JULI)
    pruefe_schluessel(AUGUST)
    pruefe_normal()
    pruefe_vorkosten()
    k = kalkulation(**BUSINESS_DELUXE)
    assert (k["Selbstkosten"], k["Barverkaufspreis"], k["Zielverkaufspreis"], k["Listenverkaufspreis"]) == (108.60, 130.32, 134.35, 149.28), k
    print("Business Deluxe:", {a: b for a, b in k.items() if a in ("Herstellkosten", "Selbstkosten", "Listenverkaufspreis")})
    print("Explorer:", kalkulation(**EXPLORER))
    for m in (JULI, AUGUST):
        a = auswerten(m)
        print("==", m["name"])
        print("Kosten gesamt", fmt(a["gesamt"]), "Einzel", fmt(a["einzel"]), "Gemein", fmt(a["gk"]))
        print("Spalten", a["spalten"], "Masch/Rest", a["masch"])
        for k, v in a["saetze"].items():
            print(f"  {k}: {v:,.4f}")
        print("GuV", a["guv"])
