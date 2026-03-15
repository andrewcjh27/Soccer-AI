from pulp import *

class Formation:
    def __init__(self, name, slots):
        self.name = name
        self.slots = slots

    def __repr__(self):
        return f"Formation({self.name})"
    
FORMATIONS = [
    Formation("1-2-2-1", ["GK", "DEF", "DEF", "MID", "MID", "FWD"]),
    Formation("1-1-3-1", ["GK", "DEF", "MID", "MID", "MID", "FWD"]),
    Formation("1-2-1-2", ["GK", "DEF", "DEF", "MID", "FWD", "FWD"]),
    Formation("1-3-1-1", ["GK", "DEF", "DEF", "DEF", "MID", "FWD"]),
    Formation("1-3-2", ["GK", "DEF", "DEF", "DEF", "FWD", "FWD"]),
]

def optimize_lineup(roster, formation):
    """
    Use linear programming to find the optimal assignment
    of players to formation slots.

    Returns (lineup, score) where lineup is a list of
    (position, player) tuples.
    """
    players = range(len(roster))
    slots = range(len(formation.slots))

    # Decision variables: x[i][j] = 1 if player i is assigned to slot j
    x = [[LpVariable(f"x_{i}_{j}", cat="Binary")
           for j in slots] for i in players]

    prob = LpProblem("Soccer_Lineup", LpMaximize)

    # Objective: maximize total position fit across all assignments
    prob += lpSum(
        x[i][j] * roster[i].position_fit(formation.slots[j])
        for i in players for j in slots
    )

    # Constraint 1: each slot gets exactly one player
    for j in slots:
        prob += lpSum(x[i][j] for i in players) == 1

        # Constraint 2: each player fills at most one slot
    for i in players:
        prob += lpSum(x[i][j] for j in slots) <= 1

    # Solve (suppress solver output)
    prob.solve(PULP_CBC_CMD(msg=0))

    # Extract the lineup from the solution
    lineup = []
    for j in slots:
        for i in players:
            if value(x[i][j]) == 1:
                lineup.append((formation.slots[j], roster[i]))

    return lineup, value(prob.objective)

def recommend(roster):
    """
    Try every formation, find the optimal lineup for each,
    and return results sorted best to worst.
    """
    results = []

    for formation in FORMATIONS:
        lineup, score = optimize_lineup(roster, formation)
        results.append({
            "formation": formation,
            "lineup": lineup,
            "score": score,
        })

    # Sort by score, best first
    results.sort(key=lambda r: r["score"], reverse=True)
    return results

