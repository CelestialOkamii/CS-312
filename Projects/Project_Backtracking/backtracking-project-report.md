# Project Report - Backtracking

Met with Ethan Rushforth for review.

## Baseline

### Design Experience

Met with Michael. Talked about the difference between the greedy and backtracking algorithms. Talked about the 
differences between backtracking and dfs. Discussed how the greedy algorithm is like Dijkstra's in a way.

### Theoretical Analysis - Greedy

#### Time 

```py 
def greedy_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:   # O(n^3) - the outermost for loop takes the longest by far and everything without a comment is pretty much constant time because they are simple alterations
    paths = []
    best_score = math.inf
    for i in range(len(edges)):              # O(n^3) - goes over ~ every node(n) two times per call and is repeated n number of times corresponding to the number of nodes
        path = [i]
        unvisited = list(range(len(edges)))
        unvisited.remove(i)
        score = 0
        prev = i
        next_node = [None, math.inf]
        while unvisited:                     # O(n^2) - repeats n - 1 times(~ n) for all unvisited nodes and each time it repeats it goes over each node(n) in the for loop
            for node in range(len(edges)):   # O(n) - repeats n times
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
```

The nested loops take the most amount of time because they require approximately n number of repetitions in order to cover every node which 
are then repeated three times. Every other operation in this function only requires constant time which means that the nested loops by far
take the most time making the time complexity O(n^3).

#### Space

```py 
def greedy_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:   # O(n^2) - nothing takes up more than n amount of space
    paths = []                               # O(n^2) - initial creation takes up constant space but it is added to up to n times which requires more space per add so it can take up to n amount of space for every addition of a path which happens n times
    best_score = math.inf
    for i in range(len(edges)):           
        path = [i]                           # O(n) - path will get one element added at a time but this will happen n times for a complete path which means that ultimately n amount of space will be needed
        unvisited = list(range(len(edges)))  # O(n) - makes a list n items long which will require n amount of space
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
                    next_node = [node, weight]   # O(1) - although next_node egts changed a lot its size stays the same so no additional space is needed other than the spall amount of space it originally takes up which makes it constant in the amount of space it needs
            if next_node[1] == math.inf:
                break
            score += next_node[1]
            path.append(next_node[0])          # O(n) - as mentioned for path, adding one item takes pretty constant space but because path is added to up to n times it takes up O(n) space
            unvisited.remove(next_node[0])
            prev = next_node[0]
            next_node = [None, math.inf]
        if score == 0 or len(path) != len(edges):
            continue
        score += edges[prev][i]
        if score < best_score:
            best_score = score
            new_path = SolutionStats(path, score, timer.time(), 0, 0, 0, 0, 0)
            paths.append(new_path)             # O(n^2) - paths gets one item of size n added at a time like path, but it can be added to up to n number of times which takes up n amount of additional space
        if timer.time_out():
            return paths
    return paths
```

The graph given as a parameter takes up O(nm) space because it contains n items each of size m, however if this is disregarded, the lists
take up the most space. Some of the lists take up n amount of space because they are added up to n number of times which requires additional space to be added n times.
Others simply have n number of items added all at once requiring the list to be size n. Regardless, nothing takes up more than O(n^2) from the paths list
which gives the function a space complexity of O(n^2).

### Empirical Data - Greedy

| N   | reduction | time (ms) |
|-----|-----------|-----------|
| 5   | 0         | < 0 secs  |
| 10  | 0         | < 0 secs  |
| 15  | 0         | 0.2       |
| 20  | 0         | 0.4       |
| 25  | 0         | 0.7       |
| 30  | 0         | 1.4       |
| 35  | 0         | 0.4       |
| 40  | 0         | 0.9       |
| 45  | 0         | 3.3       |
| 50  | 0         | 6.9       |

### Comparison of Theoretical and Empirical Results - Greedy

- Theoretical order of growth: O(n^3)
- Empirical order of growth (if different from theoretical): Same

