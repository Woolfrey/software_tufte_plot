import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib.styles import apply_tufte_style
from tufteplotlib.utils import _intermediate_ticks

####################################################################################################
#                                         Core function                                            #
####################################################################################################

def bar_base(categories, quantities, ax=None, color=None, horizontal=True, sort='descending'):
    """
    Private base function for bar-style charts.

    Parameters
    ----------
    categories : array-like
        Sequence of category labels.
    quantities : array-like
        Values for each category.
    ax : matplotlib.axes.Axes, optional
        Axis to draw on. If None, a new figure is created.
    color : color, optional
        Bar fill colour. Defaults to [0.4, 0.4, 0.4].
    horizontal : bool, optional
        If True, draws horizontal bars (categories on y-axis).
        If False, draws vertical bars (categories on x-axis). Default is True.
    sort : str, optional
        Sort order for categories. One of:
        'descending'   : largest first (top or left).
        'ascending'    : smallest first.
        'alphabetical' : alphabetical by category label.
        None           : no sorting, preserve input order.

    Returns
    -------
    fig : matplotlib.figure.Figure
    ax  : matplotlib.axes.Axes
    """
    # Convert to numpy arrays
    categories = np.asarray(categories)
    quantities = np.asarray(quantities)

    # Sort categories
    if sort == 'descending':
        order      = np.argsort(quantities)[::-1]
    elif sort == 'ascending':
        order      = np.argsort(quantities)
    elif sort == 'alphabetical':
        order      = np.argsort(categories)
    else:
        order      = np.arange(len(categories))

    categories = categories[order]
    quantities = quantities[order]

    # Create figure/axis if not provided
    if ax is None:
        fig, ax = plt.subplots(figsize=(4 * 1.618, 4))
    else:
        fig = ax.figure

    color  = color if color is not None else [0.4, 0.4, 0.4]
    pos    = np.arange(len(categories))
    qmin   = 0
    qmax   = quantities.max()

    # Compute tick positions and format
    q_ticks = [qt for qt in _intermediate_ticks(qmin, qmax, max_ticks=5, edge_fraction=0.05)
               if qt != 0.0]

    if np.all(np.array(q_ticks) % 1 == 0):
        qfmt = "{:.0f}"
    else:
        qfmt = "{:.2f}"

    min_val       = quantities.min()
    add_min_label = q_ticks and (min_val < q_ticks[0])

    if horizontal:
        ax.set_ylim(-0.35, len(categories) - 0.65)
        ax.barh(pos, quantities, color=color)
        ax.set_xlim(qmin, qmax)
        ax.set_xticks([])
        ax.invert_yaxis()

        y_min, y_max = ax.get_ylim()

        # Draw quantity labels and white vertical gridlines
        for qt in q_ticks:
            ax.text(qt, -0.03, qfmt.format(qt),
                    transform   = ax.get_xaxis_transform(),
                    va='top', ha='center', color='black', fontsize=10)
            ax.vlines(qt, y_min, y_max, color='white', linewidth=1)

        if add_min_label:
            ax.text(min_val, -0.03, qfmt.format(min_val),
                    transform   = ax.get_xaxis_transform(),
                    va='top', ha='center', color='black', fontsize=10)

        # Category labels on y-axis
        ax.set_yticks(pos)
        ax.set_yticklabels(categories)

        # Spines
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_bounds(y_min, y_max)
        ax.spines['left'].set_color([0.4, 0.4, 0.4])

    else:
        ax.set_xlim(-0.35, len(categories) - 0.65)
        ax.bar(pos, quantities, color=color)
        ax.set_ylim(qmin, qmax)
        ax.set_yticks([])

        x_min, x_max = ax.get_xlim()

        # Draw quantity labels and white horizontal gridlines
        for qt in q_ticks:
            ax.text(-0.03, qt, qfmt.format(qt),
                    transform   = ax.get_yaxis_transform(),
                    va='center', ha='right', color='black', fontsize=10)
            ax.hlines(qt, x_min, x_max, color='white', linewidth=1)

        if add_min_label:
            ax.text(-0.03, min_val, qfmt.format(min_val),
                    transform   = ax.get_yaxis_transform(),
                    va='center', ha='right', color='black', fontsize=10)

        # Category labels on x-axis
        ax.set_xticks(pos)
        ax.set_xticklabels(categories)

        # Spines
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_bounds(x_min, x_max)
        ax.spines['bottom'].set_color([0.4, 0.4, 0.4])

    apply_tufte_style(ax)

    return fig, ax
