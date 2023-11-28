import argparse
import sys

from ignishpc.common.formatter import SmartFormatter
import version.cli
import config.cli


def main():
    parser = argparse.ArgumentParser(prog="ignishpc",
                                     description="IgnisHPC is a computing framework designed to integrate High "
                                                 "Performance Computing (HPC) and Big Data applications. This "
                                                 "framework facilitates the development, combination, and execution "
                                                 "of applications using various programming languages and models "
                                                 "within a unified environment. ",
                                     formatter_class=SmartFormatter,
                                     epilog="""Examples:
                                     TODO    
                                     For more help on how to use IgnisHPC, head to https://ignishpc.readthedocs.io""")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="print debugging information")
    subparsers = parser.add_subparsers(dest="cmd", title="Available Commands", metavar='<cmd>')
    subparsers.required = True

    available_cmds = {
        "config": config.cli.setup(subparsers),
        "version": version.cli.setup(subparsers),
    }
    args = parser.parse_args()

    try:
        available_cmds[args.cmd](args)
    except Exception as ex:
        if args.debug:
            import traceback
            traceback.print_exception(ex)
        else:
            print("Error:", ex, file=sys.stderr)


if __name__ == "__main__":
    main()
