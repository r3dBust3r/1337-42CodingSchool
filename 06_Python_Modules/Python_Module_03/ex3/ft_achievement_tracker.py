print("=== Achievement Tracker System ===\n")

alice = {
    'first_kill',
    'level_10',
    'treasure_hunter',
    'speed_demon'
}
bob = {
    'first_kill',
    'level_10',
    'boss_slayer',
    'collector'
}
charlie = {
    'level_10',
    'treasure_hunter',
    'boss_slayer',
    'speed_demon',
    'perfectionist'
}
all_achievements = alice.union(bob).union(charlie)

print(f"Player alice achievements: {alice}")
print(f"Player bob achievements: {bob}")
print(f"Player charlie achievements: {charlie}")

print("\n=== Achievement Analytics ===")
print(f"All unique achievements: {all_achievements}")
print(f"Total unique achievements: {len(all_achievements)}")

print("")
common = alice.intersection(bob).intersection(charlie)
print(f"Common to all players: {common}")

alice_rare = alice.difference(bob).difference(charlie)
bob_rare = bob.difference(alice).difference(charlie)
charlie_rare = charlie.difference(alice).difference(bob)
rare = alice_rare.union(bob_rare).union(charlie_rare)
print(f"Rare achievements (1 player): {rare}")

print("")
print(f"Alice vs Bob common: {alice.intersection(bob)}")
print(f"Alice unique: {alice.difference(bob)}")
print(f"Bob unique: {bob.difference(alice)}")
