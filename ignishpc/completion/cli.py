import subprocess
import shutil
import site
import sys
import os
from ignishpc.common.formatter import SmartFormatter, desc


def _cmd(args):
    if sys.stdout.isatty():
        print(f"Use: source <(ignishpc completion)")
    else:
        cmd = "register-python-argcomplete"
        path = os.environ.get("PATH", os.defpath) + ":" + os.path.join(site.USER_BASE, "bin")
        full_cmd = shutil.which("register-python-argcomplete", path=path)
        print(f'eval "$({full_cmd if full_cmd is not None else cmd} ignishpc)"')


def setup(subparsers):
    subparsers.add_parser("completion", **desc("Generate the autocompletion script for the shell"),
                          formatter_class=SmartFormatter, epilog="""
                          To load completions in your current shell session:
                          |$ source <(ignishpc completion)
                          To load completions for every new session, execute once:
                          |$ ignishpc completion >~/.bash_completion.d/ignishpc""")
    return _cmd
