#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import numpy as np
from typing import Dict, List, Tuple


class Alliance:
  def __init__(self, team1: int, team2: int, score: int, no_foul: int, col: str):
    if no_foul > score:
      raise ValueError("No foul score cannot be higher than Overall score.")

    self.team1 = team1
    self.team2 = team2
    self.score = score
    self.no_foul = no_foul
    self.col = col


class Match:
  def __init__(self, num: int, redAlliance: Alliance, blueAlliance: Alliance):
    self.num = num
    self.redAlliance = redAlliance
    self.blueAlliance = blueAlliance


# ------------------------
# Data Loading
# ------------------------

def load_teams(filename: str) -> Dict[int, str]:
  teams = {}

  with open(filename, "r") as f:
    for line in f:
      team_num, team_name = line.strip().split("|")
      teams[int(team_num)] = team_name

  return teams


def load_matches(filename: str) -> List[Match]:
  matches = []

  with open(filename, "r") as f:
    for i, line in enumerate(f, start=1):
      data = list(map(int, line.strip().split("|")))

      redAlliance = Alliance(data[0], data[1], data[2], data[3], "Red")
      blueAlliance = Alliance(data[4], data[5], data[6], data[7], "Blue")

      matches.append(Match(i, redAlliance, blueAlliance))

  return matches


# ------------------------
# Matrix Construction
# ------------------------

def build_matrix(matches: List[Match], teams: Dict[int, str]) -> np.ndarray:
  team_list = list(teams.keys())
  M = []

  for match in matches:
    for alliance in [match.redAlliance, match.blueAlliance]:
      row = [
        1 if team in (alliance.team1, alliance.team2) else 0
        for team in team_list
      ]
      M.append(row)

  return np.array(M), team_list


def build_score_vectors(matches: List[Match]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
  scores, no_fouls, margins = [], [], []

  for match in matches:
    r, b = match.redAlliance, match.blueAlliance

    scores.extend([[r.score], [b.score]])
    no_fouls.extend([[r.no_foul], [b.no_foul]])
    margins.extend([[r.score - b.score], [b.score - r.score]])

  return np.array(scores), np.array(no_fouls), np.array(margins)


# ------------------------
# Computation
# ------------------------

def compute_ratings(
  M: np.ndarray,
  scores: np.ndarray,
  no_fouls: np.ndarray,
  margins: np.ndarray,
):
  pinv = np.linalg.pinv(M)

  return (
    pinv @ scores,
    pinv @ no_fouls,
    pinv @ margins,
  )


# ------------------------
# Processing
# ------------------------

def to_list(arr: np.ndarray) -> List[float]:
  return [round(float(x), 3) for x in arr.flatten()]


def rank_teams(
  team_list: List[int],
  oprs: np.ndarray,
  no_fouls: np.ndarray,
  ccwms: np.ndarray,
):
  oprs_l = to_list(oprs)
  no_fouls_l = to_list(no_fouls)
  ccwms_l = to_list(ccwms)

  combined = list(zip(team_list, oprs_l, no_fouls_l, ccwms_l))
  combined.sort(key=lambda x: x[1], reverse=True)

  return combined


# ------------------------
# Output
# ------------------------

def print_table(results, teams: Dict[int, str]):
  print("\nTEAM\tOPR\tNO_FOUL\tCCWM\tTeam Name")

  for team, opr, no_foul, ccwm in results:
    print(f"{team}\t{opr}\t{no_foul}\t{ccwm}\t{teams[team]}")


def save_csv(results, teams: Dict[int, str], filename: str):
  with open(filename, "w") as f:
    f.write("team,opr,no_foul,ccwm,name\n")
    for team, opr, no_foul, ccwm in results:
      f.write(f"{team},{opr},{no_foul},{ccwm},{teams[team]}\n")


# ------------------------
# Calculate OPRs
# ------------------------

def calculate_oprs(teams, matches, end_location):
  teams = load_teams(teams)
  matches = load_matches(matches)
  if len(matches) == 0:
    print(f'no match data, so no oprs written to {end_location}')
    return []

  M, team_list = build_matrix(matches, teams)
  scores, no_fouls, margins = build_score_vectors(matches)

  oprs, no_fouls_r, ccwms = compute_ratings(M, scores, no_fouls, margins)

  results = rank_teams(team_list, oprs, no_fouls_r, ccwms)

  save_csv(results, teams, end_location)
  print(f'oprs written to {end_location}')

  return results
