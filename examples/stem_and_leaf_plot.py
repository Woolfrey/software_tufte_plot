import matplotlib.pyplot as plt
import numpy as np
from tufteplotlib import stem_and_leaf_plot

# data = np.random.randint(1,30, size=100)

data = 5 + 10 * np.random.rand(50)

print("\nPrint to console:\n")
print(stem_and_leaf_plot(data, style="plain"))

print("\nMarkdown:\n")
print(stem_and_leaf_plot(data, style="Markdown"))

print("\nLaTeX:\n")
print(stem_and_leaf_plot(data, style="LaTeX"))

print("\nCSV:\n")
print(stem_and_leaf_plot(data, style="CSV"))
