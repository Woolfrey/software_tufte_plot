import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib.styles import apply_tufte_style

####################################################################################################
#                                         Core function                                            #
####################################################################################################
def rug_plot(x, y, *,
             alpha=1.0,
             ax=None,
             color='black',
             label_offset=0.02,
             margin=0.05,
             show_labels=True,
             tick_length=10.0,
             tick_width=1.0):
    """
    Create a Tufte-style rug plot with minimal ink.

    Parameters
    ----------
    x, y : array-like
        Coordinates of the rug ticks.
    alpha : float
        Transparency of the ticks.
    ax : matplotlib.axes.Axes, optional
        Axes to draw on.
    color : str
        Tick color.
    label_offset : float
        Fractional offset for min/median/max labels.
    margin : float
        Fractional margin around data.
    show_labels : bool
        Whether to show min/median/max labels.
    tick_length : float
        Length of the rug "tassels".
    tick_width : float
        Width of the rug "tassels".

    Returns
    -------
    ax : matplotlib.axes.Axes
    """

    if ax is None:
        fig, ax = plt.subplots(figsize=(5*1.618, 5))

    x = np.asarray(x)
    y = np.asarray(y)

    # Scatter points
    ax.scatter(x, y, color=color, alpha=alpha)

    # Compute min/max
    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()
    x_range = xmax - xmin
    y_range = ymax - ymin

    # Set limits with small margin
    ax.set_xlim(xmin - margin*x_range, xmax + margin*x_range)
    ax.set_ylim(ymin - margin*y_range, ymax + margin*y_range)

    # Apply Tufte style
    apply_tufte_style(ax)

    # Hide all spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Barcode ticks
    ax.set_xticks(x)
    ax.set_yticks(y)
    ax.set_xticklabels([''] * len(x))
    ax.set_yticklabels([''] * len(y))
    ax.tick_params(axis='x', length=tick_length, width=tick_width, colors=color)
    ax.tick_params(axis='y', length=tick_length, width=tick_width, colors=color)

    # Min/median/max labels
    if show_labels:
        for val in [xmin, np.median(x), xmax]:
            nearest = x[np.argmin(np.abs(x - val))]
            ax.text(nearest, ymin - 0.12*y_range, f"{val:.2f}",
                    ha='center', va='top', fontsize=10, color='black')
        for val in [ymin, np.median(y), ymax]:
            nearest = y[np.argmin(np.abs(y - val))]
            ax.text(xmin - 0.08*x_range, nearest, f"{val:.2f}",
                    ha='right', va='center', fontsize=10, color='black')
                    
    return ax
    
####################################################################################################
#                                          Test / example code                                     #
####################################################################################################     
def main():

    x = np.random.normal(loc=0, scale=1, size=200)
    y = np.random.normal(loc=0, scale=1, size=200)

    ax = rug_plot(x, y, color='black', alpha=1.0)

    ax.set_xlabel("Gastronomic Capacity", labelpad=20)
    ax.set_ylabel("Satiety", labelpad=30)
    plt.tight_layout()

    plt.show()

if __name__ == "__main__":
    main()
