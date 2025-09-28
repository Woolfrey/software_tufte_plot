# examples/histogram_plot.py
import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib.plots.histogram import histogram_plot

data = np.random.normal(loc=0.0, scale=1.0, size=500)

histogram_plot(data)

plt.show()
