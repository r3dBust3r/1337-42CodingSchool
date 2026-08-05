import arcade
import random


class PacmanView(arcade.View):
    def __init__(self, maze_grid: list[list[any]]) -> None:
        super().__init__()
        self.maze_grid = maze_grid
        self.rows = len(self.maze_grid)
        self.cols = len(self.maze_grid[0]) if self.rows > 0 else 1
        self.cell_size = 0
        
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


    def on_show_view(self) -> None:
        arcade.set_background_color(arcade.color.BLACK)
        
        # Calculate cell size
        max_cell_width = (self.window.width * 0.90) // self.cols
        max_cell_height = (self.window.height * 0.90) // self.rows
        self.cell_size = int(min(max_cell_width, max_cell_height))


        self._spawn_pacman()
        self._spawn_ghosts()


    def _spawn_ghosts(self) -> None:
        # Setup Ghost Sprites in the corners
        assets_dir = "assets"
        corners = [
            (0, 0, f"{assets_dir}/ghost-01.png"), # Top-Left
            (0, self.cols - 1, f"{assets_dir}/ghost-02.png"), # Top-Right
            (self.rows - 1, 0, f"{assets_dir}/ghost-03.png"), # Bottom-Left
            (self.rows - 1, self.cols - 1, f"{assets_dir}/ghost-04.png") # Bottom-Right
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


    def _spawn_pacman(self) -> None:
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
        self.maze_grid[self.pac_row][self.pac_col].has_pacgum = False


    def _get_center_pixels(self, row: int, col: int) -> tuple[float, float]:
        maze_width = self.cols * self.cell_size
        maze_height = self.rows * self.cell_size
        
        left_margin = (self.window.width - maze_width) / 2
        bottom_margin = (self.window.height - maze_height) / 2
        
        half_cell = self.cell_size / 2
        
        center_x = left_margin + (col * self.cell_size) + half_cell
        
        maze_top_edge = bottom_margin + maze_height
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
            arcade.exit()
            
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
                    current_cell.has_pacgum = False  
                    
                    if current_cell.super_pacgum:
                        self.score += 50

                    else:
                        self.score += 10
                
                self._update_pacman_target()
                
            else:
                if self.current_dir == "UP": self.py += move_dist
                elif self.current_dir == "DOWN": self.py -= move_dist
                elif self.current_dir == "LEFT": self.px -= move_dist
                elif self.current_dir == "RIGHT": self.px += move_dist


        # Ghost movements
        ghost_speed = self.ghost_speed * delta_time
        for ghost in self.ghost_list:
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


    def on_draw(self) -> None:
        self.clear()

        maze_width = self.cols * self.cell_size
        maze_height = self.rows * self.cell_size

        left_margin = (self.window.width - maze_width) / 2
        bottom_margin = (self.window.height - maze_height) / 2

        from_bottom = bottom_margin + maze_height - self.cell_size

        for row in self.maze_grid:
            from_left = left_margin

            for cell in row:
                self._draw_cell(cell, from_left, from_bottom)
                from_left += self.cell_size

            from_bottom -= self.cell_size

        self.ghost_list.draw()
        self._draw_pacman()


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

        # Only draw if the cell actually has a pacgum
        if cell.walls != 15 and cell.has_pacgum:
            if cell.super_pacgum:
                arcade.draw_circle_filled(
                    cell_center_x, 
                    cell_center_y, 
                    12, 
                    arcade.color.YELLOW
                )
            else:
                arcade.draw_circle_outline(
                    cell_center_x, 
                    cell_center_y, 
                    4, 
                    arcade.color.YELLOW
                )

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
