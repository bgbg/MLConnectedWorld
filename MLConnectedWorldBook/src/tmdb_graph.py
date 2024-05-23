import json
from collections import defaultdict
from datetime import timedelta

import networkx as nx
import numpy as np
import pandas as pd
from cachier import cachier
from yake import yake
from tqdm.auto import tqdm


@cachier(stale_after=timedelta(days=1))
def build_movies_and_keywords_graph(
    df: pd.DataFrame,
    n_grams: int = 2,
    top: int = 10,
) -> nx.Graph:

    kw_extractor = yake.KeywordExtractor(
        lan="en",
        n=n_grams,  # up to n-grams
        dedupLim=0.9,  # two words are considered the same if the similarity is higher than this
        dedupFunc="seqm",  # similarity function. Options are seqm, jaccard, cosine, levenshtein, jaro, jaro_winkler, monge_elkan, keywordset
        windowsSize=1,  # number of words in the window
        top=top,  # number of keywords to extract
        features=None,  # list of features to extract. If None, it uses all the features. Options are: ngram, sif, first, freq
    )
    g_movies_and_keywords = nx.Graph()
    for _, row in tqdm(
        df.iterrows(), total=len(df), desc="Building graph", leave=False
    ):
        movie_title = row["title"]
        overview = row["overview"]
        if not overview:
            continue
        overview = str(overview).lower()
        keywords = kw_extractor.extract_keywords(overview)
        # Originally, keywords are (keyword, score) pairs. The lower the score, the more important the keyword
        # We will convert the scores to weights by taking the log of the inverse of the score
        keywords = [(k[0], np.log10(1 / k[1])) for k in keywords]
        # now, we will build a graph:
        # if the movie is not in the graph, we add a node with the title as the label and the movie_id as the id
        # and MOVIE as the type. We will initialize the `count` attribute to 1
        # if the movie is already in the graph, we increment the `count` attribute
        # for each keyword:
        # - if the keyword is not in the graph, we add a node with the keyword as the label and the keyword as the id
        # and KEYWORD as the type. We will initialize the `count` attribute to 1
        # - if the keyword is already in the graph, we increment the `count` attribute
        # - if the edge between the movie and the keyword exists, we increment the weight of the edge
        # - if the edge does not exist, we add the edge with the weight
        if movie_title not in g_movies_and_keywords:
            g_movies_and_keywords.add_node(
                movie_title, label=movie_title, type="MOVIE", count=1
            )
        else:
            g_movies_and_keywords.nodes[movie_title]["count"] += 1
        for keyword, weight in keywords:
            if keyword not in g_movies_and_keywords:
                g_movies_and_keywords.add_node(
                    keyword, label=keyword, type="KEYWORD", count=1
                )
            else:
                g_movies_and_keywords.nodes[keyword]["count"] += 1
            if g_movies_and_keywords.has_edge(movie_title, keyword):
                g_movies_and_keywords.edges[movie_title, keyword]["weight"] += weight
            else:
                g_movies_and_keywords.add_edge(movie_title, keyword, weight=weight)
    return g_movies_and_keywords


def get_graph_with_credit_info(
    g_movies_and_keywords: nx.Graph,
    df_credits: pd.DataFrame,
    top_n_cast: int = 20,
) -> nx.MultiGraph:

    credit_edges = []
    # Process credits to extract relevant information
    for _, row in tqdm(
        df_credits.iterrows(), total=len(df_credits), desc="Processing credits"
    ):
        cast = json.loads(row.cast)
        for c in cast:
            if c["order"] > top_n_cast:
                continue
            credit_edges.append(
                {
                    "MOVIE": row["title"],
                    "PERSON": c["name"],
                    "type": "PARTICIPATED_IN",
                }
            )
        crew = json.loads(row.crew)
        for c in crew:
            job = c["job"]
            if job not in ["Director", "Producer", "Writer", "Screenplay"]:
                continue
            credit_edges.append(
                {"MOVIE": row["title"], "PERSON": c["name"], "type": "WORKED_ON"}
            )

    df_credit_edges = pd.DataFrame(credit_edges)

    g_multi = nx.MultiGraph()
    for u, v, data in g_movies_and_keywords.edges(data=True):
        g_multi.add_edge(u, v, key="HAS_KEYWORD", **data)

    # Preserve node attributes including type
    for node, data in g_movies_and_keywords.nodes(data=True):
        g_multi.add_node(node, **data)

    # Add the edges to the graph, and add nodes if they don't exist
    for _, row in tqdm(
        df_credit_edges.iterrows(), total=len(df_credit_edges), desc="Adding edges"
    ):
        movie = row["MOVIE"]
        person = row["PERSON"]
        edge_type = row["type"]

        if movie not in g_multi.nodes:
            g_multi.add_node(movie, type="MOVIE")
        if person not in g_multi.nodes:
            g_multi.add_node(person, type="PERSON")

        # Check if the edge already exists with the same type before adding
        if not g_multi.has_edge(movie, person, key=edge_type):
            g_multi.add_edge(movie, person, key=edge_type)

    return g_multi


def remove_isolated_nodes(graph: nx.Graph):
    nodes_to_remove = [n for n in graph.nodes if graph.degree(n) == 0]
    ret = graph.copy()
    ret.remove_nodes_from(nodes_to_remove)
    return ret


def get_largest_connected_component_graph(graph: nx.Graph) -> nx.Graph:
    largest_connected_component = max(nx.connected_components(graph), key=len)
    return graph.subgraph(largest_connected_component).copy()


def cleanup_nodes_by_percentile(
    graph: nx.Graph,
    node_attr: str = "count",
    percentile: float = 1.0,
    node_type: str = None,
):
    if node_type:
        nodes = [n for n, d in graph.nodes(data=True) if d["type"] == node_type]
    else:
        nodes = list(graph.nodes)
    counts = np.array([graph.nodes[n][node_attr] for n in nodes])
    threshold = np.percentile(counts, 100 - percentile)
    nodes_to_remove = [n for n in nodes if graph.nodes[n][node_attr] < threshold]
    ret = graph.copy()
    ret.remove_nodes_from(nodes_to_remove)
    return ret
