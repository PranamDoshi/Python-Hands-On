str = list(input())

vowels = ['a', 'e', 'i', 'o', 'u', 'y', 'A', 'I', 'O', 'E', 'U', 'Y']
output = []

for chr in str:
    if chr not in vowels:
        output.append(("." + chr).lower())

print("".join(output))