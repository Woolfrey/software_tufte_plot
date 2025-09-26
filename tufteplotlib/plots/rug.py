import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib.styles import apply_tufte_style
from tufteplotlib.utils import _data_min_max

def rug_plot(x, y, ax=None, color='black', alpha=1.0, margin=0.05,
             show_labels=False, tick_length=10, tick_width=1.0, label_offset=0.02):

    if ax is None:
        fig, ax = plt.subplots(figsize=(5*1.618, 5))

    x = np.asarray(x)
    y = np.asarray(y)

    # Scatter points
    ax.scatter(x, y, color=color, alpha=alpha)

    # Compute min/max
    xmin, xmax = _data_min_max(x)
    ymin, ymax = _data_min_max(y)
    x_range = xmax - xmin
    y_range = ymax - ymin

    # Set limits with small margin
    ax.set_xlim(xmin - margin*x_range, xmax + margin*x_range)
    ax.set_ylim(ymin - margin*y_range, ymax + margin*y_range)

    # Apply Tufte style
    apply_tufte_style(ax)

    # Hide all spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Set ticks at all data points (barcode effect)
    ax.set_xticks(x)
    ax.set_yticks(y)
    ax.set_xticklabels([''] * len(x))
    ax.set_yticklabels([''] * len(y))

    # Customize tick appearance
    ax.tick_params(axis='x', length=tick_length, width=tick_width, colors=color)
    ax.tick_params(axis='y', length=tick_length, width=tick_width, colors=color)
    

    # x-axis labels
    x_vals = [np.min(x), np.median(x), np.max(x)]

    for val in x_vals:
        # Optionally snap to nearest actual data point for alignment
        nearest = x[np.argmin(np.abs(x - val))]
        ax.text(nearest, ymin - 0.12 * y_range, f"{val:.2f}",
                ha='center', va='top', color='black', fontsize=10)
                
    # y-axis labels: min, median, max
    y_vals = [np.min(y), np.median(y), np.max(y)]

    for val in y_vals:
        # Snap to nearest actual data point for alignment
        nearest = y[np.argmin(np.abs(y - val))]
        ax.text(xmin - 0.1 * x_range, nearest, f"{val:.2f}",
                ha='right', va='center', color='black', fontsize=10)

    return ax
