from calculation import calculate_oprs
from get_data import get_events, get_teams, get_matches
from into_files import write_teams_csv, write_matches_csv, write_oprs_csv

def main():
  year = 2025
  event_codes = get_events('GB', year)
  print(event_codes)

  combined_oprs_file_path = f'./oprs/{year}/oprs-gb.csv'
  with open(combined_oprs_file_path, "w"):
    pass

  for event in event_codes:
    calculate_event_opr(event, year, combined_oprs_file_path)

def calculate_event_opr(event, year, combined_oprs_file_path):
  print(f'writing event: {event}')
  teams_file_path = f'./teams/{year}/teams-{event}.csv'
  matches_file_path = f'./matches/{year}/matches-{event}.csv'
  oprs_file_path = f'./oprs/{year}/oprs-{event}.csv'

  teams = get_teams(event, year)
  write_teams_csv(teams, teams_file_path)

  quals, playoffs = get_matches(event, year)
  write_matches_csv(quals, matches_file_path)

  results, teams = calculate_oprs(teams_file_path, matches_file_path)
  if len(results) != 0:
    write_oprs_csv(results, teams, "w", oprs_file_path)
    write_oprs_csv(results, teams, "a", combined_oprs_file_path, event)

if __name__ == "__main__":
  main()
