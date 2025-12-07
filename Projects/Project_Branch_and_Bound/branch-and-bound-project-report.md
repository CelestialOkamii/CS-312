# Project Report - Branch and Bound

## Baseline

### Design Experience

*Discussed the things below with Michael:*

- To reduce a matrix you go row by row subtracting the smallest value, which can include 0, from the rest of the rows values
- Add the minimum values from each row and add them together
- Go back over the matrix where you already edited and go over each column subtracting the minimum value in each column from the rest of the values, 0 can be the smallest number
- Add the minimums from the rows with the minimums from the column
- You now have a reduced matrix and a lower bound

- I will use a list of lists. The pros are that it is easy to use and iterate over, takes constant time to access, is easy to copy, and can store anything from ints to inf. The cons are that it is expensive to copy a matrix this way and if you don't make a copy of the matrix, the original along with "copy" will be changed.
- I don't think i've really considered cases where an entire row or column equals infinity, if a matrix has negative numbers, if the matrix is empty, and if a matrix's number of rows doesn't equal its number of columns.
 

### Theoretical Analysis - Reduced Cost Matrix

#### Time 

```py 
def altered_route(matrix, prev_node, curr_node):  # O(n^2) - the nested for loop takes up the most space as it goes through every row (m) and, for every row it goes through each column (n)
    matrix_length = len(matrix)
    altered_matrix = []
    for i in range(matrix_length):      # O(n^2) - iterates n times and each time it iterates it repeats what's in the second for loop n number of times
        row = []
        for j in range(matrix_length):  # O(n) - repeats n times
            row.append(matrix[i][j])
        altered_matrix.append(row)
    for k in range(matrix_length):      # ~O(n) - repeats n times nad while it also has an element that takes O(n) time, it only happens once which should keep it at around O(n) time
        if k == prev_node:
            altered_matrix[k] = [math.inf] * len(matrix[k]) # O(n) - basically appends to a list n times. Appending takes constant time but because it is repeated n times it takes n amount of time
        altered_matrix[k][curr_node] = math.inf
    altered_matrix[curr_node][prev_node] = math.inf
    return altered_matrix


def matrix_reducer(matrix):  # O(n^2) - the 2 outermost for loops repeat n^2 times which makes the function take O(n^2) amount of time
    rows = len(matrix)
    lower_bound = 0
    for row in range(rows):             # O(n^2) - repeats n times and each time it repeats it repeats another n times
        min_value = min(matrix[row])
        if min_value > 0 and min_value < math.inf:
            lower_bound += min_value
            for column in range(rows):  # O(n) - repeats n times
                matrix[row][column] -= min_value
    for k in range(rows):          # O(n^2) - repeats n times and each time it repeats, it repeats another n times
        min_value = math.inf
        for i in range(rows):      # O(n) - repeats n times
            if matrix[i][k] < min_value:
                min_value = matrix[i][k]
        if min_value > 0 and min_value < math.inf:
            lower_bound += min_value
            for j in range(rows):  # O(n) - repeats contents n times
                matrix[j][k] -= min_value
    return matrix, lower_bound
```

Both altered_route() and matrix_reducer() take O(n^2) time which means that the overall algorithm for reducing a matrix takes O(n^2) time. This is because 
both functions contain elements that go over every row which takes n amount of time and for every row they go over they also go over every column (n).
Because of this, even though pretty much everything, except for one line in altered_route() that happens once, takes constant time, but the actions are then repeated
n^2 number of times giving a big O of O(n^2).

#### Space

```py 
def altered_route(matrix, prev_node, curr_node): # O(n^2) - if we ignore the matrix which is a parameter, the amount of space required is still O(n^2) because of a new list n items long where each item hold n number of items is created in the first for loop
    matrix_length = len(matrix)
    altered_matrix = []
    for i in range(matrix_length):      # O(n^2) - while adding one n size item to a list only takes n amount of space, this happens once per loop which means that in total n amount of space will be added n number of times meaning that n^2 amount of space will be needed to store this list of lists
        row = []
        for j in range(matrix_length):  # O(n) - adding an item to a list takes constant time, but because this is repeated n times it is actually like adding n items to a list which requires n amount of space
            row.append(matrix[i][j])    # O(1) - adding one item to a list takes constant time
        altered_matrix.append(row)      # O(n) - adding an item of size n to a list takes n amount of space
    for k in range(matrix_length):
        if k == prev_node:
            altered_matrix[k] = [math.inf] * len(matrix[k]) # O(n) - n amount of items are added to the list which means that n amount of space will be needed
        altered_matrix[k][curr_node] = math.inf
    altered_matrix[curr_node][prev_node] = math.inf
    return altered_matrix


def matrix_reducer(matrix): # O(1) - the passed in matrix takes O(n^2) amount of space, but if this is ignored, no new space it needed or added in this function
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
```

The most amount of space taken is O(n^2) which is taken by altered_route(). This much space is needed because a new list of n number of items where each item takes n amount of space is created.
This that each item will take n amount of space and because there are n number of items being added to a list n^2 amount of space is needed.

