from src.models import ConfigModel
from src.error import PacmanError
from sys import argv
from typing import Any
import json


class Parser:
    def __init__(self) -> None:
        # --- props
        self._config_file: str = ''
        self._config: ConfigModel

        # -- methods
        self._check_arg()
        self._parse_config()


    def _strip_comments(self) -> str:
        striped = ''

        with open(self._config_file) as file:
            content = file.readlines()
            for line in content:
                line = line.strip()
                if '//' in line: line = line[0:line.index('//')]
                if '#' in line: line = line[0:line.index('#')]

                striped += line

        return striped


    def _parse_config(self) -> None:
        config: Any = self._strip_comments()
        try:
            if not config:
                raw_config = json.loads('{}')
            else:
                raw_config = json.loads(config)

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
