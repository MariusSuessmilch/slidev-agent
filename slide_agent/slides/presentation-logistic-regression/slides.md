---
theme: the-unnamed
title: "Presentation: Logistic
      Regression"
info: |
  For data science students audience
class: text-center
drawings:
  persist: false
transition: slide-left
mdc: true
fonts:
sans: Montserrat
---

# Einführung in die Logistische Regression

### Einführung in die Logistische Regression

- **Definition der logistischen Regression**
  - Statistisches Modell zur Klassifikation
  - Berechnung der Wahrscheinlichkeit von Ereignissen

- **Anwendungsbereiche in der Datenwissenschaft**
  - Krankheitsvorhersage in der Medizin
  - Kundenabwanderungsanalyse im Marketing

- **Ziele der Präsentation**
  - Grundlagen verstehen
  - Anwendungsmöglichkeiten erkennen
  - Praktische Beispiele untersuchen

<div @click="$slidev.nav.next" class="mt-12 py-1" hover:bg="white op-10">
  Drücke Space für die nächste Folie <carbon:arrow-right />
</div>

---
---
# Grundlagen der Logistischen Regression

- Sigmoid-Funktion
- Transformiert Werte in den Bereich [0, 1]
- Definiert Wahrscheinlichkeiten für binäre Klassifikation
- Logit-Funktion
- Umkehrfunktion der Sigmoid-Funktion


---
---
# Vorteile der Logistischen Regression

- Einfachheit und Effizienz
- Schnelle Implementierung und Berechnung
- Geringer Rechenaufwand
- Interpretierbarkeit der Ergebnisse
- Einfache Analyse der Koeffizienten


---
---
# Anwendungsbeispiele der Logistischen Regression

Vorhersage von Krankheiten basierend auf Patientenmerkmalen.
Einschätzung der Kreditwürdigkeit von Antragstellern.
Prognose von Kundenreaktionen auf Werbekampagnen.

- **Medizinische Diagnose**
- **Kreditrisikobewertung**
- **Marketing-Analysen**


---
---
# Implementierung in Python

```python
# Import von Bibliotheken
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Datenvorbereitung
data = pd.read_csv('data.csv')
X = data[['feature1', 'feature2']]
y = data['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Model-Training und Evaluierung
model = LogisticRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
print("Genauigkeit:", accuracy_score(y_test, predictions))
```

---
---
# Hyperparameter-Tuning

Minimierung von Überanpassung, z.B. L1, L2
Verlässliche Modellbewertung durch Datenaufteilung
Systematische Auswahl optimaler Hyperparameter

- **Regularisierungstechniken**
- **Kreuzvalidierung**
- **Grid Search**


---
---
# Vergleich mit anderen Klassifikationsmethoden

<div grid="~ cols-2 gap-4">
<div>

## Option A

```

- Vergleich mit Entscheidungsbäumen:
  - Entscheidungsbäume sind interpretierbar, Logistische Regression einfacher zu implementieren.
  - Logistische Regression eignet sich besser für lineare Trennungen.

- Vergleich mit Support-Vektor-Maschinen:
  - SVMs sind flexibler bei nicht-linearen Daten, Logistische Regression schnell

</div>
<div>

## Option B

er bei großen Datensätzen.
  - Logistische Regression liefert Wahrscheinlichkeiten, SVMs klassifizieren strikt.

- Vergleich mit Neuronalen Netzen:
  - Neuronale Netze sind leistungsfähiger bei komplexen Mustern, erfordern jedoch mehr Rechenleistung.
  - Logistische Regression ist einfacher zu trainieren und zu interpretieren.
```

</div>
</div>

---
---
# Herausforderungen und Lösungsansätze

- Multikollinearität
- Reduziert die Interpretierbarkeit des Modells
- Lösung: Verwendung von Regularisierungstechniken
- Overfitting
- Modell passt zu gut auf Trainingsdaten


---
---
# Zukünftige Entwicklungen

Kombination von Logistischer Regression
und tiefen neuronalen Netzen.
Vereinfachung und Beschleunigung des
Modelltrainingsprozesses.
Verbesserung der Skalierbarkeit und
Effizienz bei großen Datensätzen.
Automatisierung der Modellauswahl
und Parameteroptimierung.
Anpassung der Modelle für schnellere
und genauere Vorhersagen.

- **Integration mit Deep Learning**
- **Automatisierte maschinelle Lernplattformen**
- **Erweiterung auf größere Datenmengen**
- **Einsatz von AutoML**
- **Verstärkte Nutzung in Echtzeit-Anwendungen**


---
layout: center
class: text-center
---

# Zusammenfassung und Fazit

- Kernaspekte der logistischen Regression:
  - Modelliert die Wahrscheinlichkeit von Kategorien
  - Nutzt logistische Funktion für Klassifikation

- Wichtigkeit in der Datenwissenschaft:
  - Häufig für binäre Klassifikationsprobleme
  - Grundlage für viele erweiterte Modelle

- Abschließende Gedanken:
  - Trotz Einfachheit kraftvoll und vielseitig
  - Essenziell für das Verständnis komplexer Modelle
