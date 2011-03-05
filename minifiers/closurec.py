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

description = "Google Closure Compiler"

def minify(minifiers_dir, file_list, output_file = None, cli_args = []):
    jar_path = os.path.join(minifiers_dir, 'compiler.jar')
    args = ["java", "-jar", jar_path] + cli_args

    for f in file_list:
        args += ['--js', f]

    if output_file != None:
        args += ['--output_file', output_file]

    return args
        


