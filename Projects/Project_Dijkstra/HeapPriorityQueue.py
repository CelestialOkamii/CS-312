class HeapPQ:

    def __init__(self):
        self.heap_queue = []
        self.map_queue = {}

    def insert(self, weight_info):
        node = weight_info[0]
        if len(self.heap_queue) == 0 or node not in self.map_queue or self.map_queue[node][1] > weight_info[2]:
            if not node in self.map_queue:
                self.heap_queue.append(weight_info)
                self.map_queue[node] = [len(self.heap_queue) - 1, weight_info[2]]
            else:
                self.map_queue[node][1] = weight_info[2]
                self.heap_queue[self.map_queue[node][0]] = weight_info
            i = self.map_queue[node][0]
            while i > 0:
                parent = (i - 1) // 2
                if weight_info[2] < self.heap_queue[parent][2]:
                    self.heap_queue[i], self.heap_queue[parent] = self.heap_queue[parent], self.heap_queue[i]
                    self.map_queue[self.heap_queue[i][0]][0] = i
                    self.map_queue[self.heap_queue[parent][0]][0] = parent
                    i = parent
                else:
                    break
            self.map_queue[node] = [i, weight_info[2]]


    def remove_min(self):
        if len(self.heap_queue) == 0:
            return None
        min_value = self.heap_queue[0]
        self.heap_queue[0] = self.heap_queue[-1]
        self.heap_queue.pop()
        self.map_queue.pop(min_value[0])
        size_heap = len(self.heap_queue)
        if size_heap == 0:
            return min_value
        self.map_queue[self.heap_queue[0][0]][0] = 0
        i = 0
        while True:
            left_child = i * 2 + 1
            right_child = i * 2 + 2
            smallest = i
            if left_child < size_heap and self.heap_queue[left_child][2] < self.heap_queue[smallest][2]:
                smallest = left_child
            if right_child < size_heap and self.heap_queue[right_child][2] < self.heap_queue[smallest][2]:
                smallest = right_child
            if smallest == i:
                break
            self.heap_queue[i], self.heap_queue[smallest] = self.heap_queue[smallest], self.heap_queue[i]
            self.map_queue[self.heap_queue[i][0]][0] = i
            self.map_queue[self.heap_queue[smallest][0]][0] = smallest
            i = smallest
        return min_value

    def is_empty(self):
        if len(self.heap_queue) == 0:
            return True
        return False