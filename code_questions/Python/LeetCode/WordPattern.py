class WordPatter:

    def followsPattern(self, pattern, s):
        if len(pattern) != len(list(s.split())):
            return False

        patterToWord, usedWords = {}, set()

        for chr, word in zip(list(pattern), list(s.split())):
            if patterToWord.get(chr, 0) and word != patterToWord[chr]:
                return False
            else:
                if word not in usedWords:
                    patterToWord[chr] = word
                    usedWords.add(word)
                elif chr not in patterToWord.keys():
                    return False
            #print(patterToWord, usedWords)
        
        return True


if __name__ == "__main__":
    sol = WordPatter()

    pattern = input()
    s = input()

    print(sol.followsPattern(pattern, s))