def _run(args):
    if args.cmd == "run":
        _job_run(args)
    else:
        return {
            "run": _job_run,
            "list": _list,
            "info": _info,
            "cancel": _cancel,
        }[args.action](args)


def _job_run(args):
    pass


def _list(args):
    pass


def _info(args):
    pass


def _cancel(args):
    pass
