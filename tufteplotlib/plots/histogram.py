# tufteplotlib/plots/histogram.py
import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib.styles import apply_tufte_style
from tufteplotlib.utils import _intermediate_ticks

def histogram_plot(data, bins=10, *,
                   alpha=1.0,
                   ax=None,
                   color=[0.4, 0.4, 0.4],
                   edge_color="white",
                   edge_width=0.5,
                   max_ticks=5,
                   show_labels=True):
    """
    Tufte-style histogram using matplotlib's hist function.

    Features:
    - Bars with thin outlines
    - White horizontal lines for y-axis ticks (except min)
    - Custom y-axis labels (min, intermediate, max)
    - Default x-axis tick positions
    - Minimal spines and Tufte styling

    Parameters
    ----------
    data : array-like
        Input data to histogram.
    bins : int or sequence, optional
        Number of bins or explicit bin edges. Default 10.
    alpha : float, optional
        Bar transparency. Default 1.0.
    ax : matplotlib.axes.Axes, optional
        Axes to draw on. Creates new figure if None.
    color : list or tuple, optional
        Fill color of bars. Default muted gray.
    edge_color : color-like, optional
        Outline color of bars. Default white.
    edge_width : float, optional
        Line width of bar outlines. Default 0.5.
    max_ticks : int, optional
        Maximum number of y-axis ticks (including min/max). Default 5.
    show_labels : bool, optional
        Whether to show y-axis labels. Default True.

    Returns
    -------
    ax : matplotlib.axes.Axes
        Axes containing the histogram.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(4*1.618, 4))

    # Compute histogram
    counts, bin_edges, patches = ax.hist(
        data,
        bins=bins,
        alpha=alpha,
        color=color,
        edgecolor=edge_color,
        linewidth=edge_width,
        rwidth=0.6
    )

    # Y-axis: custom labels
    ymin, ymax = counts.min(), counts.max()
    y_ticks = _intermediate_ticks(ymin, ymax, max_ticks=max_ticks)
    
    # Ensure min and max are included
    if ymin not in y_ticks:
        y_ticks = np.insert(y_ticks, 0, ymin)
    if ymax not in y_ticks:
        y_ticks = np.append(y_ticks, ymax)

    if show_labels:
        ax.set_yticks(y_ticks)
        ax.set_yticklabels([f"{int(yt)}" for yt in y_ticks])
        # Draw horizontal lines for all except the first (min) tick
        for yt in y_ticks[1:]:
            ax.hlines(yt, xmin=bin_edges[0], xmax=bin_edges[-1], color='white', linewidth=1)
    else:
        ax.set_yticks([])
        ax.set_yticklabels([])

    # X-axis: default ticks
    ax.tick_params(axis='x', rotation=0)

    # Bottom spine: span from first to last bar
    ax.spines['bottom'].set_bounds(bin_edges[0], bin_edges[-1])
    # Hide left, top, right spines
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Apply Tufte style
    apply_tufte_style(ax)

    return ax
