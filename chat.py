import os
import json
import requests
import torch
from player import Player
from optimizer import recommend
from soccer_brain import load_model, predict, FORMATIONS

# ---- Your roster ----
roster = [
    Player("Junho",    ["FWD", "MID", "GK"],  {"shooting": 7, "passing": 6, "dribbling": 4, "defending": 7, "speed": 7, "stamina": 5, "positioning": 8, "vision": 7, "saving": 9}),
    Player("Declan",   ["DEF", "MID", "FWD"], {"shooting": 8, "passing": 7, "dribbling": 6, "defending": 8, "speed": 7, "stamina": 7, "positioning": 5, "vision": 7, "saving": 2}),
    Player("Allison",  ["FWD", "MID"],        {"shooting": 6, "passing": 5, "dribbling": 5, "defending": 3, "speed": 4, "stamina": 6, "positioning": 2, "vision": 4, "saving": 2}),
    Player("Daniel_L", ["FWD"],               {"shooting": 5, "passing": 4, "dribbling": 4, "defending": 3, "speed": 5, "stamina": 5, "positioning": 2, "vision": 2, "saving": 1}),
    Player("Daniel_R", ["DEF"],               {"shooting": 6, "passing": 6, "dribbling": 6, "defending": 7, "speed": 7, "stamina": 8, "positioning": 4, "vision": 5, "saving": 5}),
    Player("Brian",    ["GK", "FWD", "MID"],  {"shooting": 4, "passing": 5, "dribbling": 5, "defending": 5, "speed": 5, "stamina": 5, "positioning": 6, "vision": 4, "saving": 7}),
    Player("Roshni",   ["DEF", "FWD"],        {"shooting": 7, "passing": 7, "dribbling": 6, "defending": 7, "speed": 6, "stamina": 7, "positioning": 6, "vision": 6, "saving": 6}),
    Player("Mandy",    ["DEF"],               {"shooting": 5, "passing": 5, "dribbling": 5, "defending": 6, "speed": 5, "stamina": 6, "positioning": 2, "vision": 3, "saving": 2}),
    Player("Soleil",   ["FWD", "MID"],        {"shooting": 6, "passing": 5, "dribbling": 5, "defending": 3, "speed": 4, "stamina": 6, "positioning": 2, "vision": 3, "saving": 2}),
    Player("Katie",    ["DEF"],               {"shooting": 4, "passing": 4, "dribbling": 4, "defending": 4, "speed": 4, "stamina": 5, "positioning": 2, "vision": 2, "saving": 1}),
]


def get_opponent_info():
    """
    Ask the user for the opponent's record before the session starts.
    Returns a dict with their stats and a computed tactical recommendation.
    """
    print("\n--- Opponent Scouting ---")
    print("Enter 'skip' for any field to leave it unknown.\n")

    # Collect win / loss / draw
    def ask_int(prompt):
        while True:
            raw = input(prompt).strip()
            if raw.lower() == "skip":
                return None
            try:
                val = int(raw)
                if val < 0:
                    raise ValueError
                return val
            except ValueError:
                print("  Please enter a whole number (0 or more), or 'skip'.")

    wins   = ask_int("  Opponent wins:   ")
    losses = ask_int("  Opponent losses: ")
    draws  = ask_int("  Opponent draws:  ")

    # Optional: any extra notes (e.g. "very fast forwards", "weak GK")
    notes_raw = input("  Any notes about their playstyle? (or press Enter to skip): ").strip()
    notes = notes_raw if notes_raw.lower() not in ("", "skip") else None

    # Build the opponent context block and derive a tactical stance
    lines = ["\n=== OPPONENT SCOUTING REPORT ==="]

    total_games = sum(v for v in [wins, losses, draws] if v is not None)

    if wins is not None and losses is not None:
        total_decided = wins + losses + (draws or 0)
        win_ratio = wins / total_decided if total_decided > 0 else None

        record_parts = []
        if wins   is not None: record_parts.append(f"{wins}W")
        if losses is not None: record_parts.append(f"{losses}L")
        if draws  is not None: record_parts.append(f"{draws}D")
        lines.append(f"Record: {' / '.join(record_parts)}  ({total_decided} games played)")

        if win_ratio is not None:
            lines.append(f"Win ratio: {win_ratio:.0%}")

            # Derive tactical advice from win ratio
            if win_ratio >= 0.65:
                stance = "DEFENSIVE"
                reasoning = (
                    "This opponent wins often — treat them as a strong side. "
                    "Sit deeper, protect the defensive shape, and look for quick counter-attacks. "
                    "Prioritise keeping a clean sheet over chasing goals early."
                )
            elif win_ratio <= 0.35:
                stance = "OFFENSIVE"
                reasoning = (
                    "This opponent loses more than they win — they are beatable. "
                    "Push men forward early, press high, and take the game to them. "
                    "Use width and pace to overload their defence."
                )
            else:
                stance = "BALANCED"
                reasoning = (
                    "This is an evenly matched opponent. Play your normal structured game — "
                    "stay compact defensively but be ready to exploit any gaps that open up. "
                    "Adapt in real time depending on which team scores first."
                )

            lines.append(f"Recommended tactical stance: {stance}")
            lines.append(f"Tactical reasoning: {reasoning}")
    else:
        lines.append("Record: unknown (no win/loss data provided)")
        lines.append("Recommended tactical stance: BALANCED (default — no opponent data)")

    if notes:
        lines.append(f"Scout notes: {notes}")

    return "\n".join(lines)


