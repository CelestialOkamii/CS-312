import random
import sys
from time import time

GRAPH = dict[str, list[str]]
sys.setrecursionlimit(10000)


def prepost(graph : GRAPH) -> list[dict[str, list[int]]]:
    """
    Return a list of DFS trees.
    Each tree is a dict mapping each node label to a list of [pre, post] order numbers.
    The graph should be searched in order of the keys in the dictionary.
    """
    keys = list(graph.keys())
    dfs_forest = list()
    current_tree = {}
    trees = {}
    count = 1
    if not isinstance(graph.get(keys[0]), list):
        for item in keys:
            graph[item] = list(graph.get(item))
    for key in keys:
        if not key in trees:
            current_tree, count = dfs(graph, key, current_tree, count, trees)
            dfs_forest.append(current_tree)
            count += 1
            trees = trees | current_tree
            current_tree = {}
    return dfs_forest


def dfs(graph, node, current_tree, count, trees):
    current_tree[node] = [count]
    for item in graph[node]:
        if not item in current_tree and not item in trees:
            current_tree, count = dfs(graph, item, current_tree, count + 1, trees)
        elif item in trees or not item == graph[node][-1]:
            continue
        else:
            current_tree[node].append(count + 1)
            return current_tree, count + 1
    current_tree[node].append(count + 1)
    return current_tree, count + 1


def find_sccs(graph: GRAPH) -> list[set[str]]:
    """
    Return a list of the strongly connected components in the graph.
    The list should be returned in order of sink-to-source
    """
    return []


def classify_edges(graph: GRAPH, trees: list[dict[str, list[int]]]) -> dict[str, set[tuple[str, str]]]:
    """
    Return a dictionary containing sets of each class of edges
    """
    classification = {
        'tree/forward': set(),
        'back': set(),
        'cross': set()
    }

    return classification