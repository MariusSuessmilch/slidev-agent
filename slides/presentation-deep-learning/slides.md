---
theme: the-unnamed
title: "Presentation: Deep Learning"
info: |
  For students audience
class: text-center
drawings:
  persist: false
transition: slide-left
mdc: true
fonts:
sans: Montserrat
---

# Einführung in Deep Learning

- Was ist Deep Learning?
  - Teilgebiet des maschinellen Lernens
  - Nutzt künstliche neuronale Netze

- Bedeutung von Deep Learning
  - Revolutioniert viele Branchen
  - Bietet hochpräzise Modelle

- Anwendungsgebiete
  - Bild- und Spracherkennung
  - Autonome Fahrzeuge
  - Medizinische Diagnostik

<div @click="$slidev.nav.next" class="mt-12 py-1" hover:bg="white op-10">
  Drücke Space für die nächste Folie <carbon:arrow-right />
</div>

---
---
# Kernkonzepte des Deep Learning

- Neuronale Netze
- Modelle, die das menschliche Gehirn nachahmen
- Bestehen aus Schichten von Neuronen
- Verstärkungslernen
- Lernen durch Belohnung und Bestrafung


---
---
# Ein einfaches Beispiel: Bildklassifikation

```python
# Import von Bibliotheken
import tensorflow as tf
from tensorflow.keras import layers, models

# Modellarchitektur
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])

# Training und Evaluierung des Modells
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.fit(train_images, train_labels, epochs=5)
test_loss, test_acc = model.evaluate(test_images, test_labels)
```

---
layout: center
class: text-center
---

# Zusammenfassung und Ausblick

> Revolutioniert viele Branchen durch Automatisierung.
Weiterentwicklung von Modellen und Algorithmen.
Erschließen neuer Felder wie Medizin und Bildung.
Datensicherheit und ethische Fragestellungen.
"Die Grenzen des Deep Learning sind die Grenzen unserer Vorstellungskraft."

— Inspirierende Gedanken:
