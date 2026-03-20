from player import Player
from optimizer import recommend

roster = [
    Player("Junho",   ["FWD", "MID", "GK"], {"shooting": 7, "passing": 6, "dribbling": 4, "defending": 7, "speed": 7, "stamina": 5, "positioning": 8, "vision": 8, "saving": 9}),
    Player("Declan", ["DEF", "MID", "FWD"], {"shooting": 8, "passing": 7, "dribbling": 6, "defending": 8, "speed": 7, "stamina": 7, "positioning": 5, "vision": 5, "saving": 2}),
    Player("Allison",    ["FWD", "MID"],         {"shooting": 6, "passing": 5, "dribbling": 5, "defending": 3, "speed": 4, "stamina": 6, "positioning": 2, "vision": 2, "saving": 2}),
    Player("Daniel_L", ["FWD"],        {"shooting": 5, "passing": 4, "dribbling": 4, "defending": 3, "speed": 5, "stamina": 5, "positioning": 2, "vision": 2, "saving": 1}),
    Player("Daniel_R",  ["DEF", "FWD"],        {"shooting": 6, "passing": 6, "dribbling": 6, "defending": 7, "speed": 7, "stamina": 8, "positioning": 4, "vision": 5, "saving": 5}),
    Player("Brian",  ["GK", "FWD", "MID"],        {"shooting": 4, "passing": 5, "dribbling": 5, "defending": 5, "speed": 5, "stamina": 5, "positioning": 6, "vision": 6, "saving": 7}),
    Player("Roshni", ["DEF", "FWD"], {"shooting": 7, "passing": 7, "dribbling": 6, "defending": 7, "speed": 6, "stamina": 7, "positioning": 6, "vision": 6, "saving": 6}),
    Player("Mandy",   ["DEF"], {"shooting": 5, "passing": 5, "dribbling": 5, "defending": 6, "speed": 5, "stamina": 6, "positioning": 2, "vision": 2, "saving": 2}),
]

results = recommend(roster)

for i, r in enumerate(results[:3]):
    print(f"\n{'='*50}")
    print(f"Option {i+1}: {r['formation'].name} (score: {r['score']:.1f})")
    print(f"{'='*50}")
    for position, player in r['lineup']:
        fit = player.position_fit(position)
        print(f"  {position:4s} -> {player.name:8s} (fit: {fit:.1f})")