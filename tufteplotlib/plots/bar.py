import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib.styles import apply_tufte_style
from tufteplotlib.utils import _intermediate_ticks

####################################################################################################
#                                         Core function                                            #
####################################################################################################

def bar_chart(categories, quantities, ax=None, color=None):
    """
    Plot quantities across nominal categories as horizontal bars,
    sorted descending (largest at top).

    Parameters
    ----------
    categories : array-like
        Sequence of category labels for the y-axis.
    quantities : array-like
        Widths of the bars corresponding to each category.
    ax : matplotlib.axes.Axes, optional
        Axis to draw on. If None, a new figure is created.
    color : color, optional
        Bar fill colour. Defaults to [0.4, 0.4, 0.4].

    Returns
    -------
    fig : matplotlib.figure.Figure
    ax  : matplotlib.axes.Axes
    """
    # Convert to numpy arrays
    categories = np.asarray(categories)
    quantities = np.asarray(quantities)

    # Sort descending (largest at top)
    order      = np.argsort(quantities)[::-1]
    categories = categories[order]
    quantities = quantities[order]

    # Create figure/axis if not provided
    if ax is None:
        fig, ax = plt.subplots(figsize=(4 * 1.618, 4))
    else:
        fig = ax.figure

    color = color if color is not None else [0.4, 0.4, 0.4]
    y_pos = np.arange(len(categories))

    ax.set_ylim(-0.35, len(categories) - 0.65)
    ax.barh(y_pos, quantities, color=color)

    # Set x-axis limits
    xmin = 0
    xmax = quantities.max()
    ax.set_xlim(xmin, xmax)

    # Compute x-axis ticks (exclude zero)
    x_ticks = [xt for xt in _intermediate_ticks(xmin, xmax, max_ticks=5, edge_fraction=0.05)
               if xt != 0.0]

    if np.all(np.array(x_ticks) % 1 == 0):
        xfmt = "{:.0f}"
    else:
        xfmt = "{:.2f}"

    min_val       = quantities.min()
    add_min_label = x_ticks and (min_val < x_ticks[0])

    # Hide default x ticks and invert so largest is at top
    ax.set_xticks([])
    ax.invert_yaxis()

    y_min, y_max = ax.get_ylim()

    # Draw x-axis labels and white vertical gridlines
    for xt in x_ticks:
        ax.text(xt, -0.03, xfmt.format(xt),
                transform  = ax.get_xaxis_transform(),
                va='top', ha='center', color='black', fontsize=10)
        ax.vlines(xt, y_min, y_max, color='white', linewidth=1)

    if add_min_label:
        ax.text(min_val, -0.03, xfmt.format(min_val),
                transform  = ax.get_xaxis_transform(),
                va='top', ha='center', color='black', fontsize=10)

    # Set y-axis category labels
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories)

    # Spines
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_bounds(y_min, y_max)
    ax.spines['left'].set_color([0.4, 0.4, 0.4])

    apply_tufte_style(ax)

    return fig, ax

####################################################################################################
#                                          Test / example code                                     #
####################################################################################################

def main():
    categories = ["Satiety", "Triumvirate", "Gourmand", "Machiavellian", "Boudoir"]

    quantities = np.random.randint(3, 20, size=len(categories))

    fig, ax = bar_chart(categories, quantities)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
