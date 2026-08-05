from mazegenerator import MazeGenerator
from src.cell import Cell
from arcade import run, Window, get_display_size
from src.visualizer import PacmanView


class Pacman:
    def __init__(self, maze_w, maze_h):
        maze_gen = MazeGenerator((maze_w, maze_h), seed=1337)
        maze_grid = maze_gen.maze

        # Cell objs
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

        screen_w, screen_h = get_display_size()
        window = Window(screen_w, screen_h, fullscreen=True)

        pacman_view = PacmanView(maze)
        window.show_view(pacman_view)
        run()
