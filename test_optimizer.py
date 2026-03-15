from player import Player
from optimizer import recommend

roster = [
    Player("Junho",   ["FWD", "MID"], {"shooting": 8, "passing": 6, "dribbling": 7, "defending": 3, "speed": 9, "stamina": 7, "positioning": 5, "vision": 6, "shot_stopping": 1}),
    Player("Declan", ["DEF", "MID"], {"shooting": 4, "passing": 7, "dribbling": 5, "defending": 8, "speed": 6, "stamina": 8, "positioning": 7, "vision": 6, "shot_stopping": 2}),
    Player("Allison",    ["GK"],         {"shooting": 2, "passing": 5, "dribbling": 3, "defending": 5, "speed": 4, "stamina": 6, "positioning": 8, "vision": 5, "shot_stopping": 9}),
    Player("Daniel_L", ["MID"],        {"shooting": 6, "passing": 8, "dribbling": 6, "defending": 5, "speed": 7, "stamina": 9, "positioning": 6, "vision": 8, "shot_stopping": 1}),
    Player("Daniel_R",  ["DEF"],        {"shooting": 3, "passing": 6, "dribbling": 4, "defending": 9, "speed": 5, "stamina": 8, "positioning": 8, "vision": 5, "shot_stopping": 3}),
    Player("Brian",  ["FWD"],        {"shooting": 9, "passing": 5, "dribbling": 8, "defending": 2, "speed": 8, "stamina": 6, "positioning": 6, "vision": 5, "shot_stopping": 1}),
    Player("Roshni", ["MID", "FWD"], {"shooting": 7, "passing": 7, "dribbling": 7, "defending": 4, "speed": 7, "stamina": 7, "positioning": 6, "vision": 7, "shot_stopping": 1}),
    Player("Mandy",   ["DEF", "MID"], {"shooting": 5, "passing": 6, "dribbling": 5, "defending": 7, "speed": 6, "stamina": 9, "positioning": 7, "vision": 6, "shot_stopping": 2}),
]

results = recommend(roster)

for i, r in enumerate(results[:3]):
    print(f"\n{'='*50}")
    print(f"Option {i+1}: {r['formation'].name} (score: {r['score']:.1f})")
    print(f"{'='*50}")
    for position, player in r['lineup']:
        fit = player.position_fit(position)
        print(f"  {position:4s} -> {player.name:8s} (fit: {fit:.1f})")