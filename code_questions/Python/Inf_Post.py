priority = {'+':0, '-':0, '*':1, '/':1, '(':5}
operators = ['+', '-', '*', '/']

class stack:
    def __init__(self):
        self.top = -1
        self.Stk = []

    def push(self, i):
        self.top += 1
        self.Stk.append(i)

    def popO(self):
        p = self.Stk.pop()
        self.top -= 1
        return p

    def read(self):
        return self.Stk[self.top]

    def isEmpty(self):
        return self.top == -1

S = stack()
inf = input("Enter the Expression: ")
i = 0
while i < len(inf):
    if inf[i].isalpha():
        print(inf[i], end = '')
    elif inf[i] == '(':
        S.push(inf[i])
    elif inf[i] == ')':
        while (S.read() != '(') and (not S.isEmpty()):
            print(S.popO(), end = '')
        S.popO()
    else:
        while (not S.isEmpty()) and (S.read() in operators) and (priority[S.read()] >= priority[inf[i]]):
            print(S.popO(), end = '')
        S.push(inf[i])
    i += 1
while S.top != -1:
    print(S.popO(), end = '')
