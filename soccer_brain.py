import torch
import torch.nn as nn
import numpy as np
from game_data import games

STAT_NAMES = ["saving", "positioning", "passing", "defending",
              "stamina", "speed", "shooting", "dribbling", "vision"]

POSITIONS = ["GK", "DEF", "MID", "FWD"]

FORMATIONS = ["1-2-2-1", "1-1-3-1", "1-2-1-2", "1-3-1-1", "1-3-2"]

class SoccerBrain(nn.Module):
    """
    YOUR neural network. You train this on your team's game data.

    Architecture:
    - Input: flattened stats for all positions + formation info
    - Hidden layers: learn patterns about what wins games
    - Output heads: win probability + formation recommendation

    This is a MULTI-HEAD network — one input, multiple outputs.
    Each "head" answers a different question.
    """
    def __init__(self, input_size):
        super().__init__()

        # Shared backbone — learns general patterns
        # Every input passes through these layers first
        self.backbone = nn.Sequential(
            nn.Linear(input_size, 64),   # compress input into 64 features
            nn.ReLU(),                    # activation function (introduces non-linearity)
            nn.Dropout(0.2),              # randomly zero 20% of values (prevents overfitting)
            nn.Linear(64, 32),            # compress further to 32 features
            nn.ReLU(),
        )

        # Head 1: Win probability (single number 0-1)  
        self.win_head = nn.Sequential(
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid(),
        )

        # Head 2: Formation recommendation (score for each formation)
        self.formation_head = nn.Sequential(
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, len(FORMATIONS)),
            nn.ReLU(),
        )

        # Head 3: Goal prediction (how many goals this lineup might score)
        self.goals_head = nn.Sequential(
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.ReLU(),   # goals can't be negative
        )

    def forward(self, x):
        """
        Forward pass — data flows through the network.

        x: input tensor of shape (batch_size, input_size)
        Returns: win_prob, formation_scores, predicted_goals
        """
        shared = self.backbone(x)
        win_prob = self.win_head(shared)
        formation_scores = self.formation_head(shared)
        predicted_goals = self.goals_head(shared)
        return win_prob, formation_scores, predicted_goals
    
# ---- Feature Engineering (same logic as ml_model.py but for PyTorch) ----

def segment_to_features(segment):
    """Convert a game segment into a flat feature vector."""
    features = []

    # Position-averaged stats (4 positions x 9 stats = 36)
    for pos in POSITIONS:
        players_in_pos = [p for p in segment["lineup"]
                          if p["position"] == pos]
        if players_in_pos:
            for stat in STAT_NAMES:
                avg = np.mean([p["stats"][stat] for p in players_in_pos])
                features.append(avg)
        else:
            features.extend([0.0] * len(STAT_NAMES))

    # Duration and game minute (2)
    duration = segment["end_min"] - segment["start_min"]
    features.append(duration)
    midpoint = (segment["start_min"] + segment["end_min"]) / 2
    features.append(midpoint)

    # Players per position (4)
    for pos in POSITIONS:
        count = sum(1 for p in segment["lineup"] if p["position"] == pos)
        features.append(float(count))

    # Formation as one-hot encoding (5)
    formation = segment.get("formation", "")
    for f in FORMATIONS:
        features.append(1.0 if formation == f else 0.0)

    return features


def get_input_size():
    """Calculate how many features we generate per segment."""
    # 36 (pos stats) + 2 (time) + 4 (pos counts) + 5 (formation one-hot)
    return 47


# ---- Training ----

def build_training_data():
    """
    Convert all game history into tensors for PyTorch.

    Returns:
        X: feature tensor (num_segments x input_size)
        y_win: win labels (num_segments x 1)
        y_formation: formation indices (num_segments)
        y_goals: goals scored (num_segments x 1)
    """
    X_list = []
    y_win_list = []
    y_formation_list = []
    y_goals_list = []

    for game in games:
        for segment in game["segments"]:
            features = segment_to_features(segment)
            X_list.append(features)

            # Win label
            scored = segment.get("goals_scored", 0)
            conceded = segment.get("goals_conceded", 0)
            y_win_list.append([1.0 if scored > conceded else 0.0])

            # Formation label (index into FORMATIONS list)
            formation = segment.get("formation", FORMATIONS[0])
            if formation in FORMATIONS:
                y_formation_list.append(FORMATIONS.index(formation))
            else:
                y_formation_list.append(0)

            # Goals scored
            y_goals_list.append([float(scored)])

    X = torch.tensor(X_list, dtype=torch.float32)
    y_win = torch.tensor(y_win_list, dtype=torch.float32)
    y_formation = torch.tensor(y_formation_list, dtype=torch.long)
    y_goals = torch.tensor(y_goals_list, dtype=torch.float32)

    return X, y_win, y_formation, y_goals

