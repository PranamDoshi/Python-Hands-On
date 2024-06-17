class MedianOfArrays:

    def findMedianSortedArrays(self, nums1, nums2):
        idx1, idx2 = 0, 0

        while idx1 < len(nums1) and idx2 < len(nums2):
            if nums1[idx1] <= nums2[idx2]:
                idx1 += 1
            else:
                nums1.insert(idx1, nums2[idx2])
                idx1 += 1
                idx2 += 1
            
        while idx2 < len(nums2):
            nums1.append(nums2[idx2])
            idx2 += 1
                
        if len(nums1) & 1:
            return nums1[(len(nums1) - 1) // 2]
        else:
            return (nums1[len(nums1) // 2] + nums1[(len(nums1) // 2) - 1]) / 2


if __name__ == "__main__":
    sol = MedianOfArrays()

    nums1 = list(map(int, input().split()))
    nums2 = list(map(int, input().split()))

    print(sol.findMedianSortedArrays(nums1, nums2))