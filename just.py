#! /usr/bin/python

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

import argparse, os, sys, graphtools
from util import printout
from util import printerr
from util import JustError

def create_args_parser():
    parser = argparse.ArgumentParser(description="Compile javascript files.")

    parser.add_argument('--files', nargs='+', type=str, help='files to process.')
    parser.add_argument('--html', type=str, help='the web page.')
    parser.add_argument('--output-mode', type=str, required=True,
            choices=['tags', 'minified', 'list', 'one-script'], 
            help= """
            'tags' means that script tags are produced on the html file.
            'compiled' means that one script file is produced that is then
            put in a script tag in the html file.""")
    parser.add_argument('--output-file', type=str)
    parser.add_argument('--minifier', type=str, default='closurec', 
            help='the minifier to use')

    return parser

if __name__ == "__main__":
    if sys.hexversion < 0x2060000:
        printerr("error: 'Just' needs at least version 2.6 of python")
        sys.exit(1)
        
    parser = create_args_parser()
    args = parser.parse_args()

    # get script's working directory
    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

    # get script's minifiers directory
    minifiers_dir = os.path.join(script_dir, 'minifiers')

    try:
        # confirm list of files is valid
        for file in args.files:
            if not os.path.isfile(file):
                raise JustError("%s is not a file" % file)

            if os.path.splitext(file)[1] != '.js':
                raise JustError("all file must be javascript files")

        # build dependency list
        dep_graph = {}
        entry_points = graphtools.build_dependency_graph(dep_graph, args.files)
        dep_list = graphtools.build_dependency_list(dep_graph, entry_points)

        # redirect stdout if output-file is defined
        if args.output_file != None:
            sys.stdout = open(args.output_file, 'w')

        # if html file specified
        elif args.html != None:
            if not os.path.isfile(args.html):
                raise JustError("%s is not a file" % args.html)
            if args.output_mode == 'list':
                pass
            elif args.output_mode == 'tags':
                pass
            elif args.output_mode == 'minified':
                if args.output_file == None:
                    raise JustError("HTML file and 'minified' output mode defined, but no output file")
            elif args.output_mode == 'one-script':
                pass
        else:
            if args.output_mode == 'list':
                for f in dep_list:
                    printout(os.path.relpath(f, '.'))
            elif args.output_mode == 'tags':
                for f in dep_list:
                    printout("<script type='text/javascript' src='%s'></script>" % \
                            os.path.relpath(f, '.'))
            elif args.output_mode == 'minified':
                if os.path.isfile(os.path.join(minifiers_dir, args.minifier + '.py')):
                    exec("from minifiers.%s import minify" % args.minifier)
                    minify(minifiers_dir, dep_list)
                else:
                    raise JustError("no such minifier module %s" % args.minifier)
            elif args.output_mode == 'one-script':
                pass

    except JustError as e:
        printerr(str(e))

    sys.stdout.close()



