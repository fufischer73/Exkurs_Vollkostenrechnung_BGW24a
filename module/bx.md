---
titel: "Erweiterung (freiwillig): Vorkostenstellen und Umlage"
minuten: 45
review: entwurf
lernziele:
  - Vorkostenstellen von Hauptkostenstellen unterscheiden,
  - die Kosten der Vorkostenstellen im Treppenstufenverfahren auf die Hauptkostenstellen umlegen,
  - im erweiterten BAB die Zuschlagssätze berechnen und mit dem einfachen BAB vergleichen.
kurzcheck:
  - frage: "Was unterscheidet Vorkostenstellen von Hauptkostenstellen?"
    antworten: ["Vorkostenstellen erbringen Leistungen für andere Kostenstellen und werden auf die Hauptkostenstellen umgelegt. Die Hauptkostenstellen bilden die Zuschlagssätze.", "Vorkostenstellen haben keine Kosten.", "Hauptkostenstellen gibt es nur in der Fertigung."]
    richtig: 1
    richtig_text: "Genau. Die Kosten der Vorkostenstellen landen am Ende in den Hauptkostenstellen und damit in der Kalkulation."
    falsch_text: "Vorkostenstellen haben durchaus Kosten. Weil sie ihre Leistungen anderen Stellen zur Verfügung stellen, werden diese Kosten weitergegeben (umgelegt)."
  - frage: "Der Fuhrpark hat 6.000 € Kosten. Sie werden im Verhältnis 1 : 2 : 3 auf drei Kostenstellen umgelegt. Wie viel erhält die Stelle mit der Schlüsselzahl 3?"
    antworten: ["3.000 €", "2.000 €", "1.000 €"]
    richtig: 1
    richtig_text: "Richtig. 1 + 2 + 3 = 6 Teile, ein Teil sind 1.000 €, drei Teile also 3.000 €."
    falsch_text: "Rechne zuerst die Summe der Schlüsselzahlen (1 + 2 + 3 = 6). Dann 6.000 € ÷ 6 = 1.000 € je Teil und mal 3."
  - frage: "Warum wird im Treppenstufenverfahren zuerst der Fuhrpark umgelegt und dann die Fertigungsplanung?"
    antworten: ["Weil der Fuhrpark auch Leistungen an die Fertigungsplanung abgibt. Deren Kosten müssen vollständig sein, bevor sie umgelegt werden.", "Weil der Fuhrpark mehr Geld kostet.", "Weil das alphabetisch so geordnet ist."]
    richtig: 1
    richtig_text: "Genau. Die Reihenfolge richtet sich danach, wer wem Leistungen liefert."
    falsch_text: "Die Reihenfolge hängt von den Leistungsbeziehungen ab: Der Fuhrpark beliefert auch die Fertigungsplanung, deshalb kommt er zuerst."
quellen: [q-lehrwerk]
---
:::notiz Freiwillig
Dieses Modul ist eine **Erweiterung**. Du brauchst es nicht für die Stufe 3. Wer schneller ist oder es genauer wissen möchte, bearbeitet es nach dem Meilenstein 2.
:::

Bisher hast du fünf Kostenstellen verwendet. Größere Betriebe haben zusätzlich **Vorkostenstellen**. Sie arbeiten nicht direkt am Rucksack, sondern unterstützen andere Stellen.

## 1. Vor- und Hauptkostenstellen

| Art | Aufgabe | Beispiel bei Montelli |
| --- | --- | --- |
| **Allgemeine Kostenstelle** (Vorkostenstelle) | beliefert alle anderen Stellen | **Fuhrpark** (Gabelstapler, Lieferwagen) |
| **Hilfskostenstelle** (Vorkostenstelle) | beliefert vor allem bestimmte Hauptstellen | **Fertigungsplanung** (Arbeitsvorbereitung für die Fertigung) |
| **Hauptkostenstellen** | arbeiten direkt am Produkt, bilden die Zuschlagssätze | Material, Fertigung I, Fertigung II, Verwaltung, Vertrieb |

Die Kosten von Fuhrpark und Fertigungsplanung kann man nicht direkt in der Kalkulation verwenden. Sie müssen daher vorher auf die Hauptkostenstellen **umgelegt** werden.

## 2. Das Treppenstufenverfahren

Man legt die Kosten der Vorkostenstellen **in Stufen** um, wie bei einer Treppe:

1. **Schritt:** Die Kosten der **allgemeinen Kostenstelle** (Fuhrpark) werden auf alle anderen Stellen verteilt, auch auf die Fertigungsplanung.
2. **Schritt:** Die Kosten der **Hilfskostenstelle** (Fertigungsplanung), jetzt einschließlich des Anteils vom Fuhrpark, werden auf die Hauptkostenstellen verteilt, für die sie arbeitet (hier: die beiden Fertigungsstellen).

:::notiz Andere Verfahren
Es gibt weitere Verfahren der Umlage, zum Beispiel wenn sich Vorkostenstellen gegenseitig beliefern. Wir nutzen hier das Treppenstufenverfahren, es reicht für den Einstieg.
:::

## 3. Der erweiterte BAB für Juli

Das Rechnungswesen hat den ersten Schritt (Verteilung der Gemeinkostenarten) schon erledigt. Das Ergebnis je Kostenstelle:

