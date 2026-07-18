from graph import Graph
from drone import Drone
from zone import Zone
from connection import Connection
from typing import List, Dict, Tuple, Any
import arcade


class Visualizer(arcade.View):
    def __init__(self, graph: Graph, turns: List[str]) -> None:
        self.graph: Graph = graph
        self.turns: List[str] = turns
        self.scale: int = 400
        self.zone_size: int = 50
        self.progress: float = 0.0
        self.current_turn: int = 0
        self.current_pixel_position: Dict[Drone, Tuple] = {}
        self.target_pixel_position: Dict[Drone, Tuple] = {}
        self.delay: float = 1.0
        self.started: bool = False
        self.pause: bool = False
        self.WIN_W: int = 1920
        self.WIN_H: int = 960
        self.is_dragging: bool = False
        self.camera: arcade.Camera2D = arcade.Camera2D()
        self.fixed_camera: arcade.Camera2D = arcade.Camera2D()
        self.colors: Dict[str, Any] = {
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
            "peach": arcade.color.PEACH_ORANGE,
            "bg": arcade.color.BEAU_BLUE
        }

        self._init_drones_pos()
        self._load_turn_targets()

        super().__init__()
        self.background_color = arcade.color.BEAU_BLUE

    def _init_drones_pos(self) -> None:
        assert self.graph.start_zone is not None

        for d in self.graph.drones:
            self.current_pixel_position[d] = \
                self._calc_zone_pos(self.graph.start_zone)
            self.target_pixel_position[d] = \
                self._calc_zone_pos(self.graph.start_zone)

    def on_draw(self) -> None:
        self.clear()

        self.camera.use()

        # Drawing Connections
        for conn in self.graph.connections:
            z1_name, z2_name = conn.name.split('-')

            z1: 'Zone' = self._get_zone(z1_name)
            z2: 'Zone' = self._get_zone(z2_name)

            assert z1 is not None
            assert z2 is not None

            conn_color: str = z2.color
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

            mlc_x, mlc_y = self._calc_conn_pos(conn)

            arcade.draw_lbwh_rectangle_filled(
                mlc_x - 4,
                mlc_y + self.WIN_H - 13,
                26,
                26,
                self.colors[conn_color]
            )

            arcade.draw_text(
                conn.max_link_capacity,
                mlc_x + 5,
                mlc_y + self.WIN_H - 5,
                arcade.color.WHITE,
                12
            )

        # Drawing Zones
        for z in self.graph.zones:
            x, y = self._calc_zone_pos(z)
            color: str = z.color
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

            arcade.draw_text(
                f'MAX={z.max_drones}',
                x + 10 - (len(str(z.max_drones)) + 4) * 5,
                y + self.WIN_H - self.zone_size * 1.9,
                arcade.color.BLACK,
                12
            )

            if z.zone == 'restricted':
                arcade.draw_circle_outline(
                    x + 10,
                    y + self.WIN_H,
                    self.zone_size,
                    self.colors['bg'],
                    12
                )

                arcade.draw_circle_outline(
                    x + 10,
                    y + self.WIN_H,
                    self.zone_size,
                    self.colors['red'],
                    6
                )

        # Drawing drones
        for d in self.graph.drones:
            x, y = self.current_pixel_position[d]
            txt_x: int = x
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

    def _draw_text(self) -> None:
        arcade.draw_lbwh_rectangle_filled(
            10, 10, 420, 110, arcade.color.ASH_GREY
        )
        arcade.draw_lbwh_rectangle_filled(
            10, 120, 420, 40, arcade.color.BLACK
        )
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

        full_screen: Dict[bool, Tuple[int, int]] = {
            False: (10, 936),
            True: (10, 1060)
        }
        dx, dy = full_screen[self.window.fullscreen]

        arcade.draw_text(
            f"Turns: {self.current_turn + 1}/{len(self.turns)}",
            dx,
            dy,
            arcade.color.BLACK,
            16
        )
        if self.current_turn == len(self.turns) - 1:
            arcade.draw_text(
                "(SIMULATION FINISHED!)",
                dx + 140,
                dy,
                arcade.color.BLACK,
                12
            )

        if self.pause:
            arcade.draw_lbwh_rectangle_filled(
                10,
                160,
                420,
                40,
                arcade.color.AMBER
            )
            arcade.draw_text(
                "PAUSED: Press SPACE to Continue",
                30,
                172,
                arcade.color.BLACK,
                14
            )

        # Drawing Map Description

        # Header and Background
        arcade.draw_lbwh_rectangle_filled(
            440, 10, 420, 110, arcade.color.ASH_GREY
        )
        arcade.draw_lbwh_rectangle_filled(
            440, 120, 420, 40, arcade.color.BLACK
        )
        arcade.draw_text("Map Description", 460, 130, arcade.color.ASH_GREY, 16)

        # Restricted Zone
        arcade.draw_text(
            "Restricted Zone",
            460,
            70,
            arcade.color.BLACK,
            12
        )
        arcade.draw_circle_filled(
            475,
            35,
            18,
            self.colors['default'],
            12
        )

        arcade.draw_circle_outline(
            475,
            35,
            18,
            arcade.color.ASH_GREY,
            8
        )

        arcade.draw_circle_outline(
            475,
            35,
            18,
            self.colors['red'],
            4
        )

        # Max Link Capacity
        arcade.draw_text(
            "Max Link Capacity",
            614,
            70,
            arcade.color.BLACK,
            12
        )

        arcade.draw_line(
            614,
            30,
            714,
            30,
            self.colors["red"],
            3
        )

        arcade.draw_lbwh_rectangle_filled(
            651,
            17,
            26,
            26,
            self.colors["red"]
        )

        arcade.draw_text(
            "N",
            658,
            24,
            self.colors["white"],
            12
        )

        # Drone
        arcade.draw_text(
            "Drone",
            780,
            70,
            arcade.color.BLACK,
            12
        )

        arcade.draw_circle_filled(
            800,
            35,
            18,
            self.colors['black'],
            12
        )

        arcade.draw_text(
            "N",
            794,
            28,
            self.colors["white"],
            12
        )

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key in [arcade.key.Q, arcade.key.ESCAPE]:
            arcade.exit()

        if key == arcade.key.SPACE:
            self.pause = not self.pause

        if key == arcade.key.R:
            self._init_drones_pos()
            self.current_turn = -1

        if key == arcade.key.F or key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)

    def on_mouse_scroll(
            self,
            x: int,
            y: int,
            scroll_x: float,
            scroll_y: float
    ) -> None:
        self.camera.zoom += scroll_y * 0.1
        self.camera.zoom = max(0.2, min(self.camera.zoom, 4.0))

    def on_mouse_press(
            self,
            x: int,
            y: int,
            button: int,
            modifiers: int
    ) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.is_dragging = True

    def on_mouse_release(
            self,
            x: int,
            y: int,
            button: int,
            modifiers: int
    ) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.is_dragging = False

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        if self.is_dragging:
            self.camera.position = (
                self.camera.position[0] - (dx / self.camera.zoom),
                self.camera.position[1] - (dy / self.camera.zoom)
            )

    def on_update(self, delta_time: float) -> None:
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

    def _load_turn_targets(self) -> None:
        current_turn = self.turns[self.current_turn].split(' ')
        for move in current_turn:
            if move.count('-') == 1:
                drone_id, target_name = move.split('-')
                drone: Drone = self._get_drone(drone_id)
                target: Zone = self._get_zone(target_name)
                self.target_pixel_position[drone] = self._calc_zone_pos(target)
            else:
                drone_id, z1, z2 = move.split('-')
                drone = self._get_drone(drone_id)
                conn_name = self._get_connection(z1, z2)
                self.target_pixel_position[drone] = \
                    self._calc_conn_pos(conn_name)

    def _get_zone(self, name: str) -> Zone:
        for zone in self.graph.zones:
            if zone.name == name:
                return zone
        raise ValueError("Zone not found!")

    def _get_connection(self, z1: str, z2: str) -> Connection:
        for conn in self.graph.connections:
            if conn.name in [f'{z1}-{z2}', f'{z2}-{z1}']:
                return conn
        raise ValueError("Connection not found")

    def _get_drone(self, drone_id: str) -> Drone:
        for drone in self.graph.drones:
            if drone.id == drone_id:
                return drone
        raise ValueError("Drone not found")

    def _calc_zone_pos(self, zone: Zone) -> Tuple[int, int]:
        x = zone.x * self.scale + self.zone_size * 2
        y = zone.y * self.scale - self.zone_size * 2
        return x, y

    def _calc_conn_pos(self, conn: Connection) -> Tuple[float, float]:
        z1_name, z2_name = conn.name.split('-')
        z1 = self._get_zone(z1_name)
        z2 = self._get_zone(z2_name)
        x1, y1 = self._calc_zone_pos(z1)
        x2, y2 = self._calc_zone_pos(z2)
        return (x1 + x2) / 2, (y1 + y2) / 2
