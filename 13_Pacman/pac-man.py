from src.parser import Parser
from src.main_view import MainView
from typing import TYPE_CHECKING
import arcade


if TYPE_CHECKING:
    from models import ConfigModel

from warnings import filterwarnings
filterwarnings('ignore')


# DEB --------------
def _build_maze(maze_w, maze_h):
    from mazegenerator import MazeGenerator
    from src.cell import Cell
    maze_gen = MazeGenerator((maze_w, maze_h))
    maze_grid = maze_gen.maze

    maze = []

    for i in range(len(maze_grid)):
        maze.append([])
        for j in range(len(maze_grid[i])):
            cell = Cell(maze_grid[i][j])
            maze[i].append(cell)

            if (i == 0 and j == 0):
                cell.super_pacgum = True
            elif (i == 0 and j == len(maze_grid[0]) - 1):
                cell.super_pacgum = True
            elif (i == len(maze_grid) - 1 and j == 0):
                cell.super_pacgum = True
            elif (i == len(maze_grid) - 1 and j == len(maze_grid[0]) - 1):
                cell.super_pacgum = True

            if cell.walls != 15:
                cell.has_pacgum = True
    return maze
# DEB --------------


def main():
    # Parser
    parser: Parser = Parser()
    config: ConfigModel = parser.get_config()

    screen_w, screen_h = arcade.get_display_size()
    window = arcade.Window(screen_w, screen_h, fullscreen=True)

    # Main menu view
    main_menu = MainView(config)
    window.show_view(main_menu)


    # from src.game_view import PacmanView
    # maze = _build_maze(5,5)
    # settings = {
    #     "mute": False,
    #     "volume": 1,
    #     "invincibility": False,
    #     "speed": 300,
    #     "lives": 86,
    #     "ghost-freeze": False
    # }
    # window.show_view(PacmanView(maze, config, settings, 25))


    arcade.run()
    # Pacman(13, 9)


if __name__ == "__main__": main()

    # try: 
    #     main()
    # except Exception as e:
    #     print(e)
    #     exit(1)
