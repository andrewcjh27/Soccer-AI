import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
from game_data import games

STAT_NAMES = ["saving", "positioning", "passing", "defending",
              "stamina", "speed", "shooting", "dribbling", "vision"]

POSITIONS = ["GK", "DEF", "MID", "FWD"]


def segment_to_features(segment):
    """
    Convert one segment into a feature vector.

    Same idea as before — average stats per position —
    but now also includes:
    - duration (how long this lineup played)
    - formation as a numeric feature
    - game minute (early vs late game context)
    """
    features = []

    # Position-averaged stats (36 features)
    for pos in POSITIONS:
        players_in_pos = [p for p in segment["lineup"]
                          if p["position"] == pos]
        if players_in_pos:
            for stat in STAT_NAMES:
                avg = np.mean([p["stats"][stat] for p in players_in_pos])
                features.append(avg)
        else:
            features.extend([0] * len(STAT_NAMES))

    # Duration of this segment in minutes
    duration = segment["end_min"] - segment["start_min"]
    features.append(duration)

    # How far into the game (0.0 = start, 1.0 = end)
    # This lets the model learn that certain lineups work
    # better early vs late in the game
    midpoint = (segment["start_min"] + segment["end_min"]) / 2
    features.append(midpoint)

    # Number of players per position (captures formation shape)
    for pos in POSITIONS:
        count = sum(1 for p in segment["lineup"] if p["position"] == pos)
        features.append(count)

    # Goal scorer stats — what kind of player is scoring?
    # If no scorers recorded, fill with zeros
    scorers = segment.get("goal_scorers", [])
    if scorers:
        # Find the stats of players who scored in this segment
        scorer_stats_list = []
        for scorer_name in scorers:
            for p in segment["lineup"]:
                if p["player"] == scorer_name:
                    scorer_stats_list.append(p["stats"])
                    break

        if scorer_stats_list:
            # Average stats of goal scorers
            for stat in STAT_NAMES:
                avg = np.mean([s[stat] for s in scorer_stats_list])
                features.append(avg)
            # How many goals scored
            features.append(len(scorers))
        else:
            features.extend([0] * (len(STAT_NAMES) + 1))
    else:
        features.extend([0] * (len(STAT_NAMES) + 1))

    return features


def build_dataset():
    """
    Each segment becomes a training example.

    Label: did this segment perform well?
    We define "good" as: scored more than conceded in this segment.
    """
    X = []
    y = []

    for game in games:
        for segment in game["segments"]:
            features = segment_to_features(segment)
            X.append(features)

            # Segment-level outcome
            scored = segment.get("goals_scored", 0)
            conceded = segment.get("goals_conceded", 0)

            if scored > conceded:
                label = 1   # this lineup was winning
            elif scored == conceded:
                label = 0   # neutral
            else:
                label = 0   # this lineup was losing

            y.append(label)

    return np.array(X), np.array(y)


def train_model():
    X, y = build_dataset()

    print(f"Training on {len(X)} segments from {len(games)} games\n")

    model = GradientBoostingClassifier(
        n_estimators=100,
        max_depth=3,
        random_state=42
    )
    model.fit(X, y)

    if len(X) >= 5:
        scores = cross_val_score(model, X, y, cv=min(5, len(X)))
        print(f"Cross-validation accuracy: {scores.mean():.2f} (+/- {scores.std():.2f})")
    else:
        print(f"Only {len(X)} segments — model will improve with more games!")

    return model


def predict_segment_quality(model, lineup, formation, start_min, end_min):
    """
    Predict how well a proposed lineup will perform
    during a specific segment of the game.
    """
    segment = {
        "lineup": [{"position": pos, "stats": player.stats}
                    for pos, player in lineup],
        "start_min": start_min,
        "end_min": end_min,
    }
    features = np.array([segment_to_features(segment)])
    proba = model.predict_proba(features)[0]

    # Handle case where model has only seen one class
    if len(proba) > 1:
        return proba[1]
    return proba[0]


def get_feature_importance(model):
    """Show what the model learned matters most."""
    feature_names = []
    for pos in POSITIONS:
        for stat in STAT_NAMES:
            feature_names.append(f"{pos}_{stat}")
    feature_names.extend(["duration", "game_minute",
                          "num_GK", "num_DEF", "num_MID", "num_FWD"])
    # Goal scorer feature names
    for stat in STAT_NAMES:
        feature_names.append(f"scorer_{stat}")
    feature_names.append("num_goals")

    importances = model.feature_importances_
    pairs = sorted(zip(feature_names, importances),
                   key=lambda x: x[1], reverse=True)

    print("\nTop 10 most important features for winning:")
    print("-" * 45)
    for name, importance in pairs[:10]:
        bar = "█" * int(importance * 200)
        print(f"  {name:20s} {importance:.3f} {bar}")

    return pairs


if __name__ == "__main__":
    model = train_model()
    get_feature_importance(model)