from src.parser import Parser
from src.init import Initializer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import ConfigModel


def main():
    parser: Parser = Parser()
    config: ConfigModel = parser.get_config()

    init = Initializer(20, 11)



if __name__ == "__main__": main()

    # try: 
    #     main()
    # except Exception as e:
    #     print(e)
    #     exit(1)
