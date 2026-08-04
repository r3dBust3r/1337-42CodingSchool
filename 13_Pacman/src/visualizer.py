import arcade
from src.cell import Cell


class TestView(arcade.View):
    def __init__(self, maze_grid) -> None:
        super().__init__()
        self.maze_grid = maze_grid
        self.rows = len(self.maze_grid)
        self.cols = len(self.maze_grid[0]) if self.rows > 0 else 1
        self.cell_size = 0


    def on_show_view(self) -> None:
        arcade.set_background_color(arcade.color.BLACK)

        max_cell_width = (self.window.width * 0.90) // self.cols
        max_cell_height = (self.window.height * 0.90) // self.rows

        self.cell_size = int(min(max_cell_width, max_cell_height))


    def on_draw(self) -> None:
        self.clear()

        maze_width = self.cols * self.cell_size
        maze_height = self.rows * self.cell_size
        
        start_offset_x = (self.window.width - maze_width) / 2
        start_offset_y = (self.window.height - maze_height) / 2

        from_bottom = start_offset_y + maze_height - self.cell_size

        for row in self.maze_grid:
            from_left = start_offset_x
            
            for cell in row:
                self.draw_cell(cell, from_left, from_bottom)
                from_left += self.cell_size

            from_bottom -= self.cell_size



    def draw_cell(self, cell, from_left, from_bottom):
        cell_center_x = from_left + (self.cell_size / 2)
        cell_center_y = from_bottom + (self.cell_size / 2)
        cell_half = self.cell_size / 2

        # drawing pacgum
        if cell.walls != 15:
            if cell.super_pacgum:
                arcade.draw_circle_filled(
                    cell_center_x, 
                    cell_center_y, 
                    12,
                    arcade.color.YELLOW
                )

            else:
                arcade.draw_circle_filled(
                    cell_center_x, 
                    cell_center_y, 
                    4,
                    arcade.color.YELLOW
                )



        # drawing 42
        if cell.walls == 15:
            arcade.draw_lbwh_rectangle_filled(
                cell_center_x - self.cell_size / 2,
                cell_center_y - self.cell_size / 2,
                self.cell_size,
                self.cell_size,
                arcade.color.BABY_BLUE
            )


        # drawing walls
        if cell.walls & 1: # TOP
            arcade.draw_line(
                cell_center_x - cell_half, cell_center_y + cell_half, 
                cell_center_x + cell_half, cell_center_y + cell_half, 
                arcade.color.BABY_BLUE, 2
            )

        if cell.walls & 2: # RIGHT
            arcade.draw_line(
                cell_center_x + cell_half, cell_center_y + cell_half, 
                cell_center_x + cell_half, cell_center_y - cell_half, 
                arcade.color.BABY_BLUE, 2
            )

        if cell.walls & 4: # BOTTOM
            arcade.draw_line(
                cell_center_x - cell_half, cell_center_y - cell_half, 
                cell_center_x + cell_half, cell_center_y - cell_half, 
                arcade.color.BABY_BLUE, 2
            )

        if cell.walls & 8: # LEFT
            arcade.draw_line(
                cell_center_x - cell_half, cell_center_y - cell_half, 
                cell_center_x - cell_half, cell_center_y + cell_half, 
                arcade.color.BABY_BLUE, 2
            )


    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            arcade.exit()
