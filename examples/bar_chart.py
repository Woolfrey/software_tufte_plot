import matplotlib.pyplot as plt
import numpy as np
from tufteplotlib import bar_chart

# Categories
categories = ["Satiety",
              "Triumvirate",
              "Gourmand",
              "Machiavellian",
              "Boudoir"]

# Random integer values
values = np.random.randint(3, 20, size=len(categories))

# Left: Tufte-style bar chart
bar_chart(categories, values, show_labels=True)

plt.show()

