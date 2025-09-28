import numpy as np
import matplotlib.pyplot as plt
from tufteplotlib import quartile_plot

# Define parameters per category
params = {
    "Lowenstein": {"mu": 5, "sigma": 3, "n": 100},
    "Sneed": {"mu": 6, "sigma": 2, "n": 100},
    "Zweig": {"mu": 7, "sigma": 1, "n": 100}
}

categories = []
values = []

for cat, p in params.items():
    data = np.random.normal(loc=p["mu"], scale=p["sigma"], size=p["n"])
    categories.extend([cat]*p["n"])
    values.extend(data)

# Create the barcode plot
ax = quartile_plot(categories, values)

plt.show()
