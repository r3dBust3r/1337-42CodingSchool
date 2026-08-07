import arcade
import json
import os
# from mazegenerator import MazeGenerator
# from src.error import PacmanError
# from src.game_view import PacmanView
# from src.cell import Cell
# import json
from src.error import PacmanError


class GameOverView(arcade.View):
    def __init__(self, score: int, config, won: bool):
        super().__init__()
        self.score = score
        self.config = config
        self.save_file = config.highscore_filename
        self.won = won
        self.player_name = ""

        self.screens = {
            "won": arcade.load_texture('assets/images/screens/game-over-s.png'),
            "failed": arcade.load_texture('assets/images/screens/game-over-f.png'),
        }

        self.sounds = {
            "won": arcade.load_sound('assets/sounds/game-over-s.mp3'),
            "failed": arcade.load_sound('assets/sounds/game-over-f.mp3'),
        }


    def on_show_view(self) -> None:
        if self.won:
            self.bg_sound = arcade.play_sound(self.sounds["won"])
            self.screen = self.screens["won"]

        else:
            self.bg_sound = arcade.play_sound(self.sounds["failed"])
            self.screen = self.screens["failed"]



    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if chr(symbol).isalpha() or symbol == arcade.key.SPACE:
            if len(self.player_name) < 10:
                self.player_name += chr(symbol).upper()

        elif symbol == arcade.key.BACKSPACE:
            self.player_name = self.player_name[:-1]

        if symbol == arcade.key.ENTER:
            if not self.player_name.strip():
                return

            self._save_score()
            from src.main_view import MainView
            main_view = MainView(self.config)
            self.window.show_view(main_view)


    def _save_score(self):
        scores = []

        if os.path.exists(self.save_file):
            with open(self.save_file, 'r') as file:
                try:
                    scores = json.load(file)
                except json.JSONDecodeError:
                    pass

        scores.append({
            "name": self.player_name.strip(),
            "score": self.score 
        })

        scores = sorted(scores, key=lambda s: s["score"], reverse=True)
        scores = scores[:10]

        with open(self.save_file, 'w') as file:
            json.dump(scores, file, indent=4)
 

    def on_draw(self) -> None:
        # Screen Texture
        self.clear()
        arcade.draw_texture_rect(
            self.screen,
            arcade.XYWH(
                self.window.width / 2,
                self.window.height / 2,
                self.window.width,
                self.window.height,
            )
        )

        arcade.draw_text(
            f"YOU SCORED: {self.score} pts!",
            self.window.width / 2,
            self.window.height / 2 + 80,
            arcade.color.WHITE,
            font_size=80,
            font_name="ByteBounce",
            anchor_x='center',
            anchor_y='center',
        )

        arcade.draw_text(
            "ENTER YOUR NAME AND CLICK ENTER",
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.WHITE,
            font_size=40,
            font_name="ByteBounce",
            anchor_x='center',
            anchor_y='center',
        )

        arcade.draw_text(
            f'> {self.player_name}',
            self.window.width / 2,
            self.window.height / 2 - 80,
            arcade.color.WHITE,
            font_size=40,
            font_name="ByteBounce",
            anchor_x='center',
            anchor_y='center',
        )
