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

import os, sys, graphtools, tempfile
from subprocess import call
from optparse import OptionParser
minifiers = __import__("minifiers", globals(), locals(), ['*'], -1)
import util
from util import printout, printerr, JustError, write_tags, concat_files

OUTPUT_MODES = ['tags', 'one-script', 'minified', 'list']
MINIFIERS = minifiers.__all__

def check_minifiers():
    for mini in MINIFIERS:
        name = getattr(getattr(minifiers, mini), "name", None)
        desc = getattr(getattr(minifiers, mini), "description", None)
        func = getattr(getattr(minifiers, mini), "get_minify_args", None)
        if not name:
            raise JustError("Plugin %s does not have name property" % mini)
        if not desc:
            raise JustError("Plugin %s does not have description property" % mini)
        if not func:
            raise JustError("Plugin %s does not define the 'get_minifiy_args' function" % mini)

def create_args_parser():
    parser = OptionParser(usage="just [options] [JS-FILE [JS-FILE [...]]]")

    minifiers_desc = []
    for mini in MINIFIERS:
        name = getattr(getattr(minifiers, mini), "name")
        desc = getattr(getattr(minifiers, mini), "description")
        minifiers_desc.append("'%s' - %s" % (name, desc))


    output_mode_help  = "OUTPUT_MODE can be: "
    output_mode_help += "'list' - output a simple list of the files in the right order."
    output_mode_help += "'one-script' - output a concatenated one-file from all the files "
    output_mode_help += "in the right order."
    output_mode_help += "'tags' - like the list option but each file in a script html tag. "
    output_mode_help += "'minified' - give the list of files to a minifier (using the "
    output_mode_help += "--minifier option) and output a minified version to a file "
    output_mode_help += "(specified with --output-file option)."

    html_help = "The file to insert the script tags to."

    output_file_help = "Use OUTPUT_FILE with the minifier"

    minifier_help = "the following minifiers are available:\n"
    minifier_help += ", ".join(minifiers_desc)

    cli_help =  "A command line argument to pass to the minifier. "
    cli_help += "Can be specified more than once. "
    cli_help += "Example: to pass the arguments \"--dojo Hirushi\" do "
    cli_help += "-p --dojo -p Hirushi"

    section_help  = "If an HTML file specified, name the begining and closing "
    section_help += "comments that mark the section where the script tags will go."

    parser.add_option("-H", "--html", type="string", dest="html",
            metavar="HTMLFILE", help=html_help)
    parser.add_option("-m", "--output-mode", choices=OUTPUT_MODES, dest="output_mode", metavar="OUTPUT_MODE",
        default="list", help=output_mode_help)
    parser.add_option("-o", "--output-file", type="string", dest="output_file",
            metavar="OUTPUT_FILE", help=output_file_help)
    parser.add_option("-c", "--minifier", type="string", dest="minifier",
            metavar="MINIFIER", help=minifier_help)
    parser.add_option("-p", "--pass-arg", type="string", action="append",
            dest="cli_args", metavar="ARG", help=cli_help)
    parser.add_option("-s", "--section", type="string", dest="section",
            metavar="SECTION", help=section_help)

    return parser

def validate_cli(options, args):
    if len(args) == 0:
        raise JustError("No files specified.")

    # confirm list of files is valid
    for file in args:
        if not os.path.isfile(file):
            raise JustError("%s is not a file." % file)

    if options.output_mode:
        if options.output_mode not in OUTPUT_MODES:
            raise JustError("No such output-mode, %s" % options.output_mode)
        if options.output_mode == 'minified':
            if not options.minifier:
                raise JustError("'minified' output-mode specified but no minifier")
            if options.minifier not in MINIFIERS:
                raise JustError("No such minifier, %s" % options.minifier)
            if options.html and not options.output_file:
                raise JustError("Specified HTML file and output-mode 'minified' but no output file")
        if options.output_mode == "one-script":
            if options.html and not options.output_file:
                raise JustError("Specified HTML file and output-mode 'one-script' but no output file")
        if options.html and not options.section:
            raise JustError("Specified HTML file but no section")
    else:
        raise JustError("please specify output-mode")

if __name__ == "__main__":
    # temporary file path, defined here so can be cleaned later
    tfp = None
    try:
        if sys.hexversion < 0x2060000:
            raise JustError("'Just' needs at least version 2.6 of python")

        # get script's working directory
        script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

        # get script's minifiers directory
        minifiers_dir = os.path.join(script_dir, 'minifiers')

        check_minifiers()
        
        parser = create_args_parser()
        (options, args) = parser.parse_args()

        validate_cli(options, args)

        # build dependency list
        dep_graph = {}
        entry_points = graphtools.build_dependency_graph(dep_graph, args)
        dep_list = graphtools.build_dependency_list(dep_graph, entry_points)

        # if output mode is minified or 'one-script', create or output script
        if options.output_mode == 'minified' or options.output_mode == 'one-script':
            # create temporary file
            if options.output_file:
                splitext = os.path.splitext(dep_list[0])
                temp_file = tempfile.mkstemp(dir=os.path.dirname(options.output_file), 
                                suffix=splitext[1], text=True)
            else:
                temp_file = tempfile.mkstemp(dir=os.getcwd(), text=True)

            tfp = temp_file[1]
            tempf = os.fdopen(temp_file[0], "a")

            # concatenate dep list
            concat_files(dep_list, tempf)
            tempf.close()


            if options.output_mode == "minified":
                minifier = getattr(minifiers, options.minifier)
                if options.cli_args:
                    minify_args = minifier.get_minify_args(tfp,
                            output_file=options.output_file, cli_args=options.cli_args)
                else:
                    minify_args = minifier.get_minify_args(tfp,
                            output_file=options.output_file)

                printerr("Executing: %s" % " ".join(minify_args))
                call(minify_args)
                os.remove(tfp)
            else:
                if options.output_file:
                    os.rename(tfp, options.output_file)
                    printerr("Created the file: %s" % options.output_file)
                else:
                    tempf = open(temp_file[1], "r")
                    for line in tempf:
                        sys.stdout.write(line)
                    tempf.close()
                    os.remove(tfp)

            tfp = None

        # if html file specified
        if options.html:
            if not os.path.isfile(options.html):
                raise JustError("%s is not a file" % options.html)

            adjusted_fl = [os.path.relpath(f, os.path.dirname(options.html)) for f in dep_list]

            if options.output_mode == 'list':
                util.write_list(options.html, adjusted_fl, options.section)

            elif options.output_mode == 'tags':
                write_tags(options.html, adjusted_fl, options.section)

            elif options.output_mode == 'minified' or options.output_mode == 'one-script':
                adjusted_of = os.path.relpath(options.output_file, options.html)
                util.write_tags(options.html, [adjusted_of], options.section)
        else:
            adjusted_fl = [os.path.relpath(f, os.getcwd()) for f in dep_list]
            if options.output_mode == 'list':
                if options.output_file:
                    of = open(options.output_file, "w")
                    for f in adjusted_fl:
                        of.writeline(f)
                    of.close()
                else:
                    for f in dep_list:
                        printout(os.path.relpath(f))

            elif options.output_mode == 'tags':
                if options.output_file:
                    of = open(options.output_file, "w")
                    for f in adjusted_fl:
                        of.writeline("<script type='text/javascript' src='%s'></script>" % f)
                    of.close()
                else:
                    for f in dep_list:
                        printout("<script type='text/javascript' src='%s'></script>" % f)

    except JustError as e:
        printerr(str(e))
    finally:
        if tfp:
            os.remove(tfp)




