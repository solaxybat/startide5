"""
Decorative Who Command
 - Show who is online
 - Where they are
 - How idle they are
 - What they are

 Name, Alias, Sex, Conn/ Idle, Location

Because just knowing they're online and have been for some time
isn't much fun when you're stalking them.
"""

import time
from commands.command import Command
from evennia import default_cmds
from evennia.server.sessionhandler import SESSIONS
from commands.assist import csex, MAX_WIDTH, header, footer, timestring
from operator import itemgetter
from evennia.utils import evtable, datetime_format

class cmdPlusWho(Command):
    """
    Calls forth a list of currently connected accounts and reports their
    name, location, and some basic character information to assist in
    locating roleplaying opportunities.

    Usage:
        '+who'
    """

    key = "+who"
    aliases = ["fa", "+fa"]
    lock = "cmd:all()"
    help_category = "General"

    def func(self):

        # Build a list of touples using the same logic as the cmdWHO
        # from evennia itself.

        account = self.account
        session_list = SESSIONS.get_sessions()

        who_list = []

        for session in session_list:
            if not session.logged_in: continue
            delta_cmd = time.time() - session.cmd_last_visible
            delta_conn = time.time() - session.conn_time
            account = session.get_account()
            puppet = session.get_puppet()
            location = puppet.location.key if puppet and puppet.location else "None"
            sex = puppet.db.sex if puppet.db.sex else "None"

            who_list.append([account.name, sex, delta_cmd, delta_conn, location])

        self.caller.msg(header("+who"))
        output = evtable.EvTable("Name","Sex","Idle","Online","Location",
                                 width=MAX_WIDTH, align="l", valign="t", border="none")
        output.reformat_column(0, width=18)
        output.reformat_column(1, width=5, align="c")
        output.reformat_column(2, width=8)
        output.reformat_column(3, width=8)
        output.reformat_column(4, width=(MAX_WIDTH - 39))

        for who in who_list:
            output.add_row("|W" + str(who[0]) + "|n",
                           csex(who[1], short=True),
                           "|W" + timestring(who[2], short=True) + "|n",
                           "|G" + timestring(who[3], short=True) + "|n",
                           str(who[4]))

        self.caller.msg(output)
        self.caller.msg(footer())

        return



