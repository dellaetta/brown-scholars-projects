"""Unit one final project"""

import matplotlib.pyplot as plt

""" Reading in earthquake data """
# Open the data file and skip the first line
all_quakes = open("data/quakes_project.txt")
all_quakes.readline()

# Convert each line into a list and create a list of lists
quakes_list = []
for i in all_quakes:
    quakes_list.append(i.split('\t')) # The .split() method separates the items in each line

print("Number of earthquakes in data file: ", len(quakes_list))


""" Selecting needed data """
longitude = []
latitude = []

# Get earthquakes that occurred in Central America (1970-2018)
for i in quakes_list:
  if "1970" <= i[0] <= "2018":
    if i[8] == "100":
      latitude.append(float(i[6]))
      longitude.append(float(i[7]))
print("Latitude: ", len(latitude))
print("Longitude: ", len(longitude))


""" Making the graph """
plt.clf() # clears leftover plots

# Add image behind plot
image = plt.imread("data/earth.jpg")
fig, ax = plt.subplots()
ax.imshow(image, extent = [-180,180,-90,90])

# Crop image to needed region
plt.xlim(-100,-70)
plt.ylim(0,25)

# Create scatter plot
plt.scatter(longitude, latitude, label = "Earthquakes", s = 15, marker = "x", c = "red")
plt.title("Earthquake Locations in Central America From 1970-2018")
plt.ylabel("Latitude")
plt.xlabel("Longitude")
plt.legend()
plt.savefig("quakes_graph.png", dpi = 1000)
plt.show()
