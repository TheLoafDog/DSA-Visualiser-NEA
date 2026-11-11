"""Pure step generation for the searching visualiser (no UI).

Each function takes a list of numbers and a target value and returns a
list of animation states without modifying the input. A state is
``[colour_array, message]`` — exactly what
``searching_vis.parentFrame.run_animation`` draws.

Colour meanings (shared with searching_vis):
  grey   - not yet compared / not involved
  orange - element currently being compared with the target
  red    - compared and ruled out
  green  - a match for the target

``binary_search_steps`` expects ``data`` to already be sorted ascending,
as the binary visualiser always sorts its data before searching.
"""
import copy


def linear_search_steps(data, target_value):
    """Linear search: compare every element with the target, left to right.

    One state per element compared, then a final state summarising every
    index that matched (all matches are reported, not just the first).
    """
    data = list(data)
    states = []
    colour_array = ['grey'] * len(data)
    matches = []

    for cur_index in range(len(data)):
        colour_array[cur_index] = 'orange'

        if data[cur_index] == target_value:
            colour_array[cur_index] = 'green'
            text = "MATCH found!\nData[" + str(cur_index) + "] == " + str(target_value)
            states.append([copy.deepcopy(colour_array), text])
            matches.append(cur_index)
        else:
            text = "NO MATCH found!\nData[" + str(cur_index) + "] != " + str(target_value)
            states.append([copy.deepcopy(colour_array), text])
            colour_array[cur_index] = 'red'

    # Final state: only the matches are coloured green
    colour_array = ['grey'] * len(data)
    if matches:
        text = "Matches found at indexes: " + str(matches)[1:-1] + "."
    else:
        text = str(target_value) + " does not exist."
    for i in matches:
        colour_array[i] = 'green'
    states.append([copy.deepcopy(colour_array), text])

    return states


def binary_search_steps(data, value):
    """Binary search over sorted ``data``: halve the search range each step.

    Each iteration gives a "compare the middle" state followed by either a
    "found" state (search ends) or a state showing the discarded half in
    red. If the value is absent, a final all-grey "does not exist" state is
    added.
    """
    data = list(data)
    states = []
    colour_array = ['grey'] * len(data)
    low = 0
    high = len(data) - 1
    found = False

    while high >= low and not found:
        mid = (high + low) // 2
        colour_array[mid] = "orange"
        states.append([copy.deepcopy(colour_array),
                       "Compare the middle value with the value.\nMiddle index: " + str(mid)
                       + " = (" + str(high) + " + " + str(low) + ") // 2"])

        if value == data[mid]:
            colour_array = ['grey'] * len(data)
            colour_array[mid] = 'green'
            states.append([copy.deepcopy(colour_array),
                           "Data[" + str(mid) + "] == " + str(value)
                           + ".\nValue found at index: " + str(mid) + "."])
            found = True
        else:
            if data[mid] < value:
                # Target is in the right half
                text = ("Data[" + str(mid) + "] < " + str(value)
                        + ".\nValue is greater, so we get rid of all the values on the left side (greater values) of the middle (inclusive).")
                for i in range(low, mid + 1):
                    colour_array[i] = 'red'
                low = mid + 1
            else:
                # Target is in the left half
                text = ("Data[" + str(mid) + "] > " + str(value)
                        + ".\nValue is smaller, so we get rid of all the values on the right side (smaller values) of the middle (inclusive).")
                for i in range(mid, high + 1):
                    colour_array[i] = 'red'
                high = mid - 1

            states.append([copy.deepcopy(colour_array), text])

    if not found:
        colour_array = ['grey'] * len(data)
        states.append([copy.deepcopy(colour_array), str(value) + " does not exist."])

    return states
