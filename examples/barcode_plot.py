import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib import barcode_plot

# Example: 3 nominal categories with random data
np.random.seed(42)

categories = []
values = []

for cat in ["A", "B", "C"]:
    # Each category has 20 random points
    data = np.random.normal(loc=np.random.randint(5, 15), scale=2, size=20)
    categories.extend([cat]*len(data))
    values.extend(data)

# Create the barcode plot
ax = barcode_plot(categories, values, color='black', alpha=0.6, show_labels=True)

plt.show()
