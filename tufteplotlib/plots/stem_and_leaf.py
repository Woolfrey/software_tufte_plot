import numpy as np
import warnings
from collections import defaultdict

####################################################################################################
#                                         Core function                                            #
####################################################################################################
def stem_and_leaf_plot(data=None, style="plain", round_decimals=2):
    """
    Generate a stem-and-leaf table from integer or floating-point data.

    Parameters
    ----------
    data : array-like
        List or array of numbers. If None, random integers are generated.
    style : str
        'plain', 'Markdown', 'LaTeX', or 'CSV'.
    round_decimals : int
        Number of decimal places for floats
        
    Returns
    -------
    str
        The table in the specified style.
    """
    if data is None:
        raise ValueError(f"No data.")

    data = sorted(data)
    stems = defaultdict(list)

    if all(isinstance(x, (int, np.integer)) for x in data):
        # Integer case
        for value in data:
            s = str(value)
            if len(s) == 1:
                stem, leaf = "0", s[-1]
            else:
                stem, leaf = s[:-1], s[-1]
            stems[int(stem)].append(leaf)

        min_stem = int(min(stems))
        max_stem = int(max(stems))
        all_stems = list(range(min_stem, max_stem + 1))
        for stem in all_stems:
            stems.setdefault(stem, [])

    elif all(isinstance(x, (float, np.floating)) for x in data):
        # Float case
        for value in data:
            stem = int(np.floor(value))
            # Format leaf with fixed decimal places, preserving trailing zeros
            leaf_val = value - stem
            leaf_str = "." + f"{leaf_val:.{round_decimals}f}".split(".")[1]
            stems[stem].append(leaf_str)

        min_stem = int(np.floor(min(data)))
        max_stem = int(np.floor(max(data)))
        all_stems = list(range(min_stem, max_stem + 1))
        for stem in all_stems:
            stems.setdefault(stem, [])

    else:
        warnings.warn("Mixed data types detected. Only pure int or pure float arrays are supported.")
        return ""

    # --- Format output ---
    # Compute padding width for stem alignment
    max_stem_width = max(5, max(len(str(stem)) for stem in stems)) if stems else 1

    if style == "plain":
        lines = [f"{'Stem'.rjust(max_stem_width)} | Leaves"]
        for stem in sorted(stems):
            leaves = ' '.join(str(l) for l in stems[stem])
            lines.append(f"{str(stem).rjust(max_stem_width)} | {leaves}")
        return "\n".join(lines)

    elif style == "Markdown":
        lines  = [f"| {'Stem'.rjust(max_stem_width)} | Leaves |"]
        lines += [f"|------:|:-------|"]
        for stem in sorted(stems):
            leaves = ' '.join(str(l) for l in stems[stem])
            lines.append(f"| {str(stem).rjust(max_stem_width)} | {leaves} |")
        return "\n".join(lines)

    elif style == "CSV":
        lines = ["Stem,Leaves"]
        for stem in sorted(stems):
            leaves = ','.join(str(l) for l in stems[stem])
            lines.append(f"{str(stem).rjust(max_stem_width)},{leaves}")
        return "\n".join(lines)


    elif style == "LaTeX":
        maxleaves = max(len(leaves) for leaves in stems.values()) if stems else 0
        col_format = "r|" + "l" * maxleaves
        lines  = [f"\\begin{{tabular}}{{{col_format}}}"]
        lines += [f"Stem & \multicolumn{ {maxleaves} }{{l}}{{Leaves}} \\\\ \hline"]
        for stem in sorted(stems):
            leaves = [str(l) for l in stems[stem]]
            leaves += [""] * (maxleaves - len(leaves))
            row = f"{stem} & " + " & ".join(leaves) + " \\\\"
            lines.append(row)
        lines.append("\\end{tabular}")
        return "\n".join(lines)

    else:
        raise ValueError(f"Unknown style '{style}'")

####################################################################################################
#                                          Test / example code                                     #
####################################################################################################     
def main():

    data = np.random.randint(5,15, size=100) + np.random.rand(100)

    print("\nPrint to console:\n")
    print(stem_and_leaf_plot(data, style="plain"))

    print("\nMarkdown:\n")
    print(stem_and_leaf_plot(data, style="Markdown"))

    print("\nLaTeX:\n")
    print(stem_and_leaf_plot(data, style="LaTeX"))

    print("\nCSV:\n")
    print(stem_and_leaf_plot(data, style="CSV"))

if __name__ == "__main__":
    main()       
