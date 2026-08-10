from src.parser import Parser
from src.main_view import MainView
from typing import TYPE_CHECKING
import arcade


if TYPE_CHECKING:
    from src.models import ConfigModel

from warnings import filterwarnings
filterwarnings('ignore')


def main() -> None:
    # Parser
    parser: Parser = Parser()
    config: ConfigModel = parser.get_config()

    screen_w, screen_h = arcade.get_display_size()
    window = arcade.Window(screen_w, screen_h, fullscreen=True)

    # Main menu view
    main_menu = MainView(config)
    window.show_view(main_menu)
    arcade.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f'Error: {e}')
        exit(1)
