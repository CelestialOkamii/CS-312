import copy
import math
import random
import heapq
from itertools import count

from tsp_core import Tour, SolutionStats, Timer, score_tour, Solver
from tsp_cuttree import CutTree

PARAMS_FOR_SMART_BRANCH_AND_BOUND_SMART_TEST = {
    "n": 30,
    "euclidean": True,
    "reduction": 0.2,
    "normal": False,
    "seed": 312,
    "timeout" : 20
}

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


def dfs(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
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


def branch_and_bound(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    best_paths = [greedy_tour(edges, timer)[-1]]
    best_tour = best_paths[0].tour
    best_score = best_paths[0].score
    start_matrix, lower = matrix_reducer(edges)
    matrix_length = len(edges)
    poss_matrix = [start_matrix]
    poss_paths = [[0]]
    scores = [0]
    while poss_paths and not timer.time_out():
        path = poss_paths.pop()
        matrix = poss_matrix.pop()
        score = scores.pop()
        if score > best_score:
            continue
        if len(path) == matrix_length:
            if matrix[path[-1]][0] != math.inf:
                best_score = score + matrix[path[-1]][0]
                best_tour = path.copy()
                good_path = SolutionStats(best_tour, score + matrix[path[-1]][0], timer.time(), 0, 0, 0, 0, 0)
                best_paths.append(good_path)
            continue
        for i in range(matrix_length):
            if i in path:
                continue
            if matrix[path[-1]][i] != math.inf:
                altered_matrix = altered_route(matrix, path[-1], i)
                reduced_matrix, lower_bound = matrix_reducer(altered_matrix)
                new_score = score + matrix[path[-1]][i] + lower_bound
                if new_score < best_score:
                    poss_paths.append(path + [i])
                    scores.append(new_score)
                    poss_matrix.append(reduced_matrix)
    return best_paths


def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    best_paths = [greedy_tour(edges, timer)[-1]]
    best_tour = best_paths[0].tour
    best_score = best_paths[0].score
    cut_paths = CutTree(len(edges))
    start_matrix, lower = matrix_reducer(edges)
    queue_size = 1
    partial_paths = 0
    paths_taken = 1
    counter = count()
    matrix_length = len(edges)
    pos_paths = []
    heapq.heappush(pos_paths, (0, next(counter), ([0], start_matrix, {0})))
    while pos_paths and not timer.time_out():
        partial_paths += 1
        score, curr_count, (path, matrix, visited) = heapq.heappop(pos_paths)
        prev_node = path[-1]
        if score >= best_score:
            cut_paths.cut(path)
            continue
        if len(path) == matrix_length:
            paths_taken += 1
            if score < best_score and edges[path[-1]][0] != math.inf:
                best_tour = path.copy()
                best_score = score
                new_path = SolutionStats(best_tour, score, timer.time(), queue_size, partial_paths,
                                         cut_paths.n_leaves_cut(), paths_taken, cut_paths.fraction_leaves_covered())
                best_paths.append(new_path)
            continue
        for node in range(matrix_length):
            if node in visited or matrix[prev_node][node] == math.inf:
                continue
            altered_matrix = altered_route(matrix, prev_node, node)
            reduced_matrix, lower_bound = matrix_reducer(altered_matrix)
            lower_bound += score + matrix[prev_node][node]
            if lower_bound < best_score:
                new_visited = visited.copy()
                new_visited.add(node)
                heapq.heappush(pos_paths,
                               (lower_bound, next(counter), (path + [node], reduced_matrix, new_visited)))
        if len(pos_paths) > queue_size:
            queue_size = len(pos_paths)
    return best_paths


def altered_route(matrix, prev_node, curr_node):
    matrix_length = len(matrix)
    altered_matrix = []
    for i in range(matrix_length):
        row = []
        for j in range(matrix_length):
            row.append(matrix[i][j])
        altered_matrix.append(row)
    for k in range(matrix_length):
        if k == prev_node:
            altered_matrix[k] = [math.inf] * len(matrix[k])
        altered_matrix[k][curr_node] = math.inf
    altered_matrix[curr_node][prev_node] = math.inf
    return altered_matrix


def matrix_reducer(matrix):
    rows = len(matrix)
    lower_bound = 0
    for row in range(rows):
        min_value = min(matrix[row])
        if min_value > 0 and min_value < math.inf:
            lower_bound += min_value
            for column in range(rows):
                matrix[row][column] -= min_value
    for k in range(rows):
        min_value = math.inf
        for i in range(rows):
            if matrix[i][k] < min_value:
                min_value = matrix[i][k]
        if min_value > 0 and min_value < math.inf:
            lower_bound += min_value
            for j in range(rows):
                matrix[j][k] -= min_value
    return matrix, lower_bound