import os, re, sys

def build_dependency_graph(graph, file_list):
    """
    Creates the dependecy graph.
    If graph has a cycle in it, or it's not a single component exits program
    with an error message.

    @param {dict} graph
                is an unpopulated dictionary that will hold
                the depedency graph (neighbour lists style)
    @param {list} file_list
                is the javascript files to form the dependency graph from
                
    @return {str}
                The graph's entry point
    """
    # populate empty_graph
    for f in file_list:
        dep_graph_builder(graph, f)

    singlularity = check_singularity(graph)
    if not singlularity:
        print "error: cannot resolve entry point, more than one possibility." + \
                "\nMaybe more than one script?"
        sys.exit(1)

    has_cycle = find_dep_cycle(graph)
    if has_cycle:
        print "error: dependencies form a cycle, cannot resolve."
        sys.exit(1)

    # find entry point
    entry_point = find_entry_point(graph)

    return entry_point

def build_dependency_list(dep_graph, entry_point):
    dep_list = []

    build_dep_list_DFS(dep_graph, dep_list, entry_point)

    return dep_list

def build_dep_list_DFS(dep_graph, dep_list, node):
    for n in dep_graph[node]:
        if n not in dep_list:
            build_dep_list_DFS(dep_graph, dep_list, n)

    dep_list.append(node)


def check_singularity(graph):
    """
    Checks that graph is a single connected component

    @param {dict} graph
                the dependency graph

    @return {boolean} 
                True if graph is single connected component, False
                otherwise
    """

    nodes = graph.keys()
    count = 0

    for node1 in nodes:
        increment = True
        for node2 in nodes:
            if node1 in graph[node2]:
                increment = False
                break

        if increment:
            count += 1
        if count > 1:
            return False

    return True


def dep_graph_builder(graph, file_path):
    ''' 
    populates the graph
    @param {str} file_path 
                a path to an existing javascript file

    @return {boolean} 
                True if file_path added to graph, False otherwise
    '''

    real_path = os.path.realpath(file_path)

    if real_path in graph.keys():
        return

    graph[real_path] = []

    file = open(real_path, 'r')

    # scan only first 200 lines
    # require statements are not very reasonable out of the head of
    # the file anyway
    for _ in range(0, 200):
        line = file.readline()
        if len(line) == 0:
            break

        m = re.match(r'//\s*#require\s+([a-zA-Z_0-9.]+)', line)

        if m != None:
            dep = m.group(1)
            if not os.path.isfile(dep):
                nice_path = os.path.relpath(real_path, '.')
                print "error: not such file %s in script %s" % (dep, nice_path)
                sys.exit(1)

            if os.path.splitext(dep)[1] != '.js':
                nice_path = os.path.relpath(real_path, '.')
                print "error: file %s in script %s is not a javascript file" % (dep, nice_path)
                sys.exit(1)

            dep_real_path = os.path.realpath(dep)

            graph[real_path].append(dep_real_path)
            dep_graph_builder(graph, dep_real_path)

def find_dep_cycle(graph):
    """
    Finds a cycle in a directed graph.
    Uses 'Tarjan's algorithm'

    @param {dict} graph
                the graph

    @return {boolean}
                True if graph has cycle, False if not.
    """

    # int value in a list to pass by reference
    index = [0]
    indices = {}
    lowvals = {}
    s = []

    for node in graph:
        if node not in indices.keys():
            if tarjan_DFS(graph, index, indices, lowvals, s, node):
                return True

    return False

def tarjan_DFS(graph, index, indices, lowvals, s, node):
    """
    DFS traversal for tarjan's algorithm.

    @param {dict} graph
    @param {list} index
                a one integer list
    @param {dict} indices
    @param {dict} lowvals
    @param {list} s
    @param {str} node
                current inspected node

    @return {boolean}
                True if found a SCC with more than one node, that is a cycle.
                False otherwise.
    """
    indices[node] = index[0]
    lowvals[node] = index[0]
    index[0] += 1
    s.append(node)
    for n in graph[node]:
        if n not in indices.keys():
            tarjan_DFS(graph, index, indices, lowvals, s, n)
            lowvals[node] = min(lowvals[node], lowvals[n])
        elif n in s:
            lowvals[node] = min(lowvals[node], indices[n])

    if lowvals[node] == indices[node]:
        count = 1
        while node != (s.pop()):
            count += 1

        if count > 1:
            return True

    return False

def find_entry_point(graph):
    """
    Finds an entry point for the graph. That is a starting point to resolve
    dependecies from. Graph should be a single component with no cycles, a tree
    that is.

    @param {dict} graph

    @return {str} 
                the entry point
    """
    visited = []
    nodes = graph.keys()

    for n in nodes:
        if n not in visited:
            last = n
            entry_point_DFS(graph, visited, n)


    return last

def entry_point_DFS(graph, visited, node):
    """
    DFS traversal for find_entry_point algorithm

    @param {dict} graph
    @param {list} visited
    @param {str} node
    """

    visited.append(node)
    for n in graph[node]:
        if n in visited:
            continue
        entry_point_DFS(graph, visited, n)
