import sys

from boliau import cmdlib
from boliau.plugins.py import actionlib

def do_pyobj():
    cmd = cmdlib.as_command(actionlib.PyObj())
    cmd.add_argument('--from-string', help="object encoded in json string. ")
    args = cmd.parse_argv()
    print cmd.call(args, stdin=sys.stdin).dump()    

def do_pycall():
    cmd = cmdlib.as_command(actionlib.PyCall(), require_stdin=True)
    cmd.add_argument('func', help="function name e.x json.dump")
    args = cmd.parse_argv()
    print cmd.call(args, stdin=sys.stdin).dump()
