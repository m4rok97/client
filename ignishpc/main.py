import subprocess
import argparse
import sys

from ignishpc.common.formatter import SmartFormatter
import ignishpc.config.cli
import ignishpc.images.cli
import ignishpc.job.cli
import ignishpc.services.cli
import ignishpc.version.cli


def main():
    parser = argparse.ArgumentParser(prog="ignishpc",
                                     description="IgnisHPC is a computing framework designed to integrate High "
                                                 "Performance Computing (HPC) and Big Data applications. This "
                                                 "framework facilitates the development, combination, and execution "
                                                 "of applications using various programming languages and models "
                                                 "within a unified environment. ",
                                     formatter_class=SmartFormatter,
                                     epilog="""Examples:
                                     | $ ignishpc image build ...
                                     | $ ignishpc run myapp
                                     | $ ignishpc job cancel ...
                                     | $ ignishpc service nomad start
                                         
                                     For more help on how to use IgnisHPC, head to https://ignishpc.readthedocs.io""")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="print debugging information")
    parser.add_argument("-c", "--config", action="store", metavar="path",
                        help="specify a configuration file")
    subparsers = parser.add_subparsers(dest="cmd", title="Available Commands", metavar='<cmd>')
    subparsers.required = True

    available_cmds = {
        "config": ignishpc.config.cli.setup(subparsers),
        "images": ignishpc.images.cli.setup(subparsers),
        "job": ignishpc.job.cli.setup(subparsers),
        "run": ignishpc.job.cli.setup_run(subparsers),
        "services": ignishpc.services.cli.setup(subparsers),
        "version": ignishpc.version.cli.setup(subparsers),
    }
    args = parser.parse_args()
    from ignishpc.common import configuration
    if not configuration.load_config(args.config):
        print("warning: error in some configuration files, use 'ignishpc config info'", file=sys.stderr)
    try:
        available_cmds[args.cmd](args)
    except subprocess.CalledProcessError as ex:
        exit(ex.returncode)
    except Exception as ex:
        if args.debug:
            import traceback
            traceback.print_exception(ex)
        else:
            print("Error:", ex, file=sys.stderr)
        exit(-1)


if __name__ == "__main__":
    main()
