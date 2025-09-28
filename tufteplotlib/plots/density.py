import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib.styles import apply_tufte_style
from tufteplotlib.utils import _intermediate_ticks
from scipy.stats import gaussian_kde

def density_plot(data, *,
                 ax=None,
                 alpha=0.75,
                 color=[0.0, 0.0, 0.0],
                 show_xlabels=False,
                 show_ylabels=False,
                 tick_width=1.0,
                 tick_length=5,
                 max_ticks=5):
    """
    Create a Tufte-style density plot with shaded area under the curve
    and optional nicely spaced axis labels.

    Parameters
    ----------
    data : array-like
        1D array of numeric values.
    ax : matplotlib.axes.Axes, optional
        Axes object to draw on. If None, a new figure is created.
    alpha : float, optional
        Line/area transparency.
    color : str or list, optional
        Line and fill color.
    show_xlabels : bool, optional
        Whether to show x-axis labels and ticks.
    show_ylabels : bool, optional
        Whether to show y-axis labels and ticks.
    tick_width : float, optional
        Width of axis ticks (points).
    tick_length : float, optional
        Length of axis ticks (points).
    max_ticks : int, optional
        Maximum number of x- and y-axis tick intervals.

    Returns
    -------
    ax : matplotlib.axes.Axes
    """

    if ax is None:
        fig, ax = plt.subplots(figsize=(5*1.618, 5))

    data = np.asarray(data)
    kde = gaussian_kde(data)
    x_vals = np.linspace(data.min(), data.max(), 500)
    y_vals = kde(x_vals)

    # Plot shaded area
    ax.fill_between(x_vals, 0, y_vals, color=color, alpha=alpha)

    # Y-axis
    ymin, ymax = 0, y_vals.max()
    ax.set_ylim(ymin, ymax)
    if show_ylabels:
        y_ticks = np.linspace(ymin, ymax, min(max_ticks, 5))
        ax.set_yticks(y_ticks)
        ax.set_yticklabels([f"{ytick:.2f}" for ytick in y_ticks])
        ax.tick_params(axis='y', length=tick_length, width=tick_width, colors=color)
    else:
        ax.set_yticks([])
        ax.set_yticklabels([])
        ax.spines['left'].set_visible(False)

    # X-axis
    if show_xlabels:
        x_labels = [np.min(data), np.median(data), np.max(data)]
        ax.set_xticks(x_labels)
        ax.set_xticklabels([f"{val:.2f}" for val in x_labels])
        ax.tick_params(axis='x', length=tick_length, width=tick_width, colors=color)
    else:
        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.spines['bottom'].set_visible(False)

    # Apply Tufte style
    apply_tufte_style(ax)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    return ax
