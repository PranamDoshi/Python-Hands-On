import pickle

class SavedPasswords:

    def __init__(self):
        self.__passwords = {}
    
    def savePassword(self, category, password):
        self.__passwords[category] = password
    
    def viewPassword(self, category):
        print(self.__passwords[category])

    def delPassword(self, category):
        self.__passwords.pop(category)
    
    def viewCategories(self):
        for catg in self.__passwords.keys():
            print(catg, end = '\n')
    
    def getCategories(self):
        return list(self.__passwords.keys())

    def ChangeCategories(self, oldCatg, newCatg):
        tempPassword = self.__passwords[oldCatg]
        self.__passwords.pop(oldCatg)
        self.__passwords[newCatg] = tempPassword

    def checkCategoryIfExists(self, category):
        if self.__passwords.get(category):
            return True
        return False
