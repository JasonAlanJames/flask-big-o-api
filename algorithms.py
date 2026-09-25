from dataclasses import dataclass
from typing import List

@dataclass
class SortResult:
    values: List[int]
    comparisons: int
    swaps: int

def bubble_sort(values: List[int]) -> SortResult:
    """
    Best: O(n)
    Avg: O(n^2)
    Worst: O(n^2)
    """
    arr = values.copy()

    comparisons = 0
    swaps = 0
    n = len(arr)

    for i in range(n):
        swapped = False

        for j in range(0, n - i - 1):
            comparisons += 1

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True

        if not swapped:
            break

    return SortResult(
        values=arr,
        comparisons=comparisons,
        swaps=swaps,
    )

def merge_sort(values: List[int]) -> SortResult:
    """
    Best: O(n log n)
    Avg: O(n log n)
    Worst: O(n log n)
    """
    comparisons = 0

    def merge(left: List[int], right: List[int]) -> List[int]:
        nonlocal comparisons

        result = []
        i = 0
        j = 0

        while i < len(left) and j < len(right):
            comparisons +=  1

            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])

        return result

    def divide(arr: List[int]) -> List[int]:
        if len(arr) <= 1:
            return arr

        middle = len(arr) // 2

        left = divide(arr[:middle])
        right = divide(arr[middle:])

        return merge(left, right)

    sorted_values = divide(values.copy())

    return SortResult(
        values=sorted_values,
        comparisons=comparisons,
        swaps=0,
    )

def linear_search(values: List[int], target: int) -> tuple[int, int]:
    """
    O(n)
    """

    comparisons = 0

    for index, value in enumerate(values):
        comparisons += 1

        if value == target:
            return index, comparisons

    return -1, comparisons

def binary_search(values: List[int], target: int) -> tuple[int, int]:
    """
    O(log n)
    """
    low = 0
    high = len(values) - 1
    comparisons = 0

    while low <= high:
        middle = (low + high) // 2
        comparisons += 1

        if values[middle] == target:
            return middle, comparisons

        if values[middle] < target:
            low = middle + 1
        else:
            high = middle - 1

    return -1, comparisons