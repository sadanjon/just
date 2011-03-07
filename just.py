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

import os, sys, graphtools
from subprocess import call
from optparse import OptionParser
import minifiers
from util import printout, printerr, JustError, write_tags

def create_args_parser():
    parser = OptionParser(usage="just [options] [JS-FILE [JS-FILE [...]]]")

    output_mode_help = \
"""
OUTPUT_MODE can be:
list - output a simple list of the files in the right order.
one-script - output a concatenated one-file from all the files
in the right order.
tags - like the list option but each file in a script html tag.
minified - give the list of files to a minifier (using the
--minifier option) and output a minified version to a file
(specified with --output-file option).
"""

    html_help = "The file to insert the script tags to."

    output_file_help = "Use OUTPUT_FILE with the minifier"

    minifier_help = "Choose a minifier from the minifiers installed:\n"
    minifier_help += ", ".join(minifiers.__all__)

    parser.add_option("-H", "--html", type="string", dest="html",
            metavar="HTMLFILE", help=html_help)
    parser.add_option("-m", "--output-mode", choices=['tags', 'minified',
        'list', 'one-script'], dest="output_mode", metavar="OUTPUT_MODE",
        default="list", help=output_mode_help)
    parser.add_option("-o", "--output-file", type="string", dest="output_file",
            metavar="OUTPUT_FILE", help=output_file_help)
    parser.add_option("-c", "--minifier", type="string", dest="minifier",
            metavar="MINIFIER", help=minifier_help)

    return parser

if __name__ == "__main__":
    if sys.hexversion < 0x2060000:
        printerr("error: 'Just' needs at least version 2.6 of python")
        sys.exit(1)
        
    parser = create_args_parser()
    (options, args) = parser.parse_args()



    # get script's working directory
    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

    # get script's minifiers directory
    minifiers_dir = os.path.join(script_dir, 'minifiers')

    try:
        if len(args) == 0:
            raise JustError("no files given")

        # confirm list of files is valid
        for file in args:
            if not os.path.isfile(file):
                raise JustError("%s is not a file" % file)

            if os.path.splitext(file)[1] != '.js':
                raise JustError("all file must be javascript files")

        # build dependency list
        dep_graph = {}
        entry_points = graphtools.build_dependency_graph(dep_graph, args)
        dep_list = graphtools.build_dependency_list(dep_graph, entry_points)

        # redirect stdout if output-file is defined
        if options.output_file:
            sys.stdout = open(args.output_file, 'w')

        # if html file specified
        elif options.html:
            if not os.path.isfile(options.html):
                raise JustError("%s is not a file" % options.html)
            if options.output_mode == 'list':
                #TODO: implement
                pass
            elif options.output_mode == 'tags':
                write_tags(options.html, dep_list, "scripts")
            elif options.output_mode == 'minified':
                if not options.output_file:
                    raise JustError("HTML file and 'minified' output mode defined, but no output file")
            elif options.output_mode == 'one-script':
                #TODO: implement
                pass
        else:
            if options.output_mode == 'list':
                for f in dep_list:
                    printout(os.path.relpath(f, '.'))
            elif options.output_mode == 'tags':
                for f in dep_list:
                    printout("<script type='text/javascript' src='%s'></script>" % \
                            os.path.relpath(f, '.'))
            elif options.output_mode == 'minified':
                minifier = getattr(minifiers, options.minifier, None)
                if not minifier:
                    raise JustError("no such minifier module %s" % options.minifier)
                if not options.output_file:
                    minifier_args = minifier.minify(minifiers_dir, dep_list)
                    call(minifier_args)
                else:
                    minifier.minify(minifiers_dir, dep_list, options.output_file)
            elif options.output_mode == 'one-script':
                #TODO: implement
                pass

    except JustError as e:
        printerr(str(e))

    sys.stdout.close()



