def main():
    stateOfAccount = int(input())

    if stateOfAccount >= 0:
        print(stateOfAccount)
    else:
        stateofAccountinArray = list(str(stateOfAccount))
        possibility1 = int("".join(stateofAccountinArray[:-1]))
        stateofAccountinArray.pop(-2)
        possibility2 = int("".join(stateofAccountinArray))
        #print(possibility1, possibility2)
        if possibility1 >= possibility2:
            print(possibility1)
        else:
            print(possibility2)


if __name__ == "__main__":
    main()