from evennia import Command

class CmdSpoof(Command):
    """
    Spoof allows an account (or staff) the ability to present a block of text without
    starting it with their own name. To prevent abuse, it will append their name in
    brackets at the end of the pose.

    Usage:
        spoof [text]:   Displays 'text' with the callers name appended to the text,
                        rather then requiring it to come before.
    """

    key = "spoof"
    aliases = ["sp"]
    lock = "cmd:all()"
    help_category = "General"

    def func(self):

        caller = self.caller
        args = self.args.strip()
        location = self.caller.location

        if not args:
            caller.msg("Specify a message to spoof: 'spoof [message]'")
            return

        string = "|c"
        string += args
        string += " .. |b[|g{}|b]|n".format(caller.name)

        location.msg_contents(string)

        return