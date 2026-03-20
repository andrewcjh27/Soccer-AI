import os
import json
import requests
import torch
from player import Player
from optimizer import recommend
from soccer_brain import load_model, predict, FORMATIONS

# ---- Your roster ----
roster = [
    Player("Junho",    ["FWD", "MID", "GK"],  {"shooting": 7, "passing": 6, "dribbling": 4, "defending": 7, "speed": 7, "stamina": 5, "positioning": 8, "vision": 8, "saving": 9}),
    Player("Declan",   ["DEF", "MID", "FWD"], {"shooting": 8, "passing": 7, "dribbling": 6, "defending": 8, "speed": 7, "stamina": 7, "positioning": 5, "vision": 5, "saving": 2}),
    Player("Allison",  ["FWD", "MID"],        {"shooting": 6, "passing": 5, "dribbling": 5, "defending": 3, "speed": 4, "stamina": 6, "positioning": 2, "vision": 2, "saving": 2}),
    Player("Daniel_L", ["FWD"],               {"shooting": 5, "passing": 4, "dribbling": 4, "defending": 3, "speed": 5, "stamina": 5, "positioning": 2, "vision": 2, "saving": 1}),
    Player("Daniel_R", ["DEF"],               {"shooting": 6, "passing": 6, "dribbling": 6, "defending": 7, "speed": 7, "stamina": 8, "positioning": 4, "vision": 5, "saving": 5}),
    Player("Brian",    ["GK", "FWD", "MID"],  {"shooting": 4, "passing": 5, "dribbling": 5, "defending": 5, "speed": 5, "stamina": 5, "positioning": 6, "vision": 6, "saving": 7}),
    Player("Roshni",   ["DEF", "FWD"],        {"shooting": 7, "passing": 7, "dribbling": 6, "defending": 7, "speed": 6, "stamina": 7, "positioning": 6, "vision": 6, "saving": 6}),
    Player("Mandy",    ["DEF"],               {"shooting": 5, "passing": 5, "dribbling": 5, "defending": 6, "speed": 5, "stamina": 6, "positioning": 2, "vision": 2, "saving": 2}),
    Player("Soleil",   ["FWD", "MID"],        {"shooting": 6, "passing": 5, "dribbling": 5, "defending": 3, "speed": 4, "stamina": 6, "positioning": 2, "vision": 2, "saving": 2}),
    Player("Katie",    ["DEF"],               {"shooting": 4, "passing": 4, "dribbling": 4, "defending": 4, "speed": 4, "stamina": 5, "positioning": 2, "vision": 2, "saving": 1}),
]

def build_context():
    """
    Build a rich context string that combines:
    1. Your roster info
    2. The PuLP optimizer's recommendations
    3. The neural network's predictions
    """
    lines = ["=== ROSTER ==="]
    for p in roster:
        stats_str = ", ".join(f"{k}={v}" for k, v in p.stats.items())
        lines.append(f"- {p.name} (positions: {p.positions}, overall: {p.overall_rating():.1f}, {stats_str})")

    # Run the optimizer
    results = recommend(roster)
    lines.append("\n=== OPTIMIZER RECOMMENDATIONS ===")
    for i, r in enumerate(results[:3]):
        lines.append(f"\nOption {i+1}: {r['formation'].name} (fit score: {r['score']:.1f})")
        for position, player in r['lineup']:
            fit = player.position_fit(position)
            lines.append(f"  {position} -> {player.name} (fit: {fit:.1f})")


    # Run the neural network predictions
    try:
        model = load_model()
        lines.append("\n=== NEURAL NETWORK PREDICTIONS ===")
        for i, r in enumerate(results[:3]):
            prediction = predict(model, r['lineup'], r['formation'].name, 0, 20)
            lines.append(
                f"Formation {r['formation'].name}: "
                f"win prob={prediction['win_probability']:.0%}, "
                f"predicted goals={prediction['predicted_goals']:.1f}"
            )

        # Also show what formation the NN recommends
        best = predict(model, results[0]['lineup'], results[0]['formation'].name, 0, 20)
        lines.append(f"\nNeural network's top pick: {best['recommended_formation']}")
    except FileNotFoundError:
        lines.append("\n(Neural network not trained yet — run 'python3 soccer_brain.py' first)")

    return "\n".join(lines)


SYSTEM_PROMPT = """You are a tactical assistant for a 6v6 recreational soccer team.

You have access to THREE sources of intelligence:
1. ROSTER — each player's stats (1-10 ratings)
2. OPTIMIZER — a mathematical optimizer (PuLP) that finds the best player-position assignments
3. NEURAL NETWORK — a custom-trained model that predicts win probability and goals based on game history

Use ALL three sources to give advice. When the optimizer and neural network disagree,
explain why and give your recommendation.

Be concise, specific, and use player names. Keep it fun — this is a casual league.
If asked about a player being unavailable, mentally remove them and re-evaluate.

Here is the current analysis:

{context}
"""

def ask_ollama(system_prompt, messages):
    """
    Send a message to the local Ollama LLM.
    This runs entirely on your Mac — no API key, no internet needed.
    """
    formatted = [{"role": "system", "content": system_prompt}]
    formatted.extend(messages)

    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "llama3.2",
                "messages": formatted,
                "stream": False,
            },
            timeout=300,
        )
        response.raise_for_status()
        return response.json()["message"]["content"]
    except requests.exceptions.ConnectionError:
        return ("ERROR: Can't connect to Ollama. Make sure it's running:\n"
                "  Open a new terminal and run: ollama serve")
    except Exception as e:
        return f"ERROR: {e}"


def main():
    print("Loading team data and models...")
    context = build_context()
    system = SYSTEM_PROMPT.format(context=context)

    messages = []

    print()
    print("=" * 55)
    print("  SOCCER AI - Your Team's Tactical Assistant")
    print("  Powered by: PuLP optimizer + PyTorch brain + Llama")
    print("  Type 'quit' to exit")
    print("=" * 55)
    print()

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Good game!")
            break

        messages.append({"role": "user", "content": user_input})

        print("\nCoach AI is thinking...\n")
        reply = ask_ollama(system, messages)

        messages.append({"role": "assistant", "content": reply})
        print(f"Coach AI: {reply}\n")


if __name__ == "__main__":
    main()