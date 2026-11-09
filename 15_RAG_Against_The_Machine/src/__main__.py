from sys import stderr


def main() -> None:
    from src.cli import CommandLineInterface
    from fire import Fire
    Fire(CommandLineInterface)


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print('\nCtrl+C')

    except Exception as e:
        print(e, file=stderr)

    except BaseException as e:
        print(e, file=stderr)