def get_game_info():
    """
    Ask for basic game info before the session starts.
    Returns the total match length in minutes.
    """
    print("\n--- Game Info ---")
    while True:
        raw = input("  How long is the match in minutes? (press Enter for default 40): ").strip()
        if raw == "":
            return 40
        try:
            val = int(raw)
            if val > 0:
                return val
            print("  Must be a positive number.")
        except ValueError:
            print("  Please enter a whole number, or press Enter for 40.")


def build_sub_schedule(lineup, bench, game_length):
    """
    Compute a stamina-based substitution schedule for the starting lineup.

    For each starter, stamina_minutes() says how long they can play at peak.
    If that's less than game_length, they need a sub at that minute.
    The best available bench player (position match preferred, then overall rating)
    is assigned to replace them.

    Returns a formatted string block ready to be inserted into the AI context.
    """
    lines = [f"\n=== SUBSTITUTION SCHEDULE ({game_length}-min game) ==="]
    lines.append(
        "Fatigue formula: a player with stamina S plays at peak for "
        "round((S / 10) × game_length) minutes."
    )

    needs_sub = []   # (sub_at_minute, position, starter)
    full_game  = []  # (position, starter) — high enough stamina to last all game

    for position, player in lineup:
        sub_at = player.stamina_minutes(game_length)
        if sub_at < game_length:
            needs_sub.append((sub_at, position, player))
        else:
            full_game.append((position, player))

    # Sort by earliest sub first
    needs_sub.sort(key=lambda x: x[0])

    if not needs_sub:
        lines.append("  All starters have enough stamina to play the full game — no subs needed.")
    else:
        bench_pool = list(bench)  # working copy so we don't modify the original list

        for sub_at, position, starter in needs_sub:
            stamina = starter.stats.get("stamina", 5)

            # Prefer a bench player who plays this position naturally
            candidates = [p for p in bench_pool if position in p.positions]
            if not candidates:
                candidates = bench_pool  # fall back to anyone available

            if candidates:
                replacement = max(candidates, key=lambda p: p.overall_rating())
                bench_pool.remove(replacement)
                rep_stamina = replacement.stats.get("stamina", 5)
                lines.append(
                    f"  ~{sub_at:>2} min  |  "
                    f"OUT {starter.name} ({position}, stamina {stamina}/10)"
                    f"  →  IN {replacement.name} "
                    f"(overall {replacement.overall_rating():.1f}, stamina {rep_stamina}/10)"
                )
            else:
                lines.append(
                    f"  ~{sub_at:>2} min  |  "
                    f"OUT {starter.name} ({position}, stamina {stamina}/10)"
                    f"  →  No bench player left — rotate a previously-subbed player back in."
                )

        # Any bench players not assigned a scheduled slot yet
        if bench_pool:
            names = ", ".join(
                f"{p.name} (overall {p.overall_rating():.1f})" for p in bench_pool
            )
            lines.append(f"\n  Unscheduled bench: {names}")
            lines.append(
                "  → Hold them for injuries, tactical changes, or to re-enter "
                "a tired player who has recovered on the sideline."
            )

    # Players who go the full game
    if full_game:
        names = ", ".join(
            f"{p.name} ({pos}, stamina {p.stats.get('stamina', 5)}/10)"
            for pos, p in full_game
        )
        lines.append(f"\n  Full-game starters (no sub needed): {names}")

    return "\n".join(lines)


