# Importing libraries
import json
import statistics
import numpy as np
import matplotlib.pyplot as plt
from os import path

# setting up the current folder to find the json file
current_folder = path.dirname(__file__)
data_test_1_loc = path.join(current_folder, "data test 1.json")
with open(data_test_1_loc) as f:
    data = json.load(f)
f.close()

# this just sorts the data for ease of use
data = np.sort(data)
# A custom function to calculate
# probability distribution function
def pdf(x):
    mean = np.mean(x)
    std = np.std(x)
    y_out = 1 / (std * np.sqrt(2 * np.pi)) * np.exp(- (x - mean) ** 2 / (2 * std ** 2))
    return y_out


# To generate an array of x-values
x = data

# To generate an array of
# y-values using corresponding x-values
y = pdf(data)

# Plotting the bell-shaped curve
plt.style.use('seaborn')
plt.figure(figsize=(6, 6))
plt.plot(x, y, color='black',
         linestyle='dashed')

plt.scatter(x, y, marker='o', s=25, color='red')
plt.show()

print(data)
# could've used the builtin mean function, but I did this for some reason
mean = 0
for i in data:
    mean += i / len(data)

# displays data
print(f"Mean: {mean}")
print(f"Median: {statistics.median(data)}")
print(f"Mode: {statistics.mode(data)}")
print(f"Standard Deviation: {statistics.pstdev(data, statistics.mean(data))}")
