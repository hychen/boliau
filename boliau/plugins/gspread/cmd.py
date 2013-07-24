import sys
import getpass

from boliau import cmdlib
from boliau.plugins.gspread import actionlib
    
def do_insert():
    cmd = cmdlib.as_command(actionlib.Upsert(),
                            require_stdin=True)
    cmd.add_argument('spreadsheet', help="spreadsheet name.")
    cmd.add_argument('--email', help = "user email")
    cmd.add_argument('--worksheet', help="worksheet name.")
    args = cmd.parse_argv()
    args.password = getpass.getpass()
    print cmd.call(args, stdin=sys.stdin)
