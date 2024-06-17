from itertools import count


class OverlappingIntervals:

    def merge(self, intervals):
        intervals.sort()
        finalIntervals = []
        minimumRemovals = 0

        for interval in intervals:
            if not finalIntervals or finalIntervals[-1][1]  < interval[0]:
                finalIntervals.append(interval)
            else:
                finalIntervals[-1][1] = max(finalIntervals[-1][1], interval[1])
                minimumRemovals += 1
            
        return minimumRemovals

    def count(self, intervals):
        minimumRemovals = 0
        intervals.sort()
        low, high = 0, 1

        while high < len(intervals):
            print(intervals[high], intervals[low])
            if intervals[high][0] < intervals[low][1]:
                if intervals[high][1] > intervals[low][1]:
                    high += 1
                else:
                    low = high
                    high += 1
                minimumRemovals += 1
            else:
                low = high
                high += 1
        
        return minimumRemovals


if __name__ == "__main__":
    sol = OverlappingIntervals()

    #intervals = [[1,3],[2,6],[8,10],[15,18]]
    intervals = [[1,2],[2,3],[3,4],[1,3]]

    #print(sol.merge(intervals))
    print(sol.count(intervals))