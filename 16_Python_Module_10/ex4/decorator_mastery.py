from functools import wraps
from time import time, sleep


def spell_timer(func: callable) -> callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Casting {func.__name__}...")

        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()

        elapsed = end_time - start_time
        print(f"Spell completed in {elapsed:.3f} seconds")

        return result

    return wrapper


def power_validator(min_power: int) -> callable:
    def decorator(func: callable) -> callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                power = args[2]
            except IndexError:
                raise TypeError("Expected power as the third positional argument")

            if power >= min_power:
                return func(*args, **kwargs)

            return "Insufficient power for this spell"

        return wrapper
    return decorator


def retry_spell(max_attempts: int) -> callable:
    def decorator(func: callable) -> callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_attempts:
                        print(f"Spell failed, retrying... (attempt {attempt}/{max_attempts})")
                    else:
                        print(f"Spell failed, no more attempts left.")
                        return f"Spell casting failed after {max_attempts} attempts"
        return wrapper
    return decorator



class MageGuild:
    def __init__(self, name):
        self.name = name


    @staticmethod
    def validate_mage_name(name: str) -> bool:
        cleaned = name.strip()
        if len(cleaned) < 3:
            return False

        for ch in cleaned:
            if not (ch.isalpha() or ch.isspace()):
                return False

        return True

    @power_validator(10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


@spell_timer
def cast_spell(spell_name):
    sleep(0.101)
    return f"{spell_name.capitalize()} cast!"


def main():
    print("Testing spell timer...")
    mage = MageGuild("fireball")
    print(f"Result: {cast_spell(mage.name)}")
    
    print(f"\nTesting {mage.__class__.__name__}...")

    print(mage.validate_mage_name(mage.name))
    print(mage.validate_mage_name("invalid-Mage"))

    guild = MageGuild("Arcane")

    print(guild.cast_spell("Lightning", 15))
    print(guild.cast_spell("Fire", 8))


if __name__ == "__main__":
    main()
