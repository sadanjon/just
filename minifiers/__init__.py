import sys, os

from ..util import JustError

# get script's working directory
script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

class Minifier(object):
    MINIFIERS = []

    MINIFIERS_DIR = os.path.join(script_dir, 'minifiers')

    def __init__(self, name, args):
        Minifier.MINIFIERS.append(name)
        self.name = name

    def minify(self, file_list, output_file = None, cli_args = []):
        raise JustError("Internal error, unimplemented method called")
