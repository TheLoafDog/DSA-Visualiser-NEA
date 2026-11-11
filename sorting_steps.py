"""Pure step generation for the sorting visualiser (no UI).

Each function takes a list of numbers and returns a list of animation
states without modifying the input. A state is
``[data_snapshot, colour_array, message]`` — exactly what
``sorting_vis.parentFrame.run_animation`` draws — and the last state is
always the fully sorted list coloured green.

Colour meanings (shared with sorting_vis):
  red    - not yet in its final place / not currently involved
  orange - element(s) being compared or moved
  green  - in its final sorted position (or the merged/sorted region)
  blue   - element just inserted (insertion sort) / subarray being split (merge sort)
  purple/cyan - left/right subarrays about to be merged (merge sort)
  yellow - position an element is being placed into (merge sort)
  purple - pivot (quick sort); cyan - elements found to be <= the pivot (quick sort)
  purple - smallest value found so far in the pass (selection sort)
"""
import copy


def bubble_sort_steps(data):
    """Bubble sort: repeatedly compare neighbours and swap when out of order."""
    data = list(data)
    states = []
    n = len(data)

    for step_i in range(n - 1):
        for step_j in range(n - step_i - 1):
            text = ("Leave both values since the left one IS NOT LARGER in this comparison.\n"
                    + str(data[step_j + 1]) + " > " + str(data[step_j]))
            if data[step_j] > data[step_j + 1]:
                data[step_j], data[step_j + 1] = data[step_j + 1], data[step_j]
                text = ("Switch both values since the left one IS LARGER in this comparison.\n"
                        + str(data[step_j]) + " > " + str(data[step_j + 1]))

            # Compared pair orange, unsorted rest red, settled tail green
            colour_array = []
            for i in range(n - step_i):
                if i == step_j or i == step_j + 1:
                    colour_array.append('orange')
                else:
                    colour_array.append('red')
            for i in range(n - step_i, n):
                colour_array.append('green')

            states.append([copy.deepcopy(data), colour_array, text])

    states.append([copy.deepcopy(data), ['green'] * n, "Data has been sorted with bubble sort."])
    return states


def insertion_sort_steps(data):
    """Insertion sort: grow a sorted prefix by shifting each new key into place."""
    data = list(data)
    states = []
    n = len(data)

    for index in range(1, n):
        key = data[index]
        j = index - 1

        # Shift elements until the correct spot for `key` is found
        while j >= 0 and data[j] > key:
            colour_array = ['green' if i <= index else 'red' for i in range(n)]
            colour_array[j + 1] = 'orange'  # Highlight the bar being shifted
            states.append([copy.deepcopy(data), colour_array,
                           f"Shift elements until the correct spot for the {key} is found"])

            data[j + 1] = data[j]
            data[j] = key
            j -= 1

        # Insert the key at the correct position
        data[j + 1] = key
        text = f"{key} was inserted in front of the value: {data[j]}.\nSince, {key} > {data[j]}"

        colour_array = ['green' if i <= index else 'red' for i in range(n)]
        colour_array[j + 1] = 'blue'  # Highlight the inserted bar
        states.append([copy.deepcopy(data), colour_array, text])

    states.append([copy.deepcopy(data), ['green'] * n, "Data has been sorted with insertion sort."])
    return states


