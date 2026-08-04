from src.models import ConfigModel
from src.error import PacmanError
from sys import argv
import json


class Parser:
    def __init__(self) -> None:
        # --- props
        self._config_file: str = ''
        self._config: ConfigModel

        # -- methods
        self._check_arg()
        self._parse_config()


    def _parse_config(self) -> None:
        with open(self._config_file) as file:
            try:
                raw_config = json.load(file)
            except json.JSONDecodeError:
                raise PacmanError('invalid json format')

            try:
                config = ConfigModel(**raw_config)
            except Exception as e:
                raise PacmanError(f'invalid config: {e}')

            self._config = config


    def get_config(self) -> ConfigModel:
        return self._config


    def _check_arg(self) -> None:
        l: int = len(argv)

        if l == 1:
            raise PacmanError('please provide the config file')

        if l > 2:
            raise PacmanError('one argument is required')

        config_file: str = argv[1]
        ext: str = config_file.split('.')[-1]
        if ext != 'json':
            raise PacmanError('config file must be a json')

        try:
            with open(config_file) as file:
                pass
        except FileNotFoundError:
            raise PacmanError(f'no such file: {config_file}')

        except PermissionError:
            raise PacmanError(f'no access permissions on: {config_file}')

        self._config_file = config_file
