from collections import defaultdict

class PartitionLabels:

    def partitionLabels(self, s):
        partLengths = []

        # Store last index of each character
        lastIdx = defaultdict(int)
        for i in range(len(s)):
            lastIdx[s[i]] = i
        
        # Iterate through S between partitionStart and partitionEnd while partitionEnd < len(s)
        partitionStart, partitionEnd = 0, lastIdx[s[0]]
        while 1:
            # Iterate between given PartitionStart and partitionEnd
            # Increament partitionEnd if a character in that partition has last Index greater than partitionEnd
            tempidx = partitionStart
            while tempidx <= partitionEnd:
                if lastIdx[s[tempidx]] > partitionEnd:
                    partitionEnd = lastIdx[s[tempidx]]
                tempidx += 1
            
            # Add the current length of partition
            partLengths.append(len(s[partitionStart:partitionEnd+1]))
            #print(s[partitionStart:partitionEnd+1])
            # Update the partition range now after end of previous partition
            partitionStart = partitionEnd + 1
            if partitionStart < len(s):
                partitionEnd = lastIdx[s[partitionStart]]
            else:
                break

        return partLengths
        

if __name__ == "__main__":
    sol = PartitionLabels()

    s = input()

    print(sol.partitionLabels(s))