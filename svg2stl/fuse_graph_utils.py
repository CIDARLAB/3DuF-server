import networkx as nx
import pathlib


def find_fuse_end(G, startnode):

    # Check if start node is not in the graph, return same point
    if startnode not in list(G.nodes):
        return startnode

    # Check if start node has 0 out
    if len(G.out_edges(startnode)) == 0:
        return startnode

    # Traverse till the end of the path
    # Returns the last node in the path
    bfs_nodes = list(nx.dfs_tree(G, startnode).nodes())
    # Return the first end node that has 0 out edges
    for node in bfs_nodes:
        if G.out_degree(node) == 0:
            return node


def find_global_fuse_ends(G):
    # Find the global fuse ends
    fuse_ends = []
    for node in list(G.nodes):
        if len(G.out_edges(node)) == 0:
            fuse_ends.append(node)
    return fuse_ends


def printgraph(G, filename: str) -> None:
    tt = filename + ".dot"
    print("output:", str(tt))
    nx.nx_agraph.to_agraph(G).write(tt)

    # os.system(
    #     "dot -Tpdf {} -o {}.pdf".format(
    #         str(tt.absolute()), pathlib.Path(parameters.OUTPUT_DIR).joinpath(tt.stem)
    #     )
    # )
