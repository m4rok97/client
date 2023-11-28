from ignishpc.common.formatter import SmartFormatter, desc


def _cmd(args):
    from ignishpc.job.job import _run
    return _run(args)


def setup(subparsers, run=False):
    if run:
        actions = subparsers
    else:
        actions = _setup_job(subparsers)

    run = actions.add_parser("run", **desc("Run a job"),
                             formatter_class=SmartFormatter,
                             epilog="""Examples:
                                     | $ ignishpc TODO ...
                                     """
                             )

    return _cmd


def _setup_job(subparsers):
    parser = subparsers.add_parser("job", **desc("Manage jobs"),
                                   formatter_class=SmartFormatter,
                                   epilog="""Examples:
                                     | $ ignishpc images build ...
                                     """
                                   )

    actions = parser.add_subparsers(dest="action", title="Available Actions", metavar='<action>')

    _list = actions.add_parser("list", **desc("List jobs"),
                               formatter_class=SmartFormatter,
                               epilog="""Examples:
                                     | $ ignishpc TODO ...
                                     """
                               )

    info = actions.add_parser("info", **desc("Get job info"),
                              formatter_class=SmartFormatter,
                              epilog="""Examples:
                                     | $ ignishpc TODO ...
                                     """
                              )

    cancel = actions.add_parser("cancel", **desc("Cancel a job"),
                                formatter_class=SmartFormatter,
                                epilog="""Examples:
                                     | $ ignishpc TODO ...
                                     """
                                )

    return actions
