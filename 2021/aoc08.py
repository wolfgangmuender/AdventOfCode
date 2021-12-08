with open("input/input08.txt") as f:
    content = f.read().splitlines()

letter_displays = {
    0: ['A', 'B', 'C', 'E', 'F', 'G'],
    1: ['C', 'F'],
    2: ['A', 'C', 'D', 'E', 'G'],
    3: ['A', 'C', 'D', 'F', 'G'],
    4: ['B', 'C', 'D', 'F'],
    5: ['A', 'B', 'D', 'F', 'G'],
    6: ['A', 'B', 'D', 'E', 'F', 'G'],
    7: ['A', 'C', 'F'],
    8: ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
    9: ['A', 'B', 'C', 'D', 'F', 'G'],
}

measurements = []
for line in content:
    input, output = line.split(" | ")
    measurements.append({
        "input": input.split(" "),
        "output": output.split(" ")
    })

unique_results = 0
for measurement in measurements:
    for output in measurement["output"]:
        if len(output) in [2, 3, 4, 7]:
            unique_results += 1

print("Solution 1: digits 1, 4, 7, or 8 appear {} times".format(unique_results))


def signal_to_possible_numbers(signal):
    the_len = len(signal)
    if the_len == 2:
        return [1]
    elif the_len == 3:
        return [7]
    elif the_len == 4:
        return [4]
    elif the_len == 5:
        return [2, 3, 5]
    elif the_len == 6:
        return [0, 6, 9]
    elif the_len == 7:
        return [8]
    else:
        raise Exception("You cannot be serious!")


def get_unique_from_length(signals, the_len):
    for signal in signals:
        if len(signal) == the_len:
            return list(signal)
    raise Exception("You cannot be serious!")


def get_the_three(signals, the_one):
    for sig in signals:
        signal = list(sig)
        if len(signal) == 5 and all(elem in signal for elem in the_one):
            return signal
    raise Exception("You cannot be serious!")


def get_the_nine(signals, the_three):
    for sig in signals:
        signal = list(sig)
        if len(signal) == 6 and all(elem in signal for elem in the_three):
            return signal
    raise Exception("You cannot be serious!")


def get_null_and_six(signals, the_one, the_nine):
    the_null = None
    the_six = None
    for sig in signals:
        signal = list(sig)
        if len(signal) == 6 and signal != the_nine:
            if all(elem in signal for elem in the_one):
                the_null = signal
            else:
                the_six = signal
    if not the_null or not the_six:
        raise Exception("You cannot be serious!")
    return the_null, the_six


def get_single_diff(list1, list2):
    the_diff = [el for el in list1 if el not in list2]
    if len(the_diff) != 1:
        raise Exception("You cannot be serious!")
    return the_diff[0]


def remove_known(the_signal, the_known):
    the_diff = [el for el in the_signal if el not in the_known]
    if len(the_diff) != 1:
        raise Exception("You cannot be serious!")
    return the_diff[0]


def map_number(the_number, the_mapping):
    mapped_number = [the_mapping[n] for n in the_number]
    mapped_number.sort()
    if mapped_number == ['A', 'B', 'C', 'E', 'F', 'G']:
        return 0
    elif mapped_number == ['C', 'F']:
        return 1
    elif mapped_number == ['A', 'C', 'D', 'E', 'G']:
        return 2
    elif mapped_number == ['A', 'C', 'D', 'F', 'G']:
        return 3
    elif mapped_number == ['B', 'C', 'D', 'F']:
        return 4
    elif mapped_number == ['A', 'B', 'D', 'F', 'G']:
        return 5
    elif mapped_number == ['A', 'B', 'D', 'E', 'F', 'G']:
        return 6
    elif mapped_number == ['A', 'C', 'F']:
        return 7
    elif mapped_number == ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
        return 8
    elif mapped_number == ['A', 'B', 'C', 'D', 'F', 'G']:
        return 9
    else:
        raise Exception("You cannot be serious!")


output_sum = 0
for measurement in measurements:
    signals = measurement["input"]
    nm = {
        1: get_unique_from_length(signals, 2),
        4: get_unique_from_length(signals, 4),
        7: get_unique_from_length(signals, 3),
        8: get_unique_from_length(signals, 7),
    }
    nm[3] = get_the_three(signals, nm[1])
    nm[9] = get_the_nine(signals, nm[3])
    nm[0], nm[6] = get_null_and_six(signals, nm[1], nm[9])

    mapping = {
        'A': get_single_diff(nm[7], nm[1]),
        'B': get_single_diff(nm[4], nm[3]),
        'C': get_single_diff(nm[8], nm[6]),
        'D': get_single_diff(nm[4], nm[0]),
        'E': get_single_diff(nm[8], nm[9]),
    }
    mapping['F'] = remove_known(nm[4], mapping.values())
    mapping['G'] = remove_known(nm[0], mapping.values())

    inverse_mappping = {v: k for k, v in mapping.items()}

    output_list = [map_number(o, inverse_mappping) for o in measurement['output']]
    output_value = int("".join([str(n) for n in output_list]))

    output_sum += output_value

print("Solution 2: the sum of all the output values is {}".format(output_sum))
