import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib.plots.line import line_plot  # adjust import if necessary

# Generate example data
t = np.linspace(0, 10, 200)

# Base signals
y1 = np.sin(t)

# Add noise
noise_level = 0.1
y1_noisy = y1 + np.random.normal(0, noise_level, size=t.shape)

# Plot noisy lines
line_plot(t, y1_noisy)

plt.tight_layout()

plt.show()
