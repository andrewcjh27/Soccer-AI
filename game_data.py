"""
Game data structured in SEGMENTS.

Each game is broken into time segments. A new segment starts whenever:
- A substitution happens
- Players swap positions
- Formation changes mid-game

This captures the reality that your lineup at minute 1
might be completely different from minute 25.
"""

games = [
    {
        "opponent": "Opponent 1",
        "result": 1,           # 1=win, 0=loss/draw
        "goals_scored": 2,
        "goals_conceded": 1,
        "total_minutes": 40,   # total game length
        "segments": [
            {
                "start_min": 0,
                "end_min": 20,
                "formation": "1-2-1-2",
                "goals_scored": 0,
                "goals_conceded": 1,
                "goal_scorers": [],  
                "lineup": [
                    {"player": "Junho",    "position": "GK",  "stats": {"shooting": 7, "passing": 6, "dribbling": 4, "defending": 7, "speed": 7, "stamina": 5, "positioning": 8, "vision": 7, "saving": 9}},
                    {"player": "Roshni",  "position": "DEF", "stats": {"shooting": 7, "passing": 7, "dribbling": 6, "defending": 7, "speed": 6, "stamina": 7, "positioning": 6, "vision": 6, "saving": 6}},
                    {"player": "Declan", "position": "DEF", "stats": {"shooting": 8, "passing": 7, "dribbling": 6, "defending": 8, "speed": 7, "stamina": 7, "positioning": 5, "vision": 4, "saving": 2}},
                    {"player": "Brian", "position": "MID", "stats": {"shooting": 4, "passing": 5, "dribbling": 5, "defending": 5, "speed": 5, "stamina": 5, "positioning": 6, "vision": 7, "saving": 7}},
                    {"player": "Soleil", "position": "FWD", "stats": {"shooting": 6, "passing": 5, "dribbling": 5, "defending": 3, "speed": 4, "stamina": 6, "positioning": 2, "vision": 3, "saving": 2}},
                    {"player": "Allison",   "position": "FWD", "stats": {"shooting": 6, "passing": 5, "dribbling": 5, "defending": 3, "speed": 4, "stamina": 6, "positioning": 2, "vision": 4, "saving": 2}},
                ],
            },
            {
                "start_min": 20,
                "end_min": 40,
                "formation": "1-2-2-1",
                "goals_scored": 2,
                "goals_conceded": 0,
                "goal_scorers": ["Junho", "Declan"], 
                "lineup": [
                    {"player": "Brian",    "position": "GK",  "stats": {"shooting": 4, "passing": 5, "dribbling": 5, "defending": 5, "speed": 5, "stamina": 5, "positioning": 6, "vision": 4, "saving": 7}},
                    {"player": "Roshni",  "position": "DEF", "stats": {"shooting": 7, "passing": 7, "dribbling": 6, "defending": 7, "speed": 6, "stamina": 7, "positioning": 6, "vision": 6, "saving": 6}},
                    {"player": "Declan", "position": "DEF", "stats": {"shooting": 8, "passing": 7, "dribbling": 6, "defending": 8, "speed": 7, "stamina": 7, "positioning": 5, "vision": 7, "saving": 2}},
                    {"player": "Junho", "position": "MID", "stats": {"shooting": 7, "passing": 6, "dribbling": 4, "defending": 7, "speed": 7, "stamina": 5, "positioning": 8, "vision": 7, "saving": 9}},
                    {"player": "Soleil",   "position": "MID", "stats": {"shooting": 6, "passing": 5, "dribbling": 5, "defending": 3, "speed": 4, "stamina": 6, "positioning": 2, "vision": 3, "saving": 2}},
                    {"player": "Allison",  "position": "FWD", "stats": {"shooting": 6, "passing": 5, "dribbling": 5, "defending": 3, "speed": 4, "stamina": 6, "positioning": 2, "vision": 4, "saving": 2}},
                ],
            },
        ],
    },
    {
        "opponent": "Opponent 2",
        "result": 0,          
        "goals_scored": 1,
        "goals_conceded": 2,
        "total_minutes": 40,   
        "segments": [
            {
                "start_min": 0,
                "end_min": 10,
                "formation": "1-2-1-2",
                "goals_scored": 0,
                "goals_conceded": 0,
                "goal_scorers": [],  
                "lineup": [
                    {"player": "Junho",    "position": "GK",  "stats": {"shooting": 7, "passing": 6, "dribbling": 4, "defending": 7, "speed": 7, "stamina": 5, "positioning": 8, "vision": 7, "saving": 9}},
                    {"player": "Roshni",  "position": "DEF", "stats": {"shooting": 7, "passing": 7, "dribbling": 6, "defending": 7, "speed": 6, "stamina": 7, "positioning": 6, "vision": 6, "saving": 6}},
                    {"player": "Declan", "position": "DEF", "stats": {"shooting": 8, "passing": 7, "dribbling": 6, "defending": 8, "speed": 7, "stamina": 7, "positioning": 5, "vision": 7, "saving": 2}},
                    {"player": "Daniel R", "position": "MID", "stats": {"shooting": 6, "passing": 6, "dribbling": 6, "defending": 7, "speed": 7, "stamina": 8, "positioning": 4, "vision": 5, "saving": 5}},
                    {"player": "Soleil", "position": "FWD", "stats": {"shooting": 6, "passing": 5, "dribbling": 5, "defending": 3, "speed": 4, "stamina": 6, "positioning": 2, "vision": 3, "saving": 2}},
                    {"player": "Allison",   "position": "FWD", "stats": {"shooting": 6, "passing": 5, "dribbling": 5, "defending": 3, "speed": 4, "stamina": 6, "positioning": 2, "vision": 4, "saving": 2}},
                ],
            },
                        {
                "start_min": 10,
                "end_min": 20,
                "formation": "1-2-1-2",
                "goals_scored": 0,
                "goals_conceded": 1,
                "goal_scorers": [],  
                "lineup": [
                    {"player": "Junho",    "position": "GK",  "stats": {"shooting": 7, "passing": 6, "dribbling": 4, "defending": 7, "speed": 7, "stamina": 5, "positioning": 8, "vision": 7, "saving": 9}},
                    {"player": "Roshni",  "position": "DEF", "stats": {"shooting": 7, "passing": 7, "dribbling": 6, "defending": 7, "speed": 6, "stamina": 7, "positioning": 6, "vision": 6, "saving": 6}},
                    {"player": "Declan", "position": "DEF", "stats": {"shooting": 8, "passing": 7, "dribbling": 6, "defending": 8, "speed": 7, "stamina": 7, "positioning": 5, "vision": 7, "saving": 2}},
                    {"player": "Claudia", "position": "MID", "stats": {"shooting": 3, "passing": 4, "dribbling": 3, "defending": 3, "speed": 4, "stamina": 5, "positioning": 2, "vision": 2, "saving": 2}},
                    {"player": "Soleil", "position": "FWD", "stats": {"shooting": 6, "passing": 5, "dribbling": 5, "defending": 3, "speed": 4, "stamina": 6, "positioning": 2, "vision": 3, "saving": 2}},
                    {"player": "Daniel L",   "position": "FWD", "stats": {"shooting": 5, "passing": 4, "dribbling": 4, "defending": 3, "speed": 5, "stamina": 5, "positioning": 2, "vision": 2, "saving": 1}},
                ],
            },
            {
                "start_min": 20,
                "end_min": 40,
                "formation": "1-2-1-2",
                "goals_scored": 1,
                "goals_conceded": 1,
                "goal_scorers": ["Declan"], 
                "lineup": [
                    {"player": "Daniel R",    "position": "GK",  "stats": {"shooting": 4, "passing": 5, "dribbling": 5, "defending": 5, "speed": 5, "stamina": 5, "positioning": 6, "vision": 5, "saving": 7}},
                    {"player": "Roshni",  "position": "DEF", "stats": {"shooting": 7, "passing": 7, "dribbling": 6, "defending": 7, "speed": 6, "stamina": 7, "positioning": 6, "vision": 6, "saving": 6}},
                    {"player": "Declan", "position": "DEF", "stats": {"shooting": 8, "passing": 7, "dribbling": 6, "defending": 8, "speed": 7, "stamina": 7, "positioning": 5, "vision": 7, "saving": 2}},
                    {"player": "Junho", "position": "MID", "stats": {"shooting": 7, "passing": 6, "dribbling": 4, "defending": 7, "speed": 7, "stamina": 5, "positioning": 8, "vision": 7, "saving": 9}},
                    {"player": "Soleil",   "position": "MID", "stats": {"shooting": 6, "passing": 5, "dribbling": 5, "defending": 3, "speed": 4, "stamina": 6, "positioning": 2, "vision": 3, "saving": 2}},
                    {"player": "Allison",  "position": "FWD", "stats": {"shooting": 6, "passing": 5, "dribbling": 5, "defending": 3, "speed": 4, "stamina": 6, "positioning": 2, "vision": 4, "saving": 2}},
                ],
            },
        ],
    },
    {
        "opponent": "Opponent 3",
        "result": 0,           
        "goals_scored": 0,
        "goals_conceded": 4,
        "total_minutes": 40,   
        "segments": [
            {
                "start_min": 0,
                "end_min": 10,
                "formation": "1-3-2",
                "goals_scored": 0,
                "goals_conceded": 0,
                "goal_scorers": [],  
                "lineup": [
                    {"player": "Junho",    "position": "GK",  "stats": {"shooting": 7, "passing": 6, "dribbling": 4, "defending": 7, "speed": 7, "stamina": 5, "positioning": 8, "vision": 7, "saving": 9}},
                    {"player": "Mandy",  "position": "DEF", "stats": {"shooting": 5, "passing": 5, "dribbling": 4, "defending": 6, "speed": 4, "stamina": 7, "positioning": 2, "vision": 3, "saving": 1}},
                    {"player": "Declan", "position": "DEF", "stats": {"shooting": 8, "passing": 7, "dribbling": 6, "defending": 8, "speed": 7, "stamina": 7, "positioning": 5, "vision":7, "saving": 2}},
                    {"player": "Daniel R", "position": "DEF", "stats": {"shooting": 4, "passing": 5, "dribbling": 5, "defending": 5, "speed": 5, "stamina": 5, "positioning": 6, "vision": 5, "saving": 7}},
                    {"player": "Daniel L", "position": "FWD", "stats": {"shooting": 5, "passing": 4, "dribbling": 4, "defending": 3, "speed": 5, "stamina": 5, "positioning": 2, "vision": 2, "saving": 1}},
                    {"player": "Allison",   "position": "FWD", "stats": {"shooting": 6, "passing": 5, "dribbling": 5, "defending": 3, "speed": 4, "stamina": 6, "positioning": 2, "vision": 4, "saving": 2}},
                ],
            },
                        {
                "start_min": 10,
                "end_min": 20,
                "formation": "1-3-2",
                "goals_scored": 0,
                "goals_conceded": 1,
                "goal_scorers": [],  
                "lineup": [
                    {"player": "Junho",    "position": "GK",  "stats": {"shooting": 7, "passing": 6, "dribbling": 4, "defending": 7, "speed": 7, "stamina": 5, "positioning": 8, "vision": 7, "saving": 9}},
                    {"player": "Katie",  "position": "DEF", "stats": {"shooting": 4, "passing": 4, "dribbling": 4, "defending": 4, "speed": 4, "stamina": 5, "positioning": 2, "vision": 2, "saving": 1}},
                    {"player": "Declan", "position": "DEF", "stats": {"shooting": 8, "passing": 7, "dribbling": 6, "defending": 8, "speed": 7, "stamina": 7, "positioning": 5, "vision": 7, "saving": 2}},
                    {"player": "Daniel R", "position": "DEF", "stats": {"shooting": 4, "passing": 5, "dribbling": 5, "defending": 5, "speed": 5, "stamina": 5, "positioning": 6, "vision": 5, "saving": 7}},
                    {"player": "Brian", "position": "FWD", "stats": {"shooting": 4, "passing": 5, "dribbling": 5, "defending": 5, "speed": 5, "stamina": 5, "positioning": 6, "vision": 4, "saving": 7}},
                    {"player": "Allison",   "position": "FWD", "stats": {"shooting": 6, "passing": 5, "dribbling": 5, "defending": 3, "speed": 4, "stamina": 6, "positioning": 2, "vision": 4, "saving": 2}},
                ],
            },
                        {
                "start_min": 20,
                "end_min": 30,
                "formation": "1-3-2",
                "goals_scored": 0,
                "goals_conceded": 2,
                "goal_scorers": [],  
                "lineup": [
                    {"player": "Brian",    "position": "GK",  "stats": {"shooting": 4, "passing": 5, "dribbling": 5, "defending": 5, "speed": 5, "stamina": 5, "positioning": 6, "vision": 4, "saving": 7}},
                    {"player": "Mandy",  "position": "DEF", "stats": {"shooting": 5, "passing": 5, "dribbling": 4, "defending": 6, "speed": 4, "stamina": 7, "positioning": 2, "vision": 3, "saving": 1}},
                    {"player": "Declan", "position": "DEF", "stats": {"shooting": 8, "passing": 7, "dribbling": 6, "defending": 8, "speed": 7, "stamina": 7, "positioning": 5, "vision": 7, "saving": 2}},
                    {"player": "Daniel R", "position": "DEF", "stats": {"shooting": 4, "passing": 5, "dribbling": 5, "defending": 5, "speed": 5, "stamina": 5, "positioning": 6, "vision": 5, "saving": 7}},
                    {"player": "Junho",    "position": "GK",  "stats": {"shooting": 7, "passing": 6, "dribbling": 4, "defending": 7, "speed": 7, "stamina": 5, "positioning": 8, "vision": 7, "saving": 9}},
                    {"player": "Allison",   "position": "FWD", "stats": {"shooting": 6, "passing": 5, "dribbling": 5, "defending": 3, "speed": 4, "stamina": 6, "positioning": 2, "vision": 4, "saving": 2}},
                ],
            },
            {
                "start_min": 30,
                "end_min": 40,
                "formation": "1-3-2",
                "goals_scored": 2,
                "goals_conceded": 1,
                "goal_scorers": [], 
                "lineup": [
                    {"player": "Brian",    "position": "GK",  "stats": {"shooting": 4, "passing": 5, "dribbling": 5, "defending": 5, "speed": 5, "stamina": 5, "positioning": 6, "vision": 4, "saving": 7}},
                    {"player": "Katie",  "position": "DEF", "stats": {"shooting": 4, "passing": 4, "dribbling": 4, "defending": 4, "speed": 4, "stamina": 5, "positioning": 2, "vision": 2, "saving": 1}},
                    {"player": "Junho",    "position": "GK",  "stats": {"shooting": 7, "passing": 6, "dribbling": 4, "defending": 7, "speed": 7, "stamina": 5, "positioning": 8, "vision": 7, "saving": 9}},
                    {"player": "Daniel R", "position": "DEF", "stats": {"shooting": 4, "passing": 5, "dribbling": 5, "defending": 5, "speed": 5, "stamina": 5, "positioning": 6, "vision": 5, "saving": 7}},
                    {"player": "Daniel L", "position": "FWD", "stats": {"shooting": 5, "passing": 4, "dribbling": 4, "defending": 3, "speed": 5, "stamina": 5, "positioning": 2, "vision": 2, "saving": 1}},
                    {"player": "Allison",   "position": "FWD", "stats": {"shooting": 6, "passing": 5, "dribbling": 5, "defending": 3, "speed": 4, "stamina": 6, "positioning": 2, "vision": 4, "saving": 2}},
                ],
            },
        ],
    },
]