
class Minifier(object):
    """
    Abstract minifier class.

    All minifiers modules should inherit and implement
    the minify method. And have the exact same __init__
    signature.
    """
    def __init__(self, name, short_name):
        self.name = name
        self.short_name = short_name

    def minify(self, cli_args):
        raise NotImplementedError("Abstract method")

