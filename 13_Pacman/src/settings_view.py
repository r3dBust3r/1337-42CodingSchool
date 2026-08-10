from typing import Any
import arcade


class SettingsView(arcade.View):
    def __init__(self, game_view: Any) -> None:
        super().__init__()
        self.game_view = game_view
        self.screen = arcade.load_texture(
            'assets/images/screens/screen-03.png'
        )

        self.settings_buffer_timer: float = 0.0
        self.setting_buffer_draw = False
        self.settings_buffer = ""

        self.sounds = {
            "click": arcade.load_sound('assets/sounds/click.wav'),
        }

    def _click(self) -> None:
        arcade.play_sound(
            self.sounds["click"]
        )

    def _update_live_volume(self, new_volume: float) -> None:
        current_position = self.game_view.gameplay_music.time

        arcade.stop_sound(self.game_view.gameplay_music)

        self.game_view.gameplay_music = arcade.play_sound(
            self.game_view.sounds['bg'],
            volume=new_volume,
            loop=True
        )

        # Fast-forward the new stream to where the old one left
        self.game_view.gameplay_music.seek(current_position)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        gv_sett = self.game_view.settings
        if symbol in (arcade.key.F12, arcade.key.BACKSPACE):
            self.game_view.gameplay_music.volume = gv_sett['volume']

            if self.game_view.power_mode:
                self.game_view.scared_ghosts_music.volume = gv_sett['volume']

            self.window.show_view(self.game_view)
            return

        if symbol == arcade.key.M:
            self._click()
            self.setting_buffer_draw = True

            gv_sett["mute"] = not gv_sett["mute"]
            is_muted = gv_sett['mute']
            self.settings_buffer = 'MUTED' if is_muted else 'UNMUTED'

            if gv_sett["mute"]:
                self._update_live_volume(0.0)
            else:
                self._update_live_volume(min(1.0, gv_sett["volume"] / 2))

        elif symbol in (arcade.key.PLUS, arcade.key.EQUAL):
            self._click()
            self.setting_buffer_draw = True

            gv_sett["volume"] = min(3.0, gv_sett["volume"] + 0.1)
            vol_pct = 100 * gv_sett["volume"]
            self.settings_buffer = f'VOLUME: {vol_pct:.0f}%'

            if not gv_sett["mute"]:
                self._update_live_volume(min(1.0, gv_sett["volume"] / 2))

        elif symbol in (arcade.key.MINUS, arcade.key.UNDERSCORE):
            self._click()
            self.setting_buffer_draw = True

            gv_sett["volume"] = max(0.0, gv_sett["volume"] - 0.1)
            vol_pct = 100 * gv_sett["volume"]
            self.settings_buffer = f'VOLUME: {vol_pct:.0f}%'

            if not gv_sett["mute"]:
                self._update_live_volume(min(1.0, gv_sett["volume"] / 2))

        elif symbol == arcade.key.UP:
            self._click()
            self.setting_buffer_draw = True
            gv_sett["speed"] = min(3000, gv_sett["speed"] + 10)
            self.settings_buffer = f'SPEED: {gv_sett["speed"]}'

        elif symbol == arcade.key.DOWN:
            self._click()
            self.setting_buffer_draw = True
            gv_sett["speed"] = max(10, gv_sett["speed"] - 10)
            self.settings_buffer = f'SPEED: {gv_sett["speed"]}'

        elif symbol == arcade.key.I:
            self._click()
            self.setting_buffer_draw = True
            gv_sett["invincibility"] = not gv_sett["invincibility"]
            is_inv = gv_sett['invincibility']
            self.settings_buffer = 'INVINCIBILE' if is_inv else 'BEATABLE'

        elif symbol == arcade.key.E:
            self._click()
            self.setting_buffer_draw = True
            gv_sett["lives"] += 1
            self.settings_buffer = f'LIVES: {gv_sett["lives"]}'

        elif symbol == arcade.key.F:
            self._click()
            self.setting_buffer_draw = True
            gv_sett["ghost-freeze"] = not gv_sett["ghost-freeze"]
            is_frz = gv_sett['ghost-freeze']
            self.settings_buffer = (
                'GHOST FREEZED' if is_frz else 'GHOST UNFREEZED'
            )

    def on_update(self, delta_time: float) -> None:
        # Settings buffer
        if self.setting_buffer_draw:
            self.settings_buffer_timer += delta_time

        if self.settings_buffer_timer >= 3:
            self.setting_buffer_draw = False
            self.settings_buffer_timer = 0.0

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

        # Settings Screen
        if self.setting_buffer_draw:
            arcade.draw_text(
                self.settings_buffer,
                self.window.width / 2,
                self.window.height / 2 + 100,
                arcade.color.WHITE,
                font_size=50,
                font_name="ByteBounce",
                anchor_x='center',
                anchor_y='center',
            )
