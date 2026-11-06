"""Baut den Moodle-Kurs so, dass der ganze Lernpfad nur EINEN Abschnitt belegt: Die Stufen werden Unterabschnitte darin.
Ohne Einstufungstests (jede Stufe öffnet nur nach der Abgabe des Meilensteins davor).

Gedacht für Moodle 4.5 (BBZ-Moodle 4.5.12+) mit Unterabschnitten. Der Baukasten selbst bleibt unverändert; dieses Skript arbeitet
mit einer temporären, angepassten Kopie seiner Skripte.

Aufruf (aus dem Lernpfad-Ordner):  python3 werkzeuge/bauen_moodle_ein_abschnitt.py <pfad-zum-baukasten> [--flach]
Ergebnis: ausgabe/moodle/<kurzname>_EIN-ABSCHNITT_moodle4-5.mbz
          mit --flach: <kurzname>_EIN-ABSCHNITT-FLACH_moodle4-5.mbz (ein Abschnitt, KEINE Unterabschnitte, alles untereinander)
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

if len(sys.argv) < 2:
    sys.exit(__doc__)
baukasten = Path(sys.argv[1])
FLACH = "--flach" in sys.argv[2:]
root = Path(__file__).resolve().parent.parent


def ersetze(datei, alt, neu, anzahl=1):
    text = datei.read_text(encoding="utf-8")
    assert alt in text, f"Baukasten-Version nicht erkannt: {alt[:60]}"
    datei.write_text(text.replace(alt, neu, anzahl), encoding="utf-8")


WRAPPER = '''
FLACH = __FLACH__

def ein_abschnitt(b, kurs):
    """Alle Stufen in einen Abschnitt: Startseite direkt, jede Stufe als Unterabschnitt mit allen Aktivitäten darin."""
    stufen = []
    for a in b["abschnitte"]:
        inhalte, vorige = [], None
        nacheinander = a.get("reihenfolge", "nacheinander") == "nacheinander"
        for e in a["einheiten"]:
            ref = e.get("freischalten_nach") or (vorige if nacheinander else None)
            if FLACH and ref is None and vorige is None:
                ref = a.get("freischalten_nach")  # erstes Modul der Stufe: Freischaltung der Stufe
            for j, inh in enumerate(e["inhalte"]):
                inh = dict(inh)
                if ref:
                    inh["voraus"] = ref
                inhalte.append(inh)
                if j == 0:
                    vorige = inh["id"]
        st = dict(titel=a["titel"], text=a.get("text", ""), inhalte=inhalte)
        if a.get("freischalten_nach") and not FLACH:
            st["freischalten_nach"] = a["freischalten_nach"]
        stufen.append(st)
    einheiten = [dict(titel=i["titel"], inhalte=[i]) for i in b["allgemein"]["inhalte"]] + stufen
    b["allgemein"]["inhalte"] = []
    liste = "".join(f"<li><b>{x['titel']}</b>" + (f": {x['text']}" if x.get("text") else "") + "</li>" for x in stufen)
    text = f"<p>{kurs.k.get('untertitel', '')}</p>" + (f"<p>Die Stufen in dieser Reihenfolge:</p><ul>{liste}</ul>" if FLACH else "")
    b["abschnitte"] = [dict(titel=kurs.titel, text=text, reihenfolge="frei", einheiten=einheiten)]
    return b


_beschreibung_orig = beschreibung


def beschreibung(kurs, pakete, version, h5p_dateien=None, entwuerfe=False, hinweise=None):
    return ein_abschnitt(_beschreibung_orig(kurs, pakete, version, h5p_dateien, entwuerfe, hinweise), kurs)


'''

with tempfile.TemporaryDirectory() as tmp:
    sk = Path(tmp) / "skripte"
    shutil.copytree(baukasten / "skripte", sk)
    for extra in ("vorlage", "referenzen"):
        if (baukasten / extra).exists():
            shutil.copytree(baukasten / extra, Path(tmp) / extra)
    # 1) Einstufungstests aus
    ersetze(sk / "gemeinsam.py", 'return (self.moodle.get("freischaltung", "einstufung") == "einstufung") and len(self.stufen) > 1',
            "return False  # Einstufungstests abgeschaltet")
    # 2) Ziel „4“: Moodle 4.5 mit Unterabschnitten
    ersetze(sk / "mbz.py", '"4": dict(version="2023042400", release="4.2 (Build: 20230424)", backup_release="4.2", unterabschnitte=False, h5p=False,',
            '"4": dict(version="2024100700", release="4.5 (Build: 20241007)", backup_release="4.5", unterabschnitte=True, h5p=False,')
    # 3) Freischaltung je Aktivität innerhalb eines Unterabschnitts
    ersetze(sk / "mbz.py", '''                    akt = self.inhalt(inh, ds)
                    if j == 0:
                        vorige_haupt = inh["id"]''', '''                    akt = self.inhalt(inh, ds)
                    if akt is not None and inh.get("voraus"):
                        verzoegert.append((akt, inh["voraus"]))
                    if j == 0:
                        vorige_haupt = inh["id"]''')
    # 4) Umbau der Kursbeschreibung
    ersetze(sk / "moodle_kurs.py", "def anleitung(kurs, b, version, mbz_name):",
            WRAPPER.replace("__FLACH__", repr(FLACH)) + "def anleitung(kurs, b, version, mbz_name):")
    if FLACH:
        ersetze(sk / "mbz.py", "backup_release=\"4.5\", unterabschnitte=True,", "backup_release=\"4.5\", unterabschnitte=False,")
        ersetze(sk / "mbz.py", """                        if ref:
                            verzoegert.append((akt, ref))
                        if j == 0:
                            vorige_haupt = inh["id"]""", """                        r_ = inh.get("voraus") or ref
                        if r_:
                            verzoegert.append((akt, r_))
                        if j == 0:
                            vorige_haupt = inh["id"]""")
    ersetze(sk / "moodle_kurs.py", 'sub = version == "5" and len(e["inhalte"]) > 1', "sub = len(e[\"inhalte\"]) > 1")
    for skript, extra in (("pruefen.py", []), ("bauen.py", []), ("moodle_kurs.py", ["--moodle", "4"])):
        r = subprocess.run([sys.executable, str(sk / skript), str(root), *extra])
        if r.returncode:
            sys.exit(r.returncode)
    out = root / "ausgabe" / "moodle"
    quelle = next(out.glob("*_moodle4.mbz"))
    suffix = "_EIN-ABSCHNITT-FLACH_moodle4-5" if FLACH else "_EIN-ABSCHNITT_moodle4-5"
    ziel = out / quelle.name.replace("_moodle4.mbz", suffix + ".mbz")
    shutil.move(quelle, ziel)
    anl = out / "ANLEITUNG_moodle4.md"
    if anl.exists():
        shutil.move(anl, out / f"ANLEITUNG{suffix.replace('_moodle4-5', '')}_moodle4-5.md")
    print("✓", ziel)
