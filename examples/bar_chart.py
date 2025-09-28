import matplotlib.pyplot as plt
import numpy as np
from tufteplotlib import bar_chart

# Keep Elderberries, add some weird real fruits
categories = ["Satiety",
              "Triumvirate",
              "Gourmand",
              "Machiavellian",
              "Boudoir"]

# Random integer values for each fruit
np.random.seed()  # Randomize every run
values = np.random.randint(3, 20, size=len(categories))

# Create Tufte-style bar chart
ax = bar_chart(
    categories,
    values,
    show_labels=True  # Show value labels above bars
)

plt.show()
