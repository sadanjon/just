#   Copyright 2011 Jonathan Sadan
#
#   This file is part of 'Just'.
#
#   'Just' is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   'Just' is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with 'Just'.  If not, see <http://www.gnu.org/licenses/>.

import os
from . import MINIFIERS_DIR

name = 'closurec'
description = "Google Closure Compiler"

def get_minify_args(input_file, output_file = None, cli_args = None):
    jar_path = os.path.join(MINIFIERS_DIR, 'compiler.jar')
    args = ["java", "-jar", jar_path]

    args += ['--js', input_file]

    if output_file:
        args += ['--js_output_file', output_file]

    if cli_args:
        args += cli_args


    return args



