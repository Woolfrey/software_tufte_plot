import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib.styles import apply_tufte_style
from tufteplotlib.utils import _intermediate_ticks

####################################################################################################
#                                         Core function                                            #
####################################################################################################
def bar_chart(categories, quantities, ax=None):
    """
    Plot quantities across nominal categories as horizontal bars (categories on the y-axis),
    sorted descending (largest at top).

    Parameters
    ----------
    categories : array-like
        Sequence of category labels for the y-axis.
    quantities : array-like
        Widths of the bars corresponding to each category.
    ax : matplotlib.axes.Axes, optional
        Axis to draw on. If None, a new figure is created.

    Returns
    -------
    fig : matplotlib.figure.Figure
    ax : matplotlib.axes.Axes
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(4*1.618, 4))
    else:
        fig = ax.figure

    categories = np.asarray(categories)
    quantities = np.asarray(quantities)

    # Sort categories by descending quantities (largest first)
    order = np.argsort(quantities)[::-1]
    categories = categories[order]
    quantities = quantities[order]

    y_pos = np.arange(len(categories))
    ax.set_ylim(-0.35, len(categories)-0.65)  # minimal padding

    # Draw horizontal bars with the same minimal color
    ax.barh(y_pos, quantities, color=[0.4, 0.4, 0.4])

    # Set x-axis limits
    xmin = 0
    xmax = max(quantities)
    ax.set_xlim(xmin, xmax)

    # Compute x-axis ticks (exclude zero tick)
    x_ticks = [xt for xt in _intermediate_ticks(xmin, xmax, max_ticks=5, edge_fraction=0.05) if xt != 0.0]

    # Decide if we need to add the smallest value
    min_val = quantities.min()
    add_min_label = x_ticks and (min_val < x_ticks[0])

    # Hide default x ticks
    ax.set_xticks([])

    # Put the largest category at the top
    ax.invert_yaxis()

    # Get y-limits *after* inverting, so we can span the whole axis
    y_min, y_max = ax.get_ylim()

    # Draw x-axis labels + vertical helper lines
    for xtick in x_ticks:
        ax.text(xtick, -0.03, f"{xtick:.2f}",
                transform=ax.get_xaxis_transform(),
                va='top', ha='center', color='black', fontsize=10)
        ax.vlines(xtick, y_min, y_max, color='white', linewidth=1)

    if add_min_label:
        ax.text(min_val, -0.03, f"{min_val:.2f}",
                transform=ax.get_xaxis_transform(),
                va='top', ha='center', color='black', fontsize=10)

    # Set y-axis labels (categories)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories)

    # Hide bottom spine and make left spine span full height
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_bounds(y_min, y_max)
    ax.spines['left'].set_color([0.4, 0.4, 0.4])

    # Apply Tufte style (removes top/right spines etc.)
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
