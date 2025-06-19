---
theme: the-unnamed
title: "Presentation: Neural Networks"
info: |
  For computer science students audience
class: text-center
drawings:
  persist: false
transition: slide-left
mdc: true
fonts:
sans: Montserrat
---

# Einführung in Neuronale Netze

- **Definition von Neuronalen Netzen**
  Modelle, die das menschliche Gehirn nachahmen.

- **Bedeutung in der Informatik**
  Grundpfeiler für maschinelles Lernen und KI.

- **Anwendungsbereiche**
  Bild- und Spracherkennung, autonomes Fahren, Medizin.

- **Technische Grundlage**
  Besteht aus Schichten von Neuronen, die Daten verarbeiten.

- **Aktuelle Entwicklungen**
  Tiefe Neuronale Netze und deren Leistungsfähigkeit.

<div @click="$slidev.nav.next" class="mt-12 py-1" hover:bg="white op-10">
  Drücke Space für die nächste Folie <carbon:arrow-right />
</div>

---
---
# Grundlagen der Neuronalen Netze

- **Künstliche Neuronen**
- Nachbildung biologischer Neuronen
- Eingabe, Verarbeitung, Ausgabe von Signalen
- **Schichtenarchitektur**
- Eingabe-, versteckte und Ausgabeschichten


---
---
# Training von Neuronalen Netzen

- **Vorwärts- und Rückwärtsausbreitung**
- Übertragung von Daten durch das Netz
- Fehlerkorrektur durch Rückwärtsausbreitung
- **Gradientenabstieg**
- Optimierung von Gewichten


---
---
# Beispiel: Bildklassifikation mit Keras

```python
# Datenvorbereitung
from keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_generator = datagen.flow_from_directory(
    'pfad_zu_daten',
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary',
    subset='training'
)

validation_generator = datagen.flow_from_directory(
    'pfad_zu_daten',
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary',
    subset='validation'
)
```

---
---
# Vor- und Nachteile von Neuronalen Netzen

<div grid="~ cols-2 gap-4">
<div>

## Option A

- Hervorragende Leistung bei komplexen Aufgaben
  - Besonders bei Bild- und Spracherkennung
- Hoher Rechenaufwand
  - Benötigt leistungsstarke Hardware
- Erklärbarkei

</div>
<div>

## Option B

t der Modelle
  - Oft schwer nachvollziehbar
- Anpassungsfähigkeit
  - Gut für sich ändernde Datenmuster
- Datenintensiv
  - Erfordert große Datenmengen zum Trainieren

</div>
</div>

---
layout: center
class: text-center
---

# Zusammenfassung und Ausblick

> ```



```

— Wie könnte Ihr Beitrag zur Forschung aussehen?
