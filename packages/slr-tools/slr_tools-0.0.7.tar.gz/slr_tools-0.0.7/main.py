import argparse 
from mputils.run import parser as mputils_parser, parse_and_run

def main(): 
    main_parser = argparse.ArgumentParser(
        prog="SLR-Tools",
        description="Run various SLR tools."
    )

    subparsers = main_parser.add_subparsers(dest="command")

    # adding subparsers for the different components 
    mputils_subparser = subparsers.add_parser(
        "mputils", 
        parents=[mputils_parser], 
        add_help=False,
        help="Run mputils")
    mputils_subparser.set_defaults(func=parse_and_run)

    args = main_parser.parse_args() 

    if hasattr(args, "func"):
        args.func(args) # call corresponding command
    else: 
        main_parser.print_help()

if __name__ == "__main__":
    main()