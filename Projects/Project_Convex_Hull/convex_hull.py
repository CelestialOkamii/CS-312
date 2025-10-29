# Uncomment this line to import some functions that can help
# you debug your algorithm
from plotting import draw_line, draw_hull, circle_point
import math


def compute_hull_dvcq(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    if len(points) <= 3:
        if len(points) == 3:
            one, two, three = points
            if above_or_below(one, two, three) < 0:
                points = [one, three, two]
        return points
    sorted_points = sorted(points)
    right_points = sorted_points[math.ceil(len(points)/2):]
    left_points = sorted_points[0:math.ceil(len(points)/2)]
    left_hull = compute_hull_dvcq(left_points)
    right_hull = compute_hull_dvcq(right_points)
    merged_hulls = merge_hulls(left_hull, right_hull)
    return merged_hulls



def compute_hull_other(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Return the subset of provided points that define the convex hull"""
    return []


def merge_hulls(left_hull, right_hull):
    upper_tangent = find_upper_tangent(left_hull, right_hull)
    lower_tangent = find_lower_tangent(left_hull, right_hull)
    merged_hull = find_edges(upper_tangent[0], lower_tangent[0], left_hull) + find_edges(lower_tangent[1], upper_tangent[1], right_hull)
    return reorder(merged_hull)


def find_upper_tangent(L, R):
    left_idx = 0
    for i in range(1, len(L)):
        if L[i][0] > L[left_idx][0]:
            left_idx = i
    right_idx = 0
    for i in range(1, len(R)):
        if R[i][0] < R[right_idx][0]:
            right_idx = i
    done = False
    while not done:
        done = True
        while above_or_below(R[right_idx], L[left_idx], L[(left_idx - 1) % len(L)]) > 0:
            left_idx = (left_idx - 1) % len(L)
            done = False
        while above_or_below(L[left_idx], R[right_idx], R[(right_idx + 1) % len(R)]) < 0:
            right_idx = (right_idx + 1) % len(R)
            done = False
    return left_idx, right_idx


def find_lower_tangent(L, R):
    left_idx = 0
    for i in range(1, len(L)):
        if L[i][0] > L[left_idx][0]:
            left_idx = i
    right_idx = 0
    for i in range(1, len(R)):
        if R[i][0] < R[right_idx][0]:
            right_idx = i
    done = False
    while not done:
        done = True
        while above_or_below(R[right_idx], L[left_idx], L[(left_idx + 1) % len(L)]) < 0:
            left_idx = (left_idx + 1) % len(L)
            done = False
        while above_or_below(L[left_idx], R[right_idx], R[(right_idx - 1) % len(R)]) > 0:
            right_idx = (right_idx - 1) % len(R)
            done = False
    return left_idx, right_idx


def find_edges(idx, bound, hull):
    edges = []
    length = len(hull)
    while True:
        edges.append(hull[idx])
        if idx == bound:
            break
        idx = (idx + 1)%length
    return edges


def above_or_below(left, right, r):
    x1, y1 = left
    x2, y2 = right
    x3, y3 = r
    return (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)


def reorder(hull):
    area = 0
    length = len(hull)
    if length <= 2:
        return hull
    for idx in range(length):
        x1, y1 = hull[idx]
        x2, y2 = hull[(idx + 1)%length]
        area += (x2 - x1)*(y2 + y1)
    if area < 0:
        hull.reverse()
    return hull