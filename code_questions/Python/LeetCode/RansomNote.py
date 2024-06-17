from collections import defaultdict


class Solution:

    def canConstruct(self, ransomNote, magazine):
        magazineCount = defaultdict(int)
        #ransomNoteCount = defaultdict(int)

        for chr in magazine:
            magazineCount[chr] += 1
      
        # for chr in ransomNote:
        #     ransomNoteCount[chr] += 1
        
        # for chr in ransomNoteCount:
        #     if ransomNoteCount[chr] <= magazineCount[chr]:
        #         continue
        #     else:
        #         return FalsetempIdx = 0
        
        for chr in ransomNote:
            if magazineCount[chr] >= 1:
                magazineCount[chr] = magazineCount[chr] - 1
            else:
                return False        

        return True



if __name__ == "__main__":
    sol = Solution()

    ransomNote = input()
    magazine = input()

    print(sol.canConstruct(ransomNote, magazine))