import os
import urllib
from datetime import timedelta
from typing import Union

import networkx as nx
import pandas as pd
from cachier import cachier
import tempfile


@cachier(stale_after=timedelta(days=100))
def get_graph(dataset_name) -> Union[nx.Graph, list]:
    """Load a graph from a data collection repository"""

    dir_this = os.path.dirname(os.path.abspath(__file__))
    dir_book = os.path.join(dir_this, "MLConnectedWorldBook")
    dir_data = os.path.join(dir_book, "data")
    assert os.path.exists(dir_data), f"Data directory {dir_data} not found"

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

    dataset_path = None
    for extension in ["", ".csv", ".csv.gz"]:
        curr = os.path.join(dir_data, dataset_name + extension)
        if os.path.exists(curr):
            dataset_path = curr
            break
    if dataset_path is not None:
        # found locally
        df = pd.read_csv(dataset_path)
        assert "src" in df.columns, f"Column 'src' not found in {dataset_path}"
        assert "dst" in df.columns, f"Column 'dst' not found in {dataset_path}"
        edge_attr = [c for c in df.columns if c not in ["src", "dst"]]
        G = nx.from_pandas_edgelist(
            df,
            source="src",
            target="dst",
            edge_attr=edge_attr,
        )
        return G

    url_base = "https://snap.stanford.edu/data/"

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


if __name__ == "__main__":
    n = "corporate_undirected.csv"
    get_graph.clear_cache()
    g = get_graph(n)
    print(get_info(g))
