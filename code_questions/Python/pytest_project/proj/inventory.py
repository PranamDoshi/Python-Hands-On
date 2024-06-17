class InsufficientException(Exception):
    pass

class MobileInventory:
    def __init__(self, inventory=None):
        if inventory is None:
            self.balance_inventory = {}
        else:
            if not isinstance(inventory, dict):
                raise TypeError("Input inventory must be a dictionary")
            for model in inventory:
                if not isinstance(model, str):
                    raise ValueError("Mobile model name must be a string")
                if not isinstance(inventory[model], int) or inventory[model] < 0:
                    raise ValueError("No. of mobiles must be a positive integer")
            self.balance_inventory = inventory

    def add_stock(self, new_stock):
        if not isinstance(new_stock, dict):
            raise TypeError("Input stock must be a dictionary")
        for model in new_stock:
            if not isinstance(model, str):
                raise ValueError("Mobile model name must be a string")
            if not isinstance(new_stock[model], int) or new_stock[model] < 0:
                raise ValueError("No. of mobiles must be a positive integer")
            if model in self.balance_inventory:
                self.balance_inventory[model] += new_stock[model]
            else:
                self.balance_inventory[model] = new_stock[model]

    def sell_stock(self, requested_stock):
        if not isinstance(requested_stock, dict):
            raise TypeError("Requested stock must be a dictionary")
        for model in requested_stock:
            if not isinstance(model, str):
                raise ValueError("Mobile model name must be a string")
            if not isinstance(requested_stock[model], int) or requested_stock[model] < 0:
                raise ValueError("No. of mobiles must be a positive integer")
            if model not in self.balance_inventory:
                raise InsufficientException("No Stock. New Model Request")
            if requested_stock[model] > self.balance_inventory[model]:
                raise InsufficientException("Insufficient Stock")
            self.balance_inventory[model] -= requested_stock[model]
