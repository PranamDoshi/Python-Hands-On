import time


class Solution:
    
    def merge(self, m, nums1, n, nums2):
        i, j = 0, 0
        
        if n > 0:
            del nums1[-n:]

        while i < len(nums1) and j < n:
            #print(i, j, nums1)
            if nums1[i] <= nums2[j]:
                if i < len(nums1) - 1:
                    if nums1[i + 1] >= nums2[j]:
                        nums1.insert(i + 1, nums2[j])
                        j += 1
                        i += 2
                    else:
                        i += 1
                else:
                    nums1.insert(i + 1, nums2[j])
                    j += 1
                    i += 2
            else:
                nums1.insert(i, nums2[j])
                i += 1
                j += 1

        while j != n:
            nums1.append(nums2[j])
            j += 1


class Solution2:

    def merge(self, nums1, m, nums2, n):
        i, j = -n, 0
        print(nums1, nums2)
        while i <= -1:
            nums1[i] = nums2[j]
            i += 1
            j += 1
        print(nums1, nums2)
        nums1.sort()


if __name__ == "__main__":
    sol = Solution()
    sol2 = Solution2()

    nums1 = list(map(int, input().split()))
    m = int(input())
    nums2 = list(map(int, input().split()))
    n = int(input())
    assert len(nums2) == n
    assert len(nums1) == (m + n)

    t1 = time.time()
    sol.merge(m, nums1, n, nums2)
    
    print('{} --- {}'.format(nums1, round(time.time() - t1, 8)))

    nums1 = list(map(int, input().split()))
    m = int(input())
    nums2 = list(map(int, input().split()))
    n = int(input())
    assert len(nums2) == n
    assert len(nums1) == (m + n)

    t1 = time.time()
    sol2.merge(nums1, m, nums2, n)
    
    print('{} --- {}'.format(nums1, round(time.time() - t1, 8)))