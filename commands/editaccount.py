"""
Editaccount - Evennia port of the Account Hammer command used on
social MUCK games for setting basic default information.

Especially important as basic @set commands are not available
to standard accounts.
"""

from evennia import default_cmds
from commands.command import Command
from evennia.utils.evmenu import EvMenu
from evennia.utils.evtable import wrap
from commands import assist
from assist import header, footer, csex

class CmdEditAccount(Command):
    """
    Editaccount allows for a list-based view of the basic roleplaying attributes available
    on most social games, giving a 'one stop shop' to setting up most basic information
    used for social interaction. It is menu driven and takes no inputs.Evennia port
    by Indigo@Startide

    Usage:
        'editplayer'
        '+editplayer'
    """

    key = "editplayer"
    aliases = ["+editplayer"]
    help_category = "General"

    def func(self):

        # Use Editaccount to set initial RP Variables

        if not self.caller.db.chargen:
            self.caller.db.chargen = False
        if not self.caller.db.fullname:
            self.caller.db.fullname = "None"
        if not self.caller.db.sex:
            self.caller.db.sex = "None"
        if not self.caller.db.race:
            self.caller.db.race = "None"
        if not self.caller.db.flight:
            self.caller.db.flight = False
        if not self.caller.db.scent:
            self.caller.db.scent = "None"
        if not self.caller.db.fullname:
            self.caller.db.fullname = "None"

        EvMenu(self.caller, "commands.editaccount",
               startnode="menu_start_node",
               node_formatter=node_formatter)

def menu_start_node(caller):

    options = ()
    text = "|CName:|n " + caller.name + "\n"
    if caller.db.flight:
        text += "|CCan Fly:|n |GYes|n\n"
    else:
        text += "|CCan Fly:|n No\n"
    text += "\n" + "Enter the Number of the Item to Change.\n"

    line = "|CFull Name:|n " + caller.db.fullname
    options = options + ({"desc": line,
                          "goto": "askFullname"},)
    line = "|CSex:|n " + csex(caller.db.sex)
    options = options + ({"desc": line,
                          "goto": "askSex"},)
    line = "|CRace:|n " + caller.db.race
    options = options + ({"desc": line,
                          "goto": "askRace"},)
    line = "|CSet Description|n"
    options = options + ({"desc": line,
                          "goto": "askDesc"},)
    line = "|CScent:|n " + caller.db.scent
    options = options + ({"desc": line,
                          "goto": "askScent"},)
    options = options + ({"key": ("_default", "Q", "q", "Quit", "quit"),
                          "desc": "Quit"},)

    return text, options

def askSex(caller):

    text = "Select one of the following: \n"

    options = ({"key": ("M", "m", "Male", "male"),
                "desc": "Male",
                "exec": lambda caller: setattr(caller.db, "sex", "Male"),
                "goto": "menu_start_node"},
               {"key": ("F", "f", "Female", "female"),
                "desc": "Female",
                "exec": lambda caller: setattr(caller.db, "sex", "Female"),
                "goto": "menu_start_node"},
               {"key": ("I", "i", "Intersex", "intersex"),
                "desc": "Intersex",
                "exec": lambda caller: setattr(caller.db, "sex", "Intersex"),
                "goto": "menu_start_node"},
               {"key": ("H", "h", "Hermaphrodite", "herm"),
                "desc": "Hermaphrodite",
                "exec": lambda caller: setattr(caller.db, "sex", "Hermaphrodite"),
                "goto": "menu_start_node"},
               {"key": ("N", "n", "Neuter", "neuter"),
                "desc": "Neuter",
                "exec": lambda caller: setattr(caller.db, "sex", "Neuter"),
                "goto": "menu_start_node"})

    return text, options

def askRace(caller):

    text = "Please input a race, it must be withing 16 characters. <Return> to Cancel: "

    options = ({"key": "_default",
               "exec": setRace,
               "goto": "menu_start_node"})

    return text, options

def setRace(caller, raw_string):
    race = raw_string.strip()
    if not race:
        caller.msg("Cancelled")
    else:
        caller.db.race = race[:16]
        caller.msg("Race set to %s" % race[:16])

def askScent(caller):

    text = "Please input a scent message. <Return> to Cancel: "

    options = ({"key": "_default",
                "exec": setScent,
                "goto": "menu_start_node"})

    return text, options

def setScent(caller, raw_string):
    scent = raw_string.strip()
    if not scent:
        caller.msg("Cancelled")
    else:
        caller.db.scent = scent
        caller.msg("|CScent Message Set to:|r %s" % scent)

def askFullname(caller):

    text = "Please type in your character's full name. <Return> to Cancel: "

    options = ({"key": "_default",
                "exec": setFullname,
                "goto": "menu_start_node"})

    return text, options

def setFullname(caller, raw_string):
    fullname = raw_string.strip()
    if not fullname:
        caller.msg("Cancelled")
    else:
        caller.db.fullname = fullname
        caller.msg("|CFull Name Set to:|r %s" % fullname)

def askDesc(caller):

    text = "Please input your desc on a single line. Use ||/ for a new line "
    text += "and ||- for tab. You can change this with the 'desc' command at "
    text += "any time. <Return> to Cancel: "

    options = ({"key": "_default",
                "exec": setDesc,
                "goto": "menu_start_node"})

    return text, options

def setDesc(caller, raw_string):
    desc = raw_string.strip()
    if not desc:
        caller.msg("Cancelled")
    else:
        caller.db.desc = desc
        caller.msg("|CDesc Set to:|n %s" % desc)

def node_formatter(nodetext, optionstext, caller=None):
    separator1 = header("Edit Account")
    separator2 = ""
    return separator1 + "\n" + nodetext + "\n" + optionstext + "\n" + footer()