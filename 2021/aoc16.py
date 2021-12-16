import os
import time
from functools import reduce


def main(puzzle_input):
    transmission = puzzle_input[0]
    binary_message = to_binary(transmission)

    packet = read_packet(binary_message)

    total_version = get_total_version(packet)
    total_value = get_total_value(packet)

    print("Solution 1: the sum of the version numbers in all packets is {}".format(total_version))
    print("Solution 2: the value of the expression represented by the hexadecimal-encoded BITS transmission is {}"
          .format(total_value))


def to_binary(transmission):
    binary_message = []
    for h in transmission:
        if h == "0":
            binary_message += ["0", "0", "0", "0"]
        elif h == "1":
            binary_message += ["0", "0", "0", "1"]
        elif h == "2":
            binary_message += ["0", "0", "1", "0"]
        elif h == "3":
            binary_message += ["0", "0", "1", "1"]
        elif h == "4":
            binary_message += ["0", "1", "0", "0"]
        elif h == "5":
            binary_message += ["0", "1", "0", "1"]
        elif h == "6":
            binary_message += ["0", "1", "1", "0"]
        elif h == "7":
            binary_message += ["0", "1", "1", "1"]
        elif h == "8":
            binary_message += ["1", "0", "0", "0"]
        elif h == "9":
            binary_message += ["1", "0", "0", "1"]
        elif h == "A":
            binary_message += ["1", "0", "1", "0"]
        elif h == "B":
            binary_message += ["1", "0", "1", "1"]
        elif h == "C":
            binary_message += ["1", "1", "0", "0"]
        elif h == "D":
            binary_message += ["1", "1", "0", "1"]
        elif h == "E":
            binary_message += ["1", "1", "1", "0"]
        elif h == "F":
            binary_message += ["1", "1", "1", "1"]
        else:
            raise Exception("You cannot be serious!")

    return binary_message


def read_packet(binary_message):
    version = binary_to_number(read(binary_message, 3))
    type_id = binary_to_number(read(binary_message, 3))

    if type_id == 4:
        curr_group = read(binary_message, 5)
        decimal_literal = curr_group[1:]
        while curr_group[0] == "1":
            curr_group = read(binary_message, 5)
            decimal_literal += curr_group[1:]
        return {
            "version": version,
            "type_id": type_id,
            "literal": binary_to_number(decimal_literal)
        }
    else:
        length_type_id = read(binary_message, 1)[0]
        sub_packets = []
        if length_type_id == "0":
            length_sub_packets = binary_to_number(read(binary_message, 15))
            binary_message_sub = read(binary_message, length_sub_packets)
            while binary_message_sub:
                sub_packets.append(read_packet(binary_message_sub))
        elif length_type_id == "1":
            number_sub_packets = binary_to_number(read(binary_message, 11))
            while number_sub_packets:
                sub_packets.append(read_packet(binary_message))
                number_sub_packets -= 1
        else:
            raise Exception("You cannot be serious!")

        return {
            "version": version,
            "type_id": type_id,
            "sub_packets": sub_packets
        }


def binary_to_number(bins):
    return int("".join(bins), 2)


def read(binary_message, num):
    bins = []
    for i in range(0, num):
        bins.append(binary_message.pop(0))
    return bins


def get_total_version(packet):
    total_version = packet["version"]
    if "sub_packets" in packet:
        for sub_packet in packet["sub_packets"]:
            total_version += get_total_version(sub_packet)
    return total_version


def get_total_value(packet):
    if packet["type_id"] == 4:
        return packet["literal"]

    sub_total_values = [get_total_value(sub_packet) for sub_packet in packet["sub_packets"]]
    if packet["type_id"] == 0:
        return sum(sub_total_values)
    elif packet["type_id"] == 1:
        return prod(sub_total_values)
    elif packet["type_id"] == 2:
        return min(sub_total_values)
    elif packet["type_id"] == 3:
        return max(sub_total_values)
    elif packet["type_id"] == 5:
        return 1 if sub_total_values[0] > sub_total_values[1] else 0
    elif packet["type_id"] == 6:
        return 1 if sub_total_values[0] < sub_total_values[1] else 0
    elif packet["type_id"] == 7:
        return 1 if sub_total_values[0] == sub_total_values[1] else 0
    else:
        raise Exception("You cannot be serious!")


def prod(the_list):
    return reduce(lambda x, y: x * y, the_list, 1)


if __name__ == "__main__":
    input_filename = os.path.basename(__file__).replace("aoc", "input").replace("py", "txt")
    with open("input/{}".format(input_filename)) as f:
        content = f.read().splitlines()

    start = time.time()
    main(content)
    end = time.time()
    diff = (end - start)
    if diff >= 1:
        print("The solutions took {}s".format(round(diff)))
    else:
        print("The solutions took {}ms".format(round(diff * 1000)))
