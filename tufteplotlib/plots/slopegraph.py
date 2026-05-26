import numpy as np
import matplotlib.pyplot as plt


def _nudge_positions(values, min_gap):
    """
    Given an array of y-positions, iteratively push overlapping labels apart
    so no two are closer than min_gap. Preserves relative order.
    """
    pos = np.array(values, dtype=float)
    order = np.argsort(pos)
    pos_sorted = pos[order]

    # Iterative upward sweep: push items apart if too close
    for _ in range(100):
        moved = False
        for j in range(1, len(pos_sorted)):
            gap = pos_sorted[j] - pos_sorted[j - 1]
            if gap < min_gap:
                shift = (min_gap - gap) / 2
                pos_sorted[j - 1] -= shift
                pos_sorted[j]     += shift
                moved = True
        if not moved:
            break

    # Map back to original order
    result = np.empty_like(pos)
    result[order] = pos_sorted
    return result


def slopegraph(
    labels,
    left,
    right,
    left_label="Before",
    right_label="After",
    title=None,
    ax=None,
    sort_by="left",
    highlight_top=None,
    figsize=None,
    min_label_gap=None,
):
    """
    Tufte-style slopegraph comparing values across two states.

    Parameters
    ----------
    labels : array-like of str
        Category names, one per row.
    left : array-like of float
        Values at the left (first) time point.
    right : array-like of float
        Values at the right (second) time point.
    left_label : str
        Column header for the left axis.
    right_label : str
        Column header for the right axis.
    title : str, optional
        Chart title, placed above the headers.
    ax : matplotlib Axes, optional
        Axes to draw into. If None, a new figure is created.
    sort_by : {"left", "right", "difference", "label"}
        Controls draw order (z-order) only — which lines appear on top
        when slopes cross. Vertical position is always determined by data.
    highlight_top : int, optional
        Number of largest-difference items to emphasise (darker, thicker).
    figsize : tuple, optional
        (width, height) in inches. Defaults to (6, max(4, n*0.45)).
    min_label_gap : float, optional
        Minimum vertical gap between labels in data units. Defaults to
        (vmax - vmin) * 0.06.

    Returns
    -------
    fig : matplotlib Figure
    ax  : matplotlib Axes
    """

    # ------------------------------------------------------------------
    # 0. Input validation & coercion
    # ------------------------------------------------------------------
    labels = np.array(labels)
    left   = np.array(left,  dtype=float)
    right  = np.array(right, dtype=float)
    n = len(labels)

    if not (len(left) == len(right) == n):
        raise ValueError("labels, left, and right must be the same length.")

    # ------------------------------------------------------------------
    # 1. Vertical positioning — values map directly to y
    # ------------------------------------------------------------------
    all_vals = np.concatenate([left, right])
    vmin, vmax = all_vals.min(), all_vals.max()
    span = vmax - vmin or 1.0
    pad  = span * 0.08

    y_lo = vmin - pad
    y_hi = vmax + pad

    if min_label_gap is None:
        min_label_gap = span * 0.06

    # ------------------------------------------------------------------
    # 2. Nudge label positions to avoid overlaps (lines stay at true y)
    # ------------------------------------------------------------------
    left_label_y  = _nudge_positions(left,  min_label_gap)
    right_label_y = _nudge_positions(right, min_label_gap)

    # ------------------------------------------------------------------
    # 3. Draw order (z-order only, no effect on vertical position)
    # ------------------------------------------------------------------
    if sort_by == "left":
        draw_order = np.argsort(left)
    elif sort_by == "right":
        draw_order = np.argsort(right)
    elif sort_by == "difference":
        draw_order = np.argsort(np.abs(right - left))
    elif sort_by == "label":
        draw_order = np.argsort(labels)
    else:
        raise ValueError(
            f"sort_by must be 'left', 'right', 'difference', or 'label'; got {sort_by!r}"
        )

    # ------------------------------------------------------------------
    # 4. Highlight mask
    # ------------------------------------------------------------------
    if highlight_top is not None:
        top_indices = set(np.argsort(np.abs(right - left))[-highlight_top:])
    else:
        top_indices = set()

    # ------------------------------------------------------------------
    # 5. Figure / axes
    # ------------------------------------------------------------------
    if figsize is None:
        figsize = (6, max(4, n * 0.45))

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    X_LEFT  = 0.0
    X_RIGHT = 1.0

    # ------------------------------------------------------------------
    # 6. Draw lines and labels
    # ------------------------------------------------------------------
    for i in draw_order:
        highlighted = i in top_indices

        color  = [0.8, 0.2, 0.2] if highlighted else [0.2, 0.2, 0.2]
        lw     = 1.0             if highlighted else 0.8
        alpha  = 1.0             if highlighted else 1.0
        zorder = 3               if highlighted else 2

        # Slope line — anchored to true data values
        ax.plot(
            [X_LEFT, X_RIGHT],
            [left[i], right[i]],
            color=color,
            linewidth=lw,
            alpha=alpha,
            solid_capstyle="round",
            zorder=zorder,
        )

        # Left label — nudged y position
        ax.text(
            X_LEFT - 0.04, left_label_y[i],
            f"{labels[i]}  {left[i]:g}",
            ha="right", va="center",
            fontsize=8.5,
            color=color,
            fontfamily="serif",
        )

        # Right label — nudged y position
        ax.text(
            X_RIGHT + 0.04, right_label_y[i],
            f"{right[i]:g}  {labels[i]}",
            ha="left", va="center",
            fontsize=8.5,
            color=color,
            fontfamily="serif",
        )

    # ------------------------------------------------------------------
    # 7. Column headers
    # ------------------------------------------------------------------
    header_y = y_hi

    ax.text(X_LEFT,  header_y, left_label,
            ha="center", va="bottom",
            fontsize=10, fontfamily="serif",
            fontweight="bold", color="#1a1a1a")

    ax.text(X_RIGHT, header_y, right_label,
            ha="center", va="bottom",
            fontsize=10, fontfamily="serif",
            fontweight="bold", color="#1a1a1a")

    if title:
        ax.text(0.5, header_y, title,
                ha="center", va="bottom",
                fontsize=12, fontfamily="serif",
                fontstyle="italic", color="#1a1a1a")

    # ------------------------------------------------------------------
    # 8. Tufte-style cleanup — no vertical rules, no box, no ticks
    # ------------------------------------------------------------------
    # Expand ylim to accommodate nudged labels that may exceed data range
    nudged_min = min(left_label_y.min(), right_label_y.min())
    nudged_max = max(left_label_y.max(), right_label_y.max())

    ax.set_xlim(-0.55, 1.55)
    ax.set_ylim(min(y_lo, nudged_min - pad * 0.5),
                max(y_hi, nudged_max) + pad)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")

    plt.tight_layout()
    return fig, ax


# ----------------------------------------------------------------------
# Demo
# ----------------------------------------------------------------------
def main():
    categories = [
        "Transport", "Housing", "Food", "Healthcare",
        "Education", "Energy", "Recreation", "Clothing",
    ]
    before = [42, 78, 55, 30, 25, 18, 38, 20]
    after  = [39, 85, 52, 45, 22, 30, 41, 18]

    fig, ax = slopegraph(
        labels=categories,
        left=before,
        right=after,
        left_label="2019",
        right_label="2024",
        sort_by="difference",
        highlight_top=1,
    )

    plt.show()


if __name__ == "__main__":
    main()
