from collections import defaultdict

class FreqStack:

    def __init__(self):
        self.stack = []
        self.counter = defaultdict(int)
        
    def push(self, val):
        self.counter[val] += 1
        if self.counter[val] > len(self.stack):
            self.stack.append([val])
        else:
            self.stack[self.counter[val] - 1].append(val)
        
    def pop(self):
        while not self.stack[-1]:
            self.stack.pop()
        value = self.stack[-1].pop()
        self.counter[value] -= 1
        return value


"""
from sortedcontainer import SortedDict

class FreqStack:

    def __init__(self):
        self.stack = []
        self.counter = SortedDict()

    def push(self, val: int) -> None:
        

    def pop(self) -> int:
        


# Your FreqStack object will be instantiated and called as such:
"""
obj = FreqStack()
obj.push(5)
print(obj.stack)
obj.push(7)
print(obj.stack)
obj.push(5)
print(obj.stack)
obj.push(7)
print(obj.stack)
obj.push(4)
print(obj.stack)
obj.push(5)
print(obj.stack)
print(obj.pop())
print(obj.pop())
print(obj.pop())
print(obj.pop())