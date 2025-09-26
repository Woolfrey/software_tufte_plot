import matplotlib.pyplot as plt
import numpy as np
from tufteplotlib.styles import apply_tufte_style
from tufteplotlib.utils import _data_min_max, _intermediate_ticks

def barcode_plot(categories, values, ax=None, color='black', alpha=0.5,
                 line_width=0.6, line_thickness=2.0, show_labels=False,
                 x_label_pad=5):
    """
    Tufte-style barcode plot: horizontal lines for each data point in each nominal category.

    Parameters:
        categories : array-like of categorical labels
        values : array-like of numerical data, same length as categories
        ax : matplotlib Axes (optional)
        color : line color
        alpha : line transparency
        tick_length : length of y-axis ticks (points)
        tick_width : width of y-axis ticks (points)
        show_labels : if True, show min/intermediate/max y-axis labels
        x_label_pad : padding for x-axis labels (points)
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
    ymin, ymax = _data_min_max(values)
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
