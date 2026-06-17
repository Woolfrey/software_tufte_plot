import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

def _nudge_positions(values, min_gap):
    """
    Given an array of y-positions, iteratively push overlapping labels apart
    so no two are closer than min_gap. Preserves relative order.
    """
    pos = np.array(values, dtype=float)
    order = np.argsort(pos)
    pos_sorted = pos[order]

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

    result = np.empty_like(pos)
    result[order] = pos_sorted
    return result


def _merge_labels_by_value(vals, lbls):
    """Return a dict mapping each unique value -> merged label string."""
    groups = defaultdict(list)
    for v, l in zip(vals, lbls):
        groups[v].append(l)
    return {v: ",\n".join(ls) for v, ls in groups.items()}


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
    decimal_places=1,
):
    """
    Tufte-style slopegraph comparing values across two states.

    Items that share the same value on the left side are automatically
    merged into a single label on the left (and vice versa on the right),
    while each row still draws its own slope line.  This produces a
    fan/bundle effect for tied values.

    Parameters
    ----------
    labels : array-like of str
    left   : array-like of float
    right  : array-like of float
    left_label, right_label : str
    title  : str, optional
    ax     : matplotlib Axes, optional
    sort_by : {"left", "right", "difference", "label"}
    highlight_top : int, optional
    figsize : tuple, optional
    min_label_gap : float, optional
    decimal_places : int, optional
        Number of decimal places for numeric labels. Defaults to 1.

    Returns
    -------
    fig, ax
    """

    # ------------------------------------------------------------------
    # 0. Validate & coerce
    # ------------------------------------------------------------------
    labels = np.array(labels)
    left   = np.array(left,  dtype=float)
    right  = np.array(right, dtype=float)
    n = len(labels)

    if not (len(left) == len(right) == n):
        raise ValueError("labels, left, and right must be the same length.")

    # ------------------------------------------------------------------
    # 0b. Build merged label maps independently per side.
    #     Each unique left value gets one merged label; same for right.
    #     Every original row still contributes its own slope line.
    # ------------------------------------------------------------------
    left_label_map  = _merge_labels_by_value(left,  labels)
    right_label_map = _merge_labels_by_value(right, labels)

    # ------------------------------------------------------------------
    # 1. Vertical positioning
    # ------------------------------------------------------------------
    all_vals = np.concatenate([left, right])
    vmin, vmax = all_vals.min(), all_vals.max()
    span = vmax - vmin or 1.0
    pad  = span * 0.05

    y_lo = vmin - pad
    y_hi = vmax + pad

    # ------------------------------------------------------------------
    # 2. Nudge once on the union of all values, then rescale back to the
    #     original data range so there is no net vertical shift.
    #     min_label_gap is scaled up for merged labels so multi-line
    #     labels don't overlap their neighbours.
    # ------------------------------------------------------------------
    max_lines = max(
        max(len(v.split(",\n")) for v in left_label_map.values()),
        max(len(v.split(",\n")) for v in right_label_map.values()),
    )
    if min_label_gap is None:
        min_label_gap = span * 0.05 * max(1, max_lines * 0.75)

    all_unique_vals = np.array(sorted(
        set(left_label_map.keys()) | set(right_label_map.keys())
    ), dtype=float)

    nudged_all_vals = _nudge_positions(all_unique_vals, min_label_gap)

    # Rescale nudged positions back to the original data range so that
    # the nudging doesn't introduce a net vertical shift.
    orig_min, orig_max   = all_unique_vals.min(), all_unique_vals.max()
    nudge_min, nudge_max = nudged_all_vals.min(), nudged_all_vals.max()
    if nudge_max > nudge_min:
        nudged_all_vals = (
            (nudged_all_vals - nudge_min) / (nudge_max - nudge_min)
            * (orig_max - orig_min) + orig_min
        )

    nudge_map   = dict(zip(all_unique_vals, nudged_all_vals))
    left_nudge  = nudge_map
    right_nudge = nudge_map

    # Track which merged labels have already been drawn on each side
    left_drawn  = set()
    right_drawn = set()

    # ------------------------------------------------------------------
    # 3. Draw order
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
    fmt = f"{{:.{decimal_places}f}}"

    for i in draw_order:
        highlighted = i in top_indices

        color  = [0.8, 0.2, 0.2] if highlighted else [0.2, 0.2, 0.2]
        lw     = 1.0             if highlighted else 0.8
        zorder = 3               if highlighted else 2

        lv = left[i]
        rv = right[i]

        # Slope line — endpoints follow nudged label positions
        ax.plot(
            [X_LEFT, X_RIGHT],
            [left_nudge[lv], right_nudge[rv]],
            color=color,
            linewidth=lw,
            alpha=1.0,
            solid_capstyle="round",
            zorder=zorder,
        )

        # Left label — draw once per unique left value
        if lv not in left_drawn:
            merged = left_label_map[lv]
            # Price — close to the axis
            ax.text(
                X_LEFT - 0.04, left_nudge[lv],
                fmt.format(lv),
                ha="right", va="center",
                fontsize=8.5, color=color, fontfamily="sans-serif",
            )
            # Category name(s) — further out
            ax.text(
                X_LEFT - 0.15, left_nudge[lv],
                merged,
                ha="right", va="center",
                fontsize=8.5, color=color, fontfamily="sans-serif",
            )
            left_drawn.add(lv)

        # Right label — draw once per unique right value
        if rv not in right_drawn:
            merged = right_label_map[rv]
            # Price — close to the axis
            ax.text(
                X_RIGHT + 0.04, right_nudge[rv],
                fmt.format(rv),
                ha="left", va="center",
                fontsize=8.5, color=color, fontfamily="sans-serif",
            )
            # Category name(s) — further out
            ax.text(
                X_RIGHT + 0.15, right_nudge[rv],
                merged,
                ha="left", va="center",
                fontsize=8.5, color=color, fontfamily="sans-serif",
            )
            right_drawn.add(rv)

    # ------------------------------------------------------------------
    # 7. Column headers
    # ------------------------------------------------------------------
    header_y = y_hi

    ax.text(X_LEFT,  header_y, left_label,
            ha="center", va="bottom",
            fontsize=10, fontfamily="sans-serif",
            fontweight="bold", color="#1a1a1a")

    ax.text(X_RIGHT, header_y, right_label,
            ha="center", va="bottom",
            fontsize=10, fontfamily="sans-serif",
            fontweight="bold", color="#1a1a1a")

    if title:
        ax.text(0.5, header_y, title,
                ha="center", va="bottom",
                fontsize=12, fontfamily="sans-serif",
                fontstyle="italic", color="#1a1a1a")

    # ------------------------------------------------------------------
    # 8. Tufte-style cleanup
    # ------------------------------------------------------------------
    nudged_min = min(nudged_all_vals)
    nudged_max = max(nudged_all_vals)

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
    before = [42, 78, 55, 30, 25, 20, 38, 20]
    after  = [39, 85, 52, 42, 22, 30, 42, 18]

    fig, ax = slopegraph(
        labels=categories,
        left=before,
        right=after,
        left_label="2019",
        right_label="2024",
        sort_by="difference",
        highlight_top=1,
        decimal_places=0
    )

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
