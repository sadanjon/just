from .. import minifiers_dir
from subprocess import call

def minify(output_file = None, cli_args = []):
    #defaults = ["--compilation_level", "ADVANCED_OPTIMIZATIONS"]
    args = ["java", "-jar", "compiler.jar"] + ['--version']
    call(args, cwd=minifiers_dir)
        


