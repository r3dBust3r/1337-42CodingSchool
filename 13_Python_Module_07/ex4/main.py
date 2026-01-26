from typing import Dict
from ex4 import TournamentCard, TournamentPlatform


def main():
    print("=== DataDeck Tournament Platform ===\n")
    print("Registering Tournament Cards...")
    tournament_card1: TournamentCard = TournamentCard(
        "Fire Dragon", 10, "Legendary"
    )
    tournament_card2: TournamentCard = TournamentCard(
        "Ice Wizard", 8, "Legendary"
    )

    tournament_platform: TournamentPlatform = TournamentPlatform()
    print(tournament_platform.register_card(tournament_card1))
    print(tournament_platform.register_card(tournament_card2))

    print()
    match_return: Dict = tournament_platform.create_match(
        f"{tournament_card1.name.split(' ')[1].lower()}_001",
        f"{tournament_card2.name.split(' ')[1].lower()}_001"
    )

    print(f"Match created: {match_return}\n")

    print(
        f"{tournament_card1.name} "
        f"(ID: {tournament_card1.name.split(' ')[1].lower()}_001):"
    )
    print(f"- Interfaces: {[b.__name__ for b in TournamentCard.__bases__]}")
    print(f"- Rating: {tournament_card1.calculate_rating()}")
    print(f"- Record: {tournament_card1.record}-{tournament_card2.record}")

    print(
        f"\n{tournament_card2.name} "
        f"(ID: {tournament_card2.name.split(' ')[1].lower()}_001):"
    )
    print(f"- Interfaces: {[b.__name__ for b in TournamentCard.__bases__]}")
    print(f"- Rating: {tournament_card2.calculate_rating()}")
    print(f"- Record: {tournament_card1.record}-{tournament_card2.record}")

    print("\nCreating tournament match...")
    TournamentCard.play(
        None,
        {'opp1': tournament_card1, 'opp2': tournament_card2}
    )
    print(f"Match result: {tournament_card1.get_combat_stats()}")

    tournament_card2.record += 1

    print("\nTournament Leaderboard:")
    tournament_card1.attack(tournament_card2)
    print(
        f"1. {tournament_card1.name} "
        f"- Rating: {tournament_card1.calculate_rating()} (1-0)"
    )
    print(
        f"2. {tournament_card2.name} "
        f"- Rating: {tournament_card2.calculate_rating()} (0-1)"
    )

    print("\nPlatform Report:")
    print(f"{TournamentCard.get_tournament_stats(TournamentCard)}")

    print("\n=== Tournament Platform Successfully Deployed! ===\n")
    print("All abstract patterns working together harmoniously!")


if __name__ == "__main__":
    main()
