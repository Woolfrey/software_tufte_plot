import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib.styles import apply_tufte_style
from tufteplotlib.utils import _intermediate_ticks

####################################################################################################
#                                         Core function                                            #
####################################################################################################
def column_chart(categories, values, ax=None, labels=None, colors=None, yfmt=None, sort='alpha'):
    """
    Plot quantities across nominal categories as stacked bars, automatically formatting y-axis.

    Parameters
    ----------
    categories : array-like
        Sequence of category labels for the x-axis.
    values : array-like
        Heights of the columns. Can be 1D (single series) or 2D (series x categories).
    ax : matplotlib.axes.Axes, optional
        Axis to draw on. If None, a new figure is created.
    labels : list of str, optional
        Labels for each series (for legend).
    colors : list of colors, optional
        Colors for each series.
    yfmt : str, optional
        Format string for y-axis labels. If None, automatically detects integer/float.
    sort : str, optional
        Sort order: 'alpha' (alphabetical asc, default), 'alpha_desc', 'asc' (by total),
        or 'desc' (by total descending).

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
    values = np.asarray(values)

    # Ensure 2D for multiple series
    if values.ndim == 1:
        values = values.reshape(1, -1)

    # Sort categories
    totals = values.sum(axis=0)
    if sort == 'alpha':
        order = np.argsort(categories)
    elif sort == 'alpha_desc':
        order = np.argsort(categories)[::-1]
    elif sort == 'asc':
        order = np.argsort(totals)
    elif sort == 'desc':
        order = np.argsort(totals)[::-1]
    else:
        order = np.arange(len(categories))
    categories = categories[order]
    values     = values[:, order]

    n_series, n_cat = values.shape
    x_pos = np.arange(n_cat)
    width = 0.5

    # Stacked bars
    cumulative = np.zeros(n_cat)
    for i in range(n_series):
        color = colors[i] if colors else [0.4, 0.4, 0.4]
        label = labels[i] if labels else None
        ax.bar(
            x_pos,
            values[i],
            width=width,
            bottom=cumulative,
            color=color,
            label=label,
            edgecolor='white',
            linewidth=1
        )
        cumulative += values[i]

    # Correct y-axis to fit full stack
    ymin = 0
    ymax = cumulative.max()
    ax.set_ylim(ymin, ymax)

    # Compute y-axis ticks
    y_ticks = [yt for yt in _intermediate_ticks(ymin, ymax, max_ticks=5) if yt != 0.0]

    # Auto-detect y-axis format if not provided
    if yfmt is None:
        if np.all(np.array(y_ticks) % 1 == 0):
            yfmt = "{:.0f}"  # integers
        else:
            yfmt = "{:.2f}"  # floats

    # Decide if we need to add the smallest value
    min_val = values.min()
    add_min_label = y_ticks and (min_val < y_ticks[0])

    # Hide default ticks
    ax.set_yticks([])

    # Draw y-axis labels and horizontal lines
    for ytick in y_ticks:
        ax.text(-0.5, ytick, yfmt.format(ytick), va='center', ha='right', color='black')
        ax.hlines(ytick, -0.5, n_cat-0.5, color='white', linewidth=1)

    if add_min_label:
        ax.text(-0.5, min_val, yfmt.format(min_val), va='center', ha='right', color='black')

    # Set x-axis labels
    ax.set_xticks(x_pos)
    ax.set_xticklabels(categories)

    # Hide left spine
    ax.spines['left'].set_visible(False)

    # Set bottom spine to span only the bars
    ax.spines['bottom'].set_bounds(x_pos[0]-0.25, x_pos[-1]+0.25)
    ax.spines['bottom'].set_color([0.4, 0.4, 0.4])

    # Apply Tufte style (removes top/right spines)
    apply_tufte_style(ax)

    # Add legend if labels provided
    if labels:
        ax.legend(frameon=False)

    return fig, ax

####################################################################################################
#                                          Test / example code                                     #
####################################################################################################
def main():

    categories = ["North\nHaverbrook", "Ogdenville", "Cypress\nCreek", "Brockway", "Terror\nLake", "Cape\nFeare"]

    # Two series example
    values = np.random.randint(3, 20, size=(2, len(categories)))

    fig, ax = column_chart(
        categories,
        values,
        labels=["Series A", "Series B"],
        colors=[[0.24, 0.47, 0.59], [0.95, 0.71, 0.02]]
    )
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
