from math import sqrt

print("=== Game Coordinate System ===\n")

x = (10, 20, 5)
x_pos = sqrt((x[0]-0)**2 + (x[1]-0)**2 + (x[2]-0)**2)
print(f"Position created: {x}")
print(f"Distance between (0, 0, 0) and {x}: {x_pos:.2f}")

y = "3,4,0"
print(f"\nParsing coordinates: \"{y}\"")
y = tuple(y.split(","))
y = (int(y[0]), int(y[1]), int(y[2]))

y_pos = sqrt((y[0]-0)**2 + (y[1]-0)**2 + (y[2]-0)**2)
print(f"Position position: {y}")
print(f"Distance between (0, 0, 0) and {y}: {y_pos}")

z = "abc,def,ghi"
print(f"\nParsing invalid coordinates: \"{z}\"")
z = tuple(z.split(","))

try:
    z_pos = sqrt((int(z[0])-0)**2 + (int(z[1])-0)**2 + (int(z[2])-0)**2)
except Exception as e:
    print(f"Error parsing coordinates: {e}")
    print(f"Error details - Type: ValueError, Args: {e.args}")

print("\nUnpacking demonstration:")
print(f"Player at x={y[0]}, y={y[1]}, z={y[2]}")
print(f"Coordinates: X={y[0]}, Y={y[1]}, Z={y[2]}")
