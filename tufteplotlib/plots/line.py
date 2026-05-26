import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
from tufteplotlib.styles import apply_tufte_style
from tufteplotlib.utils import _intermediate_ticks
import numpy as np

####################################################################################################
#                                         Core function                                            #
####################################################################################################
def line_plot(x, y, ax=None, x_labels=None, linewidth=1.0, linecolor='black', autoscale=True):
    """
    Plot a line defined by a 2D dataset.
    """

    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 3))
    else:
        fig = ax.figure

    x = np.asarray(x)
    y = np.asarray(y)

    ax.plot(x, y, color=linecolor, linewidth=linewidth, alpha=1.0)

    # ------------------------------------------------------------------
    # FIX: only autoscale when explicitly enabled
    # ------------------------------------------------------------------
    if autoscale:
        xmin, xmax = x.min(), x.max()
        ymin, ymax = y.min(), y.max()

        x_range = xmax - xmin
        y_range = ymax - ymin
        margin = 0.05

        ax.set_xlim(xmin - margin * x_range, xmax + margin * x_range)
        ax.set_ylim(ymin - margin * y_range, ymax + margin * y_range)

        # Apply Tufte style scaling only once per autoscale pass
        apply_tufte_style(ax)

        ax.spines['bottom'].set_bounds(xmin, xmax)
        ax.spines['left'].set_bounds(ymin, ymax)

        ax.set_xticks(_intermediate_ticks(xmin, xmax, max_ticks=5))
        yticks = _intermediate_ticks(ymin, ymax, max_ticks=5, edge_fraction=0.07)
        ax.set_yticks(yticks)

    # Format y-axis
    ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))

    # Optional x labels override
    if x_labels is not None:
        ax.set_xticks(np.arange(len(x_labels)))
        ax.set_xticklabels(x_labels, rotation=45, ha="right")

    return fig, ax

####################################################################################################
#                                          Test / example code                                     #
####################################################################################################
def main():
    # Load sales data from CSV
    data = np.genfromtxt("sales_data.csv", delimiter=",", skip_header=1, dtype=None, encoding=None)
    dates = [row[0] for row in data]  # 'Date' column as strings
    sales = np.array([float(row[1]) for row in data])  # 'Sales' column as floats

    # X-axis as numeric indices
    x = np.arange(len(dates))

    # Plot sales time series with thicker blue line
    fig, ax = line_plot(x, sales, x_labels=dates, linewidth=2.5, linecolor='blue')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
