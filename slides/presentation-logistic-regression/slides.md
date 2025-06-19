---
theme: the-unnamed
title: "Presentation: Logistic Regression"
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

- Definition der logistischen Regression
  - Statistisches Verfahren zur Modellierung
  - Vorhersage kategorialer Ergebnisse

- Bedeutung in der Datenanalyse
  - Weit verbreitetes Werkzeug
  - Erkennung von Mustern und Beziehungen

- Überblick über die Präsentation
  - Grundlagen und Theorie
  - Anwendungsbeispiele
  - Praktische Übungen und Code-Beispiele

<div @click="$slidev.nav.next" class="mt-12 py-1" hover:bg="white op-10">
  Drücke Space für die nächste Folie <carbon:arrow-right />
</div>

---
---
# Grundlagen der Logistischen Regression

- Unterschied zu linearer Regression
- Modelliert binäre Ergebnisse statt kontinuierlicher Werte
- Nutzt logistische Funktion zur Vorhersage von Klassen
- Logistische Funktion und Sigmoid-Kurve
- Transformation von Werten zwischen 0 und 1


---
---
# Anwendungsbeispiele in der Praxis

Anwendung von logistischen Regressionen zur Vorhersage der Ausfallwahrscheinlichkeit von Krediten.
Identifikation von Kundengruppen basierend auf Kaufverhalten und Demografie.
Unterstützung bei der Diagnose von Krankheiten durch Analyse von Patientendaten.

- **Kreditrisikoanalyse**
- **Kundensegmentierung**
- **Medizinische Diagnose**


---
---
# Implementierung in Python

```python
# Import von Bibliotheken
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Datensatzvorbereitung
data = pd.read_csv('daten.csv')
X = data[['Merkmal1', 'Merkmal2']]
y = data['Zielvariable']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Modelltraining und Prognose
modell = LogisticRegression()
modell.fit(X_train, y_train)
vorhersage = modell.predict(X_test)
```

---
---
# Vor- und Nachteile der Logistischen Regression

<div grid="~ cols-2 gap-4">
<div>

## Option A

- **Einfache Implementierung**
  - Leicht zu verstehen und anzuwenden
  - Weit verbreitete Bibliotheken verfügbar

- **Begrenzungen bei nicht-linearen Beziehungen**
  - Funktioniert schlecht bei komple

</div>
<div>

## Option B

xen Mustern
  - Erfordert Feature-Engineering für bessere Anpassung

- **Überanpassungsrisiko**
  - Kann bei zu vielen Variablen überanpassen
  - Regularisierung notwendig, um Überanpassung zu vermeiden

</div>
</div>

---
---
# Erweiterungen und Alternativen

```markdown
```

- **Regularisierte logistische Regression**
- Vermeidet Überanpassung durch Regularisierungsterm
- **Kernel-Methoden**
- Erweitern die logistische Regression auf nicht-lineare Probleme
- **Andere Klassifikationsalgorithmen**


---
layout: center
class: text-center
---

# Zusammenfassung und Ausblick

- **Wichtigkeit der logistischen Regression**
  - Grundlegendes Modell für Klassifikationsprobleme
  - Einfach zu interpretieren und effizient

- **Weiterführende Literatur und Ressourcen**
  - Empfohlene Bücher und Online-Kurse
  - Fachartikel und Forschungsarbeiten

- **Einladung zu Fragen**
  - Offene Fragerunde
  - Diskussionsforum für tiefergehende Themen


