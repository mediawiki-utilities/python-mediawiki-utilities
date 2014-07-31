import heapq


class Heap(list):
    def __init__(self, *args, **kwargs):
        list.__init__(self, *args, **kwargs)
        heapq.heapify(self)

    def pop(self):
        return heapq.heappop(self)

    def push(self, item):
        heapq.heappush(self, item)

    def peek(self):
        return self[0]

    def pushpop(self, item):
        return heapq.heappushpop(self, item)

    def poppush(self, itemp):
        return heapq.replace(self, item)
