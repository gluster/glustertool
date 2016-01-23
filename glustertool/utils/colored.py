_ALL = ("default", "red", "green", "orange", "yellow")
USE_CLI_COLOR = True


def set_cli_color(flag):
    global USE_CLI_COLOR
    USE_CLI_COLOR = flag


class COLORS:
    """
    Terminal Colors
    """
    RED = "\033[31m"
    GREEN = "\033[32m"
    ORANGE = "\033[33m"
    NOCOLOR = "\033[0m"
    BOLD = "\033[1m"
    BLACK = "\033[30m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"


def default(txt):
    return txt


def bold(txt):
    if not USE_CLI_COLOR:
        return txt

    return "{0}{1}{2}".format(COLORS.BOLD,
                              txt,
                              COLORS.NOCOLOR)


def red(txt):
    if not USE_CLI_COLOR:
        return txt

    return "{0}{1}{2}".format(COLORS.RED,
                              txt,
                              COLORS.NOCOLOR)


def green(txt):
    if not USE_CLI_COLOR:
        return txt

    return "{0}{1}{2}".format(COLORS.GREEN,
                              txt,
                              COLORS.NOCOLOR)


def yellow(txt):
    if not USE_CLI_COLOR:
        return txt

    return "{0}{1}{2}".format(COLORS.YELLOW,
                              txt,
                              COLORS.NOCOLOR)


def orange(txt):
    if not USE_CLI_COLOR:
        return txt

    return "{0}{1}{2}".format(COLORS.ORANGE,
                              txt,
                              COLORS.NOCOLOR)
