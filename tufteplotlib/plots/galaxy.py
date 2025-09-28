import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from tufteplotlib.styles import apply_tufte_style

def galaxy_plot(x, y, z, *,
                ax=None,
                nx_bins=100,
                ny_bins=100,
                show_xlabels=True,
                show_ylabels=True,
                cmap='Greys'):
    """
    Tufte-style galaxy plot: discretize (x, y) into bins, take max(z) per bin,
    and plot as a grayscale intensity map.

    Parameters
    ----------
    x, y, z : array-like
        1D arrays of the same length.
    ax : matplotlib.axes.Axes, optional
        Axes to draw on. If None, a new figure is created.
    nx_bins : int
        Number of bins along x-axis.
    ny_bins : int
        Number of bins along y-axis.
    show_xlabels : bool
        Whether to display x-axis tick labels.
    show_ylabels : bool
        Whether to display y-axis tick labels.
    cmap : str or Colormap
        Colormap to use (grayscale recommended).

    Returns
    -------
    ax : matplotlib.axes.Axes
    im : matplotlib.image.AxesImage
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(5,5))

    x = np.asarray(x)
    y = np.asarray(y)
    z = np.asarray(z)

    # Create empty grid
    z_grid = np.full((ny_bins, nx_bins), np.nan)
    x_edges = np.linspace(x.min(), x.max(), nx_bins + 1)
    y_edges = np.linspace(y.min(), y.max(), ny_bins + 1)

    # Assign max z to each bin
    for i in range(nx_bins):
        for j in range(ny_bins):
            mask = ((x >= x_edges[i]) & (x < x_edges[i+1]) &
                    (y >= y_edges[j]) & (y < y_edges[j+1]))
            if np.any(mask):
                z_grid[j, i] = np.max(z[mask])

    # Handle any bins with no data
    z_grid = np.nan_to_num(z_grid, nan=np.nanmin(z_grid))

    z_min, z_max = np.nanmin(z_grid), np.nanmax(z_grid)

    im = ax.imshow(z_grid, origin='lower',
                   extent=(x.min(), x.max(), y.min(), y.max()),
                   cmap=cmap,
                   norm=Normalize(vmin=z_min, vmax=z_max),
                   aspect='auto')

    # Apply Tufte style
    apply_tufte_style(ax)

    # Hide all spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    # X-axis ticks
    if show_xlabels:
        ax.xaxis.set_visible(True)
    else:
        ax.xaxis.set_visible(False)

    # Y-axis ticks
    if show_ylabels:
        ax.yaxis.set_visible(True)
    else:
        ax.yaxis.set_visible(False)
        
    ax.set_aspect('equal')
    
    plt.tight_layout()

    return ax, im
    

def add_min_max_colorbar(im, ax=None, label='Intensity', fontsize=10, fraction=0.046, pad=0.04, labelpad=-20):
    """
    Add a minimalist colorbar showing only the min and max of an AxesImage.

    Parameters
    ----------
    im : matplotlib.image.AxesImage
        The image returned by imshow or similar.
    ax : matplotlib.axes.Axes, optional
        Axes to associate the colorbar with. If None, uses current axes.
    label : str
        Label for the colorbar.
    fontsize : int
        Font size for the colorbar label.
    fraction : float
        Fraction of the original axes size for the colorbar.
    pad : float
        Padding between the axes and the colorbar.
    labelpad : float
        Offset for the colorbar label.

    Returns
    -------
    cbar : matplotlib.colorbar.Colorbar
        The created colorbar object.
    """
    if ax is None:
        ax = plt.gca()

    vmin, vmax = im.get_array().min(), im.get_array().max()

    cbar = plt.colorbar(im, ax=ax, fraction=fraction, pad=pad)
    cbar.set_ticks([vmin, vmax])
    cbar.set_ticklabels([f"{vmin:.2f}", f"{vmax:.2f}"])
    cbar.outline.set_visible(False)
    cbar.set_label(label, fontsize=fontsize, labelpad=labelpad)

    return cbar
