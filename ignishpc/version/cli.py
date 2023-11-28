import os.path


def _cmd(args):
    import importlib.metadata
    print(importlib.metadata.version('ignishpc'))


def setup(subparsers):
    subparsers.add_parser("version", help="Show version information")
    return _cmd
