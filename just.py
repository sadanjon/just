#! /usr/bin/python

import argparse, os, sys, graphtools

def create_args_parser():
    parser = argparse.ArgumentParser(description="Compile javascript files.")

    parser.add_argument('files', nargs='+', type=str, help='files to process.')
    parser.add_argument('--html', type=str, help='the web page.')
    parser.add_argument('--output-mode', type=str, required=True,
            choices=['tags', 'minified', 'list'], 
            help= """
            'tags' means that script tags are produced on the html file.
            'compiled' means that one script file is produced that is then
            put in a script tag in the html file.""")
    parser.add_argument('--output-file', type=str)
    parser.add_argument('--minifier', type=str, default='closurec', 
            help='the minifier to use')

    return parser

if __name__ == "__main__":
    parser = create_args_parser()
    args = parser.parse_args()

    # get script's working directory
    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    # get script's minifiers directory
    minifiers_dir = os.path.join(script_dir, 'minifiers')

    # confirm list of files is valid
    for file in args.files:
        if not os.path.isfile(file):
            print "error: %s is not a file" % file
            sys.exit(1)

        if os.path.splitext(file)[1] != '.js':
            print "error: all files must be javascript files"
            sys.exit(1)

    # build dependency list
    dep_graph = {}
    entry_points = graphtools.build_dependency_graph(dep_graph, args.files)
    dep_list = graphtools.build_dependency_list(dep_graph, entry_points)

    # if list
    if args.output_mode == 'list':
        if args.output_file != None:
            out = open(args.output_file, 'w')
            for f in dep_list:
                out.write(os.path.relpath(f, '.') + '\n')
            out.close()
        else:
            for f in dep_list:
                sys.stdout.write(os.path.relpath(f, '.') + '\n')
    # if html
    elif args.html != None:
        if not os.path.isfile(args.html):
            print "error: %s is not a file" % args.html
            sys.exit(1)
        if args.output_mode == 'tags':
            pass
        elif args.output_mode == 'minified':
            pass
    # if not a list and no html specified
    else:
        if args.output_mode == 'tags':
            if args.output_file != None:
                out = open(args.output_file, 'w')
                for f in dep_list:
                    out.write("<script type='text/javascript' src='%s'></script>\n" % \
                            os.path.relpath(f, '.'))
                out.close()
            else:
                for f in dep_list:
                    sys.stdout("<script type='text/javascript' src='%s'></script>" % \
                            os.path.relpath(f, '.'))
        elif args.output_mode == 'minified':
            if os.path.isfile(os.path.join(minifiers_dir, args.minifier + '.py')):
                exec("from minifiers.%s import minify" % args.minifier)
                minify()


    if os.path.isfile(os.path.join(minifiers_dir, args.minifier + '.py')):
        __import__('minifiers.' + args.minifier)
    else:
        print "error: no such minifier %s" % args.minifier
        sys.exit(1)


