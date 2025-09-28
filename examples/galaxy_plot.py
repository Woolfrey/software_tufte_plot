import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib import add_min_max_colorbar, galaxy_plot  # adjust import if necessary

# Generate random galaxy data
n_points = 10000

# x and y positions
x = np.random.uniform(low=-1.0, high=1.0, size=n_points)
y = np.random.uniform(low=-1.0, high=1.0, size=n_points)
z = np.random.uniform(low= 0.0, high=1.0, size=n_points)

# Create plot
ax, im = galaxy_plot(x, y, z,
                     nx_bins=100,
                     ny_bins=100,
                     show_xlabels=True,
                     show_ylabels=True)

cbar = add_min_max_colorbar(im, ax=ax, label='Value')
plt.tight_layout()
plt.show()
