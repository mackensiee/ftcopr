import requests
import base64

base_url = 'https://ftc-events.firstinspires.org/v2.0'
username = '<USERNAME>'
auth_token = '<AUTH_TOKEN>'

# create api token based on username and key
def create_basic_auth_token(username: str, api_key: str) -> str:
  token_bytes = f"{username}:{api_key}".encode("utf-8")
  token_b64 = base64.b64encode(token_bytes).decode("utf-8")
  return token_b64

# base api request
def api_request(url: str, username: str, api_key: str, params: dict = None):
  token = create_basic_auth_token(username, api_key)
  headers = {
    'Authorization': f'Basic {token}'
  }

  # Don't auto-follow redirects so we can inspect Location and preserve Auth header.
  resp = requests.get(url, headers=headers, params=params, allow_redirects=False)

  if resp.status_code in (301, 302, 303, 307, 308):
    location = resp.headers.get('Location')
    if not location:
      raise RuntimeError("Redirect without Location header")
    # Follow manually, preserving Authorization header
    resp = requests.get(location, headers=headers, params=params)

  if resp.status_code != 200:
    raise RuntimeError(f"API request failed: {resp.status_code} {resp.reason}\n{resp.text}")

  return resp.json()

# get events in a certain region
def get_events(region: str, year: int):
  events_url = f'{base_url}/{year}/events'
  events = api_request(events_url, username, auth_token)

  filtered_events = [event.get("code") for event in events["events"] 
    if event.get("regionCode") == region 
    and event.get("typeName") == 'Qualifier']

  return filtered_events

# get teams at a certain event
def get_teams(event: str, year: int):
  teams_url = f'{base_url}/{year}/teams'
  params = {"eventCode": event}
  teams = api_request(teams_url, username, auth_token, params)

  filtered_teams = [
    {
      "teamNumber": team["teamNumber"],
      "nameFull": team["nameFull"],
      "nameShort": team["nameShort"]
    }
    for team in teams["teams"]
  ]
  return filtered_teams

# get matches at a certain event
def get_matches(event: str, year: int):
  matches_url = f'{base_url}/{year}/matches/{event}'
  matches = api_request(matches_url, username, auth_token)

  qual_matches = [
    {
      **extract_alliance(match),
      "redScore": match["scoreRedFinal"],
      "redNoFoulScore": match["scoreRedFinal"] - match["scoreBlueFoul"],
      "blueScore": match["scoreBlueFinal"],
      "blueNoFoulScore": match["scoreBlueFinal"] - match["scoreRedFoul"]
    }
    for match in matches["matches"]
    if match["tournamentLevel"] == "QUALIFICATION"
  ]

  playoff_matches = [
    {
      **extract_alliance(match),
      "redScore": match["scoreRedFinal"],
      "redNoFoulScore": match["scoreRedFinal"] - match["scoreBlueFoul"],
      "blueScore": match["scoreBlueFinal"],
      "blueNoFoulScore": match["scoreBlueFinal"] - match["scoreRedFoul"]
    }
    for match in matches["matches"]
    if match["tournamentLevel"] == "PLAYOFF"
  ]

  return qual_matches, playoff_matches

# get the teams in a match with their alliance
def extract_alliance(match):
  station_map = {
    team["station"]: team["teamNumber"]
    for team in match["teams"]
  }

  return {
    "red1": station_map.get("Red1"),
    "red2": station_map.get("Red2"),
    "blue1": station_map.get("Blue1"),
    "blue2": station_map.get("Blue2"),
  }