## Core

### Design Experience

*Discussed the things below with Michael*

- To branch and bound you find a lower or upper bound through whatever method applies to what you're doing
- After you have your bound you will start to explore different decision paths and at each step along the path pursue any path that is better than whichever bounds your problem has
- The lower bound that I get from my reduced cost matrix will be used to discard paths whose lower bound is greater than the upper bound that the greedy algorithm gives.
- I will use a list to store the matrices. The pros of this are that it is easy to use, takes constant time to access and is easy to use in loops. The cons are that copying a matrix is expensive, because so many lists, most of which are only pointers, it takes more overhead work to use, and the matrices can't really be changed without using loops.
- To estimate time complexity I will figure out the cost of one branch and multiply it by the estimated number of branches there could be with the pruning I have.
- To estimate my branching factor I will multiply the difference of the number of nodes and the number of nodes already visited by 0.5 because about half of the total number of paths should get pruned

### Theoretical Analysis - Branch and Bound TSP

#### Time 

```py 
def branch_and_bound(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:  # O((n/2)^n * n^3) - The while loop takes the most time by far which makes the functions time O(n! * n^3)
    best_paths = [greedy_tour(edges, timer)[-1]]   # O(n^3) - the greedy algorithm takes O(n^3) space
    best_tour = best_paths[0].tour
    best_score = best_paths[0].score
    start_matrix, lower = matrix_reducer(edges)
    matrix_length = len(edges)
    poss_matrix = [start_matrix]
    poss_paths = [[0]]
    scores = [0]
    while poss_paths and not timer.time_out(): # O((n/2)^n * n^3) - in the worst case scenario about n/2 nodes should get added to the stack for each explored partial path ((n/2)^n) and for each of those repetitions O(n^3) time is taken for the for loop
        path = poss_paths.pop()
        matrix = poss_matrix.pop()
        score = scores.pop()
        if score > best_score:
            continue
        if len(path) == matrix_length:
            if matrix[path[-1]][0] != math.inf:
                best_score = score + matrix[path[-1]][0]
                best_tour = path.copy()  # O(n) - basically append to a new list n times which takes n amount of time
                good_path = SolutionStats(best_tour, score + matrix[path[-1]][0], timer.time(), 0, 0, 0, 0, 0)
                best_paths.append(good_path)
            continue
        for i in range(matrix_length):   # O(n^3) - repeats n times and each time it repeats costs O(n^2) because of the calls to altered_route() and matrix_reducer()
            if i in path:
                continue
            if matrix[path[-1]][i] != math.inf:
                altered_matrix = altered_route(matrix, path[-1], i)  # O(n^2) - altered_route() takes O(n^2) time
                reduced_matrix, lower_bound = matrix_reducer(altered_matrix) # O(n^2) - matrix_reducer() takes O(n^2) time
                new_score = score + matrix[path[-1]][i] + lower_bound
                if new_score < best_score:
                    poss_paths.append(path + [i])
                    scores.append(new_score)
                    poss_matrix.append(reduced_matrix)
    return best_paths


def altered_route(matrix, prev_node, curr_node):  # O(n^2) - the nested for loop takes up the most space as it goes through every row (m) and, for every row it goes through each column (n)
    matrix_length = len(matrix)
    altered_matrix = []
    for i in range(matrix_length):      # O(n^2) - iterates n times and each time it iterates it repeats what's in the second for loop n number of times
        row = []
        for j in range(matrix_length):  # O(n) - repeats n times
            row.append(matrix[i][j])
        altered_matrix.append(row)
    for k in range(matrix_length):      # ~O(n) - repeats n times nad while it also has an element that takes O(n) time, it only happens once which should keep it at around O(n) time
        if k == prev_node:
            altered_matrix[k] = [math.inf] * len(matrix[k]) # O(n) - basically appends to a list n times. Appending takes constant time but because it is repeated n times it takes n amount of time
        altered_matrix[k][curr_node] = math.inf
    altered_matrix[curr_node][prev_node] = math.inf
    return altered_matrix


def matrix_reducer(matrix):  # O(n^2) - the 2 outermost for loops repeat n^2 times which makes the function take O(n^2) amount of time
    rows = len(matrix)
    lower_bound = 0
    for row in range(rows):             # O(n^2) - repeats n times and each time it repeats it repeats another n times
        min_value = min(matrix[row])
        if min_value > 0 and min_value < math.inf:
            lower_bound += min_value
            for column in range(rows):  # O(n) - repeats n times
                matrix[row][column] -= min_value
    for k in range(rows):          # O(n^2) - repeats n times and each time it repeats, it repeats another n times
        min_value = math.inf
        for i in range(rows):      # O(n) - repeats n times
            if matrix[i][k] < min_value:
                min_value = matrix[i][k]
        if min_value > 0 and min_value < math.inf:
            lower_bound += min_value
            for j in range(rows):  # O(n) - repeats contents n times
                matrix[j][k] -= min_value
    return matrix, lower_bound
```

