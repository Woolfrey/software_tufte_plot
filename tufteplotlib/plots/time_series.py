import matplotlib.pyplot as plt
from tufteplotlib.styles import apply_tufte_style
from tufteplotlib.utils import _data_min_max, _intermediate_ticks

def time_series(t, y, ax=None, color='black', s=20, alpha=1.0,
                line_width=1.0, margin=0.05, max_ticks=5,
                show_dots=True, outline_scale=2.5, **kwargs):
    """
    Tufte-style time series plot with exact spines and nicely rounded, equispaced ticks.

    Parameters:
        t : array-like, time or x-values
        y : array-like, measurements or y-values
        ax : matplotlib Axes (optional)
        color : line and marker color
        s : marker size (points^2, as in matplotlib scatter)
        alpha : marker/line transparency
        line_width : width of the line connecting points
        margin : fraction of extra space around min/max for axes
        max_ticks : approximate number of interior ticks per axis
        show_dots : whether to draw markers at each point
        outline_scale : factor to scale up the white outline size
        **kwargs : extra arguments passed to ax.plot

    Returns:
        ax : matplotlib Axes with the plot
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(5*1.618, 2.5))

    # Draw line connecting points
    ax.plot(t, y, color=color, linewidth=line_width, alpha=alpha, **kwargs)

    # Optionally draw markers with white halo
    if show_dots:
        # White "outline" layer underneath
        ax.scatter(t, y, s=s * outline_scale, facecolors='white',
                   edgecolors='none', zorder=2)
        # Main colored dots on top
        ax.scatter(t, y, s=s, facecolors=color, edgecolors='none',
                   alpha=alpha, zorder=3)

    # Compute exact min/max
    tmin, tmax = _data_min_max(t)
    ymin, ymax = _data_min_max(y)
    t_range = tmax - tmin
    y_range = ymax - ymin

    # Set axis limits with small margin
    ax.set_xlim(tmin - margin*t_range, tmax + margin*t_range)
    ax.set_ylim(ymin - margin*y_range, ymax + margin*y_range)

    # Apply Tufte-style minimal aesthetics
    apply_tufte_style(ax)

    # Force spines to exactly match min/max
    ax.spines['bottom'].set_bounds(tmin, tmax)
    ax.spines['left'].set_bounds(ymin, ymax)

    # Set nicely rounded ticks including exact min/max
    ax.set_xticks(_intermediate_ticks(tmin, tmax, max_ticks=max_ticks))
    ax.set_yticks(_intermediate_ticks(ymin, ymax, max_ticks=max_ticks))

    return ax
