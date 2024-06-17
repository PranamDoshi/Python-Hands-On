class FirstBadVersion:

    def firstBadVersion(self, n):
        badVersion = -1
        start, end = 1, n

        while start <= end:
            mid = start + ((end - start) // 2)

            if isBadVersion(mid):
                badVersion = mid
                end = mid - 1
            else:
                start = mid + 1
        
        return badVersion


def isBadVersion(n):
    if n % 2 == 0:
        return True
    return False

if __name__ == "__main__":
    sol = FirstBadVersion()

    n = int(input())

    print(FirstBadVersion(n))