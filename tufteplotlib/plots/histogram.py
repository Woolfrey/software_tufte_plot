import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib.styles import apply_tufte_style
from tufteplotlib.utils import _intermediate_ticks

####################################################################################################
#                                         Core function                                            #
####################################################################################################
def histogram_plot(data, bins=10, ax=None, orientation="vertical"):
    """
    Plot the frequency of observations for a 1-dimensional data set, distributed across discretized
    numerical categories. If the data are dense, consider using the density plot instead.

    Parameters
    ----------
    data : array-like
        Input data to histogram.
    bins : int or sequence, optional
        Number of bins or explicit bin edges. Default 10.
    ax : matplotlib.axes.Axes, optional
        Axis to draw on. If None, a new figure is created.
    orientation : str, optional
        "vertical" (default) for standard upright bars;
        "horizontal" for rotated bars (e.g. marginal distribution panel).

    Returns
    -------
    fig : matplotlib.figure.Figure
    ax  : list containing the single matplotlib.axes.Axes
    """
    if ax is None:
        fig, ax_hist = plt.subplots(figsize=(4 * 1.618, 4))
    else:
        fig = ax.figure
        ax_hist = ax

    # --- Compute bin counts and edges -----------------------------------
    counts, bin_edges = np.histogram(data, bins=bins)

    # --- Format string for tick labels ----------------------------------
    # Counts are always integers; data axis uses decimal places
    count_fmt = "d"

    # --- Count axis ticks (shared logic) --------------------------------
    cmin, cmax = counts.min(), counts.max()
    c_ticks = _intermediate_ticks(cmin, cmax, max_ticks=5)
    if cmin not in c_ticks:
        c_ticks = np.insert(c_ticks, 0, cmin)
    if cmax not in c_ticks:
        c_ticks = np.append(c_ticks, cmax)

    # --- Data axis ticks: min, median, max ------------------------------
    d_min, d_max = bin_edges[0], bin_edges[-1]
    d_median     = np.median(data)
    d_ticks      = [d_min, d_median, d_max]

    # --- Bar width ------------------------------------------------------
    bar_width = (bin_edges[1] - bin_edges[0]) * 0.7
    bar_left  = bin_edges[:-1] + (bin_edges[1] - bin_edges[0]) * 0.15  # centre the rwidth gap

    if orientation == "vertical":
        # Bars
        ax_hist.bar(
            bar_left, counts,
            width=bar_width,
            align="edge",
            color=[0.4, 0.4, 0.4],
            edgecolor="white",
            linewidth=0.5,
        )

        # Count axis (y): ticks + white reference lines
        ax_hist.set_yticks(c_ticks)
        ax_hist.set_yticklabels([f"{int(ct):{count_fmt}}" for ct in c_ticks])
        for ct in c_ticks[1:]:
            ax_hist.hlines(ct, xmin=bin_edges[0], xmax=bin_edges[-1],
                           color="white", linewidth=1)
        ax_hist.set_ylim(0, c_ticks[-1])

        # Data axis (x): min, median, max
        ax_hist.set_xticks(d_ticks)
        ax_hist.set_xticklabels([f"{dt:.2f}" for dt in d_ticks])
        ax_hist.tick_params(axis="x", length=2, width=0.5)

        # Spines
        ax_hist.spines["bottom"].set_bounds(bin_edges[0] + 0.07, bin_edges[-1] - 0.07)
        ax_hist.spines["bottom"].set_color([0.4, 0.4, 0.4])
        ax_hist.spines["left"].set_visible(False)
        ax_hist.spines["top"].set_visible(False)
        ax_hist.spines["right"].set_visible(False)

    elif orientation == "horizontal":
        # Bars drawn horizontally: data axis is y, count axis is x
        ax_hist.barh(
            bar_left, counts,
            height=bar_width,
            align="edge",
            color=[0.4, 0.4, 0.4],
            edgecolor="white",
            linewidth=0.5,
        )

        # Count axis (x): ticks + white reference lines
        ax_hist.set_xticks(c_ticks)
        ax_hist.set_xticklabels([f"{int(ct):{count_fmt}}" for ct in c_ticks])
        for ct in c_ticks[1:]:
            ax_hist.vlines(ct, ymin=bin_edges[0], ymax=bin_edges[-1],
                           color="white", linewidth=1)
        ax_hist.set_xlim(0, c_ticks[-1])

        # Data axis (y): min, median, max
        ax_hist.set_yticks(d_ticks)
        ax_hist.set_yticklabels([f"{dt:.2f}" for dt in d_ticks])
        ax_hist.tick_params(axis="y", length=2, width=0.5)

        # Spines
        ax_hist.spines["left"].set_bounds(bin_edges[0] + 0.07, bin_edges[-1] - 0.07)
        ax_hist.spines["left"].set_color([0.4, 0.4, 0.4])
        ax_hist.spines["bottom"].set_visible(False)
        ax_hist.spines["top"].set_visible(False)
        ax_hist.spines["right"].set_visible(False)

    else:
        raise ValueError(f"histogram_plot: orientation must be 'vertical' or 'horizontal', got {orientation!r}")

    # Apply Tufte style
    apply_tufte_style(ax_hist)

    return fig, [ax_hist]


####################################################################################################
#                                          Test / example code                                     #
####################################################################################################
def main():
    import matplotlib.pyplot as plt

    data = np.random.normal(loc=0.0, scale=1.0, size=100)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    histogram_plot(data, ax=axes[0], orientation="vertical")
    axes[0].set_title("Vertical")

    histogram_plot(data, ax=axes[1], orientation="horizontal")
    axes[1].set_title("Horizontal")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
