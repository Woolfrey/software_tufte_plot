import matplotlib.pyplot as plt
from tufteplotlib.styles import apply_tufte_style
from tufteplotlib.utils import _intermediate_ticks
import numpy as np
from .line import line_plot  # assuming line_plot is in the same package

def time_series(x, y, *,
                alpha=1.0,
                ax=None,
                color='black',
                line_width=1.0,
                margin=0.05,
                max_ticks=5,
                s=20,
                show_dots=True,
                **kwargs):
    """
    Tufte-style time series plot.

    Parameters
    ----------
    x : array-like
        x-values (time or sequential indices).
    y : array-like
        y-values (measurements).
    alpha : float, optional
        Transparency of line and dots.
    ax : matplotlib.axes.Axes, optional
        Axes to draw on. Creates new figure/axes if None.
    color : str, optional
        Line and dot color.
    line_width : float, optional
        Width of the connecting line.
    margin : float, optional
        Fractional margin around data for axes limits.
    max_ticks : int, optional
        Approximate number of y-axis ticks.
    s : float, optional
        Marker size for dots.
    show_dots : bool, optional
        Whether to draw markers at each data point.
    **kwargs : additional keyword arguments passed to line_plot.

    Returns
    -------
    ax : matplotlib.axes.Axes
        Axes containing the time series plot.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(5*1.618, 2.5))

    # Base line plot
    ax = line_plot(x, y,
                   alpha=alpha,
                   ax=ax,
                   color=color,
                   line_width=line_width,
                   margin=margin,
                   max_ticks=max_ticks,
                   **kwargs)

    # Remove all spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    # X-axis ticks at each data point
    ax.set_xticks(x)

    # Optionally overlay dots
    if show_dots:
        ax.scatter(x, y, s=s, color=color, alpha=alpha, zorder=3)

    # Y-axis ticks next to labels
    ymin, ymax = y.min(), y.max()
    y_ticks = _intermediate_ticks(ymin, ymax, max_ticks=max_ticks)
    ax.set_yticks(y_ticks)
    ax.tick_params(axis='y', which='both', length=5, direction='out', color='black', width=1, pad=5)

    # Hide x-axis labels if desired (can be handled by caller)
    ax.tick_params(axis='x', which='both', length=5)

    return ax
