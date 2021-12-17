from typing import List


def twoSum(nums: List[int], target: int) -> List[int]:

    return func2(nums, target)


def func1(nums: List[int], target: int):

    result: List[int] = []
    for i, val_a in enumerate(nums):
        for j, val_b in enumerate(nums):
            if j > i and val_a + val_b == target:
                result.append(i)
                result.append(j)
                return [i, j]
    return None


def func2(nums: List[int], target: int):

    element = {}
    for i, value in enumerate(nums):
        if target - value in element:
            return [element[target - value], i]

        element[value] = i
    return None


# twoSum([3, 3], 6)
