import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib import time_series

t = np.linspace(0, 10, 10)

y = 5.0*np.sin(t) + 1.0*np.random.randn(10)

ax = time_series(t, y)

plt.show()
