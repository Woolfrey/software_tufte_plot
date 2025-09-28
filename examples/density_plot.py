import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib import density_plot  # adjust import if necessary

# Generate random data
data = np.random.normal(loc=0, scale=1, size=500)

# Create density plot
ax = density_plot(
    data,
    show_xlabels=True,
    show_ylabels=True,
    tick_width=1.0,
    tick_length=5,
    max_ticks=5
)

ax.set_xlabel("Value")
ax.set_ylabel("Density")

plt.show()
