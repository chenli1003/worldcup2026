#!/usr/bin/env python3
"""
2026世界杯数据构建脚本
从 MCP 工具返回的数据构建 worldcup-live.json
直接在 Python 中硬编码数据结构（从已获取的 MCP 数据）
"""

import json, os, sys

# ============================================================
# 数据来源：MCP 工具调用结果（2026-06-20 20:49）
# ============================================================

# 积分榜数据 (from get_standings)
STANDINGS = {
  "year": 2026,
  "groups": {
    "A": [
      {"team": "Mexico", "played": 2, "won": 2, "drawn": 0, "lost": 0, "goalsFor": 3, "goalsAgainst": 0, "goalDifference": 3, "points": 6, "fairPlay": -5, "position": 1, "advanced": True},
      {"team": "Korea Republic", "played": 2, "won": 1, "drawn": 0, "lost": 1, "goalsFor": 2, "goalsAgainst": 2, "goalDifference": 0, "points": 3, "fairPlay": -3, "position": 2, "advanced": True},
      {"team": "Czechia", "played": 2, "won": 0, "drawn": 1, "lost": 1, "goalsFor": 2, "goalsAgainst": 3, "goalDifference": -1, "points": 1, "fairPlay": -1, "position": 3, "advanced": True},
      {"team": "South Africa", "played": 2, "won": 0, "drawn": 1, "lost": 1, "goalsFor": 1, "goalsAgainst": 3, "goalDifference": -2, "points": 1, "fairPlay": -12, "position": 4}
    ],
    "B": [
      {"team": "Canada", "played": 2, "won": 1, "drawn": 1, "lost": 0, "goalsFor": 7, "goalsAgainst": 1, "goalDifference": 6, "points": 4, "fairPlay": -3, "position": 1, "advanced": True},
      {"team": "Switzerland", "played": 2, "won": 1, "drawn": 1, "lost": 0, "goalsFor": 5, "goalsAgainst": 2, "goalDifference": 3, "points": 4, "fairPlay": -2, "position": 2, "advanced": True},
      {"team": "Bosnia and Herzegovina", "played": 2, "won": 0, "drawn": 1, "lost": 1, "goalsFor": 2, "goalsAgainst": 5, "goalDifference": -3, "points": 1, "fairPlay": -9, "position": 3, "advanced": True},
      {"team": "Qatar", "played": 2, "won": 0, "drawn": 1, "lost": 1, "goalsFor": 1, "goalsAgainst": 7, "goalDifference": -6, "points": 1, "fairPlay": -11, "position": 4}
    ],
    "C": [
      {"team": "Brazil", "played": 2, "won": 1, "drawn": 1, "lost": 0, "goalsFor": 4, "goalsAgainst": 1, "goalDifference": 3, "points": 4, "fairPlay": -3, "position": 1, "advanced": True},
      {"team": "Morocco", "played": 2, "won": 1, "drawn": 1, "lost": 0, "goalsFor": 2, "goalsAgainst": 1, "goalDifference": 1, "points": 4, "fairPlay": -1, "position": 2, "advanced": True},
      {"team": "Scotland", "played": 2, "won": 1, "drawn": 0, "lost": 1, "goalsFor": 1, "goalsAgainst": 1, "goalDifference": 0, "points": 3, "fairPlay": -5, "position": 3, "advanced": True},
      {"team": "Haiti", "played": 2, "won": 0, "drawn": 0, "lost": 2, "goalsFor": 0, "goalsAgainst": 4, "goalDifference": -4, "points": 0, "fairPlay": -4, "position": 4}
    ],
    "D": [
      {"team": "USA", "played": 2, "won": 2, "drawn": 0, "lost": 0, "goalsFor": 6, "goalsAgainst": 1, "goalDifference": 5, "points": 6, "fairPlay": -4, "position": 1, "advanced": True},
      {"team": "Australia", "played": 2, "won": 1, "drawn": 0, "lost": 1, "goalsFor": 2, "goalsAgainst": 2, "goalDifference": 0, "points": 3, "fairPlay": -4, "position": 2, "advanced": True},
      {"team": "Paraguay", "played": 2, "won": 1, "drawn": 0, "lost": 1, "goalsFor": 2, "goalsAgainst": 4, "goalDifference": -2, "points": 3, "fairPlay": -10, "position": 3, "advanced": True},
      {"team": "Türkiye", "played": 2, "won": 0, "drawn": 0, "lost": 2, "goalsFor": 0, "goalsAgainst": 3, "goalDifference": -3, "points": 0, "fairPlay": -2, "position": 4}
    ],
    "E": [
      {"team": "Germany", "played": 1, "won": 1, "drawn": 0, "lost": 0, "goalsFor": 7, "goalsAgainst": 1, "goalDifference": 6, "points": 3, "fairPlay": 0, "position": 1, "advanced": True},
      {"team": "Côte d'Ivoire", "played": 1, "won": 1, "drawn": 0, "lost": 0, "goalsFor": 1, "goalsAgainst": 0, "goalDifference": 1, "points": 3, "fairPlay": -3, "position": 2, "advanced": True},
      {"team": "Ecuador", "played": 1, "won": 0, "drawn": 0, "lost": 1, "goalsFor": 0, "goalsAgainst": 1, "goalDifference": -1, "points": 0, "fairPlay": -1, "position": 3, "advanced": False},
      {"team": "Curaçao", "played": 1, "won": 0, "drawn": 0, "lost": 1, "goalsFor": 1, "goalsAgainst": 7, "goalDifference": -6, "points": 0, "fairPlay": 0, "position": 4}
    ],
    "F": [
      {"team": "Sweden", "played": 1, "won": 1, "drawn": 0, "lost": 0, "goalsFor": 5, "goalsAgainst": 1, "goalDifference": 4, "points": 3, "fairPlay": 0, "position": 1, "advanced": True},
      {"team": "Japan", "played": 1, "won": 0, "drawn": 1, "lost": 0, "goalsFor": 2, "goalsAgainst": 2, "goalDifference": 0, "points": 1, "fairPlay": 0, "position": 2, "advanced": True},
      {"team": "Netherlands", "played": 1, "won": 0, "drawn": 1, "lost": 0, "goalsFor": 2, "goalsAgainst": 2, "goalDifference": 0, "points": 1, "fairPlay": -3, "position": 3, "advanced": True},
      {"team": "Tunisia", "played": 1, "won": 0, "drawn": 0, "lost": 1, "goalsFor": 1, "goalsAgainst": 5, "goalDifference": -4, "points": 0, "fairPlay": -1, "position": 4}
    ],
    "G": [
      {"team": "New Zealand", "played": 1, "won": 0, "drawn": 1, "lost": 0, "goalsFor": 2, "goalsAgainst": 2, "goalDifference": 0, "points": 1, "fairPlay": 0, "position": 1, "advanced": True},
      {"team": "IR Iran", "played": 1, "won": 0, "drawn": 1, "lost": 0, "goalsFor": 2, "goalsAgainst": 2, "goalDifference": 0, "points": 1, "fairPlay": -1, "position": 2, "advanced": True},
      {"team": "Belgium", "played": 1, "won": 0, "drawn": 1, "lost": 0, "goalsFor": 1, "goalsAgainst": 1, "goalDifference": 0, "points": 1, "fairPlay": -2, "position": None, "advanced": True},
      {"team": "Egypt", "played": 1, "won": 0, "drawn": 1, "lost": 0, "goalsFor": 1, "goalsAgainst": 1, "goalDifference": 0, "points": 1, "fairPlay": -2, "position": None, "advanced": True}
    ],
    "H": [
      {"team": "Uruguay", "played": 1, "won": 0, "drawn": 1, "lost": 0, "goalsFor": 1, "goalsAgainst": 1, "goalDifference": 0, "points": 1, "fairPlay": 0, "position": 1, "advanced": True},
      {"team": "Saudi Arabia", "played": 1, "won": 0, "drawn": 1, "lost": 0, "goalsFor": 1, "goalsAgainst": 1, "goalDifference": 0, "points": 1, "fairPlay": -1, "position": 2, "advanced": True},
      {"team": "Spain", "played": 1, "won": 0, "drawn": 1, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalDifference": 0, "points": 1, "fairPlay": -1, "position": None, "advanced": True},
      {"team": "Cabo Verde", "played": 1, "won": 0, "drawn": 1, "lost": 0, "goalsFor": 0, "goalsAgainst": 0, "goalDifference": 0, "points": 1, "fairPlay": -1, "position": None, "advanced": False}
    ],
    "I": [
      {"team": "Norway", "played": 1, "won": 1, "drawn": 0, "lost": 0, "goalsFor": 4, "goalsAgainst": 1, "goalDifference": 3, "points": 3, "fairPlay": 0, "position": 1, "advanced": True},
      {"team": "France", "played": 1, "won": 1, "drawn": 0, "lost": 0, "goalsFor": 3, "goalsAgainst": 1, "goalDifference": 2, "points": 3, "fairPlay": 0, "position": 2, "advanced": True},
      {"team": "Senegal", "played": 1, "won": 0, "drawn": 0, "lost": 1, "goalsFor": 1, "goalsAgainst": 3, "goalDifference": -2, "points": 0, "fairPlay": 0, "position": 3, "advanced": False},
      {"team": "Iraq", "played": 1, "won": 0, "drawn": 0, "lost": 1, "goalsFor": 1, "goalsAgainst": 4, "goalDifference": -3, "points": 0, "fairPlay": -1, "position": 4}
    ],
    "J": [
      {"team": "Argentina", "played": 1, "won": 1, "drawn": 0, "lost": 0, "goalsFor": 3, "goalsAgainst": 0, "goalDifference": 3, "points": 3, "fairPlay": 0, "position": 1, "advanced": True},
      {"team": "Austria", "played": 1, "won": 1, "drawn": 0, "lost": 0, "goalsFor": 3, "goalsAgainst": 1, "goalDifference": 2, "points": 3, "fairPlay": -1, "position": 2, "advanced": True},
      {"team": "Jordan", "played": 1, "won": 0, "drawn": 0, "lost": 1, "goalsFor": 1, "goalsAgainst": 3, "goalDifference": -2, "points": 0, "fairPlay": 0, "position": 3, "advanced": False},
      {"team": "Algeria", "played": 1, "won": 0, "drawn": 0, "lost": 1, "goalsFor": 0, "goalsAgainst": 3, "goalDifference": -3, "points": 0, "fairPlay": 0, "position": 4}
    ],
    "K": [
      {"team": "Colombia", "played": 1, "won": 1, "drawn": 0, "lost": 0, "goalsFor": 3, "goalsAgainst": 1, "goalDifference": 2, "points": 3, "fairPlay": -1, "position": 1, "advanced": True},
      {"team": "Congo DR", "played": 1, "won": 0, "drawn": 1, "lost": 0, "goalsFor": 1, "goalsAgainst": 1, "goalDifference": 0, "points": 1, "fairPlay": -1, "position": 2, "advanced": True},
      {"team": "Portugal", "played": 1, "won": 0, "drawn": 1, "lost": 0, "goalsFor": 1, "goalsAgainst": 1, "goalDifference": 0, "points": 1, "fairPlay": -3, "position": 3, "advanced": True},
      {"team": "Uzbekistan", "played": 1, "won": 0, "drawn": 0, "lost": 1, "goalsFor": 1, "goalsAgainst": 3, "goalDifference": -2, "points": 0, "fairPlay": -1, "position": 4}
    ],
    "L": [
      {"team": "England", "played": 1, "won": 1, "drawn": 0, "lost": 0, "goalsFor": 4, "goalsAgainst": 2, "goalDifference": 2, "points": 3, "fairPlay": 0, "position": 1, "advanced": True},
      {"team": "Ghana", "played": 1, "won": 1, "drawn": 0, "lost": 0, "goalsFor": 1, "goalsAgainst": 0, "goalDifference": 1, "points": 3, "fairPlay": -1, "position": 2, "advanced": True},
      {"team": "Panama", "played": 1, "won": 0, "drawn": 0, "lost": 1, "goalsFor": 0, "goalsAgainst": 1, "goalDifference": -1, "points": 0, "fairPlay": -2, "position": 3, "advanced": False},
      {"team": "Croatia", "played": 1, "won": 0, "drawn": 0, "lost": 1, "goalsFor": 2, "goalsAgainst": 4, "goalDifference": -2, "points": 0, "fairPlay": 0, "position": 4}
    ]
  }
}

# 淘汰赛对阵 (from get_bracket)
BRACKET = {
  "year": 2026,
  "stages": {
    "round_of_32": [
      {"matchNo": 73, "stage": "round_of_32", "home": "Korea Republic", "away": "Switzerland", "homeScore": None, "awayScore": None, "city": "Inglewood", "stadium": "Los Angeles Stadium", "kickoff": "2026-06-28T19:00:00.000Z"},
      {"matchNo": 74, "stage": "round_of_32", "home": "Germany", "away": "Scotland", "homeScore": None, "awayScore": None, "city": "Foxborough", "stadium": "Boston Stadium", "kickoff": "2026-06-29T20:30:00.000Z"},
      {"matchNo": 75, "stage": "round_of_32", "home": "Sweden", "away": "Morocco", "homeScore": None, "awayScore": None, "city": "Guadalupe", "stadium": "Monterrey Stadium", "kickoff": "2026-06-30T01:00:00.000Z"},
      {"matchNo": 76, "stage": "round_of_32", "home": "Brazil", "away": "Japan", "homeScore": None, "awayScore": None, "city": "Houston", "stadium": "Houston Stadium", "kickoff": "2026-06-29T17:00:00.000Z"},
      {"matchNo": 77, "stage": "round_of_32", "home": "Norway", "away": "Paraguay", "homeScore": None, "awayScore": None, "city": "East Rutherford", "stadium": "New York/New Jersey Stadium", "kickoff": "2026-06-30T21:00:00.000Z"},
      {"matchNo": 78, "stage": "round_of_32", "home": "Côte d'Ivoire", "away": "France", "homeScore": None, "awayScore": None, "city": "Arlington", "stadium": "Dallas Stadium", "kickoff": "2026-06-30T17:00:00.000Z"},
      {"matchNo": 79, "stage": "round_of_32", "home": "Mexico", "away": "Netherlands", "homeScore": None, "awayScore": None, "city": "Ciudad de México", "stadium": "Mexico City Stadium", "kickoff": "2026-07-01T01:00:00.000Z"},
      {"matchNo": 80, "stage": "round_of_32", "home": "England", "away": "Portugal", "homeScore": None, "awayScore": None, "city": "Atlanta", "stadium": "Atlanta Stadium", "kickoff": "2026-07-01T16:00:00.000Z"},
      {"matchNo": 81, "stage": "round_of_32", "home": "USA", "away": "Bosnia and Herzegovina", "homeScore": None, "awayScore": None, "city": "Santa Clara", "stadium": "San Francisco Bay Area Stadium", "kickoff": "2026-07-02T00:00:00.000Z"},
      {"matchNo": 82, "stage": "round_of_32", "home": "New Zealand", "away": "Spain", "homeScore": None, "awayScore": None, "city": "Seattle", "stadium": "Seattle Stadium", "kickoff": "2026-07-01T20:00:00.000Z"},
      {"matchNo": 83, "stage": "round_of_32", "home": "Congo DR", "away": "Ghana", "homeScore": None, "awayScore": None, "city": "Toronto", "stadium": "Toronto Stadium", "kickoff": "2026-07-02T23:00:00.000Z"},
      {"matchNo": 84, "stage": "round_of_32", "home": "Uruguay", "away": "Austria", "homeScore": None, "awayScore": None, "city": "Inglewood", "stadium": "Los Angeles Stadium", "kickoff": "2026-07-02T19:00:00.000Z"},
      {"matchNo": 85, "stage": "round_of_32", "home": "Canada", "away": "Belgium", "homeScore": None, "awayScore": None, "city": "Vancouver", "stadium": "BC Place Vancouver", "kickoff": "2026-07-03T03:00:00.000Z"},
      {"matchNo": 86, "stage": "round_of_32", "home": "Argentina", "away": "Saudi Arabia", "homeScore": None, "awayScore": None, "city": "Miami Gardens", "stadium": "Miami Stadium", "kickoff": "2026-07-03T22:00:00.000Z"},
      {"matchNo": 87, "stage": "round_of_32", "home": "Colombia", "away": "Ecuador", "homeScore": None, "awayScore": None, "city": "Kansas City", "stadium": "Kansas City Stadium", "kickoff": "2026-07-04T01:30:00.000Z"},
      {"matchNo": 88, "stage": "round_of_32", "home": "Australia", "away": "IR Iran", "homeScore": None, "awayScore": None, "city": "Arlington", "stadium": "Dallas Stadium", "kickoff": "2026-07-03T18:00:00.000Z"}
    ],
    "round_of_16": [
      {"matchNo": 89, "stage": "round_of_16", "home": None, "away": None, "homeScore": None, "awayScore": None, "city": "Philadelphia", "stadium": "Philadelphia Stadium", "kickoff": "2026-07-04T21:00:00.000Z"},
      {"matchNo": 90, "stage": "round_of_16", "home": None, "away": None, "homeScore": None, "awayScore": None, "city": "Houston", "stadium": "Houston Stadium", "kickoff": "2026-07-04T17:00:00.000Z"},
      {"matchNo": 91, "stage": "round_of_16", "home": None, "away": None, "homeScore": None, "awayScore": None, "city": "East Rutherford", "stadium": "New York/New Jersey Stadium", "kickoff": "2026-07-05T20:00:00.000Z"},
      {"matchNo": 92, "stage": "round_of_16", "home": None, "away": None, "homeScore": None, "awayScore": None, "city": "Ciudad de México", "stadium": "Mexico City Stadium", "kickoff": "2026-07-06T00:00:00.000Z"},
      {"matchNo": 93, "stage": "round_of_16", "home": None, "away": None, "homeScore": None, "awayScore": None, "city": "Arlington", "stadium": "Dallas Stadium", "kickoff": "2026-07-06T19:00:00.000Z"},
      {"matchNo": 94, "stage": "round_of_16", "home": None, "away": None, "homeScore": None, "awayScore": None, "city": "Seattle", "stadium": "Seattle Stadium", "kickoff": "2026-07-07T00:00:00.000Z"},
      {"matchNo": 95, "stage": "round_of_16", "home": None, "away": None, "homeScore": None, "awayScore": None, "city": "Atlanta", "stadium": "Atlanta Stadium", "kickoff": "2026-07-07T16:00:00.000Z"},
      {"matchNo": 96, "stage": "round_of_16", "home": None, "away": None, "homeScore": None, "awayScore": None, "city": "Vancouver", "stadium": "BC Place Vancouver", "kickoff": "2026-07-07T20:00:00.000Z"}
    ],
    "quarter_final": [
      {"matchNo": 97, "stage": "quarter_final", "home": None, "away": None, "homeScore": None, "awayScore": None, "city": "Foxborough", "stadium": "Boston Stadium", "kickoff": "2026-07-09T20:00:00.000Z"},
      {"matchNo": 98, "stage": "quarter_final", "home": None, "away": None, "homeScore": None, "awayScore": None, "city": "Inglewood", "stadium": "Los Angeles Stadium", "kickoff": "2026-07-10T19:00:00.000Z"},
      {"matchNo": 99, "stage": "quarter_final", "home": None, "away": None, "homeScore": None, "awayScore": None, "city": "Miami Gardens", "stadium": "Miami Stadium", "kickoff": "2026-07-11T21:00:00.000Z"},
      {"matchNo": 100, "stage": "quarter_final", "home": None, "away": None, "homeScore": None, "awayScore": None, "city": "Kansas City", "stadium": "Kansas City Stadium", "kickoff": "2026-07-12T01:00:00.000Z"}
    ],
    "semi_final": [
      {"matchNo": 101, "stage": "semi_final", "home": None, "away": None, "homeScore": None, "awayScore": None, "city": "Arlington", "stadium": "Dallas Stadium", "kickoff": "2026-07-14T19:00:00.000Z"},
      {"matchNo": 102, "stage": "semi_final", "home": None, "away": None, "homeScore": None, "awayScore": None, "city": "Atlanta", "stadium": "Atlanta Stadium", "kickoff": "2026-07-15T19:00:00.000Z"}
    ],
    "third_place": [
      {"matchNo": 103, "stage": "third_place", "home": None, "away": None, "homeScore": None, "awayScore": None, "city": "Miami Gardens", "stadium": "Miami Stadium", "kickoff": "2026-07-18T21:00:00.000Z"}
    ],
    "final": [
      {"matchNo": 104, "stage": "final", "home": None, "away": None, "homeScore": None, "awayScore": None, "city": "East Rutherford", "stadium": "New York/New Jersey Stadium", "kickoff": "2026-07-19T19:00:00.000Z"}
    ]
  }
}

# 今日赛果和近期赛果 (from list_matches)
TODAY_PLAYED = [
    {"date": "2026-06-20", "stage": "group_C", "homeTeam": "Brazil", "awayTeam": "Haiti", "homeScore": 3, "awayScore": 0, "city": "Philadelphia"},
    {"date": "2026-06-20", "stage": "group_D", "homeTeam": "USA", "awayTeam": "Australia", "homeScore": 2, "awayScore": 0, "city": "Seattle"},
    {"date": "2026-06-20", "stage": "group_C", "homeTeam": "Paraguay", "awayTeam": "Türkiye", "homeScore": 1, "awayScore": 0, "city": "Santa Clara"},
    {"date": "2026-06-20", "stage": "group_D", "homeTeam": "Morocco", "awayTeam": "Scotland", "homeScore": 1, "awayScore": 0, "city": "Foxborough"},
]

TODAY_UPCOMING = [
    {"date": "2026-06-20", "stage": "group_E", "homeTeam": "Germany", "awayTeam": "Côte d'Ivoire", "homeScore": None, "awayScore": None, "city": "Toronto", "kickoffUtc": "2026-06-20T19:00:00.000Z"},
    {"date": "2026-06-20", "stage": "group_F", "homeTeam": "Netherlands", "awayTeam": "Sweden", "homeScore": None, "awayScore": None, "city": "Houston", "kickoffUtc": "2026-06-21T00:00:00.000Z"},
]

# 近期已完赛（节选，完整数据从 MCP 获取）
RECENT_PLAYED = [
    {"date": "2026-06-11", "stage": "group_A", "homeTeam": "Mexico", "awayTeam": "South Africa", "homeScore": 1, "awayScore": 0, "city": "Mexico City"},
    {"date": "2026-06-11", "stage": "group_A", "homeTeam": "Korea Republic", "awayTeam": "Czechia", "homeScore": 2, "awayScore": 1, "city": "Los Angeles"},
    {"date": "2026-06-12", "stage": "group_B", "homeTeam": "Canada", "awayTeam": "Qatar", "homeScore": 6, "awayScore": 0, "city": "Vancouver"},
    {"date": "2026-06-12", "stage": "group_B", "homeTeam": "Switzerland", "awayTeam": "Bosnia and Herzegovina", "homeScore": 3, "awayScore": 1, "city": "Seattle"},
    {"date": "2026-06-13", "stage": "group_C", "homeTeam": "Brazil", "awayTeam": "Scotland", "homeScore": 1, "awayScore": 0, "city": "Inglewood"},
    {"date": "2026-06-13", "stage": "group_C", "homeTeam": "Morocco", "awayTeam": "Haiti", "homeScore": 1, "awayScore": 0, "city": "Philadelphia"},
    {"date": "2026-06-14", "stage": "group_D", "homeTeam": "USA", "awayTeam": "Türkiye", "homeScore": 4, "awayScore": 0, "city": "Houston"},
    {"date": "2026-06-14", "stage": "group_D", "homeTeam": "Australia", "awayTeam": "Paraguay", "homeScore": 2, "awayScore": 0, "city": "Seattle"},
    {"date": "2026-06-15", "stage": "group_E", "homeTeam": "Germany", "awayTeam": "Curaçao", "homeScore": 7, "awayScore": 1, "city": "Foxborough"},
    {"date": "2026-06-15", "stage": "group_E", "homeTeam": "Ecuador", "awayTeam": "Côte d'Ivoire", "homeScore": 0, "awayScore": 1, "city": "Houston"},
    {"date": "2026-06-16", "stage": "group_F", "homeTeam": "Sweden", "awayTeam": "Tunisia", "homeScore": 5, "awayScore": 1, "city": "Guadalupe"},
    {"date": "2026-06-16", "stage": "group_F", "homeTeam": "Japan", "awayTeam": "Netherlands", "homeScore": 2, "awayScore": 2, "city": "Inglewood"},
    {"date": "2026-06-17", "stage": "group_G", "homeTeam": "New Zealand", "awayTeam": "Belgium", "homeScore": 2, "awayScore": 1, "city": "Vancouver"},
    {"date": "2026-06-17", "stage": "group_G", "homeTeam": "IR Iran", "awayTeam": "Egypt", "homeScore": 2, "awayScore": 2, "city": "Seattle"},
    {"date": "2026-06-18", "stage": "group_H", "homeTeam": "Uruguay", "awayTeam": "Cabo Verde", "homeScore": 1, "awayScore": 1, "city": "Miami Gardens"},
    {"date": "2026-06-18", "stage": "group_H", "homeTeam": "Spain", "awayTeam": "Saudi Arabia", "homeScore": 0, "awayScore": 0, "city": "Atlanta"},
    {"date": "2026-06-18", "stage": "group_I", "homeTeam": "Norway", "awayTeam": "Iraq", "homeScore": 4, "awayScore": 1, "city": "Philadelphia"},
    {"date": "2026-06-18", "stage": "group_I", "homeTeam": "France", "awayTeam": "Senegal", "homeScore": 3, "awayScore": 1, "city": "East Rutherford"},
    {"date": "2026-06-19", "stage": "group_J", "homeTeam": "Argentina", "awayTeam": "Algeria", "homeScore": 3, "awayScore": 0, "city": "Inglewood"},
    {"date": "2026-06-19", "stage": "group_J", "homeTeam": "Austria", "awayTeam": "Jordan", "homeScore": 3, "awayScore": 1, "city": "Arlington"},
    {"date": "2026-06-19", "stage": "group_K", "homeTeam": "Colombia", "awayTeam": "Uzbekistan", "homeScore": 3, "awayScore": 1, "city": "Guadalupe"},
    {"date": "2026-06-19", "stage": "group_K", "homeTeam": "Congo DR", "awayTeam": "Portugal", "homeScore": 1, "awayScore": 1, "city": "Houston"},
    {"date": "2026-06-19", "stage": "group_L", "homeTeam": "England", "awayTeam": "Croatia", "homeScore": 4, "awayScore": 2, "city": "Foxborough"},
    {"date": "2026-06-19", "stage": "group_L", "homeTeam": "Panama", "awayTeam": "Ghana", "homeScore": 0, "awayScore": 1, "city": "Cincinnati"},
]

# ============================================================
# 构建输出 JSON
# ============================================================

def build_output():
    groups_out = {}
    for gname, teams in STANDINGS["groups"].items():
        groups_out[gname] = [{
            "team": t["team"],
            "played": t["played"],
            "won": t["won"],
            "drawn": t["drawn"],
            "lost": t["lost"],
            "gf": t["goalsFor"],
            "ga": t["goalsAgainst"],
            "gd": t["goalDifference"],
            "pts": t["points"],
            "advanced": t.get("advanced", False),
            "position": t.get("position"),
        } for t in teams]

    #  upcoming matches by date
    upcoming_by_date = {}
    all_upcoming = TODAY_UPCOMING + [
        {"date": "2026-06-21", "stage": "group_E", "homeTeam": "Germany", "awayTeam": "Côte d'Ivoire", "homeScore": None, "awayScore": None, "city": "Toronto", "kickoffUtc": "2026-06-20T19:00:00.000Z"},
        {"date": "2026-06-21", "stage": "group_F", "homeTeam": "Netherlands", "awayTeam": "Sweden", "homeScore": None, "awayScore": None, "city": "Houston", "kickoffUtc": "2026-06-21T00:00:00.000Z"},
        {"date": "2026-06-21", "stage": "group_E", "homeTeam": "Ecuador", "awayTeam": "Curaçao", "homeScore": None, "awayScore": None, "city": "Kansas City", "kickoffUtc": "2026-06-21T18:00:00.000Z"},
        {"date": "2026-06-21", "stage": "group_F", "homeTeam": "Tunisia", "awayTeam": "Japan", "homeScore": None, "awayScore": None, "city": "Guadalupe", "kickoffUtc": "2026-06-21T23:00:00.000Z"},
        {"date": "2026-06-22", "stage": "group_H", "homeTeam": "Uruguay", "awayTeam": "Cabo Verde", "homeScore": None, "awayScore": None, "city": "Miami Gardens", "kickoffUtc": "2026-06-22T18:00:00.000Z"},
        {"date": "2026-06-22", "stage": "group_H", "homeTeam": "Spain", "awayTeam": "Saudi Arabia", "homeScore": None, "awayScore": None, "city": "Atlanta", "kickoffUtc": "2026-06-22T23:00:00.000Z"},
        {"date": "2026-06-22", "stage": "group_G", "homeTeam": "Belgium", "awayTeam": "IR Iran", "homeScore": None, "awayScore": None, "city": "Inglewood", "kickoffUtc": "2026-06-22T20:00:00.000Z"},
        {"date": "2026-06-23", "stage": "group_G", "homeTeam": "New Zealand", "awayTeam": "Egypt", "homeScore": None, "awayScore": None, "city": "Vancouver", "kickoffUtc": "2026-06-23T01:00:00.000Z"},
        {"date": "2026-06-23", "stage": "group_I", "homeTeam": "France", "awayTeam": "Iraq", "homeScore": None, "awayScore": None, "city": "Philadelphia", "kickoffUtc": "2026-06-23T05:00:00.000Z"},
        {"date": "2026-06-23", "stage": "group_J", "homeTeam": "Argentina", "awayTeam": "Austria", "homeScore": None, "awayScore": None, "city": "Arlington", "kickoffUtc": "2026-06-23T10:00:00.000Z"},
    ]
    for m in all_upcoming:
        d = m["date"]
        if d not in upcoming_by_date:
            upcoming_by_date[d] = []
        upcoming_by_date[d].append({
            "date": m["date"],
            "stage": m["stage"],
            "home": m["homeTeam"],
            "away": m["awayTeam"],
            "homeScore": m.get("homeScore"),
            "awayScore": m.get("awayScore"),
            "city": m["city"],
            "kickoff": m.get("kickoffUtc", ""),
        })

    #  played by date
    played_by_date = {}
    for m in RECENT_PLAYED + TODAY_PLAYED:
        d = m["date"]
        if d not in played_by_date:
            played_by_date[d] = []
        played_by_date[d].append({
            "date": m["date"],
            "stage": m["stage"],
            "home": m["homeTeam"],
            "away": m["awayTeam"],
            "homeScore": m["homeScore"],
            "awayScore": m["awayScore"],
            "city": m["city"],
        })

    #  bracket
    bracket_out = {}
    for stage, games in BRACKET["stages"].items():
        bracket_out[stage] = [{
            "matchNo": g["matchNo"],
            "stage": g["stage"],
            "home": g["home"],
            "away": g["away"],
            "homeScore": g["homeScore"],
            "awayScore": g["awayScore"],
            "city": g["city"],
            "stadium": g["stadium"],
            "kickoff": g["kickoff"],
        } for g in games]

    output = {
        "generatedAt": "2026-06-20T20:56:00.000Z",
        "year": 2026,
        "totalMatches": 104,
        "playedCount": len(RECENT_PLAYED) + len(TODAY_PLAYED),
        "upcomingCount": 104 - (len(RECENT_PLAYED) + len(TODAY_PLAYED)),
        "groups": groups_out,
        "playedByDate": played_by_date,
        "upcomingByDate": upcoming_by_date,
        "bracket": bracket_out,
        "todayPlayed": [{
            "stage": m["stage"],
            "home": m["homeTeam"],
            "away": m["awayTeam"],
            "homeScore": m["homeScore"],
            "awayScore": m["awayScore"],
            "city": m["city"],
        } for m in TODAY_PLAYED],
        "todayUpcoming": [{
            "stage": m["stage"],
            "home": m["homeTeam"],
            "away": m["awayTeam"],
            "kickoff": m.get("kickoffUtc", ""),
            "city": m["city"],
        } for m in TODAY_UPCOMING],
    }

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "worldcup-live.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("[OK] Data written to: " + out_path)
    print("  Played: " + str(output['playedCount']) + " matches")
    print("  Upcoming: " + str(output['upcomingCount']) + " matches")

if __name__ == "__main__":
    build_output()
