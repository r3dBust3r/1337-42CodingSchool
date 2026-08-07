from src.gameover_view import GameOverView
import arcade
import random


class PacmanView(arcade.View):
    def __init__(self, maze_grid, config, settings, pacgums) -> None:
        super().__init__()
        self.maze_grid = maze_grid
        self.config = config
        self.settings = settings
        self.pacgums = pacgums

        self.rows = len(self.maze_grid)
        self.cols = len(self.maze_grid[0]) if self.rows > 0 else 1
        self.cell_size = 0

        # For Alignments
        self.maze_width = 0
        self.maze_height = 0
        self.left_margin = 0
        self.bottom_margin = 0
        self.playable_width = 0
        self.hud_width = 300

        # Stats, Controls & HUD
        self.lives = self.config.lives
        self.pause = False
        arcade.load_font("assets/fonts/ByteBounce.ttf")

        # Pacman Animation State
        self.pacman_mouth = 0.0
        self.pacman_opening = True
        
        # Pacman Movement State
        self.pacman_speed = 350.0
        self.ghost_speed = 300.0
        self.current_dir = "STOP"
        self.next_dir = "STOP"
        self.facing_angle = 0

        self.angles = {
            "RIGHT": 0,
            "UP": 90,
            "LEFT": 180,
            "DOWN": 270,
            "STOP": 0
        }

        # Grid positions
        self.pac_row = 0
        self.pac_col = 0
        self.px = 0.0
        self.py = 0.0
        self.target_px = 0.0
        self.target_py = 0.0

        # Score State
        self.score: int = 0 
        
        # Sprite Lists
        self.ghost_list = arcade.SpriteList()
        self.pacgum_list = arcade.SpriteList()

        # Sound Effects
        self.sounds = {
            "bg": arcade.load_sound("assets/sounds/bg.mp3"),
            "eat": arcade.load_sound("assets/sounds/eat.mp3"),
            "die": arcade.load_sound("assets/sounds/die.mp3"),
            "game-over": arcade.load_sound("assets/sounds/game-over.mp3"),
        }

        # Gameover
        self.gameover_sound = True


    def on_show_view(self) -> None:
        arcade.set_background_color(arcade.color.BLACK)

        # Calculate cell size
        self.playable_width = self.window.width - self.hud_width
        max_cell_width = (self.playable_width * 0.90) // self.cols
        max_cell_height = (self.window.height * 0.90) // self.rows
        self.cell_size = int(min(max_cell_width, max_cell_height))

        # For Alignments
        self.maze_width = self.cols * self.cell_size
        self.maze_height = self.rows * self.cell_size
        self.bottom_margin = (self.window.height - self.maze_height) / 2
        self.left_margin = self.hud_width + (self.playable_width - self.maze_width) / 2

        # Sound Effects
        self.gameplay_music = arcade.play_sound(self.sounds['bg'], volume=0.25, loop=True)

        # Spawn pacman, ghosts, pacgums
        self._spawn_pacman()
        self._spawn_ghosts()
        self._setup_pacgums()


    def _setup_pacgums(self):
        # Setup Pacgum
        fruit_i = 0
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.maze_grid[r][c]

                if cell.has_pacgum:
                    if cell.super_pacgum:
                        if r == 0 and c == 0:
                            super_fruit = f"assets/images/super-pacgum-01.png"

                        if r == 0 and c == self.cols - 1:
                            super_fruit = f"assets/images/super-pacgum-02.png"

                        if r == self.rows - 1 and c == 0:
                            super_fruit = f"assets/images/super-pacgum-03.png"

                        if r == self.rows - 1 and c == self.cols - 1:
                            super_fruit = f"assets/images/super-pacgum-04.png"

                        fruit = arcade.Sprite(super_fruit)
                        fruit.width = self.cell_size

                    else:
                        fruit = arcade.Sprite(f"assets/images/pacgum-0{(fruit_i % 8) + 1}.png")
                        fruit.width = self.cell_size * 0.5

                    fruit.height = fruit.width 

                    center_x, center_y = self._get_center_pixels(r, c)
                    fruit.center_x = center_x
                    fruit.center_y = center_y

                    cell.fruit = fruit
                    self.pacgum_list.append(fruit)

                fruit_i += 1


    def _spawn_ghosts(self) -> None:
        # Setup Ghost Sprites in the corners
        corners = [
            (0, 0, "assets/images/ghost-01.png"), # Top-Left
            (0, self.cols - 1, "assets/images/ghost-02.png"), # Top-Right
            (self.rows - 1, 0, "assets/images/ghost-03.png"), # Bottom-Left
            (self.rows - 1, self.cols - 1, "assets/images/ghost-04.png") # Bottom-Right
        ]

        for row, col, ghost_filename in corners:
            ghost = arcade.Sprite(ghost_filename)
            ghost.width = self.cell_size * 0.8
            ghost.height = self.cell_size * 0.8
            cx, cy = self._get_center_pixels(row, col)
            ghost.center_x = cx
            ghost.center_y = cy
            
            # Give each ghost its own tracking variables
            ghost.g_row = row
            ghost.g_col = col
            ghost.current_dir = "STOP"
            ghost.target_x = cx
            ghost.target_y = cy

            self.ghost_list.append(ghost)


    def _respawn_ghosts(self) -> None:
        corners = [
            (0, 0), # Top-Left
            (0, self.cols - 1), # Top-Right
            (self.rows - 1, 0), # Bottom-Left
            (self.rows - 1, self.cols - 1) # Bottom-Right
        ]

        for ghost, (row, col) in zip(self.ghost_list, corners):
            ghost.g_row = row
            ghost.g_col = col
            ghost.current_dir = "STOP"
            
            center_x, center_y = self._get_center_pixels(row, col)
            ghost.center_x = center_x
            ghost.center_y = center_y
            ghost.target_x = center_x
            ghost.target_y = center_y


    def _eaten_by_ghost(self, ghost):
        return False
        dist = arcade.math.get_distance(self.px, self.py, ghost.center_x, ghost.center_y)
        return dist < (self.cell_size / 2)


    def _spawn_pacman(self) -> None:
        self.current_dir = "STOP"

        center_row = self.rows // 2
        center_col = self.cols // 2
        
        # Gather every valid, open cell in the maze
        available_cells = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.maze_grid[r][c].walls != 15:
                    available_cells.append((r, c))
                    
        # Find the open cell that is mathematically closest to the true center
        closest_cell = min(
            available_cells, 
            key=lambda pos: abs(pos[0] - center_row) + abs(pos[1] - center_col)
        )

        self.pac_row = closest_cell[0]
        self.pac_col = closest_cell[1]
                
        # Lock his starting pixel coordinates to the chosen cell
        self.px, self.py = self._get_center_pixels(self.pac_row, self.pac_col)
        self.target_px, self.target_py = self.px, self.py

        # Eat the pacgum he spawns on top of
        spawn_cell = self.maze_grid[self.pac_row][self.pac_col]
        if spawn_cell.has_pacgum:
            self.pacgums -= 1
            spawn_cell.has_pacgum = False


    def _get_center_pixels(self, row: int, col: int) -> tuple[float, float]:
        half_cell = self.cell_size / 2

        center_x = self.left_margin + (col * self.cell_size) + half_cell

        maze_top_edge = self.bottom_margin + self.maze_height
        center_y = maze_top_edge - (row * self.cell_size) - half_cell
        
        return center_x, center_y


    def _get_valid_ghost_moves(self, ghost) -> list[str]:
        moves = []
        if self._can_move(ghost.g_row, ghost.g_col, "UP"): moves.append("UP")
        if self._can_move(ghost.g_row, ghost.g_col, "DOWN"): moves.append("DOWN")
        if self._can_move(ghost.g_row, ghost.g_col, "LEFT"): moves.append("LEFT")
        if self._can_move(ghost.g_row, ghost.g_col, "RIGHT"): moves.append("RIGHT")
        
        # Prevent rotating
        opposites = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT",
            "STOP": "STOP"
        }
        reverse_dir = opposites[ghost.current_dir]
        
        if len(moves) > 1 and reverse_dir in moves:
            moves.remove(reverse_dir)

        return moves


    def _can_move(self, row: int, col: int, direction: str) -> bool:
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False
    
        cell = self.maze_grid[row][col]

        if direction == "UP" and not (cell.walls & 1): return True
        if direction == "RIGHT" and not (cell.walls & 2): return True
        if direction == "DOWN" and not (cell.walls & 4): return True
        if direction == "LEFT" and not (cell.walls & 8): return True

        return False


    def _update_ghost_target(self, ghost) -> None:
        if ghost.current_dir == "UP":
            ghost.target_x, ghost.target_y = self._get_center_pixels(ghost.g_row - 1, ghost.g_col)

        elif ghost.current_dir == "DOWN":
            ghost.target_x, ghost.target_y = self._get_center_pixels(ghost.g_row + 1, ghost.g_col)

        elif ghost.current_dir == "LEFT":
            ghost.target_x, ghost.target_y = self._get_center_pixels(ghost.g_row, ghost.g_col - 1)

        elif ghost.current_dir == "RIGHT":
            ghost.target_x, ghost.target_y = self._get_center_pixels(ghost.g_row, ghost.g_col + 1)


    def _update_pacman_target(self) -> None:
        if self.next_dir != "STOP" and self._can_move(self.pac_row, self.pac_col, self.next_dir):
            self.current_dir = self.next_dir
            self.facing_angle = self.angles[self.current_dir]

        elif not self._can_move(self.pac_row, self.pac_col, self.current_dir):
            self.current_dir = "STOP"
            
        if self.current_dir == "UP":
            self.target_px, self.target_py = self._get_center_pixels(self.pac_row - 1, self.pac_col)

        elif self.current_dir == "DOWN":
            self.target_px, self.target_py = self._get_center_pixels(self.pac_row + 1, self.pac_col)

        elif self.current_dir == "LEFT":
            self.target_px, self.target_py = self._get_center_pixels(self.pac_row, self.pac_col - 1)

        elif self.current_dir == "RIGHT":
            self.target_px, self.target_py = self._get_center_pixels(self.pac_row, self.pac_col + 1)


    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            arcade.stop_sound(self.gameplay_music)

            from src.main_view import MainView
            main_view = MainView(self.config)
            self.window.show_view(main_view)

        if symbol == arcade.key.SPACE:
            self.pause = not self.pause


        if symbol == arcade.key.UP or symbol == arcade.key.W:
            self.next_dir = "UP"

        elif symbol == arcade.key.DOWN or symbol == arcade.key.S:
            self.next_dir = "DOWN"

        elif symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.next_dir = "LEFT"

        elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.next_dir = "RIGHT"


        if self.current_dir == "STOP":
            self._update_pacman_target()


    def on_update(self, delta_time: float) -> None:
        if not self.lives:
            arcade.stop_sound(self.gameplay_music)
            gameover = GameOverView(self.score, self.config, False)
            self.window.show_view(gameover)

        if self.pause:
            return

        # Pacman Mouth Animation
        animation_speed = 4.0 

        if self.pacman_opening:
            self.pacman_mouth += delta_time * animation_speed
            if self.pacman_mouth >= 1.0:
                self.pacman_mouth = 1.0
                self.pacman_opening = False
        else:
            self.pacman_mouth -= delta_time * animation_speed
            if self.pacman_mouth <= 0.0:
                self.pacman_mouth = 0.0
                self.pacman_opening = True

        # Pacman Movement
        if self.current_dir != "STOP":

            dist = arcade.math.get_distance(self.px, self.py, self.target_px, self.target_py)
            move_dist = self.pacman_speed * delta_time
            
            if dist <= move_dist:
                self.px = self.target_px
                self.py = self.target_py

                if self.current_dir == "UP": self.pac_row -= 1
                elif self.current_dir == "DOWN": self.pac_row += 1
                elif self.current_dir == "LEFT": self.pac_col -= 1
                elif self.current_dir == "RIGHT": self.pac_col += 1
                
                # Collision Check
                current_cell = self.maze_grid[self.pac_row][self.pac_col]
                
                if current_cell.has_pacgum:
                    self.pacgums -= 1
                    current_cell.has_pacgum = False

                    arcade.play_sound(self.sounds['eat'])

                    if current_cell.fruit:
                        current_cell.fruit.remove_from_sprite_lists()
                    
                    if current_cell.super_pacgum:
                        self.score += self.config.points_per_super_pacgum

                    else:
                        self.score += self.config.points_per_pacgum

                    if self.pacgums <= 0:
                        arcade.stop_sound(self.gameplay_music)
                        gameover = GameOverView(self.score, self.config, True)
                        self.window.show_view(gameover)


                self._update_pacman_target()
                
            else:
                if self.current_dir == "UP": self.py += move_dist
                elif self.current_dir == "DOWN": self.py -= move_dist
                elif self.current_dir == "LEFT": self.px -= move_dist
                elif self.current_dir == "RIGHT": self.px += move_dist


        # Ghost movements
        ghost_speed = self.ghost_speed * delta_time
        for ghost in self.ghost_list:

            if self._eaten_by_ghost(ghost):
                arcade.play_sound(self.sounds["die"])
                self._spawn_pacman()
                self._respawn_ghosts()
                self.lives -= 1


            if ghost.current_dir == "STOP":
                moves = self._get_valid_ghost_moves(ghost)
                if moves:
                    ghost.current_dir = random.choice(moves)
                    self._update_ghost_target(ghost)
            else:
                dist = arcade.math.get_distance(ghost.center_x, ghost.center_y, ghost.target_x, ghost.target_y)
                
                if dist <= ghost_speed:
                    ghost.center_x = ghost.target_x
                    ghost.center_y = ghost.target_y
                    
                    if ghost.current_dir == "UP": ghost.g_row -= 1
                    elif ghost.current_dir == "DOWN": ghost.g_row += 1
                    elif ghost.current_dir == "LEFT": ghost.g_col -= 1
                    elif ghost.current_dir == "RIGHT": ghost.g_col += 1
                    
                    moves = self._get_valid_ghost_moves(ghost)
                    if moves:
                        ghost.current_dir = random.choice(moves)
                        self._update_ghost_target(ghost)
                else:
                    if ghost.current_dir == "UP": ghost.center_y += ghost_speed
                    elif ghost.current_dir == "DOWN": ghost.center_y -= ghost_speed
                    elif ghost.current_dir == "LEFT": ghost.center_x -= ghost_speed
                    elif ghost.current_dir == "RIGHT": ghost.center_x += ghost_speed


    def _gameover(self):
        # arcade.play_sound(self.sounds["game-over"])
        # arcade.stop_sound(self.sounds["bg"])
        if self.gameover_sound:
            arcade.stop_sound(self.gameplay_music)
            arcade.play_sound(self.sounds["game-over"])

        self.gameover_sound = False

        arcade.draw_lbwh_rectangle_filled(
            0, 0,
            self.window.width,
            self.window.height,
            (0, 0, 0, 200)
        )

        arcade.draw_text(
            "GAME OVER",
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.WHITE,
            120,
            font_name="ByteBounce",
            anchor_x='center',
        )

        arcade.draw_text(
            f"YOUR SCORE: {self.score}",
            self.window.width / 2,
            self.window.height / 2 - 80,
            arcade.color.WHITE,
            60,
            font_name="ByteBounce",
            anchor_x='center',
        )


    def _button(self, content: str, left: float, bottom: float, panel_color: tuple, width_mult: int = 1) -> None:
        base_width = 60 * width_mult
        base_height = 60

        arcade.draw_lbwh_rectangle_filled(
            left, bottom, base_width, base_height, arcade.color.BLACK
        )

        x_margin = 10
        bottom_margin = 20
        top_margin = 3
        
        panel_width = base_width - (x_margin * 2)
        panel_height = base_height - bottom_margin - top_margin

        arcade.draw_lbwh_rectangle_filled(
            left + x_margin,
            bottom + bottom_margin,
            panel_width,
            panel_height,
            panel_color
        )

        arcade.draw_text(
            content,
            left + x_margin + (panel_width / 2),
            bottom + bottom_margin + (panel_height / 2),
            arcade.color.BLACK,
            font_size=28,
            font_name="ByteBounce",
            anchor_x="center",
            anchor_y="center"
        )


    def _text(self, content: str, left: float, bottom: float, color: tuple, fsize: int) -> None:
        arcade.draw_text(
            content, left, bottom, color,
            font_size=fsize,
            font_name="ByteBounce",
            anchor_y="center"
        )


    def _hud_panel(self) -> None:
        panel_color = arcade.color.DARK_CYAN
        
        arcade.draw_lbwh_rectangle_filled(
            0, 0,
            self.hud_width,
            self.window.height,
            panel_color
        )

        # self._text("Controls", 30, self.window.height - 30, arcade.color.BLACK, 60)

        # def _draw_move_pad(start_x: float, top_y: float, keys: list[str]) -> None:
            
        #     size = 60
        #     margin = 5
        #     offset = size + margin
            
        #     self._button(keys[0], start_x + offset, top_y, panel_color)
        #     self._button(keys[1], start_x, top_y - offset, panel_color)
        #     self._button(keys[2], start_x + offset, top_y - offset, panel_color)
        #     self._button(keys[3], start_x + (offset * 2), top_y - offset, panel_color)

        # _draw_move_pad(30, self.window.height - 150, ["W", "A", "S", "D"])
        # _draw_move_pad(30, self.window.height - 300, ["↑", "←", "↓", "→"])

        # actions = [
        #     ("R", "RESTART", 1),
        #     ("M", "MUTE", 1),
        #     ("ESC", "QUIT", 2),
        #     ("SPACE", "PAUSE", 4)
        # ]

        # start_y = self.window.height - 450
        # y_spacing = 70

        # for index, (key_str, label, width_mult) in enumerate(actions):
        #     current_y = start_y - (index * y_spacing)

        #     self._text(label, 30, current_y + 12, arcade.color.BLACK, 35)
        #     self._button(key_str, 180, current_y, panel_color, width_mult)


    def _pause_overlay(self):
        arcade.draw_lbwh_rectangle_filled(
            0, 0,
            self.window.width,
            self.window.height,
            (0, 0, 0, 200)
        )

        arcade.draw_text(
            "PAUSE",
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.WHITE,
            120,
            font_name="ByteBounce",
            anchor_x='center',
        )


    def on_draw(self) -> None:
        self.clear()

        # hud panel
        self._hud_panel()

        from_bottom = self.bottom_margin + self.maze_height - self.cell_size

        for row in self.maze_grid:
            from_left = self.left_margin

            for cell in row:
                self._draw_cell(cell, from_left, from_bottom)
                from_left += self.cell_size

            from_bottom -= self.cell_size

        self.pacgum_list.draw()
        self._draw_pacman()
        self.ghost_list.draw()


        if self.pause:
            self._pause_overlay()


    def _draw_pacman(self) -> None:
        arcade.draw_arc_filled(
            self.px,
            self.py,
            self.cell_size * 0.7, 
            self.cell_size * 0.7,
            arcade.color.YELLOW,
            self.facing_angle + (self.pacman_mouth * 60),
            self.facing_angle + 360 - (self.pacman_mouth * 60)
        )


    def _draw_cell(self, cell, from_left, from_bottom):
        cell_center_x = from_left + (self.cell_size / 2)
        cell_center_y = from_bottom + (self.cell_size / 2)
        cell_half = self.cell_size / 2

        if cell.walls == 15:
            arcade.draw_lbwh_rectangle_filled(
                cell_center_x - self.cell_size / 2,
                cell_center_y - self.cell_size / 2,
                self.cell_size,
                self.cell_size,
                arcade.color.CYAN
            )

        if cell.walls & 1: # TOP
            arcade.draw_line(
                cell_center_x - cell_half, cell_center_y + cell_half, 
                cell_center_x + cell_half, cell_center_y + cell_half, 
                arcade.color.CYAN, 2
            )

        if cell.walls & 2: # RIGHT
            arcade.draw_line(
                cell_center_x + cell_half, cell_center_y + cell_half, 
                cell_center_x + cell_half, cell_center_y - cell_half, 
                arcade.color.CYAN, 2
            )

        if cell.walls & 4: # BOTTOM
            arcade.draw_line(
                cell_center_x - cell_half, cell_center_y - cell_half, 
                cell_center_x + cell_half, cell_center_y - cell_half, 
                arcade.color.CYAN, 2
            )

        if cell.walls & 8: # LEFT
            arcade.draw_line(
                cell_center_x - cell_half, cell_center_y - cell_half, 
                cell_center_x - cell_half, cell_center_y + cell_half, 
                arcade.color.CYAN, 2
            )
