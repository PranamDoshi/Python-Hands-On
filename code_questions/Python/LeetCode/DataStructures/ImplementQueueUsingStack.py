import re


class Queue:

    def __init__(self):
        self.queue = []
    
    def push(self, x):
        self.queue.append(x)

    def pop(self):
        if self.queue:
            return self.queue.pop(0)
    
    def peak(self):
        if self.queue:
            return self.queue[0]
    
    def empty(self):
        return not self.queue