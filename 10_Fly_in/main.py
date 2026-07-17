from pydantic import ValidationError
from parser import Parser
from validator import Validator
from graph import Graph
from simulator import Simulator
from visualizer import Visualizer
import arcade
from sys import argv

from warnings import filterwarnings
filterwarnings('ignore')


def main() -> None:
    if len(argv) == 1:
        raise ValueError("Usage: python main.py <path/to/map>")

    parser = Parser(argv[1])
    parser.parse()
    parsed_map = parser.get_map()

    validator = Validator(parsed_map)
    validator.validate()

    graph = Graph(
        parser.zones,
        parser.connections,
        parser.nb_drones
    )
    graph.create_graph()

    paths = graph.find_multiple_paths()
    simulator = Simulator(graph, paths)
    simulator.run()
    simulator.display_turns()

    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 960
    window = arcade.Window(
        WINDOW_WIDTH,
        WINDOW_HEIGHT,
        "Fly-in Simulation",
        fullscreen=True
    )
    visualizer = Visualizer(graph, simulator.turns)
    window.show_view(visualizer)
    arcade.run()


if __name__ == "__main__":
    try:
        main()

    except ValueError as e:
        print(e)
        exit(1)

    except ValidationError as e:
        print(f"Pydantic error: {e.errors()[0]['msg']}")
        exit(1)

    except Exception as e:
        print(e)
        exit(1)
