import requests
import pandas as pd
import matplotlib.pyplot as plt

apiKey = "YOUR_API_KEY_HERE"
url = "https://api.football-data.org/v4/competitions/PL/matches"
headers = {"X-Auth-Token": apiKey}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    print("API call worked—let’s roll!")
else:
    print(f"Oof, status code {response.status_code}. Check your key or internet.")
    exit()

name, location, goals = ([] for i in range(3))

for match in response.json()['matches']:
    homeTeam = match['homeTeam']['name']
    homeGoals = match['score']['fullTime']['home'] if match['score']['fullTime']['home'] else 0
    awayTeam = match['awayTeam']['name']
    awayGoals = match['score']['fullTime']['away'] if match['score']['fullTime']['away'] else 0
    
    name.append(homeTeam)
    location.append('home')
    goals.append(homeGoals)
    name.append(awayTeam)
    location.append('away')
    goals.append(awayGoals)

team_data = pd.DataFrame({
    "name": name,
    "away/home": location,
    "goals": goals,
})

goals_by_team_loc = team_data.groupby(['name', 'away/home'])["goals"].sum().unstack().fillna(0)

total_goals = goals_by_team_loc.sum(axis=1)  # Sum home + away per team
top_5_teams = total_goals.nlargest(5).index  # Top 5 team names
top_5_data = goals_by_team_loc.loc[top_5_teams]  # Filter to those teams
top_5_data = top_5_data.sort_values(by='home', ascending=True)  # Sort by home goals (or use 'away' or total)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), sharey=True)

top_5_data['home'].plot(kind="barh", ax=ax1, color="skyblue", edgecolor="black")
ax1.set_title("Home Goals - Top 5 Teams")
ax1.set_xlabel("Goals")
ax1.set_ylabel("Teams")

top_5_data['away'].plot(kind="barh", ax=ax2, color="orange", edgecolor="black")
ax2.set_title("Away Goals - Top 5 Teams")
ax2.set_xlabel("Goals")

plt.tight_layout()
plt.savefig("home_away_goals.png")
plt.show()

team_data.to_csv("team_goals_table.csv", index=False)
print("Saved table to 'team_goals_table.csv' and chart to 'home_away_goals.png'!")
