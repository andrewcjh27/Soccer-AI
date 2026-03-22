# Soccer AI

An AI-powered soccer team management system that combines neural network player evaluation with linear programming lineup optimization and a conversational AI coach.

## Overview

Soccer AI helps recreational team managers make data-driven decisions about formations and player assignments. It evaluates players using a trained neural network, optimizes lineup assignments with linear programming, and provides tactical advice through a chat-based AI coach that considers opponent scouting data.

## Features

- **Player Evaluation** — Multi-attribute player rating system with position-specific stat weighting (GK, DEF, MID, FWD)
- **Formation Optimizer** — Linear programming (PuLP) solver that finds the optimal player-to-position assignment across multiple formations
- **Neural Network Predictions** — PyTorch model trained on game history data to predict win probability and recommend formations
- **AI Coach Chat** — Conversational interface that provides tactical recommendations, substitution advice, and opponent analysis
- **Opponent Scouting** — Pre-match scouting input to adjust tactical recommendations

## Tech Stack

- Python 3.9+
- PyTorch (neural network)
- PuLP (linear programming)
- OpenAI API (chat interface)

## Usage

```bash
pip install torch pulp requests
python chat.py
```

The chat interface will prompt for opponent scouting data, then provide an interactive coaching session with lineup recommendations.

## Project Structure

- `player.py` — Player class with position-specific stat weights and rating logic
- `optimizer.py` — LP-based lineup optimizer with formation definitions
- `soccer_brain.py` — PyTorch neural network for win prediction and formation recommendation
- `game_data.py` — Historical game data for model training
- `chat.py` — Chat-based AI coach interface
- `test_optimizer.py`, `test_players.py` — Unit tests