def build_context(opponent_block, game_length):
    """
    Build a rich context string that combines:
    1. Your roster info
    2. The opponent scouting report
    3. The PuLP optimizer's recommendations
    4. The stamina-based substitution schedule
    5. The neural network's predictions
    """
    lines = ["=== ROSTER ==="]
    for p in roster:
        stats_str = ", ".join(f"{k}={v}" for k, v in p.stats.items())
        lines.append(f"- {p.name} (positions: {p.positions}, overall: {p.overall_rating():.1f}, {stats_str})")

    # Inject the opponent scouting report right after the roster
    lines.append(opponent_block)

    # Run the optimizer
    results = recommend(roster)
    lines.append("\n=== OPTIMIZER RECOMMENDATIONS ===")
    for i, r in enumerate(results[:3]):
        lines.append(f"\nOption {i+1}: {r['formation'].name} (fit score: {r['score']:.1f})")
        for position, player in r['lineup']:
            fit = player.position_fit(position)
            lines.append(f"  {position} -> {player.name} (fit: {fit:.1f})")

    # Build the substitution schedule from the top optimizer lineup
    top_lineup  = results[0]["lineup"]
    starters    = {player for _, player in top_lineup}
    bench       = [p for p in roster if p not in starters]
    lines.append(build_sub_schedule(top_lineup, bench, game_length))

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

You have access to FIVE sources of intelligence:
1. ROSTER — each player's stats (1-10 ratings)
2. OPPONENT SCOUTING REPORT — their win/loss record, win ratio, and scout notes
3. OPTIMIZER — a mathematical optimizer (PuLP) that finds the best player-position assignments
4. SUBSTITUTION SCHEDULE — stamina-based plan showing exactly when each starter tires out
   and which bench player should replace them
5. NEURAL NETWORK — a custom-trained model that predicts win probability and goals

CRITICAL RULES — never break these:
- This is 6v6 soccer. A starting lineup ALWAYS has EXACTLY 6 players. Never list fewer.
- When recommending starters, you MUST use the Optimizer's top lineup as your base.
  List every single player from that lineup: GK, DEF(s), MID(s), FWD(s).
- Do NOT invent your own lineup from scratch or skip any position — the Optimizer has
  already done the math to find the best 6-player assignment.
- Higher overall rating = stronger player. Never recommend a lower-rated player over a
  higher-rated one for the same role unless you can cite a specific tactical reason.

OPPONENT-AWARE TACTICS:
- Always read the OPPONENT SCOUTING REPORT first.
- If the recommended stance is DEFENSIVE: suggest deeper formations (more DEFs), conservative
  passing, and counter-attack plans. Highlight your best defenders and GK.
- If the recommended stance is OFFENSIVE: suggest pushing forwards, pressing high, and
  formations with extra FWDs/MIDs. Highlight your best attackers.
- If the recommended stance is BALANCED: suggest a flexible formation and advise adapting
  based on the first 10 minutes of play.
- If scout notes mention specific opponent traits (e.g. "fast wingers"), factor that into
  your positional and tactical advice.
- If no opponent data was provided, default to a balanced approach.

SUBSTITUTION RULES — always follow these when asked about subs:
- Use the SUBSTITUTION SCHEDULE as your primary source for sub timing. Do not invent
  your own timing — the schedule already computed it from each player's stamina stat.
- When announcing a sub, always say: the minute, who comes OFF and their position,
  who comes ON and their position, and why (stamina drop).
- Since unlimited rolling substitutions are allowed, players who have rested on the
  bench can come back on — mention this if the bench runs out of fresh players.
- If the game situation changes (e.g. losing late, or a player gets hurt), advise
  pulling a sub forward earlier than scheduled rather than waiting.
- Never leave a visibly tired player on the field past their scheduled sub minute.

Use ALL five sources to give advice. When the optimizer and neural network disagree,
explain why and give your recommendation.

Be concise, specific, and use player names. Keep it fun — this is a casual league.
If asked about a player being unavailable, mentally remove them and re-evaluate,
but still always fill all 6 slots with the remaining players.

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

    # Collect game length and opponent info before building context
    game_length    = get_game_info()
    opponent_block = get_opponent_info()

    print("\nAnalysing matchup...")
    context = build_context(opponent_block, game_length)
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
