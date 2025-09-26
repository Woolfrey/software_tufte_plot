import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib import time_series

t = np.linspace(0, 10, 20)
y = 5.0*np.sin(t) + 1.0*np.random.randn(20)

ax = time_series(t, y, color='black', alpha=0.8)
plt.show()

