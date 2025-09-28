import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib.styles import apply_tufte_style
from tufteplotlib.utils import _intermediate_ticks

def bar_chart(categories, values, *,
              alpha=1.0,
              ax=None,
              bar_width=0.6,
              color=[0.4, 0.4, 0.4],
              label_angle=30,
              max_ticks=5,
              show_labels=True):
    """
    Create a Tufte-style bar chart with minimal ink, horizontal grid lines,
    and custom labels. Includes the smallest value on the y-axis if it is
    smaller than the first default tick.

    Parameters
    ----------
    categories : array-like
        Sequence of category labels for the x-axis.
    values : array-like
        Heights of the bars corresponding to each category.
    alpha : float, optional (default=1.0)
        Transparency of the bars (0 = fully transparent, 1 = fully opaque).
    ax : matplotlib.axes.Axes, optional
        Axes object to draw on. If None, a new figure and axes are created.
    bar_width : float, optional (default=0.6)
        Width of the bars.
    color : list or tuple, optional (default=[0.6, 0.6, 0.6])
        RGB values for bar color.
    label_angle : float, optional (default=30)
        Rotation angle of the x-axis labels.
    max_ticks : int, optional (default=5)
        Maximum number of y-axis tick intervals to draw.
    show_labels : bool, optional (default=True)
        Whether to show y-axis labels.

    Returns
    -------
    ax : matplotlib.axes.Axes
        The matplotlib axes with the bar chart.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(4*1.618, 4))

    categories = np.asarray(categories)
    values = np.asarray(values)
    x_pos = np.arange(len(categories))

    # Draw bars
    ax.bar(x_pos, values, color=color, alpha=alpha, width=bar_width)

    # Set y-axis limits
    ymin = 0
    ymax = max(values)
    ax.set_ylim(ymin, ymax)

    # Compute y-axis ticks
    y_ticks = [yt for yt in _intermediate_ticks(ymin, ymax, max_ticks=max_ticks) if yt != 0.0]

    # Decide if we need to add the smallest value
    min_val = values.min()
    add_min_label = False
    if y_ticks and min_val < y_ticks[0]:
        add_min_label = True

    # Hide default ticks
    ax.set_yticks([])

    # Draw y-axis labels and horizontal lines
    if show_labels:
        for ytick in y_ticks:
            ax.text(-0.5, ytick, f"{ytick:.2f}",
                    va='center', ha='right', color='black', fontsize=10)
            ax.hlines(ytick, -0.5, len(categories)-0.5,
                      color='white', linewidth=1)

        # Label smallest value if below first tick (no line)
        if add_min_label:
            ax.text(-0.5, min_val, f"{min_val:.2f}",
                    va='center', ha='right', color='black', fontsize=10)

    # Set x-axis labels
    ax.set_xticks(x_pos)
    
    ax.set_xticklabels(categories, rotation=label_angle, ha='right')

    # Hide left spine
    ax.spines['left'].set_visible(False)

    # Set bottom spine to span only the bars
    ax.spines['bottom'].set_bounds(x_pos[0]-bar_width/2,
                                   x_pos[-1]+bar_width/2)

    # Apply Tufte style (removes top/right spines)
    apply_tufte_style(ax)
    
    plt.tight_layout() # Adjust

    return ax
