from ignishpc.common.formatter import SmartFormatter, desc, key_value_t


def _cmd(args):
    from ignishpc.config.config import _run
    return _run(args)


def setup(subparsers):
    parser = subparsers.add_parser("config", **desc("Configuration Management"), formatter_class=SmartFormatter,
                                   epilog="""Examples:
                                     | $ ignishpc config info
                                     | $ ignishpc config list
                                     | $ ignishpc config set ignis.container.docker.registry=mynode:5000 ignis.wdir=~
                                     | $ ignishpc config get -s ignis.container.provider
                                     | $ ignishpc config rm -u ignis.container.image""")

    actions = parser.add_subparsers(dest="action", title="Available Actions", metavar='<action>')
    actions.required = True

    actions.add_parser("info", **desc("Show configuration"))
    _list = actions.add_parser("list", help="show properties")
    _list.add_argument("-s", "--split", action="store_true",
                       help="show properties split by file")

    set = actions.add_parser("set", **desc("Set properties"))
    set.add_argument("props", metavar="key=value", nargs="+", type=key_value_t, help="Properties")
    set.add_argument("-s", "--system", action="store_true", help="modify system file instead of user file")

    get = actions.add_parser("get", **desc("Get properties"))
    get_e = get.add_mutually_exclusive_group()
    get.add_argument("keys", metavar="key", nargs="+", help="keys")
    get_e.add_argument("-u", "--user", action="store_true",
                       help="get only from user file")
    get_e.add_argument("-s", "--system", action="store_true",
                       help="get only from system file")
    get.add_argument("-f", "--fail", action="store_true",
                     help="fail if key not found")
    get.add_argument("-v", "--only-value", action="store_true", default=False,
                     help="only print key value")
    get.add_argument("-p", "--plain-value", action="store_true",
                     help="key must have a plain value")

    rm = actions.add_parser("rm", **desc("Remove properties"))
    rm_e = rm.add_mutually_exclusive_group()
    rm.add_argument("keys", metavar="key", nargs="+", help="Keys")
    rm_e.add_argument("-u", "--user", action="store_true",
                      help="remove only from user file")
    rm_e.add_argument("-s", "--system", action="store_true",
                      help="remove only from system file")
    rm_e.add_argument("-a", "--all", action="store_true",
                      help="remove a property twice if it is defined in both files")

    return _cmd
