# -*- coding: utf-8 -*-

import heapq

class PriorityQueue:
    def __init__(self):
        
        self.elements = []
        self.counter = 0
    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority,self.counter ,item))
        self.counter += 1

    def get(self):
        return heapq.heappop(self.elements)[2]