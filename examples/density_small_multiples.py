import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib import density_plot

# Random data for 10 density plots
data_grid = [np.random.normal(loc=i, scale=1.0, size=200) for i in range(10)]

fig, axes = plt.subplots(2, 3, figsize=(15, 6), sharex=False, sharey=False)
axes = axes.flatten()

for i, ax in enumerate(axes):
    row = i // 3
    col = i % 3

    show_ylabels = (col == 0)      # Only first column
    show_xlabels = (row == 1)      # Only bottom row

    density_plot(data_grid[i],
                 ax=ax,
                 show_xlabels=show_xlabels,
                 show_ylabels=show_ylabels,
                 max_ticks=4)
                 
    ax.tick_params(axis='both', labelsize=8)

plt.show()

