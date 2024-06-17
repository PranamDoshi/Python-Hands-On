from inventory import MobileInventory

class TestClass:

    def __init__(self):
        self.inv = MobileInventory({'iPhone Model X' : 100, 'Xiaomi Model Y' : 1000, 'Nokia Model Z' : 25})
        print(self.inv.balance_inventory)
        print(self.inv.balance_inventory == {'iPhone Model X' : 100, 'Xiaomi Model Y' : 1000, 'Nokia Model Z' : 25})
        assert self.inv.balance_inventory == {'iPhone Model X' : 100, 'Xiaomi Model Y' : 1000, 'Nokia Model Z' : 25}


t = TestClass()

with open('t.txt', 'w') as f:
    for i in range(2):
        f.write("hello world\n")
        f.close()
    