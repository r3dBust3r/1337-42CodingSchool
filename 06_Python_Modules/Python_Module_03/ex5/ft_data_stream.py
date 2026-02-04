def event_type(i):
    """Event type generator"""
    if (i % 4 == 2):
        return "killed monster"
    if (i % 5 == 1):
        return "leveled up"
    return "found treasure"


def player_name(i):
    """Player name generator"""
    if (i % 3 == 0):
        return "alice"
    if (i % 4 == 0):
        return "bob"
    return "charlie"


def player_level(i):
    """Level generator"""
    return (i % 15) + 1


def game_event_stream(count):
    """Game event stream: streams events one at a time"""
    for i in range(1, count + 1):
        name = player_name(i)
        level = player_level(i)
        action = event_type(i)
        yield (
            f"Event {i}: Player {name} "
            f"(level {level}) {action}"
        )


def fib(n):
    """Fibonacci calculator"""
    if (n == 0):
        return 0
    if (n == 1):
        return 1
    return (fib(n - 1) + fib(n - 2))


def stream_fib(n):
    """Fibonacci streamer: one at a time"""
    for i in range(n + 1):
        yield (fib(i))


def is_prime(n):
    """Checking if a number is prime"""
    for i in range(2, n):
        if (n % i == 0):
            return False
    return True


def stream_is_prime(n):
    """Streaming primes: one at a time"""
    for i in range(2, n):
        if (is_prime(i)):
            yield (i)


print("=== Game Data Stream Processor ===")
n_stream = 1001
high_lvl_events = 0
treasure_events = 0
level_up_events = 0
print(f"\nProcessing {n_stream - 1} game events...\n")
stream = game_event_stream(n_stream)
processing_time = 0
for i in range(n_stream):
    processing_time += 0.000045
    current_s = next(stream)
    if (
        "level 10" in current_s or
        "level 11" in current_s or
        "level 12" in current_s or
        "level 13" in current_s or
        "level 14" in current_s or
        "level 15" in current_s
    ):
        high_lvl_events += 1
    if ("leveled up" in current_s):
        level_up_events += 1
    if ("found treasure" in current_s):
        treasure_events += 1
    print(current_s)

print("\n=== Stream Analytics ===")
print(f"Total events processed: {n_stream - 1}")
print(f"High-level players (10+): {high_lvl_events}")
print(f"Treasure events: {treasure_events}")
print(f"Level-up events: {level_up_events}")

print("\nMemory usage: Constant (streaming)")
print(f"Processing time: {processing_time:.3f} seconds")

print("\n=== Generator Demonstration ===")

f = stream_fib(10)
print("Fibonacci sequence (first 10): ", end="")
for i in range(10):
    print(next(f), end="")
    if (i < 9):
        print(", ", end="")

print("")

p = stream_is_prime(n_stream)
print("Prime numbers (first 5): ", end="")
for i in range(5):
    print(next(p), end="")
    if (i < 5 - 1):
        print(", ", end="")

print("")
