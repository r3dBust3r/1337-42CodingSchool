from pydantic import ValidationError  # type: ignore
from parser import Parser
from validator import Validator
from graph import Graph
from simulator import Simulator
from visualizer import Visualizer
import arcade # type: ignore
from sys import argv

from warnings import filterwarnings
filterwarnings('ignore')


def main():
    try:
        parser = Parser(argv[1])
        parser.parse()
        _map = parser.get_map()
    except ValueError as e:
        print(e)
        exit(1)

    try:
        validator = Validator(_map)
        validator.validate()
    except ValidationError as e:
        print(f"Pydantic error: {e.errors()[0]['msg']}")
        exit(1)


    graph = Graph(
        parser.zones,
        parser.connections,
        parser.nb_drones
    )

    try: graph.create_graph()
    except ValueError as e:
        print(e)
        exit(1)


    paths = graph.find_multiple_paths()
    simulator = Simulator(graph, paths)
    simulator.run()
    simulator.display_turns()


    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 960
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "Fly-in Simulation", fullscreen=True)
    visualizer = Visualizer(graph, simulator.turns)
    window.show_view(visualizer)
    arcade.run()


if __name__ == "__main__":
    main()
