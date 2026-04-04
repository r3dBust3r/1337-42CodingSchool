from .system import FunctionCallingSystem
import argparse
import sys


def main() -> None:
    """Parse CLI arguments and launch the function calling"""
    parser = argparse.ArgumentParser(
        description="Function calling system using constrained LLM decoding"
    )
    parser.add_argument(
        "--functions_definition",
        type=str,
        default="data/input/functions_definition.json",
        help="Path to the function definitions JSON file",
    )
    parser.add_argument(
        "--input",
        type=str,
        default="data/input/function_calling_tests.json",
        help="Path to the input prompts JSON file",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/output/function_calling_results.json",
        help="Path for the output JSON file",
    )
    args = parser.parse_args()

    try:
        system = FunctionCallingSystem(
            functions_path=args.functions_definition,
            input_path=args.input,
            output_path=args.output,
        )
        system.run()

    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(0)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
