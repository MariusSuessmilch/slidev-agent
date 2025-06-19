---
theme: the-unnamed
title: "Presentation: Data Science Basics"
info: |
  For beginners audience
class: text-center
drawings:
  persist: false
transition: slide-left
mdc: true
fonts:
sans: Montserrat
---

# Introduction to Data Science Basics
<toc />
An overview of key concepts and practical applications

<div @click="$slidev.nav.next" class="mt-12 py-1" hover:bg="white op-10">
  Drücke Space für die nächste Folie <carbon:arrow-right />
</div>

---
---
# Key Concepts in Data Science

- Data Collection: Gathering raw data from various sources
- Data Cleaning: Preparing data by removing errors and inconsistencies
- Data Analysis: Extracting insights and identifying patterns
- Data Visualization: Representing data through charts and graphs
- Machine Learning Basics: Understanding algorithms and model training


---
---
# Basic Data Science Workflow Example

```python
# Importing necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
# Data loading and exploration
data = pd.read_csv('data.csv')
print(data.head())
# Simple data visualization
plt.scatter(data['feature'], data['target'])
```

---
layout: center
class: text-center
---

# Summary and Next Steps

- Recap key points from Data Science Basics
- Encourage practice and further study in data analysis
- Highlight resources for learning, like online courses
- Inspire with the idea that data science shapes the future
- Embrace the journey of continuous learning and discovery


