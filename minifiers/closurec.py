from minifier import Minifier
from subprocess import call
from . import minifiers_list

class ClosureCompiler(Minifier):
    def __init__(self, name, short_name):
        super(ClosureCompiler, self).__init__(name, short_name);

    def minify(self, cli_args):
        args = ["java", "-jar", "compiler.jar"] + cli_args
        call(args, cwd="minifiers")
        

minifiers_list.append(ClosureCompiler("google closure compiler", "closurec"))

