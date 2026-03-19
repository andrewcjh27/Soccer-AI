from player import Player

junho = Player(
    name="Junho",
    positions=["FWD", "MID", "DEF", "GK"],
    stats={
        "shooting": 7, "passing": 6, "dribbling": 4,
        "defending": 5, "speed": 7, "stamina": 5,
        "positioning": 7, "vision": 6, "saving": 8
    }
)

declan = Player(
    name="Declan",
    positions=["DEF", "MID", "FWD"],
    stats={
        "shooting": 8, "passing": 7, "dribbling": 6,
        "defending": 8, "speed": 7, "stamina": 7,
        "positioning": 5, "vision": 5, "saving": 2
    }
)

print(junho)
print(f"  Junho as FWD: {junho.position_fit('FWD'):.1f}")
print(f"  Junho as DEF: {junho.position_fit('DEF'):.1f}")
print(f"  Junho as MID: {junho.position_fit('MID'):.1f}")
print(f"  Junho as GK: {junho.position_fit('GK'):.1f}")
print()
print(declan)
print(f"  Declan as DEF: {declan.position_fit('DEF'):.1f}")
print(f"  Declan as FWD: {declan.position_fit('FWD'):.1f}")
print(f"  Declan as MID: {declan.position_fit('MID'):.1f}")