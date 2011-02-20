#   Copyright 2011 Jonathan Sadan
#
#   This file is part of 'just'.
#
#   'just' is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   'just' is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with 'just'.  If not, see <http://www.gnu.org/licenses/>.

from .. import minifiers_dir
from subprocess import call

def minify(output_file = None, cli_args = []):
    #defaults = ["--compilation_level", "ADVANCED_OPTIMIZATIONS"]
    args = ["java", "-jar", "compiler.jar"] + ['--version']
    call(args, cwd=minifiers_dir)
        


