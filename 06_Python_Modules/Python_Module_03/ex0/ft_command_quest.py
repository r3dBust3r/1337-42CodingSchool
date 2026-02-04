from sys import argv

print("=== Command Quest ===")
arg_count = len(argv)
if (arg_count == 1):
    print("No arguments provided!")
    print(f"Program name: {argv[0]}")
    print(f"Total arguments: {arg_count}")
else:
    print(f"Program name: {argv[0]}")
    print(f"Arguments received: {arg_count - 1}")
    i = 0
    for cmd in argv:
        i += 1
        if (i == arg_count):
            break
        print(f"Argument {i}: {argv[i]}")
    print(f"Total arguments: {arg_count}")
