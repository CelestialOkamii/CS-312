class LinearPQ:

    def __init__(self):
        self.linear_queue = {}


    def insert(self, weight_info):
        node = weight_info[0]
        if len(self.linear_queue) == 0 or node not in self.linear_queue:
            self.linear_queue[node] = [weight_info[1], weight_info[2]]
        else:
            if self.linear_queue[node][1] > weight_info[2]:
                self.linear_queue[node] = [weight_info[1], weight_info[2]]


    def __find_min(self):
        if len(self.linear_queue) == 0:
            return None
        min_weight = float("inf")
        keys = list(self.linear_queue.keys())
        min_item = keys[0]
        for key in keys:
            value = self.linear_queue.get(key)
            if value[1] < min_weight:
                min_weight = value[1]
                min_item = [key] + value
        return min_item


    def remove_min(self):
        weight_info = self.__find_min()
        self.linear_queue.pop(weight_info[0])
        return weight_info


    def is_empty(self):
        if len(self.linear_queue) == 0:
            return True
        return False