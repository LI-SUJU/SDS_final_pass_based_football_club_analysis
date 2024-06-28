import json

import matplotlib.pyplot as plt

# Load the JSON data from the file
with open('generated_data/german/data.json') as f:
    data = json.load(f)

# Initialize lists to store the left and right clubs
left_clubs = []
right_clubs = []

# Iterate over the data and categorize the clubs
for club_data in data:
    club_name = list(club_data.keys())[0]
    club = club_data[club_name]
    if club['average_left_right_index'] < -2:
        right_clubs.append(club_name)
    elif club['average_left_right_index'] > 2:
        left_clubs.append(club_name)

# Generate the plot
plt.bar(['Left', 'Right'], [len(left_clubs), len(right_clubs)])
plt.xlabel('Club Position')
plt.ylabel('Count')
plt.title('Club Position Distribution')

# Add club names to the plot
plt.text(0, len(left_clubs), '\n'.join(left_clubs), ha='center', va='bottom')
plt.text(1, len(right_clubs), '\n'.join(right_clubs), ha='center', va='bottom')

plt.show()

# Generate the table