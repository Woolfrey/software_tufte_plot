import matplotlib.pyplot as plt
from tufteplotlib.styles import apply_tufte_style
from tufteplotlib.utils import _intermediate_ticks
import numpy as np

####################################################################################################
#                                         Core function                                            #
####################################################################################################
def line_plot(x, y, *,
              ax=None, color='black', line_width=1.0,
              alpha=1.0, margin=0.05, max_ticks=5, **kwargs):
    """
    Tufte-style line plot with exact spines and nicely rounded, equispaced ticks.

    Parameters
    ----------
    x : array-like
        x-values of the line.
    y : array-like
        y-values of the line.
    ax : matplotlib.axes.Axes, optional
        Axes to draw on. Creates new figure/axes if None.
    color : str, optional
        Line color.
    line_width : float, optional
        Width of the line.
    alpha : float, optional
        Transparency of the line.
    margin : float, optional
        Fractional margin around min/max for axes.
    max_ticks : int, optional
        Approximate number of interior ticks per axis.
    **kwargs : extra arguments passed to ax.plot

    Returns
    -------
    ax : matplotlib.axes.Axes
        Axes containing the line plot.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(5*1.618, 2.5))

    x = np.asarray(x)
    y = np.asarray(y)

    # Draw the line
    ax.plot(x, y, color=color, linewidth=line_width, alpha=alpha, **kwargs)

    # Compute exact min/max
    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()
    x_range = xmax - xmin
    y_range = ymax - ymin

    # Set axis limits with margin
    ax.set_xlim(xmin - margin*x_range, xmax + margin*x_range)
    ax.set_ylim(ymin - margin*y_range, ymax + margin*y_range)

    # Apply Tufte minimal style
    apply_tufte_style(ax)

    # Force spines to match min/max
    ax.spines['bottom'].set_bounds(xmin, xmax)
    ax.spines['left'].set_bounds(ymin, ymax)

    # Set nicely rounded ticks including min/max
    ax.set_xticks(_intermediate_ticks(xmin, xmax, max_ticks=max_ticks))
    ax.set_yticks(_intermediate_ticks(ymin, ymax, max_ticks=max_ticks))
    
    plt.tight_layout()

    return ax
    
####################################################################################################
#                                          Test / example code                                     #
####################################################################################################     
def main():

    t = np.linspace(0, 10, 200)

    y = np.sin(t)

    y_noisy = y + np.random.normal(0, 0.1, size=t.shape)

    line_plot(t, y_noisy)
    
    plt.show()

if __name__ == "__main__":
    main()
