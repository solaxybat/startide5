"""
What-Is XXX is a MUCK-based command allowing specific characters to set a list of 'interests'
    or likes that allow others to find them. As noted by the XXX, this particular version is
    designed primarily for adult interests. As What-Is is a fairly self contained and modular
    bit of code, it is being used as practice in coding.

Usage:
    +wi (or +wixxx):     display an output of all nearby (in the room) accounts with What-Is
                         information.

    +wi [name]:          display information of character object [name], works at range.

    +wi/set [string]:    Append a list of dictionary keys from [string] to the character's
                         what-is data.

    +wi/clear:           Remove current list of keys.

    +wi/custom [string]: Allows up to 12 characters for a custom field, at the end of the
                         final listing.

    +wi/list:            Display a full list of currently registered keys.
"""

from evennia import CmdSet
from evennia.utils import evtable
from commands import assist

class CmdWixxx(Command):
    """
    What-Is XXX is a MUCK-based command allowing specific characters to set a list of 'interests'
    or likes that allow others to find them. As noted by the XXX, this particular version is
    designed primarily for adult interests. As What-Is is a fairly self contained and modular
    bit of code, it is being used as practice in coding. Evennia port by Indigo@Startide

    Usage:
        +wi (or +wixxx):     display an output of all nearby (in the room) accounts with What-Is
                             information.

        +wi [name]:          display information of character object [name], works at range.

        +wi/set [string]:    Append a list of dictionary keys from [string] to the character's
                             what-is data.

        +wi/clear:           Remove current list of keys.

        +wi/custom [string]: Allows up to 12 characters for a custom field, at the end of the
                             final listing.

        +wi/list:            Display a full list of currently registered keys.
"""

    key = "+wi"
    aliases = ["+wixxx", "wi", "wixxx"]
    lock = "cmd:all()"
    help_category = "General"

    # Dictionary List for different flags. Edit this to create/ remove flags.

    wiData = {
        '!': 'no',
        'a': 'available',
        'ag': 'anything-goes',
        'age': 'ageplay',
        'an': 'anal',
        'ap': 'avian-preferred',
        'aq': 'aquatic',
        'bi': 'bisexual',
        'bit': 'biting',
        'blo': 'blood',
        'bod': 'body-modification',
        'cmc': 'cum-covered',
        'cml': 'cum-loving',
        'cok': 'cock-worshipping',
        'con': 'consensual-only',
        'crx': 'crossdresser',
        'cws': 'cunt-worshipping',
        'd': 'dominant',
        'dia': 'diapers',
        'dir': 'dirty-talk',
        'dis': 'disobediant',
        'dsc': 'discipline',
        'dye': 'dyes',
        'edi': 'edible',
        'el': 'electrical',
        'ema': 'emasculation',
        'en': 'enema',
        'ex': 'exhibitionist',
        'exp': 'experienced',
        'fe': 'female-biased',
        'fea': 'fear',
        'ff': 'foot-fetish',
        'fmz': 'feminization',
        'fp': 'fur-preferred',
        'fsh': 'forcedshifting',
        'fst': 'fisting',
        'fud': 'food-fetish',
        'fuk': 'fuckable',
        'gay': 'homosexual',
        'gen': 'gendershifting',
        'gro': 'group-sex',
        'het': 'heterosexual',
        'hmb': 'herm-biased',
        'hor': 'horny',
        'hu': 'humiliation',
        'hum': 'humor-and-comedy',
        'hyp': 'hypnosis',
        'i': 'inexperienced',
        'if': 'inflation',
        'inc': 'incest',
        'inf': 'infantilist',
        'int': 'intelligence-biased',
        'jo': 'masterbating',
        'l': 'lecherous',
        'la': 'large',
        'lac': 'lactating',
        'lat': 'latex',
        'le': 'leather',
        'lea': 'leashable',
        'loo': 'loose',
        'ma': 'male-biased',
        'mas': 'masochist',
        'mat': 'mated',
        'mnd': 'mind-control',
        'mag': 'magic-sex',
        'mon': 'monogomous',
        'mum': 'mummification',
        'non': 'non-consensual',
        'ns': 'non-sexual',
        'nt': 'nipple-torture',
        'null': 'nullification',
        'obj': 'objectification',
        'od': 'orgasm-denial',
        'ora': 'oral',
        'ow': 'owned',
        'pet': 'pet',
        'pie': 'piercing',
        'plt': 'plants',
        'plu': 'plushophile',
        'ply': 'polyamorous',
        'pp': 'public-property',
        'prg': 'pregnophile',
        'pri': 'private',
        'pty': 'panty-fetish',
        'pub': 'public',
        'rim': 'rimming',
        'rom': 'romantic',
        'sad': 'sadist',
        'sc': 'scat',
        'sha': 'shaving',
        'shd': 'sheaths',
        'shy': 'shy',
        'siz': 'size-queen',
        'slu': 'slutty',
        'slv': 'slave',
        'sm': 'small',
        'smc': 'sex-machines',
        'snu': 'snuff',
        'sp': 'scale-preferred',
        'spk': 'spanking',
        'str': 'strap-ons',
        'su': 'submissive',
        'sw': 'switch',
        'sxd': 'sex-doll',
        'tan': 'tantric',
        'tat': 'tattoo(ing)',
        'tea': 'teasing',
        'ten': 'tentacles',
        'tik': 'tickling',
        'tit': 'breast-loving',
        'top': 'top',
        'toy': 'toys',
        'tra': 'trainable',
        'tz': 'transformation',
        'un': 'unavailable',
        'unb': 'unbirthing',
        'up': 'uppity',
        'van': 'vanilla',
        'vi': 'virgin',
        'vor': 'voraphile',
        'voy': 'voyuer',
        'wa': 'watersports',
        'wet': 'wet-and-messy',
        'yif': 'yiffy'

    }

    def func(self):

        # Start the fun..

        caller = self.caller
        args = self.args.strip()
        switch = next(iter(self.switches or []), None)

        # If the switch is /list we can ignore everything else...

        if switch == "list":
            result = evtable.EvTable("","Flag:Meaning","", width=74, align="l", valign="t", border="none")
            for i, r, q in zip(*[iter(sorted(self.wiData))]*3):
                result.add_row("|C" + i + "|n: " + self.wiData[i], "|C" + r + "|n: " + self.wiData[r], "|C" + q + "|n: " + self.wiData[q])

            self.caller.msg(header("What-IS"))
            self.caller.msg(result)
            self.caller.msg(footer())

            return

        # If the switch is /clear then we just remove the flag property

        elif switch == "clear":
            result = "Clearing Set Flags...\n"
            caller.db.widat = ""
            self.caller.msg(header("What-IS"))
            self.caller.msg(result)
            self.caller.msg(footer())
            return

        # The /custom switch just grabs the first 12 characters of the arg
        # and turns it into a data field.

        elif switch == "custom":
            result = "Setting a custom string...\n"
            string = args[:13]
            result += '\t"' + string + '"\n'
            caller.db.widatcust = string
            self.caller.msg(header("What-IS"))
            self.caller.msg(result)
            self.caller.msg(footer())
            return

        # Set a list of keys by appending them to caller.db.widat

        elif switch == "set":
            # Sanity Check, have they been initialized?
            if not self.caller.db.widat:
                self.caller.db.widat = ""
            if not self.caller.db.widatcust:
                self.caller.db.widatcust = ""
            result = "Adding flags...\n"

            # Quietly sanitize by ignoring anything not a key.

            for i in args.split():
                if i in self.wiData:
                    result += self.wiData[i] + " "
                    caller.db.widat += i + " "

            result += "\nFor a list of: "
            for i in caller.db.widat.split():
                result += self.wiData[i] + " "

            self.caller.msg(header("What-IS"))
            self.caller.msg(result)
            self.caller.msg(footer())
            return

        elif not switch:

            # No switch found, this means we want an output.
            # Check if we want a specific output.
            if args:
                # Alright, time to set up a table...
                result = evtable.EvTable("Name","Result", width=74, align="l", valign="t", border="none")
                result.reformat_column(0, width=16)
                result.reformat_column(1, width=55)
                for i in args.split():
                    target = caller.search(i, typeclass="typeclasses.characters.Character", global_search=True)
                    if target:
                        # Expand the list of the target.
                        wi_result = ""
                        basics = ""
                        if target.db.widat:
                            for k in target.db.widat.split():
                                wi_result += self.wiData[k] + " "
                        if target.db.widatcust:
                            wi_result += caller.db.widatcust
                        if not target.db.widat and not target.db.widatcust:
                            wi_result = "No WI info set "
                        if target.db.sex:
                            wi_result += csex(target.db.sex)
                        if target.db.race:
                            wi_result += " " + target.db.race
                        else:
                            wi_result += " Unknown"
                        result.add_row(target.name,wi_result)
                    else:
                        result.add_row(i, "Character not found.")

                self.caller.msg(header("What-IS"))
                self.caller.msg(result)
                self.caller.msg(footer())
                return

            else:
                # No args. Just give the room.
                result = evtable.EvTable("Name","result", width=74, align="l", valign="t", border="none")
                result.reformat_column(0, width=16)
                result.reformat_column(1, width=55)
                for i in caller.location.contents:
                    wi_result = ""
                    basics = ""

                    if i.has_account:

                        if i.db.widat:
                            for k in i.db.widat.split():
                                wi_result += self.wiData[k] + " "
                        else:
                            wi_result = "No WI info set "
                        if i.db.sex:
                            wi_result += csex(i.db.sex)
                        if i.db.race:
                            wi_result += " " + i.db.race
                        else:
                            wi_result += " Unknown"
                        result.add_row(i.name,wi_result,basics)
                        result.add_row()

                self.caller.msg(header("What-IS"))
                self.caller.msg(result)
                self.caller.msg(footer())
                return

            self.caller.msg(output)
            return

        else:
            output += "I didn't understand that switch."
            self.caller.msg(output)
            return
