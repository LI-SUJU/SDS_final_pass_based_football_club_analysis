import json
from scipy.ndimage import gaussian_filter1d

import matplotlib.pyplot as plt
import numpy as np

# Read the JSON data from the file
data = []
with open('generated_data/england/data.json', 'r') as file:
    data = json.load(file)
with open('generated_data/spain/data.json', 'r') as file:
    data += json.load(file)
with open('generated_data/italy/data.json', 'r') as file:
    data += json.load(file)
with open('generated_data/german/data.json', 'r') as file:
    data += json.load(file)

# Extract the left_right_index values
# left_right_index_values = [team_data[list(team_data.keys())[0]]['average_left_right_index'] for team_data in data]

# # Define the range for the left-right index values
# range_start = -6
# range_end = 6
# range_step = 0.1

# # Calculate the probability distribution within the range
# total_values = len(left_right_index_values)
# probability_distribution = {}
# current_value = range_start
# while current_value <= range_end:
#     count = sum(1 for value in left_right_index_values if current_value <= value < current_value + range_step)
#     probability = count / total_values
#     probability_distribution[current_value] = probability
#     current_value += range_step

# # Plot the probability distribution
# plt.bar(probability_distribution.keys(), probability_distribution.values(), color='orange')
# plt.xlabel('Left-Right Index')
# plt.ylabel('Probability')
# plt.title('Probability Distribution of Left-Right Index')
# plt.grid(True)

# # Smooth the probability distribution using a bell curve
# smoothed_values = gaussian_filter1d(list(probability_distribution.values()), sigma=1)
# plt.plot(probability_distribution.keys(), smoothed_values, color='blue')

# # Add vertical lines to indicate different zones of distribution
# plt.axvline(x=-2, color='red', linestyle='--')
# plt.axvline(x=2, color='green', linestyle='--')

# # Add text labels for the zones
# plt.text(-5, 0.02, 'right play', color='red')
# plt.text(3, 0.02, 'left play', color='green')

# # Plot the x-axis numbers
# plt.xticks(np.arange(range_start, range_end+1, 1))

# plt.savefig('generated_data/left_right_index_distribution.png')

# extract the forward_backward_index values
forward_backward_index_values = [team_data[list(team_data.keys())[0]]['average_forward_backward_index'] for team_data in data]

# Define the range for the forward-backward index values
range_start = -15
range_end = 10
range_step = 0.1

# Calculate the probability distribution within the range
total_values = len(forward_backward_index_values)
probability_distribution = {}
current_value = range_start
while current_value <= range_end:
    count = sum(1 for value in forward_backward_index_values if current_value <= value < current_value + range_step)
    probability = count / total_values
    probability_distribution[current_value] = probability
    current_value += range_step

# Plot the probability distribution
plt.bar(probability_distribution.keys(), probability_distribution.values(), color='orange')
plt.xlabel('Forward-Backward Index')
plt.ylabel('Probability')
plt.title('Probability Distribution of Forward-Backward Index')
plt.grid(True)

# Smooth the probability distribution using a bell curve
smoothed_values = gaussian_filter1d(list(probability_distribution.values()), sigma=1)
plt.plot(probability_distribution.keys(), smoothed_values, color='blue')

# Add vertical lines to indicate different zones of distribution
plt.axvline(x=-6, color='red', linestyle='--')
plt.axvline(x=0, color='green', linestyle='--')

# plot the value of the two lines in x-axis using colors
plt.text(-6.5, -0.003, '-6', color='red')
# plt.text(0.5, -0.008, '0', color='green')

# Add text labels for the zones
plt.text(-14, 0.02, 'backward play', color='red')
plt.text(1, 0.02, 'forward play', color='green')

# Plot the x-axis numbers
# plt.xticks(np.arange(range_start, range_end+1, 1))

plt.savefig('generated_data/forward_backward_index_distribution.png')

# # extract the dispersionIndex values
# dispersionIndex_values = [team_data[list(team_data.keys())[0]]['average_dispersionIndex'] for team_data in data]
# for values in dispersionIndex_values:
#     if values < 10:
#         print(values)
# # Define the range for the dispersion index values
# range_start = 15
# range_end = 19
# range_step = 0.1

# # Calculate the probability distribution within the range
# total_values = len(dispersionIndex_values)
# probability_distribution = {}
# current_value = range_start
# while current_value <= range_end:
#     count = sum(1 for value in dispersionIndex_values if current_value <= value < current_value + range_step)
#     probability = count / total_values
#     probability_distribution[current_value] = probability
#     current_value += range_step

# # Plot the probability distribution
# plt.bar(probability_distribution.keys(), probability_distribution.values(), color='orange')
# plt.xlabel('Dispersion Index')
# plt.ylabel('Probability')
# plt.title('Probability Distribution of Dispersion Index')
# plt.grid(True)

# # Smooth the probability distribution using a bell curve
# smoothed_values = gaussian_filter1d(list(probability_distribution.values()), sigma=1)
# plt.plot(probability_distribution.keys(), smoothed_values, color='blue')

# # Add vertical lines to indicate different zones of distribution
# plt.axvline(x=16.5, color='red', linestyle='--')
# plt.axvline(x=17.5, color='green', linestyle='--')
# # plot the value of the two lines in x-axis using colors
# plt.text(16.3, -0.008, '16.5', color='red')
# plt.text(17.3, -0.008, '17.5', color='green')
# # Add text labels for the zones
# plt.text(15, 0.05, 'compressed play', color='red')
# plt.text(18, 0.05, 'wing play', color='green')

# # Plot the x-axis numbers
# # plt.xticks(list(probability_distribution.keys()))

# plt.savefig('generated_data/dispersion_index_distribution.png')