def merge_sort_steps(data):
    """Merge sort (in place on a working copy): split, then merge sorted halves."""
    arr = list(data)
    states = []

    def merge_sort(left, right):  # Splits the data into subarrays
        if left < right:
            mid = (left + right) // 2

            # Visualise the splitting phase
            colour_array = ['red'] * len(arr)
            for i in range(left, right + 1):
                colour_array[i] = 'blue'
            text = f"Splitting array [{left}:{right}]: {arr[left:right+1]}\n"
            text += f"Into left half [{left}:{mid}]: {arr[left:mid+1]}\n"
            text += f"And right half [{mid+1}:{right}]: {arr[mid+1:right+1]}"
            states.append([copy.deepcopy(arr), colour_array, text])

            merge_sort(left, mid)
            merge_sort(mid + 1, right)

            # Visualise before merging
            colour_array = ['red'] * len(arr)
            for i in range(left, mid + 1):
                colour_array[i] = 'purple'  # Left subarray
            for i in range(mid + 1, right + 1):
                colour_array[i] = 'cyan'    # Right subarray
            text = "About to merge two sorted subarrays:\n"
            text += f"Left subarray [{left}:{mid}]: {arr[left:mid+1]}\n"
            text += f"Right subarray [{mid+1}:{right}]: {arr[mid+1:right+1]}"
            states.append([copy.deepcopy(arr), colour_array, text])

            merge(left, mid, right)

    def merge(left, mid, right):  # Compares and merges the subarrays into sorted ones
        L = arr[left:mid + 1]
        R = arr[mid + 1:right + 1]
        i = j = 0
        k = left

        while i < len(L) and j < len(R):
            colour_array = ['red'] * len(arr)
            colour_array[left + i] = 'orange'     # Element from left subarray
            colour_array[mid + 1 + j] = 'orange'  # Element from right subarray
            text = f"Comparing L[{i}]={L[i]} with R[{j}]={R[j]}"
            colour_array[k] = 'yellow'            # Position where element will be placed

            if L[i] <= R[j]:
                text += f"\nPlacing L[{i}]={L[i]} at position {k}, since L[{i}]={L[i]} ≤ R[{j}]={R[j]}"
                arr[k] = L[i]
                states.append([copy.deepcopy(arr), colour_array, text])
                i += 1
            else:
                text += f"\nPlacing R[{j}]={R[j]} at position {k} since, L[{i}]={L[i]} > R[{j}]={R[j]}"
                arr[k] = R[j]
                states.append([copy.deepcopy(arr), colour_array, text])
                j += 1
            k += 1

        # Copy any remaining elements of the left subarray
        while i < len(L):
            current_array = copy.deepcopy(arr)
            colour_array = ['red'] * len(arr)
            colour_array[left + i] = 'orange'
            colour_array[k] = 'yellow'
            current_array[k] = L[i]
            states.append([current_array, colour_array,
                           f"Copying remaining element L[{i}]={L[i]} to position {k}"])
            arr[k] = L[i]
            i += 1
            k += 1

        # Copy any remaining elements of the right subarray
        while j < len(R):
            current_array = copy.deepcopy(arr)
            colour_array = ['red'] * len(arr)
            colour_array[mid + 1 + j] = 'orange'
            colour_array[k] = 'yellow'
            current_array[k] = R[j]
            states.append([current_array, colour_array,
                           f"Copying remaining element R[{j}]={R[j]} to position {k}"])
            arr[k] = R[j]
            j += 1
            k += 1

        # Show the completed merge
        colour_array = ['red'] * len(arr)
        for i in range(left, right + 1):
            colour_array[i] = 'green'
        states.append([copy.deepcopy(arr), colour_array,
                       f"Merged subarray [{left}:{right}]: {arr[left:right+1]}"])

    merge_sort(0, len(arr) - 1)
    states.append([copy.deepcopy(arr), ['green'] * len(arr), "Data has been sorted with merge sort."])
    return states


