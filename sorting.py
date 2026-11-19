"""Sorting algorithms (Unit 1). Each sorts a list of items using key(item)."""
import random


def merge_sort(arr, key=lambda x: x):
    """Stable merge sort. Time O(n log n) always, Space O(n)."""
    if len(arr) <= 1:
        return list(arr)
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)
    merged, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):   # <= keeps equal items in order (stable)
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def quick_sort(arr, key=lambda x: x):
    """Quick sort, random pivot. Average O(n log n), worst O(n^2), Space O(log n)."""
    a = list(arr)

    def sort(lo, hi):
        if lo >= hi:
            return
        p = random.randint(lo, hi)
        a[p], a[hi] = a[hi], a[p]
        pivot = key(a[hi])
        i = lo
        for j in range(lo, hi):
            if key(a[j]) < pivot:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[hi] = a[hi], a[i]
        sort(lo, i - 1)
        sort(i + 1, hi)

    sort(0, len(a) - 1)
    return a


def heap_sort(arr, key=lambda x: x):
    """Heap sort. Time O(n log n) always, Space O(1) extra."""
    a = list(arr)
    n = len(a)

    def heapify(size, i):
        largest = i
        l, r = 2 * i + 1, 2 * i + 2
        if l < size and key(a[l]) > key(a[largest]):
            largest = l
        if r < size and key(a[r]) > key(a[largest]):
            largest = r
        if largest != i:
            a[i], a[largest] = a[largest], a[i]
            heapify(size, largest)

    for i in range(n // 2 - 1, -1, -1):   # build max-heap
        heapify(n, i)
    for end in range(n - 1, 0, -1):       # move max to the end
        a[0], a[end] = a[end], a[0]
        heapify(end, 0)
    return a
