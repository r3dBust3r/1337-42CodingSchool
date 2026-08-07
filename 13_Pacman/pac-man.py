from src.parser import Parser
from src.main_view import MainView
from typing import TYPE_CHECKING
import arcade


if TYPE_CHECKING:
    from models import ConfigModel

from warnings import filterwarnings
filterwarnings('ignore')


def main():
    # Parser
    parser: Parser = Parser()
    config: ConfigModel = parser.get_config()

    screen_w, screen_h = arcade.get_display_size()
    window = arcade.Window(screen_w, screen_h, fullscreen=True)

    # Main menu view
    main_menu = MainView(config)
    window.show_view(main_menu)


    arcade.run()
    # Pacman(13, 9)


if __name__ == "__main__": main()

    # try: 
    #     main()
    # except Exception as e:
    #     print(e)
    #     exit(1)
