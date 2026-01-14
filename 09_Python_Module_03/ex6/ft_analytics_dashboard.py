print("=== Game Analytics Dashboard ===")

players = ["alice", "bob", "charlie", "diana", "james"]
scores = {
    "alice": 2300,
    "bob": 1800,
    "charlie": 2090,
    "diana": 2100,
    "james": 990
}
achievements = {
    "alice": [
        "first_kill",
        "level_10",
        "boss_slayer",
        "explorer",
        "veteran"
    ],
    "bob": [
        "first_kill",
        "explorer",
        "level_10"
    ],
    "charlie": [
        "first_kill",
        "level_10",
        "boss_slayer",
        "elite",
        "veteran",
        "master",
        "legend"
    ],
    "diana": ["first_kill"],
    "james": []
}
regions = [
    "north",
    "east",
    "central",
    "north",
    "east"
]

print("\n=== List Comprehension Examples ===")

high_scorers = [p for p, s in scores.items() if s > 2000]
doubled_scores = [s * 2 for s in scores.values()]
active_players = [p for p, s in scores.items() if s > 2000]

print(f"High scorers (>2000): {high_scorers}")
print(f"Scores doubled: {doubled_scores}")
print(f"Active players: {active_players}")

print("\n=== Dict Comprehension Examples ===")

player_scores = {p: s for p, s in scores.items()}
score_categories = {
    "high": len([s for s in scores.values() if s > 2000]),
    "medium": len([s for s in scores.values() if 1500 <= s <= 2000]),
    "low": len([s for s in scores.values() if s < 1500])
}
achievement_counts = {p: len(a) for p, a in achievements.items()}

print(f"Player scores: {player_scores}")
print(f"Score categories: {score_categories}")
print(f"Achievement counts: {achievement_counts}")

print("\n=== Set Comprehension Examples ===")

unique_players = {p for p in players}
unique_achievements = {a for lst in achievements.values() for a in lst}
active_regions = {r for r in regions}

print(f"Unique players: {unique_players}")
print(f"Unique achievements: {unique_achievements}")
print(f"Active regions: {active_regions}")

print("\n=== Combined Analysis ===")

total_players = len(unique_players)
total_unique_achievements = len(unique_achievements)
average_score = sum(scores.values()) / len(scores)
top_player = max(scores, key=scores.get)

print(f"Total players: {total_players}")
print(f"Total unique achievements: {total_unique_achievements}")
print(f"Average score: {average_score}")
print(
    "Top performer:",
    top_player,
    f"({scores[top_player]} points,",
    f"{achievement_counts[top_player]} achievements)"
)
