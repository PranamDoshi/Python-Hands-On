def BinarySearchIterative(nums, target):
    """
    Iterative Algorithm
    """
    start, end = 0, len(nums) - 1

    while start <= end:
        mid = start + ((end - start) // 2)

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            start = mid + 1
        elif nums[mid] > target:
            end = mid - 1
        
    return - 1

def BinarySearchRecursive(nums, start, end, target):
    if start <= end:
        mid = start + ((end - start) // 2)
        
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            return BinarySearchRecursive(nums, mid + 1, end, target)
        else:
            return BinarySearchRecursive(nums, start, mid - 1, target)

    else: 
        return -1