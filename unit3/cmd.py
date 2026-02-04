"""
Unit three final project: CMD for star cluster
Make a Color Magnitude Diagram for assigned star cluster (Praesepe)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mpl

""" .loc[] indexing """
sample_df = pd.DataFrame({"Smartphone": ["iPhone 11", "Samsung Galaxy S20", "Google Pixel 4", "LG V60", 
    "Nokia 9", "Sony Xperia 1", "iPhone SE"], "Price": [700,1000,800,700,450,1000,399]})
sample_df["Smartphone"].loc[sample_df["Price"] == 700]

# All the values from the "Smartphone" column where the value on that same row in the "Price" column is equal to 1000
sample_df["Smartphone"].loc[sample_df["Price"] == 1000]

# Select all the values from the "Price" column where the value on that same row in the "Smartphone" column
# contains the word "iPhone"
sample_df["Price"].loc[sample_df["Smartphone"].str.contains("iPhone")]

# Select all the values from the "Smartphone" column where the value on that same row in the "Price" column 
# is less than or equal to 700.
sample_df["Smartphone"].loc[sample_df["Price"] <= 700]

""" Finding absolute magnitude """
# absolute magnitude = G - 5 * log(distance) + 5
df = pd.read_csv("data/oh_table.csv")

# Find the log of distance:
distance = df["distance"].loc[df["group_id"] == 6]
g = df["G"].loc[df["group_id"] == 6]
j = df["J"].loc[df["group_id"] == 6]

absolute_magnitude = g - 5 * np.log10(distance) + 5
color = g - j
print(absolute_magnitude)

""" Create CMD graph """
plt.scatter(color,absolute_magnitude)
plt.title("Praesepe Color Magnitude Diagram")
plt.xlabel("Color")
plt.ylabel("Absolute Magnitude")
plt.show()

# Adding sun
sun_g = 5.12
sun_j = 3.64
sun_distance = 1
sun_color = sun_g - sun_j
sun_absolute_magnitude = sun_g - 5 * np.log10(sun_distance) + 5

plt.scatter(color,absolute_magnitude)
plt.scatter(sun_color, sun_absolute_magnitude)
plt.title("Praesepe Color Magnitude Diagram")
plt.xlabel("Color")
plt.ylabel("Absolute Magnitude")
plt.show()

# Adding color map
cm = plt.get_cmap("RdYlBu")
plt.scatter(color,absolute_magnitude,c=absolute_magnitude, cmap=cm)
plt.scatter(sun_color, sun_absolute_magnitude)
plt.title("Praesepe Color Magnitude Diagram")
plt.xlabel("Color")
plt.ylabel("Absolute Magnitude")
plt.show()

# Create histograms for the absolute magnitude and color of Praesepe
plt.hist(absolute_magnitude)
plt.hist(color)
plt.show()