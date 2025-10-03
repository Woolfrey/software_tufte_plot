import numpy as np
import matplotlib.pyplot as plt
from .bar import bar_chart

def pareto_chart(categories, quantities, ax=None):
    """
    Horizontal Pareto-style chart with cumulative % on the right y-axis.

    Parameters
    ----------
    categories : list-like
        Category names.
    quantities : array-like
        Values for each category.
    ax : matplotlib.axes.Axes, optional
        Axis to plot on. If None, a new figure is created.

    Returns
    -------
    fig : matplotlib.figure.Figure
    ax_list : list of matplotlib.axes.Axes
        [ax_bar, ax_cumulative]
    """
    # Convert to numpy arrays
    categories = np.asarray(categories)
    quantities = np.asarray(quantities)

    # Sort descending
    order = np.argsort(quantities)[::-1]
    categories_sorted = categories[order]
    quantities_sorted = quantities[order]

    # Create figure/axis if not provided
    if ax is None:
        fig, ax_bar = plt.subplots(figsize=(4 * 1.618, 4))
    else:
        fig = ax.figure
        ax_bar = ax

    # Draw horizontal bars using your custom bar_chart
    bar_chart(categories_sorted, quantities_sorted, ax=ax_bar)
    
    # Compute cumulative percentages
    cum_percent = np.cumsum(quantities_sorted) / np.sum(quantities_sorted) * 100

    # Create secondary y-axis for cumulative %
    ax_cum = ax_bar.twinx()
    ax_cum.set_ylim(ax_bar.get_ylim())  # match bar positions
    ax_cum.set_yticks(np.arange(len(categories_sorted)))
    ax_cum.set_yticklabels([f"{p:.2f}%" for p in cum_percent])
    ax_cum.tick_params(axis='y', length=0, pad=25)
    ax_cum.spines['left'].set_visible(False)
    ax_cum.spines['right'].set_visible(False)
    ax_cum.spines['bottom'].set_visible(False)
    
    return fig, [ax_bar, ax_cum]

####################################################################################################
#                                          Test / example code                                     #
####################################################################################################
def main():

    categories = ["Sneed's", "Costington's", "Try'n'Save", "Shøp"]
    
    np.random.seed()
    
    quantities = np.random.rand(len(categories)) * 20  # float values
    
    fig, ax = pareto_chart(categories, quantities)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()

