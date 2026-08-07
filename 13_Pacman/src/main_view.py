from mazegenerator import MazeGenerator
from src.error import PacmanError
from src.game_view import PacmanView
from src.cell import Cell
import arcade
import json


class MainView(arcade.View):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.pacgums = 0

        # Screens
        self.screens = {
            "main-menu": arcade.load_texture('assets/images/screens/screen-01.png'),
            "high-scores": arcade.load_texture('assets/images/screens/screen-02.png'),
            "settings": arcade.load_texture('assets/images/screens/screen-03.png'),
            "credits": arcade.load_texture('assets/images/screens/screen-04.png'),
            "instructions": arcade.load_texture('assets/images/screens/screen-05.png'),
        }


        # Settings
        self.settings = {
            "mute": False,
            "volume": 1,
            "invincibility": False,
            "speed": 300,
            "lives": config.lives,
            "ghost-freeze": False
        }

        # Sounds
        self.sounds = {
            "bg": arcade.load_sound('assets/sounds/main-menu.mp3')
        }


    def on_show_view(self) -> None:
        self.current_screen = self.screens["main-menu"]
        self._load_highscores()

        self.bg_sound = arcade.play_sound(self.sounds["bg"])


    def _build_maze(self, maze_w, maze_h):
        maze_gen = MazeGenerator((maze_w, maze_h), seed=self.config.seed)
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
                    self.pacgums += 1

        return maze


    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol in (arcade.key.ESCAPE, arcade.key.BACKSPACE):
            if self.current_screen == self.screens["main-menu"]:
                if symbol == arcade.key.ESCAPE:
                    arcade.exit()
            else:
                self.current_screen = self.screens["main-menu"]
            return


        # Main Menu
        if self.current_screen == self.screens["main-menu"]:
            if symbol == arcade.key.ENTER:
                arcade.stop_sound(self.bg_sound)
                maze_grid = self._build_maze(3,3)
                game_view = PacmanView(maze_grid, self.config, self.settings, self.pacgums)
                self.window.show_view(game_view)


            elif symbol == arcade.key.H:
                self.current_screen = self.screens["high-scores"]


            elif symbol == arcade.key.S:
                self.current_screen = self.screens["settings"]


            elif symbol == arcade.key.C:
                self.current_screen = self.screens["credits"]


            elif symbol == arcade.key.I:
                self.current_screen = self.screens["instructions"]


        # Settings Screen
        if self.current_screen == self.screens["settings"]:
            if symbol == arcade.key.M:
                self.settings["mute"] = not self.settings["mute"]
                
            elif symbol in (arcade.key.PLUS, arcade.key.EQUAL):
                self.settings["volume"] = min(3, self.settings["volume"] + 0.1)

            elif symbol == arcade.key.MINUS:
                self.settings["volume"] = max(0, self.settings["volume"] - 0.1)

            elif symbol == arcade.key.UP:
                self.settings["speed"] = min(3000, self.settings["speed"] + 10)

            elif symbol == arcade.key.DOWN:
                self.settings["speed"] = max(10, self.settings["speed"] - 10)
                
            elif symbol == arcade.key.I:
                self.settings["invincibility"] = not self.settings["invincibility"]
                
            elif symbol == arcade.key.E:
                self.settings["lives"] += 1

            elif symbol == arcade.key.F:
                self.settings["ghost-freeze"] = not self.settings["ghost-freeze"]

            return
            


    def on_update(self, delta_time: float) -> None:
        ...


    def on_draw(self) -> None:
        # Screen Texture
        self.clear()
        arcade.draw_texture_rect(
            self.current_screen,
            arcade.XYWH(
                self.window.width / 2,
                self.window.height / 2,
                self.window.width,
                self.window.height,
            )
        )

        # High Scores Screen
        if self.current_screen == self.screens["high-scores"]:
            self._draw_highscores()


    def _draw_highscores(self) -> None:
        fsize = 45

        if not self.cached_scores:
            arcade.draw_text(
                "No High Scores Yet!",
                self.window.width / 2,
                self.window.height / 2,
                arcade.color.WHITE,
                font_size=fsize,
                font_name="ByteBounce",
                anchor_x='center',
                anchor_y='center',
            )
            return

        for i, s in enumerate(self.cached_scores, 1):
            name = s["name"]
            score = s["score"]

            arcade.draw_text(
                f'{i}: {name.upper()} ({score} pts)',
                self.window.width / 2,
                self.window.height / 1.5 - (i * fsize * 1.25),
                arcade.color.WHITE,
                font_size=fsize,
                font_name="ByteBounce",
                anchor_x='center',
                anchor_y='center',
            )


    def _load_highscores(self) -> None:
        hs_fname = self.config.highscore_filename
        
        try:
            with open(hs_fname) as hs:
                try:
                    scores = json.load(hs)
                except json.JSONDecodeError:
                    raise PacmanError(f'invalid json file: {hs_fname}')

            scores = sorted(scores, key=lambda s: s['score'], reverse=True)
            self.cached_scores = scores[:10]

        except FileNotFoundError:
            self.cached_scores = []
            print(f"no such file: {hs_fname}")

        except PermissionError:
            raise PacmanError(f'no access permission to: {hs_fname}')
