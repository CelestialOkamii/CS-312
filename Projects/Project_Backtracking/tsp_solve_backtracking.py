import math
import random

from utils import Tour, SolutionStats, Timer, score_tour, Solver
from cuttree import CutTree


def random_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    while True:
        if timer.time_out():
            return stats

        tour = random.sample(list(range(len(edges))), len(edges))
        n_nodes_expanded += 1

        cost = score_tour(tour, edges)
        if math.isinf(cost):
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        if stats and cost > stats[-1].score:
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        stats.append(SolutionStats(
            tour=tour,
            score=cost,
            time=timer.time(),
            max_queue_size=1,
            n_nodes_expanded=n_nodes_expanded,
            n_nodes_pruned=n_nodes_pruned,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        ))

    if not stats:
        return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]


def greedy_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    paths = []
    best_score = math.inf
    for i in range(len(edges)):
        path = [i]
        unvisited = list(range(len(edges)))
        unvisited.remove(i)
        score = 0
        prev = i
        next_node = [None, math.inf]
        while unvisited:
            for node in range(len(edges)):
                if not node in unvisited:
                    continue
                weight = edges[prev][node]
                if weight < next_node[1]:
                    next_node = [node, weight]
            if next_node[1] == math.inf:
                break
            score += next_node[1]
            path.append(next_node[0])
            unvisited.remove(next_node[0])
            prev = next_node[0]
            next_node = [None, math.inf]
        if score == 0 or len(path) != len(edges):
            continue
        score += edges[prev][i]
        if score < best_score:
            best_score = score
            new_path = SolutionStats(path, score, timer.time(), 0, 0, 0, 0, 0)
            paths.append(new_path)
        if timer.time_out():
            return paths
    return paths



def backtracking(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    paths = []
    poss_paths = [[0]]
    scores = [0]
    best_score = math.inf
    while poss_paths and not timer.time_out():
        path = poss_paths.pop()
        score = scores.pop()
        if score > best_score:
            continue
        if len(path) == len(edges):
            if edges[path[-1]][0] != math.inf and score + edges[path[-1]][0] < best_score:
                best_score = score + edges[path[-1]][0]
                good_path = SolutionStats(path, score + edges[path[-1]][0], timer.time(), 0, 0, 0, 0, 0)
                paths.append(good_path)
            continue
        for i in range(len(edges)):
            if i in path:
                continue
            if edges[path[-1]][i] != math.inf:
                poss_path = path[:]
                poss_path.append(i)
                poss_paths.append(poss_path)
                new_score = score + edges[path[-1]][i]
                scores.append(new_score)
    return paths


def backtracking_bssf(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    return []