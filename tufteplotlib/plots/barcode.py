import matplotlib.pyplot as plt
import numpy as np
from tufteplotlib.styles import apply_tufte_style
from tufteplotlib.utils import _intermediate_ticks

####################################################################################################
#                                         Core function                                            #
####################################################################################################
def barcode_plot(categories, values, *,
                 alpha=0.5,
                 ax=None,
                 color='black',
                 line_thickness=2.0,
                 line_width=0.4,
                 show_labels=False,
                 x_label_pad=5):
    """
    Create a Tufte-style barcode plot: horizontal lines for each data point in 
    each nominal category with minimal ink.

    Parameters
    ----------
    categories : array-like
        Sequence of categorical labels for the x-axis.
    values : array-like
        Numerical data corresponding to each category.
    alpha : float, optional (default=0.5)
        Transparency of the lines (0 = fully transparent, 1 = fully opaque).
    ax : matplotlib.axes.Axes, optional
        Axes object to draw on. If None, a new figure and axes are created.
    color : str, optional (default='black')
        Color of the barcode lines.
    line_thickness : float, optional (default=2.0)
        Thickness of each barcode line.
    line_width : float, optional (default=0.4)
        Horizontal span of each line in axis units.
    show_labels : bool, optional (default=False)
        Whether to show min/intermediate/max y-axis labels.
    x_label_pad : float, optional (default=5)
        Padding (in points) for x-axis labels.

    Returns
    -------
    ax : matplotlib.axes.Axes
        The matplotlib axes containing the barcode plot.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(5*1.618, 5))

    categories = np.asarray(categories)
    values = np.asarray(values)

    # Map categories to numeric positions
    unique_categories = sorted(list(set(categories)))
    cat_to_x = {cat: i for i, cat in enumerate(unique_categories)}
    x_positions = np.array([cat_to_x[cat] for cat in categories])

    # Draw horizontal barcode lines
    for x, y in zip(x_positions, values):
        ax.hlines(y, x - line_width/2.0, x + line_width/2.0, color=color, alpha=alpha, linewidth=line_thickness)

    # Compute y-axis limits exactly
    ymin = values.min()
    ymax = values.max()
    ax.set_ylim(ymin, ymax)

    # Set x-axis ticks at category positions with labels
    ax.set_xticks(range(len(unique_categories)))
    ax.set_xticklabels(unique_categories)
    ax.tick_params(axis='x', which='both', length=10, pad=x_label_pad)

    # Hide top, right, and bottom spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Set x-axis ticks (for labels only) and hide tick marks
    ax.set_xticks([])           
    for i, label in enumerate(unique_categories):
        ax.text(i, ymin - 0.05*(ymax-ymin), label, ha='center', va='top', color='black')
        
    # Set nice y-axis ticks (min, intermediate, max)
    y_ticks = _intermediate_ticks(ymin, ymax)
    ax.set_yticks(y_ticks)
    if show_labels:
        ax.set_yticklabels([f"{t:.2f}" for t in y_ticks])
    else:
        ax.set_yticklabels([])

    # Apply Tufte style
    apply_tufte_style(ax)

    return ax
    
####################################################################################################
#                                          Test / example code                                     #
####################################################################################################  
def main():

    params = {
        "Lowenstein": {"mu": 5, "sigma": 3, "n": 50},
        "Zweig": {"mu": 7, "sigma": 1, "n": 50},
        "Sneed": {"mu": 6, "sigma": 2, "n": 50}
    }

    categories = []
    
    values = []

    for cat, p in params.items():
        data = np.random.normal(loc=p["mu"], scale=p["sigma"], size=p["n"])
        categories.extend([cat]*p["n"])
        values.extend(data)

    ax = barcode_plot(categories, values, color='black', alpha=0.7, show_labels=True)
    
    plt.show()

if __name__ == "__main__":
    main()