![](https://github.com/CelestialOkamii/CS-312/blob/main/Projects/Project_Backtracking/baseline_empirical.png)

## Core

### Design Experience

Discussed everything with Michael. Talked about how to keep track of scores without using a dictionary, recursion, and still keeping it tied to a path.
Discussed how to get rid of incomplete paths and how to add to each path.

### Theoretical Analysis - Backtracking

#### Time 

```py 
def backtracking(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:  # O(n! * n) - for each item that is added to paths (n! number of items) the while loop repeats and in for each repetition the for loop repeats n number of times which requires nm amount of time
    paths = []
    poss_paths = [[0]]
    scores = [0]
    best_score = math.inf
    while poss_paths and not timer.time_out():     # O(n! * n) - repeats n! number of times in order to go through every child of every combination in poss_paths and the for loop in it repeats n number of times corresponding to the number of nodes.
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
        for i in range(len(edges)):               # O(n) - repeats n number of times in order to check each node
            if i in path:
                continue
            if edges[path[-1]][i] != math.inf:
                poss_path = path[:]
                poss_path.append(i)
                poss_paths.append(poss_path)
                new_score = score + edges[path[-1]][i]
                scores.append(new_score)
    return paths
```

Because poss_paths is added to for every possible path from every node to every other node, the while loop will repeat up to n! times. In the while loop, the for loop will then
also repeat n times, once per node. The cost of running the while loop so many times and having parts of its code repeated n number of times by far takes the most time
in this function especially because everything else takes constant time. This means that the time complexity will be O(n! * n).

#### Space

```py 
def backtracking(edges: list[list[float]], timer: Timer) -> list[SolutionStats]: # O(n^2) - the list of lists stored in poss_paths and paths requires n amount of space to be added n times which takes up the most space
    paths = []            # O(n^2) - while this list is initially empty, it will have n amount of n sized items added to it requiring it to expand and take up n amount of space n number of times
    poss_paths = [[0]]    # O(n^2) - initially only one element is added which takes constant space, however this is added to n times which means that n amount of space will eventually be added n number of times
    scores = [0]          # O(n) - initially only one element is added which takes constant space, however this is added to n times which means that n amount of space will eventually be added
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
                poss_path = path[:]  # O(n) - a new list is made which requires n amount of space to fit all of the elemnts of the list it is copying
                poss_path.append(i)
                poss_paths.append(poss_path)
                new_score = score + edges[path[-1]][i]
                scores.append(new_score)  # O(n) - appending one item takes constant time but this happens n times which means that n amount of space will eventually be needed
    return paths
```

There are two variables that will take O(n^2). These variables, poss_paths and paths, store n number of items each of size n
which means that the list will require an increase of n amount of space n times which requires O(n^2) space. The other elements that take
up notable space only take O(n) amount of space to store n number of items in lists while everything else takes a constant amount of space.
This means that the function will have a space complexity of O(n^2).

### Empirical Data - Backtracking

| N   | reduction | time (ms) |
|-----|-----------|-----------|
| 5   | 0         | < 0 sec   |
| 10  | 0         | 12.4      |
| 15  | 0         | 4,164     |
| 20  | 0         | 59,470    |
| 25  | 0         | 58,110    |
| 30  | 0         | 59,370    |
| 35  | 0         | 57,742    |
| 40  | 0         | 38,173    |
| 45  | 0         | 59,026    |
| 50  | 0         | 54,570    |

### Comparison of Theoretical and Empirical Results - Backtracking

- Theoretical order of growth: O(n! * n)
- Empirical order of growth (if different from theoretical): Same

![](https://github.com/CelestialOkamii/CS-312/blob/main/Projects/Project_Backtracking/core_empirical.png)

### Greedy v Backtracking

It seems like backtracking is far more costly than being greedy both in the amount of time and space it takes to run, however backtracking
seems to be more precise as it considers every possibility.

![](https://github.com/CelestialOkamii/CS-312/blob/main/Projects/Project_Backtracking/baseline_vs_core_empirical.png)

### Water Bottle Scenario 

#### Scenario 1

**Algorithm:** 

I'd use BSSF Backtracking because it will be able to quickly find an upper bound which will help me to prune paths when backtracking
much earlier. This will allow me to have the quickness of the greedy algorithm with the thorough nature of backtracking.

#### Scenario 2

**Algorithm:** 

Because of the number of tasks and the time constraint i'd use the greedy algorithm. Using bssf would provide an order with a better overall cost, but
it would still take much longer than greedy and as in this situation, time is much more important than cost it makes sense to
choose the fastest algorithm.

#### Scenario 2

**Algorithm:** 

Because the number of tasks isn't too big and time isn't an issue it makes sense to choose either bssf or backtracking. If I had to choose one, 
I'd use backtracking because my boss wants the best possible solution and while bssf is likely to find a good or even the best
solution, I know that I will be gaunted to find the best solution using backtracking which is what matters most in this scenario.


## Stretch 1

### Design Experience

*Fill me in*

### Demonstrate BSSF Backtracking Works Better than No-BSSF Backtracking 

*Fill me in*

### BSSF Backtracking v Backtracking Complexity Differences

*Fill me in*

### Time v Solution Cost

![Plot]()

*Fill me in*

## Stretch 2

### Design Experience

*Fill me in*

### Cut Tree

*Fill me in*

### Plots 

*Fill me in*

## Project Review

*Fill me in*
