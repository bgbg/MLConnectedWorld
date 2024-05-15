import os
import urllib
from datetime import timedelta
from typing import Union

import networkx as nx
from cachier import cachier
import tempfile


@cachier(stale_after=timedelta(days=100))
def get_graph(dataset_name) -> Union[nx.Graph, list]:
    """Load a graph from SNAP dataset"""
    url_base = "https://snap.stanford.edu/data/"
    data_names = {
        "ca-AstroPh": "ca-AstroPh.txt.gz",
        "ca-CondMat": "ca-CondMat.txt.gz",
        "ca-GrQc": "ca-GrQc.txt.gz",
        "ca-HepPh": "ca-HepPh.txt.gz",
        "ca-HepTh": "ca-HepTh.txt.gz",
        # "cit-Patents": "cit-Patents.txt.gz",
    }
    if dataset_name == "list":
        return list(data_names.keys())
    if dataset_name.endswith(".txt.gz"):
        url = dataset_name
        if not url.startswith("http"):
            url = url_base + url
    else:
        if dataset_name not in data_names:
            msg = (
                f"Dataset {dataset_name} not available. "
                f" Choose from {list(data_names.keys())}, "
            )
            raise ValueError(msg)
        url = url_base + data_names[dataset_name]
    with tempfile.TemporaryDirectory() as tmpdirname:
        fn = os.path.join(tmpdirname, "graph.txt.gz")
        # download the file
        urllib.request.urlretrieve(url, fn)
        # load the graph
        G = nx.read_edgelist(fn, nodetype=int)
    return G


def get_info(G: nx.Graph):
    """Get info about a graph"""
    ret = []
    ret.append(f"Name: {G.name}. Directed: {G.is_directed()}")
    ret.append(f"Number of nodes: {G.number_of_nodes():,d}")
    ret.append(f"Number of edges: {G.number_of_edges():,d}")
    ret.append(f"Average clustering: {nx.average_clustering(G)}")
    if nx.is_connected(G):
        ret.append(
            f"Average shortest path length: {nx.average_shortest_path_length(G)}"
        )
    else:
        ret.append("Graph is not connected")
    return "\n".join(ret)
