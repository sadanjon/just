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

import sys, re, os

def printout(string):
    sys.stdout.write(string + '\n')

def printerr(string):
    sys.stderr.write(string + '\n')

def write_tags(htmlpath, filelist, section=""):
    """
    Writes the tag(s) into the html/php/whatever file

    @param {str} htmlpath a valid path to a text file
    @param {list.<str>} filelist an ordered list of js files
    @param {str} section the name of the script tags section
    """

    begin_pattern = re.compile(r'(\s*)<!--\s*begin\s+(.*)\s*-->\s*')
    end_pattern = re.compile(r'(\s*)<!--\s*end\s*-->\s*')

    indentation = None

    htmlfile = open(htmlpath, "r+")

    before_tags = []
    after_tags = []

    tags = ["<script src=\"%s\" type=\"text/javascript\"></script>\n" % \
            os.path.relpath(f, os.path.dirname(htmlpath)) \
            for f in filelist]

    state = 0
    for line in htmlfile:
        if state == 0:
            before_tags.append(line)
            match_begin = begin_pattern.match(line)
            if match_begin:
                if section.split() == match_begin.group(2).split():
                    indentation = match_begin.group(1)
                    state = 1
        elif state == 1:
            match_end = end_pattern.match(line)
            if match_end:
                after_tags.append(line)
                state = 2
                break

    if state != 2:
        if state == 0:
            raise JustError("Could not find begin marker for section %s" % \
                    section)
        elif state == 1:
            raise JustError("Could not find end marker for section htmlfile.close()")

    # add rest of file to tags list
    for line in htmlfile:
        after_tags += line

    htmlfile.close()

    htmlfile = open(htmlpath, "w+")

    # adjust indentation
    tags = [indentation + t for t in tags]

    # write the entire file again
    htmlfile.writelines(before_tags + tags + after_tags)

    htmlfile.close()


def concatenate_files(file_list, output_file):
    pass

class JustError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "error: %s" % self.msg
