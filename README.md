# FTC UK OPR Calculator

This is a tool to calculate FIRST Tech Challenge (FTC) team statistics (OPR, Foul-less OPR, CCWM). This is currently configured for UK FTC events in 2025-26.

 * OPR (Offensive Power Rating): Attempts to find each team’s robot’s average scoring contribution per match.
 * Foul-less OPR: Attempts to find each team's robot's average scoring contribution per match ignoring fouls.
 * CCWM (Calculated Contribution to Winning Margin): On average, how many more/fewer points each team's robot scored than their opponents per match.

## Quick start (macOS):
1. Install dependencies (`numpy`)
2. Configure credentials: you will need to get API access from [FTC Events](https://ftc-events.firstinspires.org/services/API). Once you have credentials, set `username` and `auth_token` in `get_data.py`.
3. To get data for a region, change the region from 'GB' in `get_oprs.py` and then run the file. You can also run the function `calculate_event_opr()` with an event code if you only want data for one event.

## What it outputs

#### `teams/<year>/teams-<event-code>.csv`:
This is a text file which contains information about the teams in the form `<team number>|<short team name>|<long team name>`

#### `matches/<year>/matches-<event-code>.csv`:
This is a text file which contains information about matches in the form `<red 1>|<red 2>|<red score>|<red score without fouls>|<blue 1>|<blue 2>|<blue score>|<blue score without fouls>`.

#### `oprs/<year>/oprs-<event-code>.csv`:
This is a text file which contains calculated information about teams for the event in the form `<team>|<opr>|<no foul opr>|<ccwm>|<name>`

#### python files:
- `get_oprs.py` - main file where everything is run from
- `calculation.py` - calculates the OPRs given team and match data
- `get_data.py` - fetches the data from the FTC API
- `into_files.py` - writes match and team data into csvs

## How OPR is calculated

Essentially you are trying to solve an overdetermined linear system of equations.

 * M: Matrix of alliances x teams where each item represents whether or not a team is in the alliance specified by the row.
 * Scores, Autos, and Margins: Single-column matrices of alliances x 1 with the scores of each alliance (Scores), autonomous scores of each alliance (Autos), and winning/losing margins for each alliance (Margins).

Finding the match statistics (OPR, Auto OPR, CCWM) for each team sets up a system of equations:

    Mx = R

where M is the matrix M, x is the statistic matrix of 1 x teams that we are solving for, and R is the results matrix, either Scores, Autos, or Margins.

Since the system is overdetermined with more equations (alliances) than variables (teams), the Python program multiplies the results matrix by the pseudo inverse of M to find the matrix x.

Math used inspired by: https://blog.thebluealliance.com/2017/10/05/the-math-behind-opr-an-introduction/

## TODO

- add config to avoid hardcoded credentials
- make easier to run for non-coders
- integrate with sheets to easily put data in