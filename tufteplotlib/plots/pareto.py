import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib.styles import apply_tufte_style
from tufteplotlib.utils import _intermediate_ticks

####################################################################################################
#                                         Core function                                            #
####################################################################################################

def pareto_chart(categories,
                 quantities,
                 ax = None,
                 bar_color = [0.3, 0.3, 0.3],
                 line_color = [1.0, 0.3, 0.3]):
    """
    Vertical Pareto chart: categories on x-axis, sorted descending, with
    cumulative % overlaid as a line on the right y-axis.

    Parameters
    ----------
    categories : array-like
        Sequence of category labels for the x-axis.
    quantities : array-like
        Heights of the bars corresponding to each category.
    ax : matplotlib.axes.Axes, optional
        Axis to draw on. If None, a new figure is created.
    bar_color : color, optional
        Bar fill colour. Defaults to [0.4, 0.4, 0.4].
    line_color : color, optional
        Colour for the cumulative % line and annotations. Default is 'darkred'.

    Returns
    -------
    fig : matplotlib.figure.Figure
    ax_list : list of matplotlib.axes.Axes
        [ax_bar, ax_cumulative]
    """
    # Convert to numpy arrays
    categories = np.asarray(categories)
    quantities = np.asarray(quantities)

    # Sort descending (largest at left)
    order      = np.argsort(quantities)[::-1]
    categories = categories[order]
    quantities = quantities[order]

    # Create figure/axis if not provided
    if ax is None:
        fig, ax_bar = plt.subplots(figsize=(4 * 1.618, 4))
    else:
        fig    = ax.figure
        ax_bar = ax

    x_pos     = np.arange(len(categories))

    # Draw vertical bars
    ax_bar.bar(x_pos, quantities, width=0.5, color=bar_color, edgecolor=None, linewidth=1)

    # Set y-axis limits
    ymin = 0
    ymax = quantities.max()
    ax_bar.set_ylim(ymin, ymax)

    # Compute y-axis ticks (exclude zero)
    y_ticks = [yt for yt in _intermediate_ticks(ymin, ymax, max_ticks=5) if yt != 0.0]

    if np.all(np.array(y_ticks) % 1 == 0):
        yfmt = "{:.0f}"
    else:
        yfmt = "{:.2f}"

    min_val       = quantities.min()
    add_min_label = y_ticks and (min_val < y_ticks[0])

    # Hide default y ticks and draw custom labels and white gridlines
    ax_bar.set_yticks([])

    x_min, x_max = -0.35, len(categories) - 0.65

    for yt in y_ticks:
        ax_bar.text(-0.03, yt, yfmt.format(yt),
                    transform  = ax_bar.get_yaxis_transform(),
                    va='center', ha='right', color='black', fontsize=10)
        ax_bar.hlines(yt, x_min, x_max, color='white', linewidth=1)

    if add_min_label:
        ax_bar.text(-0.03, min_val, yfmt.format(min_val),
                    transform  = ax_bar.get_yaxis_transform(),
                    va='center', ha='right', color='black', fontsize=10)

    # Set x-axis category labels
    ax_bar.set_xticks(x_pos)
    ax_bar.set_xticklabels(categories)
    ax_bar.set_xlim(x_min, x_max)

    # Spines
    ax_bar.spines['left'].set_visible(False)
    ax_bar.spines['bottom'].set_bounds(x_pos[0] - 0.25, x_pos[-1] + 0.25)
    ax_bar.spines['bottom'].set_color([0.4, 0.4, 0.4])

    apply_tufte_style(ax_bar)

    # Compute cumulative percentages
    cum_percent = np.cumsum(quantities) / np.sum(quantities) * 100

    # Overlay cumulative % line on a twin y-axis (right)
    ax_cum = ax_bar.twinx()
    ax_cum.set_ylim(0, 105)
    ax_cum.set_xlim(ax_bar.get_xlim())

    ax_cum.plot(x_pos, cum_percent, color=line_color, marker="o", linewidth=1.0)

    # Annotate each point with its % value
    for x, y in zip(x_pos, cum_percent):
        ax_cum.annotate(
            f"{y:.1f}%",
            xy         = (x, y),
            xytext     = (0, 6),
            textcoords = "offset points",
            va         = "bottom",
            ha         = "center",
            fontsize   = 9,
            color      = line_color,
        )

    # Hide all twin axis ticks and spines
    ax_cum.set_yticks([])
    ax_cum.spines['top'].set_visible(False)
    ax_cum.spines['right'].set_visible(False)
    ax_cum.spines['bottom'].set_visible(False)
    ax_cum.spines['left'].set_visible(False)

    return fig, [ax_bar, ax_cum]

####################################################################################################
#                                          Test / example code                                     #
####################################################################################################

def main():
    categories = ["Sneed's", "Costington's", "Try'n'Save", "Shøp", "The Leftorium", "Houseware\nWarehouse"]

    np.random.seed()

    quantities = np.random.rand(len(categories)) * 20  # float values

    fig, ax = pareto_chart(categories, quantities)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
