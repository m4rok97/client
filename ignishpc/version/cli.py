from ignishpc.common.formatter import desc

def _cmd(args):
    import importlib.metadata
    print(importlib.metadata.version('ignishpc'))


def setup(subparsers):
    subparsers.add_parser("version", **desc("Show version information"))
    return _cmd
