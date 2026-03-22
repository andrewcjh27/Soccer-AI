class Player:
    def __init__(self, name, positions, stats):
        self.name = name
        self.positions = positions
        self.stats = stats
        self.minutes_played = 0

    def overall_rating(self):
        values = self.stats.values()
        return sum(values) / len(values)
    
    def position_fit(self, position):
        position_weights = {
            "GK":  {"saving": 3, "positioning": 2, "passing": 1},
            "DEF": {"defending": 3, "positioning": 2, "stamina": 1},
            "MID": {"passing": 3, "vision": 2, "stamina": 2, "defending": 1},
            "FWD": {"shooting": 3, "speed": 2, "dribbling": 2},
        }

        weights = position_weights.get(position, {})
        score = 0
        total_weight = 0

        for stat_name, weight in weights.items():
            if stat_name in self.stats:
                score += self.stats[stat_name] * weight
                total_weight += weight

        if total_weight == 0:
            return 0
        base_score = score / total_weight

        # Apply a multiplier based on whether this is the player's preferred position.
        # Without this, the optimizer ignores position preferences entirely and can
        # assign a FWD-only player to DEF, displacing a proper defender.
        if position in self.positions:
            return base_score * 1.3   # 30% bonus for playing a natural position
        else:
            return base_score * 0.5   # 50% penalty for playing out of position

    def __repr__(self):
        return f"Player({self.name}, rating={self.overall_rating():.1f})"