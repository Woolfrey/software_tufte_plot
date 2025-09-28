import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib.styles import apply_tufte_style
from tufteplotlib.utils import _intermediate_ticks

def quartile_plot(categories, values, *,
                  alpha = 1.0,
                  ax = None,
                  color = "black",
                  iqr_mask_thickness = 6.0,
                  line_thickness = 1.0,
                  max_ticks = 5,
                  median_marker_size = 36,
                  outlier_marker_size = 1,
                  show_labels = True):
    """
    Tufte-style quartile plot using (categories, values) inputs.
    Interquartile range is masked (blank), median is shown as a dot,
    whiskers span non-outlier values, and outliers appear as tiny dots.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(5 * 1.618, 5))

    categories = np.asarray(categories)
    values = np.asarray(values)

    if categories.shape[0] != values.shape[0]:
        raise ValueError("categories and values must have the same length")

    unique_categories = list(dict.fromkeys(categories.tolist()))
    n_cat = len(unique_categories)
    cat_to_x = {cat: i for i, cat in enumerate(unique_categories)}

    whisker_mins = []
    whisker_maxs = []
    all_outliers = []

    bg_color = ax.get_facecolor()

    # Compute stats and draw
    for cat in unique_categories:
        mask = (categories == cat)
        cat_vals = values[mask]
        if cat_vals.size == 0:
            continue

        q1, q2, q3 = np.percentile(cat_vals, [25, 50, 75])
        iqr = q3 - q1
        lower_fence = q1 - 1.5 * iqr
        upper_fence = q3 + 1.5 * iqr

        non_outliers = cat_vals[(cat_vals >= lower_fence) & (cat_vals <= upper_fence)]
        if non_outliers.size > 0:
            whisker_min = non_outliers.min()
            whisker_max = non_outliers.max()
        else:
            whisker_min = cat_vals.min()
            whisker_max = cat_vals.max()

        whisker_mins.append(whisker_min)
        whisker_maxs.append(whisker_max)

        outliers = cat_vals[(cat_vals < lower_fence) | (cat_vals > upper_fence)]
        if outliers.size > 0:
            all_outliers.append(outliers)

        x = cat_to_x[cat]

        # thin whisker line
        ax.vlines(x, whisker_min, whisker_max, color=color,
                  linewidth=line_thickness, alpha=alpha, zorder=1)

        # thick mask over IQR
        ax.vlines(x, q1, q3, color=bg_color,
                  linewidth=iqr_mask_thickness, zorder=2)

        # median dot
        ax.scatter([x], [q2], s=median_marker_size, color=color,
                   zorder=3, alpha=alpha)

        # outliers
        if outliers.size > 0:
            ax.scatter(np.full(outliers.shape, x), outliers,
                       s=outlier_marker_size, color=color,
                       alpha=alpha, zorder=4)

    # X-axis
    ax.set_xticks(range(n_cat))
    ax.set_xticklabels(unique_categories)
    ax.set_xlim(-0.5, n_cat - 0.5)

    # Y-axis (now includes outliers)
    if len(whisker_mins) == 0:
        ymin, ymax = values.min(), values.max()
    else:
        ymin = min(min(whisker_mins), *(o.min() for o in all_outliers)) if all_outliers else min(whisker_mins)
        ymax = max(max(whisker_maxs), *(o.max() for o in all_outliers)) if all_outliers else max(whisker_maxs)

    y_range = ymax - ymin if ymax > ymin else 1.0
    pad = 0.02 * y_range
    ax.set_ylim(ymin - pad, ymax + pad)

    y_ticks = _intermediate_ticks(ymin, ymax, max_ticks=max_ticks)
    ax.set_yticks(y_ticks)
    if show_labels:
        ax.set_yticklabels([f"{t:.2f}" for t in y_ticks])
    else:
        ax.set_yticklabels([])

    # Tufte styling
    apply_tufte_style(ax)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    return ax
