---
theme: the-unnamed
title: "Presentation: Machine Learning Basics"
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

# Einführung in Maschinelles Lernen

- **Definition von Maschinellem Lernen**
  - Systeme, die automatisch aus Daten lernen
  - Anpassung ohne explizite Programmierung

- **Relevanz in der Datenwissenschaft**
  - Schlüsseltechnologie zur Datenanalyse
  - Ermöglicht Vorhersagen und Mustererkennung

- **Ziele des Vortrags**
  - Grundlegende Begriffe und Konzepte
  - Verständnis der Anwendungsmöglichkeiten

<div @click="$slidev.nav.next" class="mt-12 py-1" hover:bg="white op-10">
  Drücke Space für die nächste Folie <carbon:arrow-right />
</div>

---
---
# Schlüsselkonzepte im Maschinellen Lernen

- **Überwachtes Lernen**
- Modelle mit gekennzeichneten Daten trainieren
- Ziel: Vorhersage neuer, unbekannter Daten
- **Unüberwachtes Lernen**
- Muster in unmarkierten Daten finden


---
---
# Ein einfaches Beispiel: Lineare Regression

```python
# Datenvorbereitung
import pandas as pd
from sklearn.model_selection import train_test_split

# Daten laden
data = pd.read_csv('data.csv')
X = data.drop('Zielvariable', axis=1)
y = data['Zielvariable']

# Daten aufteilen
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modelltraining
from sklearn.linear_model import LinearRegression

# Modell initialisieren
model = LinearRegression()

# Modell trainieren
model.fit(X_train, y_train)

# Vorhersage
y_pred = model.predict(X_test)
print(y_pred)
```

---
---
# Vor- und Nachteile von Maschinellem Lernen

<div grid="~ cols-2 gap-4">
<div>

## Option A

```

- Automatisierung und Effizienz
  - + Reduziert menschlichen Arbeitsaufwand
  - + Verbessert Prozessgeschwindigkeit
- Komplexität und Ausreißer
  - - Erfordert

</div>
<div>

## Option B

komplexe Algorithmen
  - - Empfindlich gegenüber Ausreißern
- Datenabhängigkeit
  - - Hohe Datenqualität notwendig
  - - Begrenzte Leistung bei ungenügenden Daten
```

</div>
</div>

---
layout: center
class: text-center
---

# Zusammenfassung und Ausblick

> Machine Learning wird zunehmend unverzichtbar in vielen Branchen.

Fortlaufendes Lernen und Anpassung sind entscheidend für den Erfolg.

ML-Techniken erweitern die Möglichkeiten der Datenanalyse erheblich.

— **Beitrag zur Datenwissenschaft**