def quick_sort_steps(data):
    """Quick sort (Lomuto partition, last element as pivot).

    Each partition pass compares every element of the subarray with the
    pivot, swapping small elements into a growing "less than or equal to the
    pivot" region, then swaps the pivot into its final place. Pivots that
    have been placed stay green.
    """
    arr = list(data)
    states = []
    n = len(arr)
    settled = set()  # Indexes whose final value is known (placed pivots / 1-element subarrays)

    def colours(low, high, pivot=None, current=None, boundary=None):
        colour_array = ['red'] * n
        for i in range(low, high + 1):
            colour_array[i] = 'blue'          # Subarray being partitioned
        if boundary is not None:
            for i in range(low, boundary + 1):
                colour_array[i] = 'cyan'      # Elements already found to be <= pivot
        if current is not None:
            colour_array[current] = 'orange'  # Element being compared with the pivot
        if pivot is not None:
            colour_array[pivot] = 'purple'    # The pivot
        for i in settled:
            colour_array[i] = 'green'
        return colour_array

    def quick_sort(low, high):
        if low > high:
            return
        if low == high:
            settled.add(low)
            states.append([copy.deepcopy(arr), colours(low, high),
                           f"Subarray [{low}:{high}] has one element ({arr[low]}), so it is already in place."])
            return

        pivot = arr[high]
        states.append([copy.deepcopy(arr), colours(low, high, pivot=high),
                       f"Partitioning subarray [{low}:{high}]: {arr[low:high+1]}\n"
                       f"Pivot = last element, {pivot} (index {high})."])

        i = low - 1  # Last index of the "<= pivot" region
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                text = (f"{arr[i]} <= pivot {pivot}, so swap it into the 'smaller' region\n"
                        f"(index {j} -> index {i}).")
            else:
                text = f"{arr[j]} > pivot {pivot}, so leave it where it is."
            states.append([copy.deepcopy(arr), colours(low, high, pivot=high, current=j, boundary=i), text])

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        settled.add(i + 1)
        states.append([copy.deepcopy(arr), colours(low, high, boundary=i),
                       f"Swap the pivot {pivot} into index {i + 1}: everything to its left is <= {pivot} "
                       f"and everything to its right is > {pivot}.\nThe pivot is now in its final position."])

        quick_sort(low, i)
        quick_sort(i + 2, high)

    quick_sort(0, n - 1)
    states.append([copy.deepcopy(arr), ['green'] * n, "Data has been sorted with quick sort."])
    return states


def selection_sort_steps(data):
    """Selection sort: repeatedly find the minimum of the unsorted part and swap it to the front.

    Each comparison shows the element being scanned (orange) against the
    current minimum (purple); the sorted prefix stays green.
    """
    arr = list(data)
    states = []
    n = len(arr)

    def colours(sorted_upto, minimum=None, current=None):
        colour_array = ['green' if i < sorted_upto else 'red' for i in range(n)]
        if minimum is not None:
            colour_array[minimum] = 'purple'   # Smallest value found so far
        if current is not None:
            colour_array[current] = 'orange'   # Element being compared with it
        return colour_array

    for i in range(n - 1):
        min_index = i
        states.append([copy.deepcopy(arr), colours(i, minimum=min_index),
                       f"Pass {i + 1}: find the smallest value in the unsorted part {arr[i:]}.\n"
                       f"Start by assuming {arr[i]} (index {i}) is the smallest."])
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                text = (f"{arr[j]} < {arr[min_index]}, so {arr[j]} (index {j}) is the new smallest value so far.")
                min_index = j
                states.append([copy.deepcopy(arr), colours(i, minimum=min_index), text])
            else:
                states.append([copy.deepcopy(arr), colours(i, minimum=min_index, current=j),
                               f"{arr[j]} >= {arr[min_index]}, so the smallest value so far stays {arr[min_index]}."])

        if min_index != i:
            arr[i], arr[min_index] = arr[min_index], arr[i]
            text = (f"Swap the smallest value {arr[i]} (was index {min_index}) with {arr[min_index]} at index {i}.\n"
                    f"Index {i} is now in its final position.")
        else:
            text = f"{arr[i]} is already the smallest value, so no swap is needed.\nIndex {i} is now in its final position."
        states.append([copy.deepcopy(arr), colours(i + 1), text])

    states.append([copy.deepcopy(arr), ['green'] * n, "Data has been sorted with selection sort."])
    return states


STEP_FUNCTIONS = {
    "Bubble Sort": bubble_sort_steps,
    "Insertion Sort": insertion_sort_steps,
    "Merge Sort": merge_sort_steps,
    "Quick Sort": quick_sort_steps,
    "Selection Sort": selection_sort_steps,
}
