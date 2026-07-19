*This project has been created as part of the 42 curriculum by ottalhao.*

# Fly-in

## Description

Fly-in is a drone routing and visualization project. It reads a custom map file, validates the topology, builds a graph of zones and connections, computes the best delivery paths, simulates drone movement turn by turn, and renders the result in an interactive Arcade window.

The goal is to move all drones from the start hub to the end hub while respecting:

- zone capacity limits
- connection capacity limits
- zone types such as normal, priority, restricted, and blocked
- the order and constraints defined in the map file

## Instructions

### Requirements

- Python 3.10 or newer
- `uv` for environment management and execution

### Installation

Install the project dependencies with:

```bash
make install
```

This runs `uv sync` and installs the packages declared in `pyproject.toml`:

- `arcade`
- `pydantic`
- `flake8`
- `mypy`

### Usage

Run the project with the default map:

```bash
make
```

Run it with a custom map:

```bash
make map=maps/easy/02_simple_fork.txt
```

You can also launch it directly:

```bash
uv run python3 main.py path/to/map.txt
```

Useful helper targets:

```bash
make lint
make debug
make clean
```

## Map Format

The parser expects a plain text file with this structure:

```text
nb_drones: 5

start_hub: start 0 0 [color=green]
hub: waypoint 1 0 [color=blue zone=priority max_drones=2]
end_hub: goal 2 0 [color=red]

connection: start-waypoint
connection: waypoint-goal [max_link_capacity=2]
```

Rules enforced by the parser:

- `nb_drones` must appear first and must be a positive integer.
- A map must contain at least one zone, one connection, one start hub, and one end hub.
- Zone lines use `start_hub`, `hub`, or `end_hub`.
- Connection lines use `connection: zone1-zone2`.
- Metadata is optional; when omitted, defaults are applied.
- `blocked` zones are not traversed by the path search.

Supported zone metadata:

- `color=<word>`
- `max_drones=<int>`
- `zone=normal|blocked|restricted|priority`

Supported connection metadata:

- `max_link_capacity=<int>`

## Algorithm

The routing logic uses a uniform-cost search over the zone graph.

Each zone contributes a movement cost based on its type:

- `normal` = `1.0`
- `priority` = `0.999`
- `restricted` = `2.0`
- `blocked` = not traversable

The graph search keeps a priority queue ordered by accumulated path cost and returns the two lowest-cost paths from the start zone to the end zone. Those paths are then assigned to drones in a round-robin manner using the drone identifier.

This approach is useful here because the project is not just looking for any path: it needs the cheapest valid route while still accounting for different terrain costs and capacity constraints. The slightly lower cost for priority zones nudges the search toward faster routes without changing the overall behavior of a cost-based search.

During simulation, each turn checks:

- the current zone capacity
- the connection capacity
- restricted-zone transit rules
- whether the drone has already been delivered

The simulation stops when every drone reaches the end hub or a safety limit is hit.

## Visualizer

The visualizer renders:

- zones with their names, colors, and capacity labels
- connections with their max link capacity
- drones as moving markers with IDs
- restricted zones with a distinct outline
- a control panel and map legend

Controls:

- `SPACE` pauses or resumes the animation
- `R` resets the animation
- `F` or `F11` toggles fullscreen
- `Q` or `ESC` quits the application
- mouse wheel zooms
- left mouse drag pans the camera

## Example Input & Output

### input
```bash
make map=maps/easy/01_linear_path.txt
```

### Output
```
D1-waypoint1
D1-waypoint2 D2-waypoint1
D1-goal D2-waypoint2
D2-goal

Total turns: 4
```

## Project Structure

- `main.py` orchestrates parsing, validation, graph creation, simulation, and visualization.
- `parser.py` reads and validates the custom map syntax.
- `validator.py` applies Pydantic validation to parsed data.
- `graph.py` builds the graph and computes the candidate paths.
- `simulator.py` executes the turn-based drone movement.
- `visualizer.py` renders the interactive animation with Arcade.

## Resources

- https://api.arcade.academy/en/stable/
- https://www.youtube.com/watch?v=EFg3u_E6eHU
- https://www.youtube.com/watch?v=rvxt42na8Ss
- https://www.geeksforgeeks.org/artificial-intelligence/uniform-cost-search-ucs-in-ai/
- https://docs.python.org/3/library/warnings.html#warnings.filterwarnings

AI was used for project explanation and some debugging support.

