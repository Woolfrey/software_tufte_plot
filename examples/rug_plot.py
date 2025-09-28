import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib import rug_plot

# Random data (new each run)
x = np.random.normal(loc=0, scale=1, size=200)
y = np.random.normal(loc=0, scale=1, size=200)

# Generate the plot
ax = rug_plot(x, y, color='black', alpha=1.0)

# Add labels
ax.set_xlabel("Gastronomic Capacity", labelpad=20)
ax.set_ylabel("Satiety", labelpad=30)
plt.tight_layout()

plt.show()
