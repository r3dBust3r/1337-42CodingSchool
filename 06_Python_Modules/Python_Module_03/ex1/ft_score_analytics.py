from sys import argv

print("=== Player Score Analytics ===")

if (len(argv) != 1):
    scores = []
    for arg in argv[1:]:
        try:
            scores.append(int(arg))
        except Exception:
            print(f"[!] Not a valid score: {arg}")
    try:
        print(f"Scores processed: {scores}")
        print(f"Total players: {len(scores)}")
        print(f"Total score: {sum(scores)}")
        print(f"Average score: {sum(scores) / len(scores)}")
        print(f"High score: {max(scores)}")
        print(f"Low score: {min(scores)}")
        print(f"Score range: {max(scores) - min(scores)}")
    except ZeroDivisionError:
        print("No scores to process!")
else:
    print(
        "No scores provided. Usage: python3 "
        "ft_score_analytics.py <score1> <score2> ..."
    )
