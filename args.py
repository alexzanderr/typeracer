

import argparse




def ParseProgramArguments():
    """just parses the arguments from command-line interface

    Returns:
        argparse.ArgumentParser: returns an object of this
        type with all the args parsed from command-line
    """

    argument_parser = argparse.ArgumentParser(description="typeracer.py usage")
    #
    argument_parser.add_argument(
        "--code-from-txt",
        type=str,
        help="load custom code/multiline text from text file (warning: format must be valid)",
        default=None)

    argument_parser.add_argument(
        "--code-from-json",
        type=str,
        help="load custom code/multiline text from JSON file (warning: format must be valid)",
        default=None)

    argument_parser.add_argument(
        "--minimalist",
        type=bool,
        help="run the game without title and many details",
        default=False
    )

    argument_parser.add_argument(
        "--custom-quote",
        type=str,
        help="load custom single line text into the game",
        default=None
    )

    argument_parser.add_argument(
        "--save-stats",
        type=bool,
        help="if this is on, then you will get saved analytics of your matches; this requires a python simple web server which is by default shipped with the package",
        default=True
    )

    argument_parser.add_argument(
        "--ui-theme",
        type=str,
        help="gruvbox is the best",
        default="gruvbox"
    )

    return argument_parser.parse_args()
