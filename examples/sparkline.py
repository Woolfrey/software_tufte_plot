import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib.plots.sparkline import sparkline

y = np.random.normal(0, 1, 30).cumsum()

sparkline(y, show_dots=True, show_labels=True)

plt.show()