def train(epochs=500, lr=0.01):
    """
    Train the SoccerBrain on your game data.

    epochs: how many times to loop through all the data
    lr: learning rate (how big each adjustment step is)
    """
    input_size = get_input_size()
    model = SoccerBrain(input_size)

    X, y_win, y_formation, y_goals = build_training_data()

    print(f"Training on {len(X)} segments from {len(games)} games")
    print(f"Input features: {input_size}")
    print(f"Formations: {FORMATIONS}")
    print()

    # Loss functions — one for each head
    win_loss_fn = nn.BCELoss()                    # binary cross-entropy for win/loss
    formation_loss_fn = nn.CrossEntropyLoss()     # multi-class for formation
    goals_loss_fn = nn.MSELoss()                  # mean squared error for goal count

    # Optimizer — Adam is the go-to for most neural networks
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    for epoch in range(epochs):
        # Forward pass — run data through the network
        pred_win, pred_formation, pred_goals = model(X)

        # Calculate losses for each head
        loss_win = win_loss_fn(pred_win, y_win)
        loss_formation = formation_loss_fn(pred_formation, y_formation)
        loss_goals = goals_loss_fn(pred_goals, y_goals)

        # Combined loss — weight them so one head doesn't dominate
        total_loss = loss_win + 0.5 * loss_formation + 0.3 * loss_goals

        # Backward pass — calculate gradients
        optimizer.zero_grad()   # clear old gradients
        total_loss.backward()   # compute new gradients
        optimizer.step()        # update weights

        # Print progress every 100 epochs
        if (epoch + 1) % 100 == 0:
            print(f"Epoch {epoch+1}/{epochs} | "
                  f"Loss: {total_loss.item():.4f} | "
                  f"Win loss: {loss_win.item():.4f} | "
                  f"Formation loss: {loss_formation.item():.4f} | "
                  f"Goals loss: {loss_goals.item():.4f}")

    # Save the trained model
    torch.save(model.state_dict(), "soccer_brain.pth")
    print(f"\nModel saved to soccer_brain.pth")

    return model


def load_model():
    """Load a previously trained model."""
    input_size = get_input_size()
    model = SoccerBrain(input_size)
    model.load_state_dict(torch.load("soccer_brain.pth", weights_only=True))
    model.eval()  # switch to evaluation mode (disables dropout)
    return model


def predict(model, lineup, formation, start_min, end_min):
    """
    Ask the trained model about a proposed lineup.

    Returns a dict with win probability, recommended formation, and predicted goals.
    """
    segment = {
        "lineup": [{"position": pos, "stats": player.stats, "player": player.name}
                    for pos, player in lineup],
        "formation": formation,
        "start_min": start_min,
        "end_min": end_min,
    }

    features = segment_to_features(segment)
    x = torch.tensor([features], dtype=torch.float32)

    with torch.no_grad():  # no need to track gradients for prediction
        win_prob, formation_scores, pred_goals = model(x)

    # Get best formation
    best_formation_idx = torch.argmax(formation_scores, dim=1).item()

    return {
        "win_probability": win_prob.item(),
        "recommended_formation": FORMATIONS[best_formation_idx],
        "formation_confidence": torch.softmax(formation_scores, dim=1)[0].tolist(),
        "predicted_goals": pred_goals.item(),
    }


# ---- Run training directly ----

if __name__ == "__main__":
    model = train()

    # Quick test with the training data
    X, y_win, y_formation, y_goals = build_training_data()
    with torch.no_grad():
        pred_win, pred_form, pred_goals = model(X)

    print("\n--- Predictions on training data ---")
    for i, game in enumerate(games):
        for j, seg in enumerate(game["segments"]):
            idx = sum(len(g["segments"]) for g in games[:i]) + j
            print(f"{game['opponent']} seg {j+1}: "
                  f"win={pred_win[idx].item():.2f} "
                  f"goals={pred_goals[idx].item():.1f} "
                  f"(actual: win={y_win[idx].item():.0f} goals={y_goals[idx].item():.0f})")