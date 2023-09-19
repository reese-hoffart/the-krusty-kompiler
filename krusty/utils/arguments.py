# import pkg_resources
from argparse import ArgumentParser, Namespace
from pathlib import Path

def get_args() -> Namespace:
    """Parse and return arguments

    Returns:
        Namespace: Parsed argu
    """
    distribution = "0.1" #pkg_resources.get_distribution("krusty")

    parser = ArgumentParser(
        prog="krusty " + distribution,
        description="A krappy kompiler",
    )

    parser.add_argument("PROGRAM", type=str, help="Filename of input program")

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Path to generated LLVM",
        default=""
    )

    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version=f"{parser.prog} {distribution}",
    )

    args = parser.parse_args()

    if args.output == "":
        args.output = Path(args.PROGRAM).stem + ".ll"
    
    return args