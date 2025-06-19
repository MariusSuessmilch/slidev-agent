---
theme: the-unnamed
title: "Presentation: Machine Learning Grundlagen"
info: |
  For Studenten audience
class: text-center
drawings:
  persist: false
transition: slide-left
mdc: true
fonts:
sans: Montserrat
---

# Einführung in die Grundlagen des Machine Learning

An overview of key concepts and practical applications

<div @click="$slidev.nav.next" class="mt-12 py-1" hover:bg="white op-10">
  Drücke Space für die nächste Folie <carbon:arrow-right />
</div>

---
---
# Was ist Machine Learning?

- Definition von Machine Learning
- Überwachung, unbeaufsichtigt und bestärkendes Lernen
- Beispiele im Alltag


---
---
# Wichtige Algorithmen im Machine Learning

- Lineare Regression
- Entscheidungsbäume
- Neurale Netze
- Support Vector Machines
- K-Nearest Neighbors


---
---
# Ein einfaches Beispiel in Python

```python
import numpy as np
from sklearn.linear_model import LinearRegression
# Einfaches Modell erstellen
x = np.array([[1], [2], [3], [4]])
y = np.array([2, 3, 5, 7])
model = LinearRegression().fit(x, y)
# Ergebnisse interpretieren
print("Koeffizient:", model.coef_)
print("Intercept:", model.intercept_)
```

---
---
# Vorteile und Herausforderungen von Machine Learning

<div grid="~ cols-2 gap-4">
<div>

## Option A

- Automatisierung und Effizienz: Steigerung der Produktivität durch automatisierte Prozesse
- Datenabhängigkeit: Qualität und Menge der Daten sind entscheidend
- Komplexität der Modelle: Erfordert

</div>
<div>

## Option B

tiefes Verständnis und Expertise
- Ethik und Datenschutz: Sicherstellung der Privatsphäre und ethischer Standards
- Balance zwischen Chancen und Risiken: Notwendig für verantwortungsvolle Nutzung

</div>
</div>

---
---
# Anwendungen von Machine Learning

```
```

- Gesundheitswesen
- Finanzen
- E-Commerce
- Transportwesen


---
layout: center
class: text-center
---

# Zusammenfassung und Ausblick

- Machine Learning hat unser Verständnis von Daten revolutioniert.
- Die Zukunft von ML verspricht grenzenlose Anwendungen.
- Bleiben Sie neugierig und innovativ.
- Gestalten Sie mit ML eine bessere Zukunft.
- Beginnen Sie heute, um morgen zu inspirieren.


