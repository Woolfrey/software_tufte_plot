import matplotlib.pyplot as plt
import numpy as np
from tufteplotlib import pareto_chart  # adjust import if necessary

# Example categories
categories = [
    "Jimbo",
    "Nelson",
    "Dolph",
    "Kearny",
    "Kearny Jnr."
]

# Random values for each category
np.random.seed()  # random each run
values = np.random.randint(1, 20, size=len(categories))

# Create Pareto chart
ax = pareto_chart(
    categories,
    values,
    alpha=0.9,
    bar_width=0.6,
    show_labels=True,
    max_ticks=5
)

plt.show()
