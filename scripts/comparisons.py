import numpy as np
import matplotlib.pyplot as plt
import tufteplotlib as tpl

####################################################################################################
#                                          BAR CHART                                               #
####################################################################################################
categories = ["Satiety", "Triumvirate", "Gourmand", "Machiavellian", "Boudoir"]
values = np.random.randint(3, 20, size=len(categories))

x = np.linspace(0, 10, 50)
y = np.sin(x) + 0.2 * np.random.randn(len(x))

x_scatter = np.random.randn(100)
y_scatter = x_scatter * 0.5 + 0.2 * np.random.randn(100)

fig, axs = plt.subplots(1, 2, figsize=(10, 4))

# Tufteplotlib version (left)
tpl.bar_chart(categories, values, ax=axs[0])

# Matplotlib version (right, horizontal bars)
axs[1].barh(categories, values)

fig.subplots_adjust(wspace=0.4)  # increase horizontal spacing

####################################################################################################
#                                        BARCODE PLOT                                              #
####################################################################################################

# Example data for barcode / interquartile plots
params = {
    "Lowenstein": {"mu": 5, "sigma": 3, "n": 50},
    "Zweig"     : {"mu": 7, "sigma": 2, "n": 50},
    "Monroe"    : {"mu": 6, "sigma": 1, "n": 50}
}

categories = []
observations = []

for cat, p in params.items():
    data = np.random.normal(loc=p["mu"], scale=p["sigma"], size=p["n"])
    categories.extend([cat]*p["n"])
    observations.extend(data)

# Compare Tufte barcode vs. Matplotlib boxplot
fig, axs = plt.subplots(1, 2, figsize=(10, 4))

# Tufteplotlib barcode plot (left)
tpl.barcode_plot(categories, observations, ax=axs[0])

# Matplotlib boxplot (right, shows interquartile range)
# group data by category
grouped_data = []
labels = []
for cat in params.keys():
    cat_data = [val for c, val in zip(categories, observations) if c == cat]
    grouped_data.append(cat_data)
    labels.append(cat)

axs[1].boxplot(grouped_data, labels=labels, vert=True, patch_artist=True)

####################################################################################################
#                                        COLUMN CHART                                              #
####################################################################################################

categories = [
    "North\nHaverbrook", "Ogdenville", "Cypress\nCreek",
    "Brockway"
]
values = np.random.randint(3, 20, size=len(categories))

fig, axs = plt.subplots(1, 2, figsize=(10, 4))

# Tufteplotlib column chart (left)
tpl.column_chart(categories, values, ax=axs[0])

# Matplotlib vertical bar chart (right)
axs[1].bar(categories, values)

####################################################################################################
#                                        DENSITY PLOT                                              #
####################################################################################################

# Example data
data = np.random.normal(loc=0, scale=1, size=500)

fig, axs = plt.subplots(1, 2, figsize=(10, 4))

# Tufteplotlib density plot (left)
tpl.density_plot(data, ax=axs[0])

# Matplotlib histogram (right, density normalized)
axs[1].hist(data, bins=30, density=True, alpha=0.7, edgecolor="black")

####################################################################################################
#                                        HISTOGRAM PLOT                                            #
####################################################################################################

# Example data
data = np.random.normal(loc=0.0, scale=1.0, size=100)

fig, axs = plt.subplots(1, 2, figsize=(10, 4))

# Tufteplotlib histogram (left)
tpl.histogram_plot(data, ax=axs[0])

# Matplotlib histogram (right)
axs[1].hist(data, bins=10, edgecolor="black", alpha=0.7)

####################################################################################################
#                                          LINE PLOT                                               #
####################################################################################################

# Example data
t = np.linspace(0, 10, 200)
y = np.sin(t)
y_noisy = y + np.random.normal(0, 0.1, size=t.shape)

fig, axs = plt.subplots(1, 2, figsize=(10, 1))

# Tufteplotlib line plot (left)
tpl.line_plot(t, y_noisy, ax=axs[0])

# Matplotlib line plot (right)
axs[1].plot(t, y_noisy, label="Noisy sine")
axs[1].legend()

####################################################################################################
#                                        QUARTILE vs BOX                                           #
####################################################################################################

params = {
    "Riviera" : {"mu": 5, "sigma": 3, "n": 100},
    "Hibbert" : {"mu": 6, "sigma": 2, "n": 100},
    "Zweig"   : {"mu": 7, "sigma": 1, "n": 100}
}

categories = []
values = []

for cat, p in params.items():
    data = np.random.normal(loc=p["mu"], scale=p["sigma"], size=p["n"])
    categories.extend([cat]*p["n"])
    values.extend(data)

fig, axs = plt.subplots(1, 2, figsize=(10, 4))

# Tufteplotlib quartile plot (left)
tpl.quartile_plot(categories, values, ax=axs[0])

# Matplotlib box plot (right)
grouped_data = []
labels = []
for cat in params.keys():
    cat_data = [val for c, val in zip(categories, values) if c == cat]
    grouped_data.append(cat_data)
    labels.append(cat)

axs[1].boxplot(grouped_data, labels=labels, vert=True, patch_artist=True)

####################################################################################################
#                                   SCATTER PLOT (Anscombe)                                        #
####################################################################################################

import random
from tufteplotlib.datasets import anscombe

# Pick a random dataset from Anscombe's quartet
dataset = random.choice(list(anscombe.keys()))
data = anscombe[dataset]

# Split into x and y
x, y = data[:, 0], data[:, 1]

fig, axs = plt.subplots(1, 2, figsize=(10, 4))

# Tufteplotlib scatter plot (left)
tpl.scatter_plot(x, y, ax=axs[0])

# Matplotlib scatter plot (right)
axs[1].scatter(x, y, edgecolor="black", alpha=0.7)

####################################################################################################
#                                       TIME SERIES PLOT                                           #
####################################################################################################

# Example data
t = np.linspace(0, 10, 10)
y = 5.0 * np.sin(t) + 1.0 * np.random.randn(10)

fig, axs = plt.subplots(1, 2, figsize=(10, 2))

# Tufteplotlib time series (left)
tpl.time_series(t, y, ax=axs[0])

# Matplotlib time series (right)
axs[1].plot(t, y, marker="o", linestyle="-")

plt.tight_layout()
plt.show()
