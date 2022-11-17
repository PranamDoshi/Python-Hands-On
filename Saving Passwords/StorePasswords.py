import pickle
from PasswordDictionaryClass import SavedPasswords

#Globalvariables
dictPickleFile = 'Saved.pkl'

if __name__ == "__main__":
    passwords = SavedPasswords()
    # with open(dictPickleFile, 'rb') as pklFile:
    #     passwords = pickle.load(pklFile)
    
    while True:
        inp = int(input("1 - Save Password \
                        \n2 - View Password \
                        \n3 - View Categories \
                        \n4 - Change a Passowrd Category \
                        \n5 - Delete categories (Provide comma separated indexs.) \
                        \n0 - I'm Done\n"))

        if inp == 1:
            name = input("Enter Category Name:")
            
            # Checks if the category already exists.
            if passwords.checkCategoryIfExists(name):
                print("Please use the existing category!")
            
            if name not in ['0', None, '', '\t', '\n']:
                password = input("Enter Password:")
                passwords.savePassword(name, password)
        elif inp == 2:
            categories = passwords.getCategories()
            if categories:
                for idx, catg in enumerate(categories):
                    # print("%d - %s" % (idx, catg))
                    print(f"{idx} - {catg}")
                
                inp = int(input("Which category: "))
                if inp >= 0 and inp < len(categories):
                    passwords.viewPassword(categories[inp])
                else:
                    print("Select a Valid Option")
            else:
                print("No passwords Saved")
        elif inp == 3:
            passwords.viewCategories()
        elif inp == 4:
            oldCategory = input("Enter the old category")
            newCategory = input("Enter the new category")

            passwords.ChangeCategories(oldCategory, newCategory)
        elif inp == 5:
            categories = passwords.getCategories()
            inpIdxs = list(map(int, input().split(',')))

            for idx in inpIdxs:
                passwords.delPassword(categories[inpIdxs])
        else:
            break
     
    with open(dictPickleFile, 'wb') as pklFile:
        pickle.dump(passwords, pklFile)
