from flask import abort

class EnforcersMethods:

    def __int__(self):
        pass

    def white_space_trail_cleaner(self, arg):
        if isinstance(arg, str):
            if arg[len(arg) - 1] == ' ' or arg[0] == ' ':
                return arg.strip()

        return arg

    def arbitrary_rule_enforcer(self, arg):
        if isinstance(arg, str):
            for c in arg:
                if c == '|':
                    return abort(405, description="Arbitrary rule - The char | is not allowed in registration")
