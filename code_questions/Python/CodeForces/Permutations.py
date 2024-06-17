def permutation(inp, perm, step = 0):
    if step == len(inp):
        if "".join(inp) not in perm:
            perm.append("".join(inp))
    for i in range(step, len(inp)):
        inp_copy = [c for c in inp]
        #print(inp_copy, i, step)
        inp_copy[step], inp_copy[i] = inp_copy[i], inp_copy[step]
        permutation(inp_copy, perm, step + 1)

def permutations_merger(chrs, perm):
    for i in range(1, len(chrs)):
        for idx in range(len(chrs) - i):
            permutation("".join(chrs[idx:idx + i + 1]), perm)

chrs = list(input())
perm = [c for c in chrs]

permutations_merger(chrs, perm)

print(perm)