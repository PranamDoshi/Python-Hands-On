import pickle
from collections import defaultdict
from datetime import datetime
from pathlib import Path
import json
from pprint import pprint, PrettyPrinter

prettyPrinterConfig = PrettyPrinter(indent=4)
def print_data(obj):
    prettyPrinterConfig.pprint(obj)


class SavedPasswords:
    passwords = {}

    @staticmethod
    def savePassword(title: str, password: str, **kwargs):
        if SavedPasswords.checkIfTitleExists(title):
            SavedPasswords.passwords[title]['password'] = password
            SavedPasswords.passwords[title]['password_history'].append(
                f"{datetime.now().strftime('%y-%m-%d')}_{password}"
            )

        else:
            SavedPasswords.passwords[title] = {
                'password_history': [f"{datetime.now().strftime('%y-%m-%d')}_{password}"],
                'password': password,
                'title_history': [f"{datetime.now().strftime('%y-%m-%d')}_{title}"]
            }

            # Add other parameters if received any.
            kwargs.pop('password', None)
            SavedPasswords.passwords[title].update(kwargs)

    @staticmethod
    def getPassword(title: str)-> str:
        return SavedPasswords.passwords[title]

    @staticmethod
    def getPasswordTitles()-> list:
        return list(SavedPasswords.passwords.keys())

    @staticmethod
    def delPassword(title: str):
        SavedPasswords.passwords.pop(title)

    @staticmethod
    def updatePasswordTitle(currentTitle: str, newTitle: str):
        SavedPasswords.passwords[newTitle] = SavedPasswords.passwords[currentTitle]
        SavedPasswords.passwords[newTitle]['title_history'].append(
            f"{datetime.now().strftime('%y-%m-%d')}_{newTitle}"
        )

        SavedPasswords.passwords.pop(currentTitle, None)

    @staticmethod
    def checkIfTitleExists(title: str)-> bool:
        if SavedPasswords.passwords.get(title, False):
            return True

        return False

    @staticmethod
    def dumpToPickle(filepath: str):
        with open(filepath, 'wb') as file:
            pickle.dump(SavedPasswords.passwords, file)

    @staticmethod
    def readFromPickle(filepath: str):
        with open(filepath, 'rb') as file:
            SavedPasswords.passwords = pickle.load(file)

    @staticmethod
    def dumpToJSON():
        print(json.dumps(SavedPasswords.passwords, indent=3))

    @staticmethod
    def readFromJSON(filepath: str):
        with open(filepath, 'r') as file:
            SavedPasswords.passwords = json.load(file)


#Globalvariables
dictPickleFile = f"{Path(Path(__file__).parent).as_posix()}/Saved.pkl"

def savePassword():
    """ Save/Update Password """
    title = input("What is the title? :- ").strip()
    password = input("What is the password? :- ").strip()
    email = input("What is the associated email? (If any) :- ")

    if title not in {'', ' '}:
        SavedPasswords.savePassword(title, password, email=email)
        SavedPasswords.dumpToPickle(dictPickleFile)

def viewPassword():
    """ View Password """
    titles = SavedPasswords.getPasswordTitles()
    for case, title in enumerate(titles):
        print(f"{case} -- {title}", end='\n')
    inp = int(input("Choose the number beside the password you want to update:- "))

    if inp < len(titles):
        print_data(SavedPasswords.getPassword(titles[inp]))

    else:
        print(f"Title not found.\n")

def viewTitles():
    """ View Password Titles """
    titles = SavedPasswords.getPasswordTitles()
    print_data({case: title for case, title in enumerate(titles)})

def deletePassword():
    """ Delete an existing password """
    titles = SavedPasswords.getPasswordTitles()
    for case, title in enumerate(titles):
        print(f"{case} -- {title}", end='\n')

    inp = int(input("Choose the number beside the password you want to update:- "))
    if inp < len(titles):
        SavedPasswords.delPassword(titles[inp])
        SavedPasswords.dumpToPickle(dictPickleFile)

    else:
        print("No password exist for given value. Try again!")
        deletePassword()

def updatePasswordTitle():
    """ Update an existing password title """
    titles = SavedPasswords.getPasswordTitles()
    for case, title in enumerate(titles):
        print(f"{case} -- {title}", end='\n')

    inp = int(input("Choose the number beside the password you want to update:- "))
    if inp < len(titles):    
        newTitle = input("What is the new title? :- ").strip()

        SavedPasswords.updatePasswordTitle(titles[inp], newTitle)
        SavedPasswords.dumpToPickle(dictPickleFile)

    else:
        print("Not an actual title. Try again!")
        updatePasswordTitle()

def allDone():
    """ All Done! """
    print(f"\nIt was Great to see you. Come back soon!")
    exit()

case_to_function = {
    1: savePassword,
    2: viewPassword,
    3: viewTitles,
    4: deletePassword,
    5: updatePasswordTitle,
    6: allDone
}

def getUserChoice()-> int:
    for case, function in case_to_function.items():
        print(f"{case} -{function.__doc__}", end='\n')

    inp = int(input("Choose one of the option from above:- "))

    return inp

if __name__ == "__main__":
    # SavedPasswords.readFromJSON("Saved.json")
    # SavedPasswords.dumpToPickle(dictPickleFile)
    SavedPasswords.readFromPickle(dictPickleFile)
    # SavedPasswords.dumpToJSON()

    try:

        while True:
            inp = getUserChoice()

            if case_to_function.get(inp, False):
                case_to_function[inp]()
            
            else:
                print(f"Not a valid option. Try again!\n")

    except KeyboardInterrupt:
        case_to_function[6]()
