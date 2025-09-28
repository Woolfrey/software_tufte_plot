import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib.styles import apply_tufte_style
from tufteplotlib.utils import _intermediate_ticks

def pareto_chart(categories, values, *,
                 alpha=1.0,
                 ax=None,
                 bar_width=0.6,
                 bar_color=[0.4, 0.4, 0.4],
                 line_color=[0.0, 0.0, 0.0],
                 dot_size=40,
                 line_width=1.5,
                 max_ticks=5,
                 show_labels=True,
                 x_label_pad=0):
    """
    Create a Tufte-style Pareto chart:
    - Bars represent raw values (sorted descending)
    - Cumulative percentage line with dots
    - Minimalist style with manual tick labels

    Parameters
    ----------
    alpha : float, default=1.0
        Bar transparency.
    ax : matplotlib.axes.Axes, optional
        Axes object to draw the chart on. If None, a new figure is created.
    bar_width : float, default=0.6
        Width of bars.
    categories : list-like
        Names of the categories.
    color : str or list/tuple, default=[0.5, 0.5, 0.5]
        Bar color.
    dot_size : float, default=40
        Size of dots on cumulative line.
    line_width : float, default=1.5
        Width of cumulative line.
    max_ticks : int, default=5
        Approximate number of interior y-axis ticks.
    show_labels : bool, default=True
        Whether to show horizontal grid line labels.
    values : array-like
        Bar heights.
    x_label_pad : float, default=0
        Padding for x-axis labels.

    Returns
    -------
    ax : matplotlib.axes.Axes
        The Axes containing the Pareto chart.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(5*1.618, 5))

    categories = np.asarray(categories)
    values = np.asarray(values)

    # Sort descending
    sort_idx = np.argsort(values)[::-1]
    categories = categories[sort_idx]
    values = values[sort_idx]
    x_pos = np.arange(len(categories))

    # Draw bars (always from 0)
    ax.bar(x_pos, values, color=bar_color, alpha=alpha, width=bar_width, bottom=0)

    # Compute cumulative percentages
    cumulative = np.cumsum(values)
    cumulative_pct = 100 * cumulative / cumulative[-1]

    # Overlay cumulative line with dots
    ax2 = ax.twinx()
    ax2.plot(x_pos, cumulative_pct, color=line_color, linewidth=line_width, alpha=0.8, zorder=3)
    ax2.scatter(x_pos, cumulative_pct, color=line_color, s=dot_size,
                edgecolor='white', linewidth=1.0, zorder=4)

    # Percentage labels above dots
    for i, pct in enumerate(cumulative_pct):
        ax2.text(x_pos[i], pct + 1, f"{pct:.1f}%", ha='center', va='bottom', fontsize=9, color=line_color)

    # Left y-axis: bars
    ymin, ymax = values.min(), values.max()
    y_ticks = _intermediate_ticks(ymin, ymax, max_ticks=max_ticks)

    # Ensure smallest bar value is included if below first tick
    if ymin < y_ticks[0]:
        y_ticks = np.insert(y_ticks, 0, ymin)

    ax.set_ylim(0, ymax + 5)
    ax.set_yticks([])

    # Draw horizontal lines and manual labels
    for i, yt in enumerate(y_ticks):
        if i == 0 and yt == ymin and yt != 0:
            # Label smallest bar value, no line
            if show_labels:
                ax.text(-0.6, yt, f"{yt:.0f}", ha='left', va='center', fontsize=9, color='black')
        else:
            ax.hlines(yt, -0.5, len(categories) - 0.5, color='white', linewidth=1)
            if show_labels:
                ax.text(-0.6, yt, f"{yt:.0f}", ha='left', va='center', fontsize=9, color='black')

    # X-axis: remove ticks, manually place labels
    ax.tick_params(axis='x', length=0)
    for i, label in enumerate(categories):
        ax.text(i, -0.02 * ymax, label, ha='center', va='top', rotation=0.0, fontsize=9)

    # Bottom spine limited to first and last bar
    ax.spines['bottom'].set_bounds(x_pos[0] - bar_width / 2, x_pos[-1] + bar_width / 2)
    ax.spines['bottom'].set_color(bar_color)

    # Remove right y-axis ticks
    ax2.set_yticks([])
    ax2.set_xticks([])

    # Set ax2 limits so the line starts higher up
    ax2.set_ylim(-cumulative_pct[0], 105)

    # Apply Tufte style
    apply_tufte_style(ax)
    apply_tufte_style(ax2)
    
     # Hide other spines
    for spine_name, spine in ax.spines.items():
        if spine_name != 'bottom':
            spine.set_visible(False)
    for spine in ax2.spines.values():
        spine.set_visible(False)

    plt.tight_layout()
    return ax
