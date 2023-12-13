import argparse
from ignishpc.common.formatter import SmartFormatter, desc, key_value_t, time_t


def _cmd(args):
    from ignishpc.job.job import _run
    return _run(args)


def setup(subparsers):
    parser = subparsers.add_parser("job", **desc("Manage jobs"))

    actions = parser.add_subparsers(dest="action", title="Available Actions", metavar="<action>")
    actions.required = True

    setup_run(actions)

    _list = actions.add_parser("list", **desc("Display jobs"))

    info = actions.add_parser("info", **desc("Get job info"))
    info.add_argument("id", action="store", metavar="str",
                      help="job id")

    cancel = actions.add_parser("cancel", **desc("Cancel a job"))
    cancel.add_argument("id", action="store", metavar="str",
                        help="job id")

    return _cmd


def setup_run(subparsers):
    run = subparsers.add_parser("run", **desc("Run a job"),
                                formatter_class=SmartFormatter,
                                epilog="""Examples:
                                     | $ ignishpc run myapp
                                     | $ ignishpc run --cores 4 --instance 2 --mem 10GB myapp --app-arg 1
                                     | $ ignishpc run --img ./myimg.sif --cores 4 --static - myapp 1 2 3""")

    run.add_argument("command", action="store",
                     help="command to run")
    run.add_argument("args", action="store", nargs=argparse.REMAINDER, default=[],
                     help="arguments for the command")

    run.add_argument("-n", "--name", action="store", metavar="str",
                     help="specify a name for the job")
    run.add_argument("-j", "--img", action="store", metavar="str",
                     help="specify a image for all containers of the job")
    run.add_argument("-p", "--property", action="append", metavar="key=value", type=key_value_t,
                     help="set a jot property", default=[])
    run.add_argument("-i", "--interactive", action="store_true", default=False,
                     help="attach to STDIN, STDOUT and STDERR, but job die when you exit")
    run.add_argument("-e", "--env", action="append", metavar="key=value", default=[], type=key_value_t,
                     help="set a job enviroment variable")
    run.add_argument("-b", "--bind", action="append", metavar="key[=value]", default=[],
                     help="set a job bind path")
    run.add_argument("-t", "--time", action="store", metavar="[[dd-]hh:]mm:ss", type=time_t,
                     help="set a limit on the total run time of the job")
    run.add_argument("-s", "--static", action="store", metavar="path",
                     help="force static allocation, cluster properties are load from a file. "
                          "Use '-' for a single cluster")
    run.add_argument("-v", "--verbose", action="store_true", default=False,
                     help="display detailed information about the job's execution")

    props = run.add_argument_group("resource properties alias")
    props.add_argument("--cores", action="store", metavar="n", type=int,
                       help="set executor cores (ignis.executor.cores)")
    props.add_argument("--instances", action="store", metavar="n", type=int,
                       help="set executor instances (ignis.executor.instances)")
    props.add_argument("--mem", action="store", metavar="n",
                       help="set executor memory (ignis.executor.memory)")
    props.add_argument("--gpu", action="store", metavar="str",
                       help="set executor gpu (ignis.executor.gpu)")
    props.add_argument("--driver-cores", "--dcores", action="store", metavar="n", type=int,
                       help="set driver cores (ignis.driver.cores)")
    props.add_argument("--driver-mem", "--dmem", action="store", metavar="n",
                       help="set driver memory (ignis.driver.memory)")
    props.add_argument("--driver-img", "--dimg", action="store", metavar="str",
                       help="set driver image (ignis.driver.image)")

    return _cmd
