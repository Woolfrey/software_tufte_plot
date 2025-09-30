import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib.styles import apply_tufte_style
from tufteplotlib.utils import _intermediate_ticks

####################################################################################################
#                                         Core function                                            #
####################################################################################################
def pareto_chart(categories, values):
    """
    Minimal API Tufte-style Pareto chart with cumulative percentage line.

    Parameters
    ----------
    categories : list-like
        Category names.
    values : array-like
        Bar heights.

    Returns
    -------
    fig : matplotlib.figure.Figure
    ax : matplotlib.axes.Axes
    """
    fig, ax = plt.subplots(figsize=(5*1.618, 5))

    categories = np.asarray(categories)
    values = np.asarray(values)

    # Sort descending
    sort_idx = np.argsort(values)[::-1]
    categories = categories[sort_idx]
    values = values[sort_idx]
    x_pos = np.arange(len(categories))

    # Draw bars
    ax.bar(x_pos, values, color=[0.4, 0.4, 0.4], alpha=1.0, width=0.6, bottom=0)

    # Cumulative percentage line with dots
    cumulative = np.cumsum(values)
    cumulative_pct = 100 * cumulative / cumulative[-1]

    ax2 = ax.twinx()
    ax2.plot(x_pos, cumulative_pct, color=[0.0, 0.0, 0.0], linewidth=1.5, alpha=0.8, zorder=3)
    ax2.scatter(x_pos, cumulative_pct, color=[0.0, 0.0, 0.0], s=40,
                edgecolor='white', linewidth=1.0, zorder=4)

    # Percentage labels above dots
    for i, pct in enumerate(cumulative_pct):
        ax2.text(x_pos[i], pct + 1, f"{pct:.1f}%", ha='center', va='bottom', fontsize=9, color=[0.0,0.0,0.0])

    # Y-axis ticks for bars
    ymin, ymax = values.min(), values.max()
    y_ticks = _intermediate_ticks(ymin, ymax, max_ticks=5)
    if ymin < y_ticks[0]:
        y_ticks = np.insert(y_ticks, 0, ymin)

    ax.set_ylim(0, values.max()*1.1)
    ax.set_yticks([])

    # Draw horizontal lines and manual labels
    for i, yt in enumerate(y_ticks):
        if i == 0 and yt == ymin and yt != 0:
            ax.text(-0.6, yt, f"{yt:.0f}", ha='left', va='center', fontsize=9, color='black')
        else:
            ax.hlines(yt, -0.5, len(categories)-0.5, color='white', linewidth=1)
            ax.text(-0.6, yt, f"{yt:.0f}", ha='left', va='center', fontsize=9, color='black')

    # X-axis labels manually
    ax.tick_params(axis='x', length=0)
    for i, label in enumerate(categories):
        ax.text(i, -0.02*ymax, label, ha='center', va='top', rotation=0.0, fontsize=9)

    # Bottom spine
    ax.spines['bottom'].set_bounds(x_pos[0]-0.3, x_pos[-1]+0.3)
    ax.spines['bottom'].set_color([0.4,0.4,0.4])

    # Hide other spines
    for spine_name, spine in ax.spines.items():
        if spine_name != 'bottom':
            spine.set_visible(False)
    for spine in ax2.spines.values():
        spine.set_visible(False)

    # Hide ax2 ticks
    ax2.set_yticks([])
    ax2.set_xticks([])
    ax2.set_ylim(0, 105)

    # Apply Tufte style
    apply_tufte_style(ax)
    apply_tufte_style(ax2)

    plt.tight_layout()
    
    return fig, [ax, ax2]

####################################################################################################
#                                          Test / example code                                     #
####################################################################################################
def main():

    categories = ["Jimbo", "Nelson", "Dolph", "Kearny", "Kearny Jnr."]
    
    np.random.seed()
    
    values = np.random.randint(1, 20, size=len(categories))

    fig, ax = pareto_chart(categories, values)
    
    plt.show()

if __name__ == "__main__":
    main()
