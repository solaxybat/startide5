"""
IC/OOC Teleporter script.
Command Set accessible via icTeleport
"""

from commands.command import Command
from evennia import CmdSet
from evennia import search_object

# This is the dbref to send people to as the OOC root room
ooc_root = "#5"


class goOOC(Command):
    """
    IC/OOC System is a common utility on social games that utilize a system of in
    character and out of character rooms. It saves your current position in a db
    attribute and sends you to the center of the OOC rooms when going "Out of
    Character". It then sends back to your last saved position when you go "In
    Character".

    Usage:
        +ooc:  sends you out of character and sets your icstat to false.

        +ic:   sends you in character and sets you icstat to true.
    """
    key = "+ooc"
    aliases = []
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
        caller = self.caller

        if not caller.db.icloc:
            caller.db.icloc = None
            caller.db.icstat = True

        if caller.db.icstat:
            caller.db.icstat = False
            caller.db.icloc = caller.location
            caller.move_to(search_object(ooc_root)[0])
        else:
            caller.msg("You are already OOC!")


class goIC(Command):
    """
    IC/OOC System is a common utility on social games that utilize a system of in
    character and out of character rooms. It saves your current position in a db
    attribute and sends you to the center of the OOC rooms when going "Out of
    Character". It then sends back to your last saved position when you go "In
    Character".

    Usage:
        +ooc:  sends you out of character and sets your icstat to false.

        +ic:   sends you in character and sets you icstat to true.
    """
    key = "+ic"
    aliases = []
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
        caller = self.caller

        if not caller.db.icloc:
            caller.msg("You have not used +ooc yet!")
        else:
            if caller.db.icstat:
                caller.msg("You are already IC!")
            else:
                caller.db.icstat = True
                caller.move_to(search_object(caller.db.icloc)[0])

class icTeleport(CmdSet):
    key = "iCTeleportCmdSet"
    mergetype = "Union"

    def at_cmdset_creation(self):
        self.add(goIC)
        self.add(goOOC)
