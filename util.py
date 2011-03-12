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

import sys, re

def printout(string):
    sys.stdout.write(string + '\n')

def printerr(string):
    sys.stderr.write(string + '\n')

def write_list(htmlpath, str_list, section=""):
    """
    Writes the str_list into the html/php/whatever file

    @param {str} htmlpath a valid path to a text file
    @param {list.<str>} list of strings to write to file
    @param {str} section name of the script tags section
    """

    begin_pattern = re.compile(r'(\s*)<!--\s*begin\s+(.*)\s*-->\s*')
    end_pattern = re.compile(r'(\s*)<!--\s*end(\s*| .*)-->\s*')

    indentation = None

    htmlfile = open(htmlpath, "r+")

    before_section = []
    after_section = []

    state = 0
    for line in htmlfile:
        if state == 0:
            before_section.append(line)
            match_begin = begin_pattern.match(line)
            if match_begin:
                if section.split() == match_begin.group(2).split():
                    indentation = match_begin.group(1)
                    state = 1
        elif state == 1:
            match_end = end_pattern.match(line)
            if match_end:
                after_section.append(line)
                state = 2
                break

    if state != 2:
        if state == 0:
            raise JustError("Could not find begin marker for section: %s" % \
                    section if len(section) > 0 else "(empty section name)")
        elif state == 1:
            raise JustError("Could not find end marker for section: %s")

    # add rest of file to tags list
    for line in htmlfile:
        after_section += line

    htmlfile.close()

    # reopen with truncating writing skills!
    htmlfile = open(htmlpath, "w+")

    # adjust indentation
    str_list = [indentation + s + "\n" for s in str_list]

    # write the entire file again
    htmlfile.writelines(before_section + str_list + after_section)

    htmlfile.close()

def write_tags(htmlpath, filelist, section=""):
    """
    Writes the tag(s) into the html/php/whatever file

    @param {str} htmlpath a valid path to a text file
    @param {list.<str>} filelist an ordered list of js files
    @param {str} section the name of the script tags section
    """

    tags = ["<script src=\"%s\" type=\"text/javascript\"></script>" %\
            f for f in filelist]

    write_list(htmlpath, tags, section)

def concat_files(file_list, output_file):
    """
    Concatenate a list of files

    @param {list.<str>} file_list a list of file paths to concatenate
    @param {file} output_file an open file object to output the concatenated
    result
    """
    for file_path in file_list:
        input = open(file_path, "r")
        output_file.writelines(input)
        input.close()


class JustError(BaseException):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "'Just' has encountered a problem:\n\t" + self.msg
