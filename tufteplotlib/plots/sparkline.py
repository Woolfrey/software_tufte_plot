import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib.styles import apply_tufte_style

####################################################################################################
#                                         Core function                                            #
####################################################################################################
def sparkline(y, *,
              ax=None,
              color="black",
              line_width=1.0,
              show_dots=True,
              show_labels=True,
              start_end_color="black",
              min_max_color="red",
              dot_size=12,
              margin=0.05):
    """
    Tufte-style sparkline: intense, simple time-series with minimal ink.

    Parameters
    ----------
    y : array-like
        Sequence of values to plot.
    ax : matplotlib.axes.Axes, optional
        Axes to draw on. If None, a new figure/axes is created.
    color : str, optional
        Line color. Default black.
    line_width : float, optional
        Width of the sparkline. Default 1.0.
    show_dots : bool, optional
        Whether to draw dots for start/end, min/max. Default True.
    show_labels : bool, optional
        Whether to draw labels for start (left) and end (right). Default True.
    start_end_color : str, optional
        Color of start/end dots. Default black.
    min_max_color : str, optional
        Color of min/max dots. Default red.
    dot_size : float, optional
        Marker size for dots. Default 12.
    margin : float, optional
        Fraction of y-range to add as vertical margin. Default 0.05.

    Returns
    -------
    ax : matplotlib.axes.Axes
        The matplotlib axes containing the sparkline.
    """
    y = np.asarray(y)
    x = np.arange(len(y))

    if ax is None:
        fig, ax = plt.subplots(figsize=(4*1.618, 1))

    # Draw sparkline
    ax.plot(x, y, color=color, linewidth=line_width, zorder=1)

    if show_dots:
        # Start and end dots
        ax.scatter([x[0]], [y[0]], color=start_end_color, s=dot_size, zorder=2)
        ax.scatter([x[-1]], [y[-1]], color=start_end_color, s=dot_size, zorder=2)

        # Min/max dots
        ymin_idx = np.argmin(y)
        ymax_idx = np.argmax(y)
        ax.scatter([x[ymin_idx]], [y[ymin_idx]], color=min_max_color, s=dot_size, zorder=2)
        ax.scatter([x[ymax_idx]], [y[ymax_idx]], color=min_max_color, s=dot_size, zorder=2)

    if show_labels:
        # Place start value on left edge
        ax.text(x[0] - 0.2, y[0], f"{y[0]:.2f}", ha="right", va="center")
        # Place end value on right edge
        ax.text(x[-1] + 0.2, y[-1], f"{y[-1]:.2f}", ha="left", va="center")

    # Clean up axes
    ymin, ymax = y.min(), y.max()
    yrange = ymax - ymin
    ax.set_ylim(ymin - margin*yrange, ymax + margin*yrange)
    
    # Add horizontal margin to prevent clipping of start/end dots
    x_margin = 0.05 * (x[-1] - x[0]) if len(x) > 1 else 0.5
    ax.set_xlim(x[0] - x_margin, x[-1] + x_margin)

    ax.set_xticks([])
    ax.set_yticks([])
    
    for spine in ax.spines.values():
        spine.set_visible(False)

    apply_tufte_style(ax)

    plt.tight_layout()
    
    return ax
    
####################################################################################################
#                                          Test / example code                                     #
####################################################################################################     
def main():

    y = np.random.normal(0, 1, 30).cumsum()

    sparkline(y, show_dots=True, show_labels=True)

    plt.show()

if __name__ == "__main__":
    main()