| Kostenstelle | Gemeinkosten nach Schritt 1 |
| --- | --- |
| Fuhrpark (allgemeine Kostenstelle) | 12.000 € |
| Material | 35.400 € |
| Fertigungsplanung (Hilfskostenstelle) | 8.000 € |
| Fertigung I | 42.625 € |
| Fertigung II (Maschinenplatz) | 79.200 € |
| Verwaltung | 56.000 € |
| Vertrieb | 33.700 € |
| **Summe** | **266.925 €** |

**Umlageschlüssel:**

| Kostenstelle | Fuhrpark: Transportaufträge | Fertigungsplanung: Planungsstunden |
| --- | --- | --- |
| Material | 4 | – |
| Fertigungsplanung | 1 | – |
| Fertigung I | 3 | 5 |
| Fertigung II | 2 | 4 |
| Verwaltung | 0 | – |
| Vertrieb | 2 | – |

:::material material/AB-bx-vorkostenstellen.docx Arbeitsblatt BX: Vorkostenstellen und Umlage (Querformat)
Enthält den vollständigen BAB nach Schritt 1, die Schlüssel und die leere Umlagetabelle.
:::

:::material material/umlage-vorlage.xlsx Excel-Vorlage: Umlage im Treppenstufenverfahren
Gelbe Felder ausfüllen. Die Tabelle rechnet die Umlagen.
:::

:::aufgabe basis 30 1 · Umlage durchführen
1. **Umlage 1:** Lege die 12.000 € des Fuhrparks mit den Transportaufträgen auf die anderen Stellen um. Bilde die Zwischensummen.
2. **Umlage 2:** Lege die Fertigungsplanung (jetzt mit dem Anteil vom Fuhrpark) mit den Planungsstunden auf Fertigung I und II um. Bilde die Endsummen der Hauptkostenstellen.
3. **Probe:** Die Endsummen der Hauptkostenstellen müssen zusammen **266.925 €** ergeben.
4. Berechne den **MGK-Satz** und den **FGK-Satz der Fertigung I** mit den Bezugsgrößen aus Modul B2 (Fertigungsmaterial 200.000 €, Fertigungslöhne Handarbeit 62.500 €). Vergleiche mit den Ergebnissen aus Stufe 2.

:::checkliste Selbstcheck
- Bei Umlage 1 habe ich die Schlüsselzahlen aller sechs Stellen addiert (12).
- Die Fertigungsplanung hat nach Umlage 1 neue Kosten (9.000 €), das ist die Grundlage für Umlage 2.
- Fuhrpark und Fertigungsplanung stehen am Ende auf 0 €.
- Die Probe stimmt (266.925 €).
:::

:::loesung Lösung
| Kostenstelle | Schritt 1 | Umlage Fuhrpark | Zwischensumme | Umlage Planung | Endsumme |
| --- | --- | --- | --- | --- | --- |
| Fuhrpark | 12.000 | −12.000 | 0 | | 0 |
| Material | 35.400 | +4.000 | 39.400 | | 39.400 |
| Fertigungsplanung | 8.000 | +1.000 | 9.000 | −9.000 | 0 |
| Fertigung I | 42.625 | +3.000 | 45.625 | +5.000 | 50.625 |
| Fertigung II | 79.200 | +2.000 | 81.200 | +4.000 | 85.200 |
| Verwaltung | 56.000 | 0 | 56.000 | | 56.000 |
| Vertrieb | 33.700 | +2.000 | 35.700 | | 35.700 |

Rechenwege: Fuhrpark 12.000 € ÷ 12 Teile = 1.000 € je Teil. Fertigungsplanung 9.000 € ÷ 9 Teile = 1.000 € je Teil.

MGK-Satz: 39.400 × 100 ÷ 200.000 = **19,70 %**. FGK-Satz Fertigung I: 50.625 × 100 ÷ 62.500 = **81,00 %**. Beide Sätze sind **gleich** wie in Stufe 2.
:::
:::

:::notiz Warum kommt dasselbe heraus?
In diesem Beispiel haben wir die Zahlen so gewählt, dass die Sätze mit denen aus Stufe 2 übereinstimmen. So kannst du dein Ergebnis kontrollieren. In der Praxis ändern sich die Sätze, wenn man Vorkostenstellen genauer erfasst: Die Kosten werden dann **verursachungsgerechter** auf die Hauptkostenstellen verteilt.
:::

:::aufgabe plus 10 2 · Reihenfolge der Umlage
Was würde passieren, wenn du die Fertigungsplanung zuerst umlegst und den Fuhrpark danach? Begründe, warum die Reihenfolge wichtig ist.

:::loesung Lösung
Der Fuhrpark gibt auch an die Fertigungsplanung Kosten ab (1.000 €). Legst du die Fertigungsplanung zuerst um, fehlen diese 1.000 €. Sie würden nach der Umlage des Fuhrparks bei der Fertigungsplanung hängen bleiben und nicht mehr auf die Fertigung kommen. Der Betrag ginge in der Kalkulation **verloren**. Deshalb legt man die Stelle zuerst um, die an die anderen Vorkostenstellen liefert.
:::
:::
