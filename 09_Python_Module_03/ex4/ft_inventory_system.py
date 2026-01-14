def format_attributes(attributes):
    """Attributes formater that removes (')"""
    count = len(attributes)
    format_attrs = "("
    i = 0
    for attr in attributes:
        format_attrs += attr
        if (i < count - 1):
            format_attrs += ", "
        i += 1
    format_attrs += ")"
    return format_attrs


def inventory_stats(inventory, printable=True):
    """Inventory statistics function"""
    inventory_value = 0
    item_count = 0
    weapon_count = 0
    consumable_count = 0
    armor_count = 0
    for item in inventory:
        count = inventory.get(item)['count']
        price = inventory.get(item)['price']
        attributes = inventory.get(item)['attributes']
        if (printable):
            print(
                f"{item} {format_attributes(attributes)}: "
                f"{count}x @ {price} gold each = {price * count} gold")
        inventory_value += price * count
        item_count += count
        if ("weapon" in attributes):
            weapon_count += count
        if ("consumable" in attributes):
            consumable_count += count
        if ("armor" in attributes):
            armor_count += count
    return (
        inventory_value,
        item_count,
        weapon_count,
        consumable_count,
        armor_count
    )


print("=== Player Inventory System ===")

print("\n=== Alice's Inventory ===")
alice_inventory = {
    "sword": {
        "count": 1,
        "price": 500,
        "attributes": ("weapon", "rare")
    },
    "potion": {
        "count": 5,
        "price": 50,
        "attributes": ("consumable", "common")
    },
    "shield": {
        "count": 1,
        "price": 200,
        "attributes": ("armor", "uncommon")
    },
}

alice_inventory_value, \
    alice_item_count, \
    alice_weapon_count, \
    alice_consumable_count, \
    alice_armor_count = inventory_stats(alice_inventory)

print(f"\nInventory value: {alice_inventory_value} gold")
print(f"Item count: {alice_item_count} items")
print(
    f"Categories: weapon({alice_weapon_count}), "
    f"consumable({alice_consumable_count}), armor({alice_armor_count})"
)

bob_inventory = {
    "magic_ring": {"count": 1, "price": 150, "attributes": ("rare")},
}

given = 2
print(f"\n=== Transaction: Alice gives Bob {given} potions ===")
alice_inventory.update(
    {
        "potion": {
            "count": alice_inventory["potion"]["count"] - given,
            "price": 50,
            "attributes": ("consumable", "common")
        },
    }
)

bob_inventory.update(
    {
        "potion": {
            "count": given,
            "price": 50,
            "attributes": ("consumable", "common")
        },
    }
)

print("Transaction successful!")

print("\n=== Updated Inventories ===")
print(f"Alice potions: {alice_inventory['potion']['count']}")
print(f"Bob potions: {bob_inventory['potion']['count']}")

bob_inventory_value, \
    bob_item_count, \
    bob_weapon_count, \
    bob_consumable_count, \
    bob_armor_count = inventory_stats(bob_inventory, False)

alice_inventory_value, \
    alice_item_count, \
    alice_weapon_count, \
    alice_consumable_count, \
    alice_armor_count = inventory_stats(alice_inventory, False)

print("\n=== Inventory Analytics ===")

most_val_plr = {}

if (alice_inventory_value > bob_inventory_value):
    most_val_plr = {
        "name": "alice",
        "value": alice_inventory_value,
        "item_count": alice_item_count
    }
else:
    most_val_plr = {
        "name": "bob",
        "value": bob_inventory_value,
        "item_count": bob_item_count
    }

print(
    f"Most valuable player: "
    f"{most_val_plr['name'].capitalize()} ({most_val_plr['value']} gold)"
)
print(
    f"Most items: "
    f"{most_val_plr['name'].capitalize()} ({most_val_plr['item_count']} items)"
)

print("Rarest items: ", end="")
for item in alice_inventory:
    if ("rare" in alice_inventory[item]['attributes']):
        print(item, end="")
print("", end=", ")
for item in bob_inventory:
    if ("rare" in bob_inventory[item]['attributes']):
        print(item, end="")
print("")
