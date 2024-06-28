import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

# Load JSON data
with open('data/eventing/matches/2/27.json') as f:
    data = json.load(f)

# Convert JSON data to DataFrame
df = pd.json_normalize(data)

team_names = df['home_team.home_team_name'].unique()
# calculate the number of wins, draws, and losses for each team
team_wins = {}
for team in team_names:
    home_team_wins = df[df['home_score'] > df['away_score']]['home_team.home_team_name'].value_counts()
    away_team_wins = df[df['home_score'] < df['away_score']]['away_team.away_team_name'].value_counts()
    team_wins[team] = home_team_wins[team] + away_team_wins[team]
    print(f'{team} wins: {home_team_wins[team] + away_team_wins[team]}')
# plot the number of wins for each team
plt.barh(list(team_wins.keys()), list(team_wins.values()), color='orange')
plt.xlabel('Number of Wins')
plt.ylabel('Team')
plt.title('Number of Wins for Each Team')
plt.tight_layout()  # Add this line to adjust the spacing
# save the plot into current directory
plt.savefig('data/eventing/matches/2/team_wins.png')