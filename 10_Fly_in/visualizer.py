import arcade # type: ignore


class Visualizer(arcade.View):
    def __init__(self, graph, turns):
        self.graph = graph
        self.turns = turns
        self.scale = 400
        self.zone_size = 50
        self.progress = 0
        self.current_turn = 0
        self.current_pixel_position = {}
        self.target_pixel_position = {}
        self.delay = 1
        self.started = False
        self.pause = False
        self.WIN_W = 1920
        self.WIN_H = 960
        self.is_dragging = False
        self.camera = arcade.Camera2D()
        self.fixed_camera = arcade.Camera2D()
        self.colors = {
            "default": arcade.color.DIM_GRAY,
            "black": arcade.color.BLACK,
            "white": arcade.color.GLITTER,
            "red": arcade.color.AMARANTH,
            "green": arcade.color.BUD_GREEN,
            "blue": arcade.color.BLUEBERRY,
            "yellow": arcade.color.BANANA_YELLOW,
            "orange": arcade.color.CADMIUM_ORANGE,
            "purple": arcade.color.DARK_PASTEL_PURPLE,
            "pink": arcade.color.DARK_PINK,
            "brown": arcade.color.WOOD_BROWN,
            "gray": arcade.color.GRAY,
            "cyan": arcade.color.ELECTRIC_CYAN,
            "magenta": arcade.color.PALE_MAGENTA,
            "lime": arcade.color.FRENCH_LIME,
            "silver": arcade.color.SILVER,
            "gold": arcade.color.GOLDENROD,
            "beige": arcade.color.BEIGE,
            "violet": arcade.color.AFRICAN_VIOLET,
            "mint": arcade.color.MAGIC_MINT,
            "peach": arcade.color.PEACH_ORANGE
        }

        self._init_drones_pos()
        self._load_turn_targets()

        super().__init__()
        self.background_color = arcade.color.BEAU_BLUE


    def _init_drones_pos(self):
        for d in self.graph.drones:
            self.current_pixel_position[d] = self._calc_zone_pos(self.graph.start_zone)
            self.target_pixel_position[d] = self._calc_zone_pos(self.graph.start_zone)


    def on_draw(self):
        self.clear()

        self.camera.use()

        # Drawing Connections
        for conn in self.graph.connections:
            z1, z2 = conn.name.split('-')

            z1 = self._get_zone(z1)
            z2 = self._get_zone(z2)

            conn_color = z2.color
            if conn_color not in self.colors:
                conn_color = 'default'

            z1_x, z1_y = self._calc_zone_pos(z1)
            z2_x, z2_y = self._calc_zone_pos(z2)

            arcade.draw_line(
                z1_x + 10,
                z1_y + self.WIN_H,
                z2_x + 10,
                z2_y + self.WIN_H,
                self.colors[conn_color],
                3
            )

        # Drawing Zones
        for z in self.graph.zones:
            x, y = self._calc_zone_pos(z)
            color = z.color
            if color not in self.colors:
                color = "default"

            arcade.draw_circle_filled(
                x + 10,
                y + self.WIN_H,
                self.zone_size,
                self.colors[color]
            )

            arcade.draw_text(
                z.name.upper(),
                x + 10 - len(z.name) * 5,
                y + self.WIN_H - self.zone_size * 1.5,
                arcade.color.BLACK,
                12
            )

            if z.zone == 'restricted':
                arcade.draw_text(
                    f'( {z.zone.upper()} )',
                    x + 10 - len(z.zone) * 4.5,
                    y + self.WIN_H - self.zone_size * 1.9,
                    self.colors['red'],
                    10
                )


        # Drawing drones
        for d in self.graph.drones:
            x, y = self.current_pixel_position[d]
            txt_x = x
            if len(d.id) == 3:
                txt_x -= 5

            arcade.draw_circle_filled(
                x + 10,
                y + self.WIN_H,
                20,
                arcade.color.BLACK
            )

            arcade.draw_text(
                d.id,
                txt_x,
                y + 954,
                arcade.color.WHITE,
                12
            )

        # Drawing text
        self.fixed_camera.use()
        self._draw_text()


    def _draw_text(self):
        arcade.draw_lbwh_rectangle_filled(10, 10, 420, 110, arcade.color.ASH_GREY)
        arcade.draw_lbwh_rectangle_filled(10, 120, 420, 40, arcade.color.BLACK)
        arcade.draw_text("CONTROLS", 30, 130, arcade.color.ASH_GREY, 16)
        arcade.draw_text("SPACE", 30, 90, arcade.color.BLACK, 12)
        arcade.draw_text("R", 30, 70, arcade.color.BLACK, 12)
        arcade.draw_text("F / F11", 30, 50, arcade.color.BLACK, 12)
        arcade.draw_text("Q / ESC", 30, 30, arcade.color.BLACK, 12)

        arcade.draw_text("." * 30, 100, 90, arcade.color.BLACK, 12)
        arcade.draw_text("." * 30, 100, 70, arcade.color.BLACK, 12)
        arcade.draw_text("." * 30, 100, 50, arcade.color.BLACK, 12)
        arcade.draw_text("." * 30, 100, 30, arcade.color.BLACK, 12)

        arcade.draw_text("Pause Animation", 264, 90, arcade.color.BLACK, 12)
        arcade.draw_text("Reset Animation", 264, 70, arcade.color.BLACK, 12)
        arcade.draw_text("Full Screen", 264, 50, arcade.color.BLACK, 12)
        arcade.draw_text("Quit", 264, 30, arcade.color.BLACK, 12)

        full_screen = {
            False: (10, 936),
            True: (10, 1060)
        }
        dx, dy = full_screen[self.window.fullscreen]

        arcade.draw_text(f"Turns: {self.current_turn + 1}/{len(self.turns)}", dx, dy, arcade.color.BLACK, 16)
        if self.current_turn == len(self.turns) - 1:
            arcade.draw_text(f"(SIMULATION FINISHED!)", dx + 120, dy, arcade.color.BLACK, 12)

        if self.pause:
            arcade.draw_lbwh_rectangle_filled(10, 160, 420, 40, arcade.color.AMBER)
            arcade.draw_text("PAUSED: Press SPACE to Continue", 30, 172, arcade.color.BLACK, 14)


    def on_key_press(self, key, modifiers):
        if key in [arcade.key.Q, arcade.key.ESCAPE]:
            arcade.exit()

        if key == arcade.key.SPACE:
            self.pause = not self.pause

        if key == arcade.key.R:
            self._init_drones_pos()
            self.current_turn = -1

        if key == arcade.key.F or key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)


    
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.camera.zoom += scroll_y * 0.1
        self.camera.zoom = max(0.2, min(self.camera.zoom, 4.0))


    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.is_dragging = True


    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.is_dragging = False

    def on_mouse_motion(self, x, y, dx, dy):
        if self.is_dragging:
            self.camera.position = (
                self.camera.position[0] - (dx / self.camera.zoom),
                self.camera.position[1] - (dy / self.camera.zoom)
            )


    def on_update(self, delta_time):
        if self.pause:
            return

        if not self.started:
            self.delay -= delta_time
            if self.delay <= 0:
                self.started = True
            return

        self.progress += delta_time

        if self.progress >= 1.0:
            for d in self.graph.drones:
                self.current_pixel_position[d] = self.target_pixel_position[d]

            self.progress = 0

            if self.current_turn < len(self.turns) - 1:
                self.current_turn += 1
                self._load_turn_targets()

        for d in self.graph.drones:
            sx, sy = self.current_pixel_position[d]
            ex, ey = self.target_pixel_position[d]
            lx = sx + (ex - sx) * self.progress
            ly = sy + (ey - sy) * self.progress
            self.current_pixel_position[d] = (lx, ly)


    def _load_turn_targets(self):
        current_turn = self.turns[self.current_turn].split(' ')
        for move in current_turn:
            if move.count('-') == 1:
                drone, target = move.split('-')
                drone = self._get_drone(drone)
                target = self._get_zone(target)
                self.target_pixel_position[drone] = self._calc_zone_pos(target)
            else:
                drone, z1, z2 = move.split('-')
                drone = self._get_drone(drone)
                conn_name = self._get_connection(z1, z2)
                self.target_pixel_position[drone] = self._calc_conn_pos(conn_name)


    def _get_zone(self, name):
        for zone in self.graph.zones:
            if zone.name == name:
                return zone
        return None


    def _get_connection(self, z1, z2):
        for conn in self.graph.connections:
            if conn.name in [f'{z1}-{z2}', f'{z2}-{z1}']:
                return conn
        return None


    def _get_drone(self, drone_id):
        for drone in self.graph.drones:
            if drone.id == drone_id:
                return drone
        return None


    def _calc_zone_pos(self, zone):
        x = zone.x * self.scale + self.zone_size * 2
        y = zone.y * self.scale - self.zone_size * 2
        return x, y


    def _calc_conn_pos(self, conn):
        z1, z2 = conn.name.split('-')
        z1 = self._get_zone(z1)
        z2 = self._get_zone(z2)
        x1, y1 = self._calc_zone_pos(z1)
        x2, y2 = self._calc_zone_pos(z2)
        return (x1 + x2) / 2, (y1 + y2) / 2
