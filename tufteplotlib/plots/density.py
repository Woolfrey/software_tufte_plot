import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib.styles import apply_tufte_style
from tufteplotlib.utils import _intermediate_ticks
from scipy.stats import gaussian_kde

####################################################################################################
#                                         Core function                                            #
####################################################################################################
def density_plot(data, ax=None, orientation="vertical"):
    """
    Illustrate the distribution of values within a 1-dimensional data set.
    Best used for dense data sets. For sparse data, consider using a histogram.

    Parameters
    ----------
    data : array-like
        1D array of numeric values.
    ax : matplotlib.axes.Axes, optional
        Axis to draw on. If None, a new figure is created.
    orientation : str, optional
        "vertical" (default) for standard upright density curve;
        "horizontal" for rotated curve (e.g. marginal distribution panel).

    Returns
    -------
    fig : matplotlib.figure.Figure
    ax  : matplotlib.axes.Axes
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(4 * 1.618, 4))
    else:
        fig = ax.figure

    data = np.asarray(data)
    kde    = gaussian_kde(data)
    d_vals = np.linspace(data.min(), data.max(), 500)  # data axis
    k_vals = kde(d_vals)                                # density axis

    # Data axis ticks: min, median, max
    d_ticks = [data.min(), np.median(data), data.max()]

    # Density axis ticks
    k_min, k_max = 0, k_vals.max()
    k_ticks = _intermediate_ticks(k_min, k_max, max_ticks=5)

    if orientation == "vertical":
        # Shaded area: x = data, y = density
        ax.fill_between(d_vals, 0, k_vals, color=[0.4, 0.4, 0.4], alpha=1.0)

        # Data axis (x)
        ax.set_xticks(d_ticks)
        ax.set_xticklabels([f"{dt:.2f}" for dt in d_ticks])

        # Density axis (y)
        ax.set_ylim(k_min, k_max)
        ax.set_yticks(k_ticks)
        ax.set_yticklabels([f"{kt:.2f}" for kt in k_ticks])

        # Spines
        ax.spines["bottom"].set_bounds(data.min(), data.max())
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    elif orientation == "horizontal":
        # Shaded area: x = density, y = data
        ax.fill_betweenx(d_vals, 0, k_vals, color=[0.4, 0.4, 0.4], alpha=1.0)

        # Data axis (y)
        ax.set_yticks(d_ticks)
        ax.set_yticklabels([f"{dt:.2f}" for dt in d_ticks])

        # Density axis (x)
        ax.set_xlim(k_min, k_max)
        ax.set_xticks(k_ticks)
        ax.set_xticklabels([f"{kt:.2f}" for kt in k_ticks])

        # Spines
        ax.spines["left"].set_bounds(data.min(), data.max())
        ax.spines["bottom"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    else:
        raise ValueError(
            f"density_plot: orientation must be 'vertical' or 'horizontal', got {orientation!r}"
        )

    apply_tufte_style(ax)

    return fig, ax


####################################################################################################
#                                          Test / example code                                     #
####################################################################################################
def main():
    data = np.random.normal(loc=0, scale=1, size=500)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    density_plot(data, ax=axes[0], orientation="vertical")
    axes[0].set_title("Vertical")
    axes[0].set_xlabel("Value")
    axes[0].set_ylabel("Density")

    density_plot(data, ax=axes[1], orientation="horizontal")
    axes[1].set_title("Horizontal")
    axes[1].set_xlabel("Density")
    axes[1].set_ylabel("Value")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
