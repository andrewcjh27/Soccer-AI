class Player:
    # Stat weights per position — single source of truth used by both
    # overall_rating() and position_fit() so they never disagree.
    POSITION_WEIGHTS = {
        "GK":  {"saving": 3, "positioning": 2, "passing": 1},
        "DEF": {"defending": 3, "positioning": 2, "stamina": 1},
        "MID": {"passing": 3, "vision": 2, "stamina": 2, "defending": 1},
        "FWD": {"shooting": 3, "speed": 2, "dribbling": 2},
    }

    def __init__(self, name, positions, stats):
        self.name = name
        self.positions = positions
        self.stats = stats
        self.minutes_played = 0

    def overall_rating(self):
        """
        Rate the player only on the stats that matter for the positions they play.

        For each of their positions we compute a weighted score using
        POSITION_WEIGHTS, then average across all their positions.

        Examples:
          Declan (DEF/MID/FWD) — rated on defending, passing, shooting, etc.
                                  saving is never touched.
          Junho  (FWD/MID/GK)  — rated on shooting, passing, saving, etc.
                                  all three role-sets count equally.
        """
        scores = []
        for pos in self.positions:
            weights = self.POSITION_WEIGHTS.get(pos, {})
            if not weights:
                continue
            score = 0
            total_weight = 0
            for stat_name, weight in weights.items():
                if stat_name in self.stats:
                    score += self.stats[stat_name] * weight
                    total_weight += weight
            if total_weight > 0:
                scores.append(score / total_weight)

        if not scores:
            # Fallback for a player with no recognised positions
            return sum(self.stats.values()) / len(self.stats)

        return sum(scores) / len(scores)

    def stamina_minutes(self, game_length=40):
        """
        Estimate how many minutes this player can sustain peak effort
        before their performance drops off noticeably.

        Formula: (stamina / 10) × game_length
          stamina 10 → full game  (e.g. 40 min)
          stamina 7  → 70% of game (e.g. 28 min)
          stamina 5  → half the game (e.g. 20 min)
          stamina 3  → 30% of game (e.g. 12 min)
        """
        return round((self.stats.get("stamina", 5) / 10) * game_length)

    def position_fit(self, position):
        """
        Score how well this player fits a specific position slot.
        Uses POSITION_WEIGHTS and applies a bonus/penalty based on
        whether this position is in their natural repertoire.
        """
        weights = self.POSITION_WEIGHTS.get(position, {})
        score = 0
        total_weight = 0

        for stat_name, weight in weights.items():
            if stat_name in self.stats:
                score += self.stats[stat_name] * weight
                total_weight += weight

        if total_weight == 0:
            return 0
        base_score = score / total_weight

        # Bonus for natural position, penalty for playing out of position
        if position in self.positions:
            return base_score * 1.3
        else:
            return base_score * 0.5

    def __repr__(self):
        return f"Player({self.name}, rating={self.overall_rating():.1f})"