The branch and bound algorithm takes the most time because it visits about n/2 branches for each partial path and for each partial path additionally takes O(n^3) time to alter and reduce the matrix as well as copy the partial path taken.
gives us a cost of O((n/2)^n * n^3).

#### Space

```py 
def branch_and_bound(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:  # O((n/2)^n * n^2) - poss_matrix takes the most space
    best_paths = [greedy_tour(edges, timer)[-1]]   # O((n/2)^n * n) - worst case scenario (n/2)^n items will fit the criteria and the size needed for each item will be O(n) since n number of items are stored in one SolutionStats
    best_tour = best_paths[0].tour
    best_score = best_paths[0].score
    start_matrix, lower = matrix_reducer(edges)  # O(1) -  since this just alters the edges matrix no additional space is taken
    matrix_length = len(edges)
    poss_matrix = [start_matrix] # O((n/2)^n * n^2) - each matrix takes up O(n^2) space and there can be up to ~ (n/2)^n matrices added if every path that isn't pruned produces a valid path
    poss_paths = [[0]]           # O((n/2)^n * n) - each path takes up n amount of space and if every path that isn't pruned is added then n amount of space will be added ~ (n/2)^2 times which means that it would need O((n/2)^2 * n) space
    scores = [0]                 # O((n/2)^2) - each item takes up constant space but since up to (n/2)^n items can be added it can take up to O((n/2)^n) space
    while poss_paths and not timer.time_out():
        path = poss_paths.pop()
        matrix = poss_matrix.pop()
        score = scores.pop()
        if score > best_score:
            continue
        if len(path) == matrix_length:
            if matrix[path[-1]][0] != math.inf:
                best_score = score + matrix[path[-1]][0]
                best_tour = path.copy()   # O(n) - makes a list that takes up n amount of space
                good_path = SolutionStats(best_tour, score + matrix[path[-1]][0], timer.time(), 0, 0, 0, 0, 0)  # O(n) - basically creates a data structure that will store n items which means it will need n amount of space
                best_paths.append(good_path) # O(n) - each path takes n amount of space so appending one item requires an additional n amount of space in the list it is stored in
            continue
        for i in range(matrix_length):
            if i in path:
                continue
            if matrix[path[-1]][i] != math.inf:
                altered_matrix = altered_route(matrix, path[-1], i)  # O(n^2) - makes a new matrix which takes up O(n^2) space
                reduced_matrix, lower_bound = matrix_reducer(altered_matrix)
                new_score = score + matrix[path[-1]][i] + lower_bound
                if new_score < best_score:
                    poss_paths.append(path + [i])
                    scores.append(new_score)
                    poss_matrix.append(reduced_matrix)
    return best_paths


def altered_route(matrix, prev_node, curr_node): # O(n^2) - if we ignore the matrix which is a parameter, the amount of space required is still O(n^2) because of a new list n items long where each item hold n number of items is created in the first for loop
    matrix_length = len(matrix)
    altered_matrix = []
    for i in range(matrix_length):      # O(n^2) - while adding one n size item to a list only takes n amount of space, this happens once per loop which means that in total n amount of space will be added n number of times meaning that n^2 amount of space will be needed to store this list of lists
        row = []
        for j in range(matrix_length):  # O(n) - adding an item to a list takes constant time, but because this is repeated n times it is actually like adding n items to a list which requires n amount of space
            row.append(matrix[i][j])    # O(1) - adding one item to a list takes constant time
        altered_matrix.append(row)      # O(n) - adding an item of size n to a list takes n amount of space
    for k in range(matrix_length):
        if k == prev_node:
            altered_matrix[k] = [math.inf] * len(matrix[k]) # O(n) - n amount of items are added to the list which means that n amount of space will be needed
        altered_matrix[k][curr_node] = math.inf
    altered_matrix[curr_node][prev_node] = math.inf
    return altered_matrix


def matrix_reducer(matrix): # O(1) - the passed in matrix takes O(n^2) amount of space, but if this is ignored, no new space it needed or added in this function
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
```

Overall branch_and_bound() takes the most space by far because its lists can have items of up to size n^2 added up to (n/2)^n times.
This gives the algorithm an overall space complexity of O((n/2)^n * n^2).

### Empirical Data

| N  | Seed | Solution Score | time (s) |
|----|------|----------------|----------|
| 6  | 306  | 2.163          | 0.0001   |
| 9  | 306  | 1.743          | 0.0164   |
| 12 | 306  | 2.212          | 1.5491   |
| 15 | 306  | 2.743          | 27.3992  |

### Comparison of Theoretical and Empirical Results

- Empirical order of growth: 13
- Measured constant of proportionality: 7.7 * 10^-15

![img](core_emperical_graph.png)

Yes, it fits

## Stretch 1 

### Design Experience

*Fill me in*

### Search Space Over Time

![Plot demonstrating search space explored over time]()

*Fill me in*

## Stretch 2

### Design Experience

*Fill me in*

### Selected PQ Key

*Fill me in*

### Branch and Bound versus Smart Branch and Bound

*Fill me in*

## Project Report 

*Fill me in*

