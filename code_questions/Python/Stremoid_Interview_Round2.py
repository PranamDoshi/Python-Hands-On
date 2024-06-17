def simplify_directions(Directions):
    redundantDirections = {'NORTH': 'SOUTH', 'SOUTH': 'NORTH', 'WEST': 'EAST', 'EAST': 'WEST'}

    idx = 0
    while idx < len(Directions) - 1:

        while idx < len(Directions) - 1 and redundantDirections[Directions[idx].upper()] == Directions[idx+1] and idx >= 0:
            # print(f'{idx} -- {Directions[idx]} -- {Directions[idx+1]} -- {redundantDirections[Directions[idx]]} \n {Directions}')
            Directions.pop(idx)
            # print(f'{idx} -- {Directions[idx]} -- {Directions[idx+1]} -- {redundantDirections[Directions[idx]]} \n {Directions}')
            Directions.pop(idx)
            # print(f'{idx} -- {Directions[idx]} -- {Directions[idx+1]} -- {redundantDirections[Directions[idx]]} \n {Directions}')

            idx -= 1
        
        idx += 1

    return Directions

assert simplify_directions(["NORTH", "SOUTH", "SOUTH", "EAST", "WEST", "NORTH", "WEST"]) == ['WEST']

assert simplify_directions(["North", "West", "South"]) == ["North", "West", "South"]

assert simplify_directions(["SOUTH", "EAST", "NORTH", "SOUTH", "SOUTH", "EAST", "WEST", "NORTH", "WEST"]) 

print('Pass')
