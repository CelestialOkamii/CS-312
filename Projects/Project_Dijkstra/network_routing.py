import LinearPriorityQueue
import HeapPriorityQueue


def find_shortest_path_with_heap(
        graph: dict[int, dict[int, float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the heap-based algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """
    pq = HeapPriorityQueue.HeapPQ()
    return run_dijkstras(graph, pq, source, target)


def find_shortest_path_with_linear_pq(
        graph: dict[int, dict[int, float]],
        source: int,
        target: int
) -> tuple[list[int], float]:
    """
    Find the shortest (least-cost) path from `source` to `target` in `graph`
    using the array-based (linear lookup) algorithm.

    Return:
        - the list of nodes (including `source` and `target`)
        - the cost of the path
    """
    pq = LinearPriorityQueue.LinearPQ()
    return run_dijkstras(graph, pq, source, target)


def run_dijkstras(graph, pq, source, target):
    weights = {source: [None, 0]}
    path = []
    pq.insert([source, None, 0])
    while not pq.is_empty():
        min_value = pq.remove_min()
        current_node = min_value[0]
        prev_node = min_value[1]
        weight = min_value[2]
        children = graph[current_node]
        if current_node not in weights:
            weights[current_node] = [prev_node, weight]
        elif prev_node is not None and weights.get(current_node)[1] > weight + weights.get(prev_node)[1]:
            weights[current_node] = [prev_node, weight + weights.get(prev_node)[1]]
        for key in children:
            current_weight = weights.get(current_node)[1]
            if key not in weights or children[key] + current_weight < weights[key][1]:
                if key in weights:
                    weights[key] = children[key] + current_weight
                    continue
                pq.insert((key, current_node, children[key] + current_weight))
    current_node = target
    if target not in weights:
        return [], float('inf')
    while current_node != source:
        path.insert(0, current_node)
        current_node = weights[current_node][0]
    path.insert(0, source)
    return path, weights.get(target)[1]