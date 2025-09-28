import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib.styles import apply_tufte_style
from tufteplotlib.utils import _intermediate_ticks

def scatter_plot(x, y, ax=None, color='black', s=20, alpha=1.0, margin=0.05, max_ticks=5, **kwargs):
    """
    Tufte-style scatter plot with exact spines and nicely rounded, equispaced ticks.

    Parameters:
        x, y : list or array-like data
        ax : matplotlib Axes (optional)
        color : marker color
        s : marker size
        alpha : marker transparency
        margin : fraction of extra space around min/max for axes
        max_ticks : approximate number of interior ticks per axis
        **kwargs : extra arguments passed to ax.scatter

    Returns:
        ax : matplotlib Axes with the plot
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(5*1.618, 5))
             
    x = np.asarray(x)
    y = np.asarray(y)

    # Plot scatter points
    ax.scatter(x, y, color=color, s=s, alpha=alpha, **kwargs)

    # Compute exact min/max
    xmin = x.min()
    xmax = x.max()
    ymin = y.min()
    ymax = y.max()

    # Add small margin for axes limits
    x_range = xmax - xmin
    y_range = ymax - ymin
    ax.set_xlim(xmin - margin * x_range, xmax + margin * x_range)
    ax.set_ylim(ymin - margin * y_range, ymax + margin * y_range)

    # Apply Tufte minimal style
    apply_tufte_style(ax)

    # Force spines to exactly match true min/max
    ax.spines['bottom'].set_bounds(xmin, xmax)
    ax.spines['left'].set_bounds(ymin, ymax)

    # Compute ticks including min/max and rounded interior ticks
    ax.set_xticks(_intermediate_ticks(xmin, xmax, max_ticks=max_ticks))
    ax.set_yticks(_intermediate_ticks(ymin, ymax, max_ticks=max_ticks))

    return ax

