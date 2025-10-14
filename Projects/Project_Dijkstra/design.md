# Baseline

## How Dijkstra's Algorithm Works

* You start at the chosen node and mark that it has been visited, mark down any nodes that you can get to immediately 
from there and mark down the cost of getting to them, and go to the connecting node with the smallest edge weight.
* At that node you mark that it has been visited, the node that got you there, and then mark down any connecting nodes and the edge weight to get there 
plus the weight it took to get to this node.
* If you can get to a node that has already been marked down and the weight to get from this node to it is less than its 
previous weight change the weight to the new weight and change its previous node to this node.
* You repeat these steps until every node has been visited.
* At this point you can start with any node and find the shortest path to the starting node by retracing which node was marked as its
contributing node until the contributing node is the start node.

## Linear Priority Queue

* My linear priority queue will use a map with nodes as the key and
previous nodes and the weight to get to that node in a list as the value.

### To insert

* use bisect.insort(list, item) to add weight to list
* add new key pair to dict with the current node as the key and a list consisting of the previous node and the weight as the value

### To delete min

* I will have to go through each node in my map to see which has the smallest weight.

### To decrease a key

* To decrease the weight to get to a node I would check to see what the weight to get from my current node to that node is and
look in my map to see if the weight from this node to that node is smaller than the weight stored.
* If the new weight is smaller than the old weight I will change the value for that node to store this node as the previous node and the 
new weight as the smallest weight to get to that node.

## Data Structures For This Algorithm

* A map and around three lists, one list for visited nodes, one for unvisited nodes, and the other for the priority queue
* I will put my priority queue in its own class so that I can easily swap which type of priority queue I use
* To reduce code duplication for core I will make two separate classes for each different priority queue so that I can call dijkstras and not have to rewrite it

## I expect that this will be O(n^2) for time and O(1) for space 



# Core


## Heap Priority Queue

### How It Works

* The smallest values are stored in the lowest indexes and everytime something is inserted or deleted the queue is sorted so that the parent is always 
bigger than its children.

### Insert

* Basically everytime anything is added to the queue it is added to the bottom of the list.
* At the bottom, it checks to see if its value is < or > its parent.
* If it is > it stays where it is.
* If it is < then it switches places with its parent and will repeat the previous steps until it is properly sorted.

### Delete min

* To delete the smallest value in the queue you move the value that is furthest right at the bottom of the heap to the top of the heap and then delete it from its old spot.
* After this happens the heap will sort itself so that if the new top value is smaller than one or both of its descendants it will switch
places with the smallest descendant and this will keep happening until it is smaller than any descendants it may have.
* Because of this comparison method the value at the top of the heap will then be the next smallest value.

### Decrease key

* I will have a map that holds nodes as keys and previous nodes and the nodes weight in a list as its value.
* Whenever a path that has a weight less than the current weight of a node is discovered the value for the nodes weight
will be changed to the smaller weight and the previous node will be changed to the node that lead to the node getting its smaller weight

## Data Structures

* I will use a map to keep track of weight values and 3 lists.
* One list will keep track of visited nodes, another will keep track of unvisited nodes, and the last will be my heap

## The time complexity should be O(n) and the space should be O(1)