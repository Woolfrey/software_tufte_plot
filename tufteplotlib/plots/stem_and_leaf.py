import numpy as np
import warnings
from collections import defaultdict
import matplotlib.pyplot as plt

####################################################################################################
#                                         Core function                                            #
####################################################################################################
def stem_and_leaf_plot(data=None, output="plain", round_decimals=2, render_fig=False):
    """
    Generate a stem-and-leaf table from integer or floating-point data.

    Parameters
    ----------
    data : array-like
        List or array of numbers. If None, random integers are generated.
    output : str
        'plain', 'Markdown', 'LaTeX', or 'CSV'
    round_decimals : int
        Number of decimal places for floats
    render_fig : bool
        If True, render the table text as a matplotlib figure.
       
        
    Returns
    -------
    str
        The table in the specified output.
    """
    if data is None:
        raise ValueError("No data provided.")

    data = sorted(data)
    stems = defaultdict(list)

    # --- Organize stems and leaves ---
    if all(isinstance(x, (int, np.integer)) for x in data):
        for value in data:
            s = str(value)
            if len(s) == 1:
                stem, leaf = "0", s[-1]
            else:
                stem, leaf = s[:-1], s[-1]
            stems[int(stem)].append(leaf)
        min_stem = int(min(stems))
        max_stem = int(max(stems))
        for stem in range(min_stem, max_stem + 1):
            stems.setdefault(stem, [])

    elif all(isinstance(x, (float, np.floating)) for x in data):
        for value in data:
            stem = int(np.floor(value))
            leaf_val = value - stem
            leaf_str = "." + f"{leaf_val:.{round_decimals}f}".split(".")[1]
            stems[stem].append(leaf_str)
        min_stem = int(np.floor(min(data)))
        max_stem = int(np.floor(max(data)))
        for stem in range(min_stem, max_stem + 1):
            stems.setdefault(stem, [])
            
    else:
        warnings.warn("Mixed data types detected. Only pure int or pure float arrays are supported.")
        return ""

    # --- Format table text ---
    max_stem_width = max(5, max(len(str(stem)) for stem in stems)) if stems else 1

    if output == "plain":
        lines  = [f"{'Stem'.rjust(max_stem_width)} | Leaves"]
        lines += [f"{'-----'.rjust(max_stem_width)} | -------"]
        for stem in sorted(stems):
            leaves = ' '.join(str(l) for l in stems[stem])
            lines.append(f"{str(stem).rjust(max_stem_width)} | {leaves}")
        table_text = "\n".join(lines)

    elif output == "Markdown":
        lines = [f"| {'Stem'.rjust(max_stem_width)} | Leaves |"]
        lines += ["|------:|:-------|"]
        for stem in sorted(stems):
            leaves = ' '.join(str(l) for l in stems[stem])
            lines.append(f"| {str(stem).rjust(max_stem_width)} | {leaves} |")
        table_text = "\n".join(lines)

    elif output == "CSV":
        lines = ["Stem,Leaves"]
        for stem in sorted(stems):
            leaves = ','.join(str(l) for l in stems[stem])
            lines.append(f"{str(stem).rjust(max_stem_width)},{leaves}")
        table_text = "\n".join(lines)

    elif output == "LaTeX":
        maxleaves = max(len(leaves) for leaves in stems.values()) if stems else 0
        col_format = "r|" + "l" * maxleaves
        lines = [f"\\begin{{tabular}}{{{col_format}}}"]
        lines += [f"Stem & \multicolumn{{{maxleaves}}}{{l}}{{Leaves}} \\\\ \\hline"]
        for stem in sorted(stems):
            leaves = [str(l) for l in stems[stem]]
            leaves += [""] * (maxleaves - len(leaves))
            row = f"{stem} & " + " & ".join(leaves) + " \\\\"
            lines.append(row)
        lines.append("\\end{tabular}")
        table_text = "\n".join(lines)
    else:
        if output != None:
            raise ValueError(f"Unknown output '{output}'")
        
    if output:
        print(table_text)

    if render_fig:
        font_size = 12  # points
        n_rows = len(lines)
        max_leaves = max(len(line) for line in lines)  # approximate width in characters

        # scaling factors to convert characters / font points to inches
        row_scale = 0.016     # vertical spacing per row
        col_scale = 0.01     # horizontal spacing per character

        fig_height = font_size * n_rows * row_scale
        fig_width  = font_size * max_leaves * col_scale

        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
        ax.axis('off')

        for i, line in enumerate(lines[::-1]):  # reverse: first line on top
            ax.text(0, i, line, fontsize=font_size, fontfamily='monospace', va='top', ha='left')

        ax.set_xlim(0, 1)
        ax.set_ylim(0, len(lines))
        plt.tight_layout()
        
        return fig, ax

####################################################################################################
#                                          Test / example code                                     #
####################################################################################################  
def main():
    data = np.random.randint(5,15, size=20) + np.random.rand(20)

    print("\nPlain text:\n")
    fig, ax = stem_and_leaf_plot(data, output="plain", render_fig=True)
    
    print("\nMarkdown:\n")
    stem_and_leaf_plot(data, output="Markdown")
    
    print("\nLaTeX:\n")
    stem_and_leaf_plot(data, output="LaTeX")
    
    print("\nCSV:\n")
    stem_and_leaf_plot(data, output="CSV")
    
    plt.show()

if __name__ == "__main__":
    main()

