#! /usr/bin/python

import argparse, os, sys, graphtools

def create_args_parser():
    parser = argparse.ArgumentParser(description="Compile javascript files.",
           usage='just.py --html html_file --output {tags, compiled} file [ files ... ]')

    parser.add_argument('files', nargs='+', type=str, help='files to process.')
    parser.add_argument('--html', required=True, type=str, help='the web page.')
    parser.add_argument('--output', type=str, required=True,
            choices=['tags', 'compiled'], 
            help= """
            'tags' means that script tags are produced on the html file.
            'compiled' means that one script file is produced that is then
            put in a script tag in the html file.""")

    return parser


if __name__ == "__main__":
    parser = create_args_parser()
    args = parser.parse_args()


    # confirm list of files is valid
    for file in args.files:
        if not os.path.isfile(file):
            print "error: %s is not a file" % file
            sys.exit(1)

        if os.path.splitext(file)[1] != '.js':
            print "error: all files must be javascript files"
            sys.exit(1)

    # confirm that the html file exists and is a file
    if not os.path.isfile(args.html):
        print "error: %s is not a file" % args.html
        sys.exit(1)


    dep_graph = {}
    entry_point = graphtools.build_dependency_graph(dep_graph, args.files)
    dep_list = graphtools.build_dependency_list(dep_graph, entry_point)

    for f in dep_list:
        print os.path.relpath(f, '.')

    












