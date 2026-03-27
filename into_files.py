import csv
from typing import Dict

# write teams into csvs
def write_teams_csv(teams, file_name):
  with open(file_name, "w", newline="") as f:
    writer = csv.writer(f, delimiter="|")

    for team in teams:
      team_number = team["teamNumber"]
      short = team["nameShort"]
      full = team["nameFull"] or ""
      name = f"{short} - {full}" if full else short
      writer.writerow([team_number, name])
    print(f'teams written to {file_name}')

# write matches into csvs
def write_matches_csv(matches, file_name):
  with open(file_name, "w", newline="") as f:
    writer = csv.writer(f, delimiter="|")

    for match in matches:
      red1 = match["red1"]
      red2 = match["red2"]
      redScore = match["redScore"]
      redNoFoulScore = match["redNoFoulScore"]
      blue1 = match["blue1"]
      blue2 = match["blue2"]
      blueScore = match["blueScore"]
      blueNoFoulScore = match["blueNoFoulScore"]
      writer.writerow([red1, red2, redScore, redNoFoulScore, blue1, blue2, blueScore, blueNoFoulScore])
    print(f'matches written to {file_name}')

def write_oprs_csv(results, teams: Dict[int, str], type: str, file_name: str, event = ""):
  with open(file_name, type) as f:
    for team, opr, no_foul, ccwm in results:
      if event != "":
        f.write(f"{team}|{opr}|{no_foul}|{ccwm}|{teams[team]}|{event}\n")
      else:
        f.write(f"{team}|{opr}|{no_foul}|{ccwm}|{teams[team]}\n")
    print(f'oprs written to {file_name}')
